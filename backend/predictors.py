import numpy as np
import pandas as pd
from typing import Dict, List, Any
from abc import ABC, abstractmethod

class BasePredictor(ABC):
    """Base class for all health predictors"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a prediction based on input data"""
        pass
    
    @abstractmethod
    def get_required_fields(self) -> List[str]:
        """Get list of required input fields"""
        pass
    
    def get_field_descriptions(self) -> Dict[str, str]:
        """Get descriptions for input fields"""
        return {}
    
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

# Disease Risk & Diagnosis Predictors
class HeartDiseasePredictor(BasePredictor):
    def __init__(self):
        super().__init__(
            "Heart Disease Risk Predictor",
            "Predicts cardiovascular disease risk based on clinical parameters"
        )
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Mock prediction logic - replace with actual ML model
        age = data.get('age', 50)
        cholesterol = data.get('cholesterol', 200)
        blood_pressure = data.get('systolic_bp', 120)
        smoking = data.get('smoking', False)
        diabetes = data.get('diabetes', False)
        
        # Simple risk calculation
        risk_score = 0.0
        risk_score += min(age / 100, 0.3)
        risk_score += min(cholesterol / 400, 0.25)
        risk_score += min(blood_pressure / 200, 0.2)
        risk_score += 0.15 if smoking else 0
        risk_score += 0.1 if diabetes else 0
        
        risk_level = self.calculate_risk_level(risk_score)
        
        recommendations = []
        if cholesterol > 240:
            recommendations.append("Consider cholesterol-lowering medication")
        if blood_pressure > 140:
            recommendations.append("Monitor blood pressure regularly")
        if smoking:
            recommendations.append("Quit smoking immediately")
        recommendations.append("Regular exercise and healthy diet")
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "confidence": 0.85
        }
    
    def get_required_fields(self) -> List[str]:
        return ['age', 'cholesterol', 'systolic_bp', 'smoking', 'diabetes']
    
    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            'age': 'Age in years',
            'cholesterol': 'Total cholesterol level (mg/dL)',
            'systolic_bp': 'Systolic blood pressure (mmHg)',
            'smoking': 'Current smoking status (true/false)',
            'diabetes': 'Diabetes diagnosis (true/false)'
        }
    
    def identify_contributing_factors(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify heart disease contributing factors with detailed analysis"""
        factors = []
        
        # Age factor
        age = data.get('age', 0)
        if age > 65:
            factors.append({
                "factor": "Advanced age",
                "value": f"{age} years",
                "severity": "high" if age > 75 else "moderate",
                "impact": "high",
                "description": f"Age {age} significantly increases cardiovascular risk. Risk doubles every decade after 55."
            })
        elif age > 45:
            factors.append({
                "factor": "Mature age",
                "value": f"{age} years",
                "severity": "moderate",
                "impact": "moderate",
                "description": f"Age {age} represents moderate cardiovascular risk increase."
            })
        
        # Cholesterol assessment
        cholesterol = data.get('cholesterol', 0)
        if cholesterol > 240:
            factors.append({
                "factor": "High cholesterol",
                "value": f"{cholesterol} mg/dL",
                "severity": "severe" if cholesterol > 300 else "moderate",
                "impact": "high",
                "description": f"Total cholesterol {cholesterol} mg/dL is significantly elevated (normal <200). Increases heart attack risk by 2-3x."
            })
        elif cholesterol > 200:
            factors.append({
                "factor": "Borderline high cholesterol",
                "value": f"{cholesterol} mg/dL",
                "severity": "mild",
                "impact": "moderate",
                "description": f"Cholesterol {cholesterol} mg/dL is borderline high. Lifestyle changes recommended."
            })
        
        # Blood pressure assessment
        bp = data.get('systolic_bp', 0)
        if bp > 140:
            factors.append({
                "factor": "Hypertension",
                "value": f"{bp} mmHg systolic",
                "severity": "severe" if bp > 180 else "moderate",
                "impact": "high",
                "description": f"Systolic BP {bp} mmHg indicates hypertension. Each 20 mmHg increase doubles heart disease risk."
            })
        elif bp > 120:
            factors.append({
                "factor": "Elevated blood pressure",
                "value": f"{bp} mmHg systolic",
                "severity": "mild",
                "impact": "moderate",
                "description": f"BP {bp} mmHg is elevated (normal <120). Early intervention recommended."
            })
        
        # Smoking status
        if data.get('smoking', False):
            factors.append({
                "factor": "Current smoking",
                "value": "Active smoker",
                "severity": "severe",
                "impact": "high",
                "description": "Smoking increases heart disease risk by 2-4x and accelerates atherosclerosis."
            })
        
        # Diabetes status
        if data.get('diabetes', False):
            factors.append({
                "factor": "Diabetes mellitus",
                "value": "Diagnosed",
                "severity": "severe",
                "impact": "high",
                "description": "Diabetes increases heart disease risk by 2-4x through accelerated atherosclerosis."
            })
        
        return factors
    
    def analyze_health_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze heart disease-specific health metrics"""
        return {
            "cardiovascular_assessment": {
                "age_risk": {"value": data.get('age', 0), "risk_level": "high" if data.get('age', 0) > 65 else "moderate" if data.get('age', 0) > 45 else "low"},
                "cholesterol_status": {"value": data.get('cholesterol', 0), "category": "high" if data.get('cholesterol', 0) > 240 else "borderline" if data.get('cholesterol', 0) > 200 else "normal"},
                "blood_pressure": {"systolic": data.get('systolic_bp', 0), "category": "hypertensive" if data.get('systolic_bp', 0) > 140 else "elevated" if data.get('systolic_bp', 0) > 120 else "normal"}
            },
            "risk_factors": {
                "modifiable": {"smoking": bool(data.get('smoking', False)), "diabetes": bool(data.get('diabetes', False))},
                "non_modifiable": {"age": data.get('age', 0)}
            },
            "risk_stratification": {
                "framingham_equivalent": self._calculate_framingham_risk(data),
                "risk_category": self._categorize_overall_risk(data)
            }
        }
    
    def assess_lifestyle_impact(self, data: Dict[str, Any]) -> str:
        """Assess lifestyle impact on heart disease risk"""
        impact_factors = []
        
        if data.get('smoking', False):
            impact_factors.append("smoking cessation (can reduce risk by 50% within 1 year)")
        
        if data.get('cholesterol', 0) > 200:
            impact_factors.append("dietary modifications and possible statin therapy (can reduce risk by 25-35%)")
        
        if data.get('systolic_bp', 0) > 120:
            impact_factors.append("blood pressure management through diet, exercise, and medication (can reduce risk by 20-25%)")
        
        if data.get('diabetes', False):
            impact_factors.append("optimal diabetes control (HbA1c <7% can reduce cardiovascular events by 10%)")
        
        if impact_factors:
            return f"Your lifestyle significantly impacts heart disease risk. Key interventions: {', '.join(impact_factors)}. Combined lifestyle changes can reduce risk by up to 80%."
        else:
            return "Your current risk factors are well-controlled. Continue heart-healthy lifestyle: regular exercise, balanced diet, no smoking, and stress management."
    
    def calculate_field_risk_contribution(self, field_name: str, value: Any, normalized_value: float) -> float:
        """Calculate heart disease-specific field risk contribution"""
        risk_weights = {
            'age': 0.25,
            'cholesterol': 0.20,
            'systolic_bp': 0.20,
            'smoking': 0.20,
            'diabetes': 0.15
        }
        
        base_weight = risk_weights.get(field_name, 0.1)
        
        if field_name == 'age':
            return base_weight * min(value / 80, 1.0)
        elif field_name == 'cholesterol':
            return base_weight * min(max(0, value - 150) / 200, 1.0)
        elif field_name == 'systolic_bp':
            return base_weight * min(max(0, value - 90) / 100, 1.0)
        elif field_name in ['smoking', 'diabetes']:
            return base_weight if value else 0
        
        return base_weight * abs(normalized_value)
    
    def explain_field_risk(self, field_name: str, value: Any) -> str:
        """Explain heart disease-specific field risk"""
        explanations = {
            'age': f"Age {value} years - cardiovascular risk increases exponentially with age due to arterial stiffening",
            'cholesterol': f"Cholesterol {value} mg/dL - elevated levels promote atherosclerotic plaque formation",
            'systolic_bp': f"Systolic BP {value} mmHg - high pressure damages arterial walls and accelerates atherosclerosis",
            'smoking': "Smoking damages endothelium, increases inflammation, and promotes blood clotting",
            'diabetes': "Diabetes accelerates atherosclerosis through glycation and inflammatory processes"
        }
        return explanations.get(field_name, f"Field {field_name} with value {value} contributes to heart disease risk")
    
    def get_factor_specific_recommendation(self, factor: Dict[str, Any]) -> str:
        """Get heart disease-specific recommendations"""
        factor_name = factor['factor'].lower()
        
        if 'age' in factor_name:
            return "Enhanced cardiovascular monitoring, regular exercise, and preventive medications as appropriate"
        elif 'cholesterol' in factor_name:
            return "Statin therapy consideration, dietary changes (reduce saturated fat), and regular lipid monitoring"
        elif 'blood pressure' in factor_name or 'hypertension' in factor_name:
            return "ACE inhibitor/ARB therapy, DASH diet, sodium restriction, and regular BP monitoring"
        elif 'smoking' in factor_name:
            return "URGENT: Smoking cessation program, nicotine replacement therapy, and behavioral counseling"
        elif 'diabetes' in factor_name:
            return "Optimal glycemic control (HbA1c <7%), metformin therapy, and cardiovascular risk reduction"
        else:
            return "Comprehensive cardiovascular risk reduction: lifestyle modifications and appropriate medications"
    
    def generate_health_metrics_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate heart disease-specific chart data"""
        return {
            "labels": ["Age Risk", "Cholesterol", "Blood Pressure", "Smoking Risk", "Diabetes Risk"],
            "data": [
                min(data.get('age', 0) / 80 * 100, 100),
                min(max(0, data.get('cholesterol', 0) - 150) / 200 * 100, 100),
                min(max(0, data.get('systolic_bp', 0) - 90) / 100 * 100, 100),
                100 if data.get('smoking', False) else 0,
                100 if data.get('diabetes', False) else 0
            ],
            "normal_ranges": [30, 25, 20, 0, 0],
            "chart_type": "radar",
            "colors": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"]
        }
    
    def _calculate_framingham_risk(self, data: Dict[str, Any]) -> float:
        """Calculate Framingham-equivalent risk score"""
        risk = 0.0
        age = data.get('age', 0)
        if age > 40:
            risk += (age - 40) * 0.02
        if data.get('smoking', False):
            risk += 0.15
        if data.get('diabetes', False):
            risk += 0.12
        cholesterol = data.get('cholesterol', 0)
        if cholesterol > 200:
            risk += (cholesterol - 200) / 1000
        bp = data.get('systolic_bp', 0)
        if bp > 120:
            risk += (bp - 120) / 500
        return min(risk, 1.0)
    
    def _categorize_overall_risk(self, data: Dict[str, Any]) -> str:
        """Categorize overall cardiovascular risk"""
        risk_score = self._calculate_framingham_risk(data)
        if risk_score < 0.1:
            return "Low risk (<10% 10-year risk)"
        elif risk_score < 0.2:
            return "Intermediate risk (10-20% 10-year risk)"
        else:
            return "High risk (>20% 10-year risk)"

class StrokeRiskPredictor(BasePredictor):
    def __init__(self):
        super().__init__(
            "Stroke Risk Predictor",
            "Analyzes blood pressure, cholesterol, lifestyle, and family history to predict stroke risk"
        )
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Extract features
        age = data.get('age', 50)
        gender = data.get('gender', 0)
        hypertension = data.get('hypertension', 0)
        heart_disease = data.get('heart_disease', 0)
        ever_married = data.get('ever_married', 1)
        work_type = data.get('work_type', 0)
        residence_type = data.get('residence_type', 1)
        avg_glucose = data.get('avg_glucose_level', 100)
        bmi = data.get('bmi', 25)
        smoking_status = data.get('smoking_status', 0)
        alcohol_consumption = data.get('alcohol_consumption', 0)
        physical_activity = data.get('physical_activity', 1)
        family_history_stroke = data.get('family_history_stroke', 0)
        
        # Calculate comprehensive risk score
        risk_score = 0.0
        
        # Age factor (strongest predictor)
        risk_score += min(age / 100, 0.35)
        
        # Medical conditions
        risk_score += 0.25 if hypertension else 0
        risk_score += 0.2 if heart_disease else 0
        
        # Glucose and BMI
        risk_score += min(avg_glucose / 300, 0.15)
        risk_score += max(0, (bmi - 25) / 50) * 0.1
        
        # Lifestyle factors
        smoking_risk = [0, 0.05, 0.15, 0.1]  # never, formerly, current, unknown
        risk_score += smoking_risk[min(smoking_status, 3)]
        
        alcohol_risk = [0, 0.02, 0.05, 0.12]  # never, occasional, moderate, heavy
        risk_score += alcohol_risk[min(alcohol_consumption, 3)]
        
        activity_risk = [0.08, 0.04, 0.02, 0]  # sedentary, light, moderate, vigorous
        risk_score += activity_risk[min(physical_activity, 3)]
        
        # Family history
        risk_score += 0.1 if family_history_stroke else 0
        
        # Gender factor (males slightly higher risk)
        risk_score += 0.02 if gender == 1 else 0
        
        # Social factors (minor impact)
        risk_score += 0.01 if ever_married == 0 else 0
        risk_score += 0.01 if work_type == 4 else 0  # never worked
        
        # Cap the risk score
        risk_score = min(risk_score, 1.0)
        
        risk_level = self.calculate_risk_level(risk_score)
        
        # Generate recommendations
        recommendations = []
        if hypertension:
            recommendations.append("Manage blood pressure with medication and lifestyle changes")
        if avg_glucose > 126:
            recommendations.append("Monitor and control blood glucose levels")
        if bmi > 30:
            recommendations.append("Weight management through diet and exercise")
        if smoking_status == 2:
            recommendations.append("Quit smoking immediately - single most important change")
        if alcohol_consumption >= 3:
            recommendations.append("Reduce alcohol consumption to moderate levels")
        if physical_activity == 0:
            recommendations.append("Increase physical activity - aim for 150 minutes/week")
        if family_history_stroke:
            recommendations.append("Regular screening due to family history")
        
        recommendations.append("Regular cardiovascular exercise")
        recommendations.append("Maintain healthy diet low in sodium and saturated fats")
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "confidence": 0.87
        }
    
    def get_required_fields(self) -> List[str]:
        return [
            'age', 'gender', 'hypertension', 'heart_disease', 'ever_married',
            'work_type', 'residence_type', 'avg_glucose_level', 'bmi',
            'smoking_status', 'alcohol_consumption', 'physical_activity',
            'family_history_stroke'
        ]
    
    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            'age': 'Age in years',
            'gender': 'Gender (1 = Male, 0 = Female)',
            'hypertension': 'Hypertension (1 = Yes, 0 = No)',
            'heart_disease': 'Heart disease (1 = Yes, 0 = No)',
            'ever_married': 'Ever married (1 = Yes, 0 = No)',
            'work_type': 'Work type (0 = Private, 1 = Self-employed, 2 = Government, 3 = Children, 4 = Never worked)',
            'residence_type': 'Residence type (1 = Urban, 0 = Rural)',
            'avg_glucose_level': 'Average glucose level (mg/dL)',
            'bmi': 'Body Mass Index',
            'smoking_status': 'Smoking status (0 = Never smoked, 1 = Formerly smoked, 2 = Smokes, 3 = Unknown)',
            'alcohol_consumption': 'Alcohol consumption (0 = Never, 1 = Occasional, 2 = Moderate, 3 = Heavy)',
            'physical_activity': 'Physical activity level (0 = Sedentary, 1 = Light, 2 = Moderate, 3 = Vigorous)',
            'family_history_stroke': 'Family history of stroke (1 = Yes, 0 = No)'
        }

class CancerDetectionPredictor(BasePredictor):
    def __init__(self):
        super().__init__(
            "Cancer Detection Predictor",
            "Early cancer detection based on symptoms and risk factors"
        )
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        age = data.get('age', 50)
        family_history = data.get('family_history', False)
        smoking_years = data.get('smoking_years', 0)
        symptoms_count = data.get('symptoms_count', 0)
        
        risk_score = 0.0
        risk_score += min(age / 100, 0.3)
        risk_score += 0.2 if family_history else 0
        risk_score += min(smoking_years / 50, 0.25)
        risk_score += min(symptoms_count / 10, 0.25)
        
        risk_level = self.calculate_risk_level(risk_score)
        
        recommendations = [
            "Regular cancer screening as per age guidelines",
            "Maintain healthy lifestyle",
            "Avoid tobacco and excessive alcohol"
        ]
        
        if family_history:
            recommendations.append("Genetic counseling consultation")
        if smoking_years > 10:
            recommendations.append("Immediate smoking cessation")
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "confidence": 0.75
        }
    
    def get_required_fields(self) -> List[str]:
        return ['age', 'family_history', 'smoking_years', 'symptoms_count']

class KidneyDiseasePredictor(BasePredictor):
    def __init__(self):
        super().__init__(
            "Kidney Disease Predictor",
            "Chronic kidney disease risk assessment"
        )
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        age = data.get('age', 50)
        blood_pressure = data.get('blood_pressure', 120)
        specific_gravity = data.get('specific_gravity', 1.020)
        albumin = data.get('albumin', 0)
        sugar = data.get('sugar', 0)
        
        risk_score = 0.0
        risk_score += min(age / 100, 0.25)
        risk_score += min(blood_pressure / 200, 0.3)
        risk_score += abs(specific_gravity - 1.020) * 10
        risk_score += albumin * 0.2
        risk_score += sugar * 0.15
        
        risk_level = self.calculate_risk_level(risk_score)
        
        recommendations = [
            "Regular kidney function monitoring",
            "Maintain healthy blood pressure",
            "Stay hydrated",
            "Limit sodium intake"
        ]
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "confidence": 0.80
        }
    
    def get_required_fields(self) -> List[str]:
        return ['age', 'blood_pressure', 'specific_gravity', 'albumin', 'sugar']

class LiverDiseasePredictor(BasePredictor):
    def __init__(self):
        super().__init__(
            "Liver Disease Predictor",
            "Liver disease risk assessment based on clinical markers"
        )
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        age = data.get('age', 50)
        bilirubin = data.get('bilirubin', 1.0)
        alkaline_phosphotase = data.get('alkaline_phosphotase', 200)
        alamine_aminotransferase = data.get('alamine_aminotransferase', 40)
        alcohol_consumption = data.get('alcohol_consumption', 0)
        
        risk_score = 0.0
        risk_score += min(age / 100, 0.2)
        risk_score += min(bilirubin / 10, 0.25)
        risk_score += min(alkaline_phosphotase / 500, 0.2)
        risk_score += min(alamine_aminotransferase / 200, 0.25)
        risk_score += min(alcohol_consumption / 10, 0.1)
        
        risk_level = self.calculate_risk_level(risk_score)
        
        recommendations = [
            "Regular liver function tests",
            "Limit alcohol consumption",
            "Maintain healthy weight",
            "Avoid hepatotoxic medications"
        ]
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "confidence": 0.78
        }
    
    def get_required_fields(self) -> List[str]:
        return ['age', 'bilirubin', 'alkaline_phosphotase', 'alamine_aminotransferase', 'alcohol_consumption']

class AlzheimerPredictor(BasePredictor):
    def __init__(self):
        super().__init__(
            "Alzheimer's Disease Predictor",
            "Early Alzheimer's disease risk assessment"
        )
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        age = data.get('age', 50)
        family_history = data.get('family_history', False)
        education_years = data.get('education_years', 12)
        cognitive_score = data.get('cognitive_score', 30)
        
        risk_score = 0.0
        risk_score += min(age / 100, 0.4)
        risk_score += 0.25 if family_history else 0
        risk_score += max(0, (16 - education_years) / 16) * 0.15
        risk_score += max(0, (30 - cognitive_score) / 30) * 0.2
        
        risk_level = self.calculate_risk_level(risk_score)
        
        recommendations = [
            "Regular cognitive assessments",
            "Mental stimulation activities",
            "Physical exercise",
            "Social engagement",
            "Healthy diet (Mediterranean style)"
        ]
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "confidence": 0.72
        }
    
    def get_required_fields(self) -> List[str]:
        return ['age', 'family_history', 'education_years', 'cognitive_score']

class ParkinsonPredictor(BasePredictor):
    def __init__(self):
        super().__init__(
            "Parkinson's Disease Predictor",
            "Parkinson's disease risk assessment based on motor symptoms"
        )
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        age = data.get('age', 50)
        tremor_score = data.get('tremor_score', 0)
        rigidity_score = data.get('rigidity_score', 0)
        bradykinesia_score = data.get('bradykinesia_score', 0)
        postural_instability = data.get('postural_instability', False)
        
        risk_score = 0.0
        risk_score += min(age / 100, 0.3)
        risk_score += tremor_score / 10
        risk_score += rigidity_score / 10
        risk_score += bradykinesia_score / 10
        risk_score += 0.1 if postural_instability else 0
        
        risk_level = self.calculate_risk_level(risk_score)
        
        recommendations = [
            "Regular neurological evaluation",
            "Physical therapy",
            "Regular exercise",
            "Stress management"
        ]
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "confidence": 0.76
        }
    
    def get_required_fields(self) -> List[str]:
        return ['age', 'tremor_score', 'rigidity_score', 'bradykinesia_score', 'postural_instability']

# Condition & Complication Predictors
class SepsisPredictor(BasePredictor):
    def __init__(self):
        super().__init__(
            "Sepsis Risk Predictor",
            "Early sepsis detection and risk assessment"
        )
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        temperature = data.get('temperature', 98.6)
        heart_rate = data.get('heart_rate', 70)
        respiratory_rate = data.get('respiratory_rate', 16)
        white_blood_cells = data.get('white_blood_cells', 7000)
        
        risk_score = 0.0
        # Temperature abnormalities
        if temperature > 100.4 or temperature < 96.8:
            risk_score += 0.25
        # Tachycardia
        if heart_rate > 90:
            risk_score += 0.25
        # Tachypnea
        if respiratory_rate > 20:
            risk_score += 0.25
        # WBC abnormalities
        if white_blood_cells > 12000 or white_blood_cells < 4000:
            risk_score += 0.25
        
        risk_level = self.calculate_risk_level(risk_score)
        
        recommendations = [
            "Immediate medical evaluation if high risk",
            "Monitor vital signs closely",
            "Blood culture if indicated",
            "Consider antibiotic therapy"
        ]
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "confidence": 0.88
        }
    
    def get_required_fields(self) -> List[str]:
        return ['temperature', 'heart_rate', 'respiratory_rate', 'white_blood_cells']

class HospitalReadmissionPredictor(BasePredictor):
    def __init__(self):
        super().__init__(
            "Hospital Readmission Predictor",
            "30-day hospital readmission risk assessment"
        )
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        age = data.get('age', 50)
        length_of_stay = data.get('length_of_stay', 3)
        num_diagnoses = data.get('num_diagnoses', 1)
        num_medications = data.get('num_medications', 5)
        discharge_disposition = data.get('discharge_disposition', 'home')
        
        risk_score = 0.0
        risk_score += min(age / 100, 0.3)
        risk_score += min(length_of_stay / 30, 0.2)
        risk_score += min(num_diagnoses / 20, 0.25)
        risk_score += min(num_medications / 50, 0.15)
        
        if discharge_disposition != 'home':
            risk_score += 0.1
        
        risk_level = self.calculate_risk_level(risk_score)
        
        recommendations = [
            "Comprehensive discharge planning",
            "Medication reconciliation",
            "Follow-up appointment scheduling",
            "Patient education on warning signs"
        ]
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "confidence": 0.81
        }
    
    def get_required_fields(self) -> List[str]:
        return ['age', 'length_of_stay', 'num_diagnoses', 'num_medications', 'discharge_disposition']

class ICUMortalityPredictor(BasePredictor):
    def __init__(self):
        super().__init__(
            "ICU Mortality Predictor",
            "ICU mortality risk assessment"
        )
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        age = data.get('age', 50)
        apache_score = data.get('apache_score', 15)
        mechanical_ventilation = data.get('mechanical_ventilation', False)
        sepsis = data.get('sepsis', False)
        
        risk_score = 0.0
        risk_score += min(age / 100, 0.3)
        risk_score += min(apache_score / 50, 0.4)
        risk_score += 0.2 if mechanical_ventilation else 0
        risk_score += 0.1 if sepsis else 0
        
        risk_level = self.calculate_risk_level(risk_score)
        
        recommendations = [
            "Intensive monitoring",
            "Optimize organ support",
            "Infection control measures",
            "Family communication"
        ]
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "confidence": 0.85
        }
    
    def get_required_fields(self) -> List[str]:
        return ['age', 'apache_score', 'mechanical_ventilation', 'sepsis']

class PostSurgeryComplicationPredictor(BasePredictor):
    def __init__(self):
        super().__init__(
            "Post-Surgery Complication Predictor",
            "Post-operative complication risk assessment"
        )
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        age = data.get('age', 50)
        surgery_duration = data.get('surgery_duration', 120)
        asa_score = data.get('asa_score', 2)
        emergency_surgery = data.get('emergency_surgery', False)
        
        risk_score = 0.0
        risk_score += min(age / 100, 0.25)
        risk_score += min(surgery_duration / 600, 0.25)
        risk_score += (asa_score - 1) / 5 * 0.3
        risk_score += 0.2 if emergency_surgery else 0
        
        risk_level = self.calculate_risk_level(risk_score)
        
        recommendations = [
            "Close post-operative monitoring",
            "Early mobilization",
            "Pain management",
            "Infection prevention"
        ]
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "confidence": 0.79
        }
    
    def get_required_fields(self) -> List[str]:
        return ['age', 'surgery_duration', 'asa_score', 'emergency_surgery']

class PregnancyComplicationPredictor(BasePredictor):
    def __init__(self):
        super().__init__(
            "Pregnancy Complication Predictor",
            "Pregnancy and delivery complication risk assessment"
        )
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        maternal_age = data.get('maternal_age', 28)
        gestational_age = data.get('gestational_age', 38)
        previous_complications = data.get('previous_complications', False)
        multiple_pregnancy = data.get('multiple_pregnancy', False)
        
        risk_score = 0.0
        if maternal_age < 18 or maternal_age > 35:
            risk_score += 0.2
        if gestational_age < 37:
            risk_score += 0.3
        risk_score += 0.25 if previous_complications else 0
        risk_score += 0.25 if multiple_pregnancy else 0
        
        risk_level = self.calculate_risk_level(risk_score)
        
        recommendations = [
            "Regular prenatal care",
            "Nutritional counseling",
            "Fetal monitoring",
            "Delivery planning"
        ]
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "confidence": 0.83
        }
    
    def get_required_fields(self) -> List[str]:
        return ['maternal_age', 'gestational_age', 'previous_complications', 'multiple_pregnancy']

# Lifestyle & Preventive Health Predictors
class ObesityRiskPredictor(BasePredictor):
    def __init__(self):
        super().__init__(
            "Obesity Risk Predictor",
            "Obesity risk assessment based on lifestyle factors"
        )
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        current_bmi = data.get('current_bmi', 25)
        physical_activity = data.get('physical_activity_hours', 2)
        caloric_intake = data.get('daily_calories', 2000)
        family_history = data.get('family_history_obesity', False)
        
        risk_score = 0.0
        risk_score += max(0, (current_bmi - 25) / 25) * 0.4
        risk_score += max(0, (3 - physical_activity) / 3) * 0.25
        risk_score += max(0, (caloric_intake - 2200) / 1000) * 0.2
        risk_score += 0.15 if family_history else 0
        
        risk_level = self.calculate_risk_level(risk_score)
        
        recommendations = [
            "Balanced diet with portion control",
            "Regular physical activity (150 min/week)",
            "Weight monitoring",
            "Behavioral counseling if needed"
        ]
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "confidence": 0.84
        }
    
    def get_required_fields(self) -> List[str]:
        return ['current_bmi', 'physical_activity_hours', 'daily_calories', 'family_history_obesity']

class HypertensionPredictor(BasePredictor):
    def __init__(self):
        super().__init__(
            "Hypertension Risk Predictor",
            "High blood pressure risk assessment"
        )
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        age = data.get('age', 50)
        systolic_bp = data.get('systolic_bp', 120)
        diastolic_bp = data.get('diastolic_bp', 80)
        sodium_intake = data.get('sodium_intake_mg', 2300)
        family_history = data.get('family_history', False)
        
        risk_score = 0.0
        risk_score += min(age / 100, 0.25)
        risk_score += max(0, (systolic_bp - 120) / 60) * 0.3
        risk_score += max(0, (diastolic_bp - 80) / 40) * 0.2
        risk_score += max(0, (sodium_intake - 2300) / 2000) * 0.15
        risk_score += 0.1 if family_history else 0
        
        risk_level = self.calculate_risk_level(risk_score)
        
        recommendations = [
            "Reduce sodium intake (<2300mg/day)",
            "Regular exercise",
            "Weight management",
            "Limit alcohol consumption",
            "Stress management"
        ]
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "confidence": 0.87
        }
    
    def get_required_fields(self) -> List[str]:
        return ['age', 'systolic_bp', 'diastolic_bp', 'sodium_intake_mg', 'family_history']

class CholesterolRiskPredictor(BasePredictor):
    def __init__(self):
        super().__init__(
            "Cholesterol Risk Predictor",
            "High cholesterol risk assessment"
        )
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        age = data.get('age', 50)
        total_cholesterol = data.get('total_cholesterol', 200)
        hdl_cholesterol = data.get('hdl_cholesterol', 50)
        ldl_cholesterol = data.get('ldl_cholesterol', 100)
        triglycerides = data.get('triglycerides', 150)
        
        risk_score = 0.0
        risk_score += min(age / 100, 0.2)
        risk_score += max(0, (total_cholesterol - 200) / 200) * 0.25
        risk_score += max(0, (50 - hdl_cholesterol) / 50) * 0.2
        risk_score += max(0, (ldl_cholesterol - 100) / 100) * 0.25
        risk_score += max(0, (triglycerides - 150) / 300) * 0.1
        
        risk_level = self.calculate_risk_level(risk_score)
        
        recommendations = [
            "Heart-healthy diet (low saturated fat)",
            "Regular physical activity",
            "Weight management",
            "Consider statin therapy if indicated"
        ]
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "confidence": 0.86
        }
    
    def get_required_fields(self) -> List[str]:
        return ['age', 'total_cholesterol', 'hdl_cholesterol', 'ldl_cholesterol', 'triglycerides']

class MentalHealthPredictor(BasePredictor):
    def __init__(self):
        super().__init__(
            "Mental Health Risk Predictor",
            "Depression and anxiety risk assessment"
        )
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        stress_level = data.get('stress_level', 5)  # 1-10 scale
        sleep_hours = data.get('sleep_hours', 7)
        social_support = data.get('social_support_score', 7)  # 1-10 scale
        life_events = data.get('recent_life_events', 0)
        
        risk_score = 0.0
        risk_score += (stress_level - 1) / 9 * 0.3
        risk_score += max(0, abs(sleep_hours - 8) / 8) * 0.25
        risk_score += (10 - social_support) / 9 * 0.25
        risk_score += min(life_events / 5, 1) * 0.2
        
        risk_level = self.calculate_risk_level(risk_score)
        
        recommendations = [
            "Stress management techniques",
            "Regular sleep schedule (7-9 hours)",
            "Social connection and support",
            "Professional counseling if needed",
            "Regular exercise and mindfulness"
        ]
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "confidence": 0.78
        }
    
    def get_required_fields(self) -> List[str]:
        return ['stress_level', 'sleep_hours', 'social_support_score', 'recent_life_events']

class SleepApneaPredictor(BasePredictor):
    def __init__(self):
        super().__init__(
            "Sleep Apnea Risk Predictor",
            "Obstructive sleep apnea risk assessment"
        )
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        age = data.get('age', 50)
        bmi = data.get('bmi', 25)
        neck_circumference = data.get('neck_circumference', 15)
        snoring = data.get('loud_snoring', False)
        daytime_sleepiness = data.get('daytime_sleepiness', False)
        
        risk_score = 0.0
        risk_score += min(age / 100, 0.2)
        risk_score += max(0, (bmi - 25) / 25) * 0.3
        risk_score += max(0, (neck_circumference - 16) / 6) * 0.2
        risk_score += 0.15 if snoring else 0
        risk_score += 0.15 if daytime_sleepiness else 0
        
        risk_level = self.calculate_risk_level(risk_score)
        
        recommendations = [
            "Weight management if overweight",
            "Sleep study evaluation",
            "Sleep hygiene practices",
            "Avoid alcohol before bedtime"
        ]
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "confidence": 0.82
        }
    
    def get_required_fields(self) -> List[str]:
        return ['age', 'bmi', 'neck_circumference', 'loud_snoring', 'daytime_sleepiness']

# Specialized Predictors
class CovidRiskPredictor(BasePredictor):
    def __init__(self):
        super().__init__(
            "COVID-19 Risk Predictor",
            "COVID-19 severity and complication risk assessment"
        )
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        age = data.get('age', 50)
        comorbidities = data.get('comorbidity_count', 0)
        vaccination_status = data.get('fully_vaccinated', False)
        symptoms_severity = data.get('symptoms_severity', 1)  # 1-5 scale
        
        risk_score = 0.0
        risk_score += min(age / 100, 0.35)
        risk_score += min(comorbidities / 5, 1) * 0.3
        risk_score += 0 if vaccination_status else 0.2
        risk_score += (symptoms_severity - 1) / 4 * 0.15
        
        risk_level = self.calculate_risk_level(risk_score)
        
        recommendations = [
            "Follow isolation guidelines",
            "Monitor symptoms closely",
            "Seek medical care if symptoms worsen",
            "Stay hydrated and rest"
        ]
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "confidence": 0.80
        }
    
    def get_required_fields(self) -> List[str]:
        return ['age', 'comorbidity_count', 'fully_vaccinated', 'symptoms_severity']

class AsthmaCopdPredictor(BasePredictor):
    def __init__(self):
        super().__init__(
            "Asthma/COPD Risk Predictor",
            "Respiratory disease risk assessment"
        )
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        age = data.get('age', 50)
        smoking_history = data.get('smoking_pack_years', 0)
        family_history = data.get('family_history_respiratory', False)
        environmental_exposure = data.get('environmental_exposure', False)
        
        risk_score = 0.0
        risk_score += min(age / 100, 0.25)
        risk_score += min(smoking_history / 50, 1) * 0.4
        risk_score += 0.2 if family_history else 0
        risk_score += 0.15 if environmental_exposure else 0
        
        risk_level = self.calculate_risk_level(risk_score)
        
        recommendations = [
            "Smoking cessation if applicable",
            "Avoid environmental triggers",
            "Regular pulmonary function tests",
            "Vaccination (flu, pneumonia)"
        ]
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "confidence": 0.84
        }
    
    def get_required_fields(self) -> List[str]:
        return ['age', 'smoking_pack_years', 'family_history_respiratory', 'environmental_exposure']

class AnemiaPredictor(BasePredictor):
    def __init__(self):
        super().__init__(
            "Anemia Risk Predictor",
            "Anemia risk assessment based on clinical factors"
        )
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        hemoglobin = data.get('hemoglobin', 14)
        iron_level = data.get('serum_iron', 100)
        menstrual_bleeding = data.get('heavy_menstrual_bleeding', False)
        dietary_iron = data.get('dietary_iron_adequate', True)
        
        risk_score = 0.0
        if hemoglobin < 12:  # Low hemoglobin
            risk_score += (12 - hemoglobin) / 12 * 0.4
        if iron_level < 60:  # Low iron
            risk_score += (60 - iron_level) / 60 * 0.3
        risk_score += 0.2 if menstrual_bleeding else 0
        risk_score += 0.1 if not dietary_iron else 0
        
        risk_level = self.calculate_risk_level(risk_score)
        
        recommendations = [
            "Iron-rich diet",
            "Vitamin C to enhance iron absorption",
            "Address underlying causes",
            "Regular blood tests"
        ]
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "confidence": 0.85
        }
    
    def get_required_fields(self) -> List[str]:
        return ['hemoglobin', 'serum_iron', 'heavy_menstrual_bleeding', 'dietary_iron_adequate']

class ThyroidDisorderPredictor(BasePredictor):
    def __init__(self):
        super().__init__(
            "Thyroid Disorder Predictor",
            "Thyroid dysfunction risk assessment"
        )
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        age = data.get('age', 50)
        gender = data.get('gender', 'female')  # female higher risk
        family_history = data.get('family_history_thyroid', False)
        autoimmune_history = data.get('autoimmune_disease', False)
        
        risk_score = 0.0
        risk_score += min(age / 100, 0.25)
        risk_score += 0.2 if gender.lower() == 'female' else 0.1
        risk_score += 0.3 if family_history else 0
        risk_score += 0.25 if autoimmune_history else 0
        
        risk_level = self.calculate_risk_level(risk_score)
        
        recommendations = [
            "Regular thyroid function tests",
            "Adequate iodine intake",
            "Monitor for symptoms",
            "Stress management"
        ]
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "confidence": 0.77
        }
    
    def get_required_fields(self) -> List[str]:
        return ['age', 'gender', 'family_history_thyroid', 'autoimmune_disease']

class CancerRecurrencePredictor(BasePredictor):
    def __init__(self):
        super().__init__(
            "Cancer Recurrence Predictor",
            "Cancer recurrence risk assessment for survivors"
        )
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        cancer_stage = data.get('original_cancer_stage', 1)  # 1-4
        time_since_treatment = data.get('months_since_treatment', 12)
        treatment_response = data.get('complete_response', True)
        tumor_markers = data.get('elevated_tumor_markers', False)
        
        risk_score = 0.0
        risk_score += (cancer_stage - 1) / 3 * 0.4
        risk_score += max(0, (24 - time_since_treatment) / 24) * 0.25
        risk_score += 0 if treatment_response else 0.25
        risk_score += 0.1 if tumor_markers else 0
        
        risk_level = self.calculate_risk_level(risk_score)
        
        recommendations = [
            "Regular oncology follow-up",
            "Surveillance imaging as scheduled",
            "Healthy lifestyle maintenance",
            "Report new symptoms promptly"
        ]
        
        return {
            "risk_score": round(risk_score, 3),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "confidence": 0.79
        }
    
    def get_required_fields(self) -> List[str]:
        return ['original_cancer_stage', 'months_since_treatment', 'complete_response', 'elevated_tumor_markers']