from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

class BasePredictor(ABC):
    """Base class for all health predictors"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_names = []
        
    @abstractmethod
    def get_required_fields(self) -> Dict[str, str]:
        """Return dictionary of required input fields and their types"""
        pass
    
    @abstractmethod
    def get_field_descriptions(self) -> Dict[str, str]:
        """Return dictionary of field descriptions for UI"""
        pass
    
    @abstractmethod
    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        """Preprocess input data for prediction"""
        pass
    
    def validate_input(self, data: Dict[str, Any]) -> bool:
        """Validate input data against required fields"""
        required_fields = self.get_required_fields()
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
            
            # Type validation
            expected_type = required_fields[field]
            if expected_type == 'float' and not isinstance(data[field], (int, float)):
                try:
                    data[field] = float(data[field])
                except ValueError:
                    raise ValueError(f"Field {field} must be a number")
            elif expected_type == 'int' and not isinstance(data[field], int):
                try:
                    data[field] = int(data[field])
                except ValueError:
                    raise ValueError(f"Field {field} must be an integer")
            elif expected_type == 'str' and not isinstance(data[field], str):
                data[field] = str(data[field])
        
        return True
    
    def calculate_risk_level(self, risk_score: float) -> str:
        """Convert risk score to risk level"""
        if risk_score < 0.3:
            return "Low"
        elif risk_score < 0.6:
            return "Moderate"
        elif risk_score < 0.8:
            return "High"
        else:
            return "Very High"
    
    def get_recommendations(self, risk_score: float, risk_level: str, data: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on risk level and input data"""
        recommendations = []
        
        if risk_level == "Low":
            recommendations.extend([
                "Maintain your current healthy lifestyle",
                "Continue regular check-ups with your healthcare provider",
                "Stay physically active and eat a balanced diet"
            ])
        elif risk_level == "Moderate":
            recommendations.extend([
                "Consider lifestyle modifications to reduce risk",
                "Schedule more frequent health screenings",
                "Consult with your healthcare provider about prevention strategies",
                "Monitor relevant health metrics regularly"
            ])
        elif risk_level == "High":
            recommendations.extend([
                "Seek immediate consultation with a healthcare professional",
                "Consider comprehensive health screening",
                "Implement significant lifestyle changes",
                "Follow up with specialist if recommended"
            ])
        else:  # Very High
            recommendations.extend([
                "Urgent medical consultation recommended",
                "Comprehensive diagnostic testing may be needed",
                "Consider immediate lifestyle interventions",
                "Follow all medical advice strictly"
            ])
        
        return recommendations
    
    def generate_detailed_analysis(self, data: Dict[str, Any], risk_score: float, risk_level: str) -> Dict[str, Any]:
        """Generate detailed medical analysis"""
        analysis = {
            "severity_assessment": self.assess_severity(risk_score, data),
            "contributing_factors": self.identify_contributing_factors(data),
            "health_metrics_analysis": self.analyze_health_metrics(data),
            "lifestyle_impact": self.assess_lifestyle_impact(data),
            "preventive_measures": self.suggest_preventive_measures(risk_score, data)
        }
        return analysis
    
    def analyze_risk_factors(self, data: Dict[str, Any], processed_data: np.ndarray) -> List[Dict[str, Any]]:
        """Analyze individual risk factors and their contributions"""
        risk_factors = []
        field_descriptions = self.get_field_descriptions()
        
        # Analyze each field for risk contribution
        for i, (field_name, field_type) in enumerate(self.get_required_fields().items()):
            if i < len(processed_data):
                value = data.get(field_name, 0)
                normalized_value = processed_data[i]
                
                risk_contribution = self.calculate_field_risk_contribution(field_name, value, normalized_value)
                
                if risk_contribution > 0.1:  # Only include significant risk factors
                    risk_factors.append({
                        "factor": field_descriptions.get(field_name, field_name),
                        "value": value,
                        "risk_level": self.categorize_field_risk(risk_contribution),
                        "contribution_score": risk_contribution,
                        "explanation": self.explain_field_risk(field_name, value)
                    })
        
        # Sort by risk contribution
        risk_factors.sort(key=lambda x: x["contribution_score"], reverse=True)
        return risk_factors[:10]  # Return top 10 risk factors
    
    def get_enhanced_recommendations(self, risk_score: float, risk_level: str, data: Dict[str, Any], risk_factors: List[Dict[str, Any]]) -> List[str]:
        """Generate enhanced personalized recommendations"""
        recommendations = []
        
        # Base recommendations from original method
        base_recommendations = self.get_recommendations(risk_score, risk_level, data)
        recommendations.extend(base_recommendations)
        
        # Add specific recommendations based on top risk factors
        for factor in risk_factors[:5]:  # Top 5 risk factors
            specific_rec = self.get_factor_specific_recommendation(factor)
            if specific_rec and specific_rec not in recommendations:
                recommendations.append(specific_rec)
        
        # Add lifestyle recommendations
        lifestyle_recs = self.get_lifestyle_recommendations(data, risk_score)
        recommendations.extend(lifestyle_recs)
        
        # Add monitoring recommendations
        monitoring_recs = self.get_monitoring_recommendations(risk_level, risk_factors)
        recommendations.extend(monitoring_recs)
        
        return recommendations[:15]  # Limit to 15 recommendations
    
    def calculate_confidence(self, data: Dict[str, Any], risk_score: float, risk_factors: List[Dict[str, Any]]) -> float:
        """Calculate prediction confidence based on data quality and risk factors"""
        base_confidence = 0.75
        
        # Adjust based on data completeness
        required_fields = len(self.get_required_fields())
        provided_fields = len([v for v in data.values() if v is not None and v != ''])
        completeness_factor = provided_fields / required_fields
        
        # Adjust based on risk score certainty
        certainty_factor = 1.0 - abs(0.5 - risk_score) * 2  # Higher confidence for extreme scores
        
        # Adjust based on number of significant risk factors
        risk_factor_confidence = min(1.0, len(risk_factors) / 5.0)
        
        confidence = base_confidence * (0.4 * completeness_factor + 0.4 * certainty_factor + 0.2 * risk_factor_confidence)
        return min(0.95, max(0.60, confidence))  # Clamp between 60% and 95%
    
    def generate_chart_data(self, data: Dict[str, Any], risk_score: float, risk_factors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate data for charts and visualizations"""
        return {
            "risk_gauge": {
                "value": risk_score * 100,
                "ranges": [
                    {"from": 0, "to": 20, "color": "#22c55e", "label": "Low Risk"},
                    {"from": 20, "to": 40, "color": "#84cc16", "label": "Mild Risk"},
                    {"from": 40, "to": 60, "color": "#eab308", "label": "Moderate Risk"},
                    {"from": 60, "to": 80, "color": "#f97316", "label": "High Risk"},
                    {"from": 80, "to": 100, "color": "#ef4444", "label": "Very High Risk"}
                ]
            },
            "risk_factors_chart": {
                "labels": [rf["factor"] for rf in risk_factors[:8]],
                "data": [rf["contribution_score"] * 100 for rf in risk_factors[:8]],
                "colors": [self.get_risk_color(rf["contribution_score"]) for rf in risk_factors[:8]]
            },
            "health_metrics": self.generate_health_metrics_chart(data),
            "comparison_data": self.generate_population_comparison(data, risk_score)
        }
    
    def generate_explanation(self, data: Dict[str, Any], risk_score: float, risk_level: str, risk_factors: List[Dict[str, Any]]) -> str:
        """Generate detailed explanation of the prediction"""
        explanation_parts = []
        
        # Overall assessment
        explanation_parts.append(f"Based on the provided health information, your {self.name.lower()} shows a {risk_level.lower()} risk level with a score of {risk_score:.1%}.")
        
        # Key contributing factors
        if risk_factors:
            top_factors = [rf["factor"] for rf in risk_factors[:3]]
            explanation_parts.append(f"The primary contributing factors are: {', '.join(top_factors)}.")
        
        # Risk level specific explanation
        if risk_score < 0.3:
            explanation_parts.append("This indicates a relatively low risk, but maintaining healthy habits is important for prevention.")
        elif risk_score < 0.6:
            explanation_parts.append("This suggests moderate risk that can be managed through lifestyle modifications and regular monitoring.")
        else:
            explanation_parts.append("This indicates elevated risk that requires immediate attention and potentially medical intervention.")
        
        return " ".join(explanation_parts)
    
    # Helper methods for detailed analysis
    def assess_severity(self, risk_score: float, data: Dict[str, Any]) -> str:
        """Assess the severity of the condition"""
        if risk_score < 0.2:
            return "Minimal - Very low likelihood of developing the condition"
        elif risk_score < 0.4:
            return "Mild - Low to moderate risk with good prognosis if managed"
        elif risk_score < 0.6:
            return "Moderate - Significant risk requiring active management"
        elif risk_score < 0.8:
            return "High - Elevated risk requiring immediate intervention"
        else:
            return "Critical - Very high risk requiring urgent medical attention"
    
    def identify_contributing_factors(self, data: Dict[str, Any]) -> List[str]:
        """Identify key contributing factors"""
        factors = []
        # This will be overridden by specific predictors
        return factors
    
    def analyze_health_metrics(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Analyze health metrics"""
        # This will be overridden by specific predictors
        return {}
    
    def assess_lifestyle_impact(self, data: Dict[str, Any]) -> str:
        """Assess lifestyle impact on risk"""
        # This will be overridden by specific predictors
        return "Lifestyle factors play a significant role in risk development."
    
    def suggest_preventive_measures(self, risk_score: float, data: Dict[str, Any]) -> List[str]:
        """Suggest preventive measures"""
        measures = [
            "Regular health screenings and check-ups",
            "Maintain a balanced, nutritious diet",
            "Engage in regular physical activity",
            "Manage stress through relaxation techniques",
            "Avoid smoking and limit alcohol consumption"
        ]
        return measures
    
    def calculate_field_risk_contribution(self, field_name: str, value: Any, normalized_value: float) -> float:
        """Calculate how much a field contributes to risk"""
        # Simple heuristic - can be overridden by specific predictors
        return abs(normalized_value - 0.5) * 2
    
    def categorize_field_risk(self, contribution: float) -> str:
        """Categorize field risk level"""
        if contribution < 0.2:
            return "Low"
        elif contribution < 0.5:
            return "Moderate"
        elif contribution < 0.8:
            return "High"
        else:
            return "Very High"
    
    def explain_field_risk(self, field_name: str, value: Any) -> str:
        """Explain why a field contributes to risk"""
        # This will be overridden by specific predictors
        return f"The value {value} for {field_name} contributes to the overall risk assessment."
    
    def get_factor_specific_recommendation(self, factor: Dict[str, Any]) -> str:
        """Get recommendation specific to a risk factor"""
        # This will be overridden by specific predictors
        return f"Address the {factor['factor']} to reduce risk."
    
    def get_lifestyle_recommendations(self, data: Dict[str, Any], risk_score: float) -> List[str]:
        """Get lifestyle-specific recommendations"""
        recommendations = []
        if risk_score > 0.5:
            recommendations.extend([
                "Implement a heart-healthy diet rich in fruits and vegetables",
                "Establish a regular exercise routine (150 minutes/week moderate activity)",
                "Practice stress management techniques like meditation or yoga"
            ])
        return recommendations
    
    def get_monitoring_recommendations(self, risk_level: str, risk_factors: List[Dict[str, Any]]) -> List[str]:
        """Get monitoring recommendations based on risk level"""
        recommendations = []
        if risk_level in ["High", "Very High"]:
            recommendations.extend([
                "Schedule regular follow-up appointments with your healthcare provider",
                "Monitor key health metrics daily or weekly as advised",
                "Keep a health diary to track symptoms and improvements"
            ])
        return recommendations
    
    def get_risk_color(self, contribution: float) -> str:
        """Get color for risk visualization"""
        if contribution < 0.2:
            return "#22c55e"  # Green
        elif contribution < 0.5:
            return "#eab308"  # Yellow
        elif contribution < 0.8:
            return "#f97316"  # Orange
        else:
            return "#ef4444"  # Red
    
    def generate_health_metrics_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate health metrics chart data"""
        # This will be overridden by specific predictors
        return {"labels": [], "data": [], "normal_ranges": []}
    
    def generate_population_comparison(self, data: Dict[str, Any], risk_score: float) -> Dict[str, Any]:
        """Generate population comparison data"""
        age = data.get('age', 50)
        age_group = f"{(age // 10) * 10}-{(age // 10) * 10 + 9}"
        
        return {
            "user_risk": risk_score * 100,
            "age_group_average": max(10, min(90, (age - 20) * 1.5 + np.random.normal(0, 5))),
            "population_average": 35,
            "age_group": age_group
        }
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make prediction and return comprehensive result with detailed analysis"""
        # Validate input
        self.validate_input(data)
        
        # Preprocess data
        processed_data = self.preprocess_data(data)
        
        # Make prediction
        if not self.is_trained:
            self._train_default_model()
        
        # Get prediction probability
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(processed_data.reshape(1, -1))[0]
            risk_score = float(probabilities[1] if len(probabilities) > 1 else probabilities[0])
        else:
            prediction = self.model.predict(processed_data.reshape(1, -1))[0]
            risk_score = float(prediction)
        
        # Ensure risk score is between 0 and 1
        risk_score = max(0.0, min(1.0, risk_score))
        
        # Calculate risk level
        risk_level = self.calculate_risk_level(risk_score)
        
        # Generate comprehensive analysis
        detailed_analysis = self.generate_detailed_analysis(data, risk_score, risk_level)
        risk_factors = self.analyze_risk_factors(data, processed_data)
        recommendations = self.get_enhanced_recommendations(risk_score, risk_level, data, risk_factors)
        
        # Calculate confidence with more sophisticated logic
        confidence = self.calculate_confidence(data, risk_score, risk_factors)
        
        # Generate visualization data
        chart_data = self.generate_chart_data(data, risk_score, risk_factors)
        
        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "detailed_analysis": detailed_analysis,
            "risk_factors": risk_factors,
            "recommendations": recommendations,
            "confidence": confidence,
            "chart_data": chart_data,
            "explanation": self.generate_explanation(data, risk_score, risk_level, risk_factors)
        }
    
    def _train_default_model(self):
        """Train a default model with synthetic data for demonstration"""
        # Generate synthetic training data
        n_samples = 1000
        n_features = len(self.get_required_fields())
        
        # Create synthetic features
        X = np.random.randn(n_samples, n_features)
        
        # Create synthetic labels with some logic
        y = (X.sum(axis=1) + np.random.randn(n_samples) * 0.1 > 0).astype(int)
        
        # Train model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, y)
        self.is_trained = True
    
    def save_model(self, filepath: str):
        """Save trained model to file"""
        if self.model is not None:
            joblib.dump({
                'model': self.model,
                'scaler': self.scaler,
                'feature_names': self.feature_names,
                'is_trained': self.is_trained
            }, filepath)
    
    def load_model(self, filepath: str):
        """Load trained model from file"""
        if os.path.exists(filepath):
            data = joblib.load(filepath)
            self.model = data['model']
            self.scaler = data['scaler']
            self.feature_names = data['feature_names']
            self.is_trained = data['is_trained']
            return True
        return False