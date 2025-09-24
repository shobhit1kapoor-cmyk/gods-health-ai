import numpy as np
from typing import Dict, List, Any
from .base_predictor import BasePredictor

class HeartDiseasePredictor(BasePredictor):
    """Predicts risk of heart disease including heart attack, arrhythmia, and heart failure"""
    
    def __init__(self):
        super().__init__(
            name="Heart Disease Risk Predictor",
            description="Predicts risk of heart attack, arrhythmia, or heart failure based on clinical and lifestyle factors"
        )
    
    def get_required_fields(self) -> Dict[str, str]:
        return {
            "age": "int",
            "sex": "int",  # 1 = male, 0 = female
            "chest_pain_type": "int",  # 0-3
            "resting_bp": "float",  # resting blood pressure
            "cholesterol": "float",  # serum cholesterol mg/dl
            "fasting_blood_sugar": "int",  # > 120 mg/dl (1 = true, 0 = false)
            "resting_ecg": "int",  # 0-2
            "max_heart_rate": "float",
            "exercise_angina": "int",  # 1 = yes, 0 = no
            "st_depression": "float",
            "st_slope": "int",  # 0-2
            "smoking": "int",  # 1 = yes, 0 = no
            "family_history": "int"  # 1 = yes, 0 = no
        }
    
    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            "age": "Age in years",
            "sex": "Sex (1 = Male, 0 = Female)",
            "chest_pain_type": "Chest pain type (0 = Typical angina, 1 = Atypical angina, 2 = Non-anginal pain, 3 = Asymptomatic)",
            "resting_bp": "Resting blood pressure (mm Hg)",
            "cholesterol": "Serum cholesterol (mg/dl)",
            "fasting_blood_sugar": "Fasting blood sugar > 120 mg/dl (1 = Yes, 0 = No)",
            "resting_ecg": "Resting ECG results (0 = Normal, 1 = ST-T wave abnormality, 2 = Left ventricular hypertrophy)",
            "max_heart_rate": "Maximum heart rate achieved",
            "exercise_angina": "Exercise induced angina (1 = Yes, 0 = No)",
            "st_depression": "ST depression induced by exercise relative to rest",
            "st_slope": "Slope of peak exercise ST segment (0 = Upsloping, 1 = Flat, 2 = Downsloping)",
            "smoking": "Smoking status (1 = Yes, 0 = No)",
            "family_history": "Family history of heart disease (1 = Yes, 0 = No)"
        }
    
    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        features = [
            data["age"] / 100.0,  # Normalize age
            data["sex"],
            data["chest_pain_type"] / 3.0,
            data["resting_bp"] / 200.0,  # Normalize BP
            data["cholesterol"] / 400.0,  # Normalize cholesterol
            data["fasting_blood_sugar"],
            data["resting_ecg"] / 2.0,
            data["max_heart_rate"] / 220.0,  # Normalize heart rate
            data["exercise_angina"],
            data["st_depression"] / 5.0,
            data["st_slope"] / 2.0,
            data["smoking"],
            data["family_history"]
        ]
        return np.array(features)


class DiabetesPredictor(BasePredictor):
    """Predicts Type 2 diabetes risk using clinical and lifestyle factors"""
    
    def __init__(self):
        super().__init__(
            name="Diabetes Risk Predictor",
            description="Predicts Type 2 diabetes risk using glucose levels, BMI, family history, and lifestyle factors"
        )
        self.required_fields = [
            "age", "gender", "bmi", "glucose_level", "blood_pressure", 
            "insulin_level", "family_history_diabetes", "physical_activity",
            "pregnancies", "skin_thickness", "diabetes_pedigree_function"
        ]
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict diabetes risk"""
        try:
            # Extract features
            age = data.get('age', 30)
            bmi = data.get('bmi', 25)
            glucose = data.get('glucose_level', 100)
            blood_pressure = data.get('blood_pressure', 80)
            insulin = data.get('insulin_level', 80)
            pregnancies = data.get('pregnancies', 0)
            skin_thickness = data.get('skin_thickness', 20)
            diabetes_pedigree = data.get('diabetes_pedigree_function', 0.5)
            family_history = data.get('family_history_diabetes', False)
            physical_activity = data.get('physical_activity', 3)  # hours per week
            
            # Calculate risk score based on clinical factors
            risk_score = 0.0
            
            # Age factor (risk increases with age)
            if age >= 45:
                risk_score += 0.2
            elif age >= 35:
                risk_score += 0.1
            
            # BMI factor
            if bmi >= 30:
                risk_score += 0.25
            elif bmi >= 25:
                risk_score += 0.15
            
            # Glucose level (fasting)
            if glucose >= 126:
                risk_score += 0.4  # Diabetic range
            elif glucose >= 100:
                risk_score += 0.2  # Pre-diabetic range
            
            # Blood pressure
            if blood_pressure >= 90:
                risk_score += 0.1
            
            # Insulin resistance indicator
            if insulin > 120:
                risk_score += 0.15
            
            # Family history
            if family_history:
                risk_score += 0.2
            
            # Pregnancies (gestational diabetes risk)
            if pregnancies > 0:
                risk_score += min(pregnancies * 0.05, 0.15)
            
            # Diabetes pedigree function
            risk_score += min(diabetes_pedigree * 0.3, 0.2)
            
            # Physical activity (protective factor)
            if physical_activity < 2:
                risk_score += 0.1
            elif physical_activity >= 5:
                risk_score -= 0.05
            
            # Ensure risk score is between 0 and 1
            risk_score = max(0, min(1, risk_score))
            
            # Determine risk level
            if risk_score >= 0.7:
                risk_level = "High"
            elif risk_score >= 0.4:
                risk_level = "Medium"
            else:
                risk_level = "Low"
            
            # Generate recommendations
            recommendations = []
            if glucose >= 100:
                recommendations.append("Monitor blood glucose levels regularly")
            if bmi >= 25:
                recommendations.append("Maintain healthy weight through diet and exercise")
            if physical_activity < 3:
                recommendations.append("Increase physical activity to at least 150 minutes per week")
            if family_history:
                recommendations.append("Regular screening due to family history")
            
            recommendations.extend([
                "Follow a balanced, low-sugar diet",
                "Regular medical check-ups",
                "Stress management and adequate sleep"
            ])
            
            return {
                "risk_score": round(risk_score, 3),
                "risk_level": risk_level,
                "recommendations": recommendations,
                "confidence": 0.87,
                "risk_factors": self._identify_risk_factors(data),
                "explanation": f"Based on clinical factors, your diabetes risk is {risk_level.lower()}. Key factors include glucose level ({glucose} mg/dL), BMI ({bmi}), and lifestyle factors."
            }
            
        except Exception as e:
            return {
                "error": f"Prediction failed: {str(e)}",
                "risk_score": 0.0,
                "risk_level": "Unknown",
                "recommendations": ["Please consult with a healthcare provider"],
                "confidence": 0.0
            }
    
    def _identify_risk_factors(self, data: Dict[str, Any]) -> List[str]:
        """Identify specific risk factors present"""
        risk_factors = []
        
        if data.get('age', 0) >= 45:
            risk_factors.append("Age over 45")
        if data.get('bmi', 0) >= 25:
            risk_factors.append("Overweight or obesity")
        if data.get('glucose_level', 0) >= 100:
            risk_factors.append("Elevated glucose levels")
        if data.get('family_history_diabetes', False):
            risk_factors.append("Family history of diabetes")
        if data.get('physical_activity', 0) < 3:
            risk_factors.append("Sedentary lifestyle")
        if data.get('blood_pressure', 0) >= 90:
            risk_factors.append("High blood pressure")
        
        return risk_factors
    
    def get_required_fields(self) -> Dict[str, str]:
        """Return dictionary of required input fields and their types"""
        return {
            "age": "int",
            "gender": "str",
            "bmi": "float",
            "glucose_level": "float",
            "blood_pressure": "float",
            "insulin_level": "float",
            "family_history_diabetes": "str",
            "physical_activity": "float",
            "pregnancies": "int",
            "skin_thickness": "float",
            "diabetes_pedigree_function": "float"
        }
    
    def get_field_descriptions(self) -> Dict[str, str]:
        """Return descriptions for input fields"""
        return {
            "age": "Age in years",
            "gender": "Gender (Male/Female)",
            "bmi": "Body Mass Index (kg/m²)",
            "glucose_level": "Fasting blood glucose level (mg/dL)",
            "blood_pressure": "Diastolic blood pressure (mmHg)",
            "insulin_level": "Serum insulin level (μU/mL)",
            "family_history_diabetes": "Family history of diabetes (Yes/No)",
            "physical_activity": "Physical activity hours per week",
            "pregnancies": "Number of pregnancies (for women)",
            "skin_thickness": "Triceps skin fold thickness (mm)",
            "diabetes_pedigree_function": "Diabetes pedigree function (0.0-2.5)"
        }
    
    def _prepare_features(self, data: Dict[str, Any]) -> np.ndarray:
        """Prepare features for model prediction"""
        features = [
            data.get("pregnancies", 0),
            data.get("glucose_level", 100),
            data.get("blood_pressure", 80),
            data.get("skin_thickness", 20),
            data.get("insulin_level", 80),
            data.get("bmi", 25),
            data.get("diabetes_pedigree_function", 0.5),
            data.get("age", 30),
            1 if data.get("family_history_diabetes", False) else 0,
            data.get("physical_activity", 3)
        ]
        return np.array(features)
    
    def preprocess_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Preprocess input data for diabetes prediction"""
        processed_data = data.copy()
        
        # Ensure numeric fields are properly typed
        numeric_fields = ['age', 'bmi', 'glucose_level', 'blood_pressure', 
                         'insulin_level', 'pregnancies', 'skin_thickness', 
                         'diabetes_pedigree_function', 'physical_activity']
        
        for field in numeric_fields:
            if field in processed_data:
                try:
                    processed_data[field] = float(processed_data[field])
                except (ValueError, TypeError):
                    # Use default values for invalid inputs
                    defaults = {
                        'age': 30, 'bmi': 25, 'glucose_level': 100,
                        'blood_pressure': 80, 'insulin_level': 80,
                        'pregnancies': 0, 'skin_thickness': 20,
                        'diabetes_pedigree_function': 0.5, 'physical_activity': 3
                    }
                    processed_data[field] = defaults.get(field, 0)
        
        # Handle boolean fields
        if 'family_history_diabetes' in processed_data:
            val = processed_data['family_history_diabetes']
            if isinstance(val, str):
                processed_data['family_history_diabetes'] = val.lower() in ['yes', 'true', '1']
            else:
                processed_data['family_history_diabetes'] = bool(val)
        
        return processed_data
    
    def identify_contributing_factors(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify Parkinson's disease contributing factors with detailed analysis"""
        factors = []
        
        # Motor symptoms assessment
        tremor = data.get('tremor_severity', 0)
        rigidity = data.get('rigidity_score', 0)
        bradykinesia = data.get('bradykinesia_score', 0)
        postural = data.get('postural_instability', 0)
        
        motor_total = tremor + rigidity + bradykinesia + postural
        if motor_total > 4:
            severity = "severe" if motor_total > 10 else "moderate" if motor_total > 6 else "mild"
            factors.append({
                "factor": "Motor symptoms",
                "value": f"Tremor: {tremor}, Rigidity: {rigidity}, Bradykinesia: {bradykinesia}, Postural: {postural}",
                "severity": severity,
                "impact": "high",
                "description": f"Classic Parkinson's motor triad present with {severity} severity. UPDRS motor score equivalent: {motor_total * 4}/68"
            })
        
        # Voice analysis - Jitter (frequency perturbation)
        jitter = data.get('mdvp_jitter_percent', 0)
        if jitter > 1.0:
            factors.append({
                "factor": "Voice frequency instability",
                "value": f"Jitter: {jitter}%",
                "severity": "severe" if jitter > 3.0 else "moderate" if jitter > 2.0 else "mild",
                "impact": "high",
                "description": "Increased vocal jitter indicates laryngeal muscle rigidity and reduced vocal cord control typical in Parkinson's"
            })
        
        # Voice analysis - Shimmer (amplitude perturbation)
        shimmer = data.get('mdvp_shimmer', 0)
        if shimmer > 0.03:
            factors.append({
                "factor": "Voice amplitude instability",
                "value": f"Shimmer: {shimmer}",
                "severity": "severe" if shimmer > 0.08 else "moderate" if shimmer > 0.05 else "mild",
                "impact": "high",
                "description": "Elevated shimmer reflects reduced respiratory and laryngeal control affecting voice amplitude consistency"
            })
        
        # Noise-to-harmonics ratio
        nhr = data.get('nhr', 0)
        if nhr > 0.03:
            factors.append({
                "factor": "Voice quality deterioration",
                "value": f"NHR: {nhr}",
                "severity": "moderate",
                "impact": "moderate",
                "description": "Increased noise-to-harmonics ratio indicates breathiness and vocal fold irregularities"
            })
        
        # Harmonics-to-noise ratio
        hnr = data.get('hnr', 30)
        if hnr < 20:
            factors.append({
                "factor": "Reduced voice clarity",
                "value": f"HNR: {hnr} dB",
                "severity": "moderate",
                "impact": "moderate",
                "description": "Low harmonics-to-noise ratio indicates hoarse, breathy voice quality characteristic of Parkinson's"
            })
        
        # Nonlinear dynamics measures
        rpde = data.get('rpde', 0)
        dfa = data.get('dfa', 0)
        if rpde > 0.6 or dfa > 0.8:
            factors.append({
                "factor": "Voice pattern complexity",
                "value": f"RPDE: {rpde}, DFA: {dfa}",
                "severity": "moderate",
                "impact": "moderate",
                "description": "Altered nonlinear voice dynamics suggest disrupted neural control of vocalization"
            })
        
        # Age and gender factors
        age = data.get('age', 0)
        if age > 60:
            factors.append({
                "factor": "Age-related risk",
                "value": f"Age: {age} years",
                "severity": "moderate",
                "impact": "moderate",
                "description": f"Parkinson's incidence increases significantly after age 60, current risk level: {'high' if age > 70 else 'moderate'}"
            })
        
        # Family history
        if data.get('family_history', 0) == 1:
            factors.append({
                "factor": "Genetic predisposition",
                "value": "Family history present",
                "severity": "moderate",
                "impact": "moderate",
                "description": "Family history increases Parkinson's risk 2-3 fold through genetic mutations (LRRK2, SNCA, PARK genes)"
            })
        
        return factors
    
    def analyze_health_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze Parkinson's-specific health metrics"""
        # Calculate composite scores
        updrs_motor_score = self._calculate_updrs_motor_score(data)
        voice_impairment_score = self._calculate_voice_impairment_score(data)
        disease_stage = self._estimate_disease_stage(data)
        
        return {
            "motor_assessment": {
                "tremor": {"value": data.get('tremor_severity', 0), "scale": "0-4", "interpretation": self._interpret_motor_score(data.get('tremor_severity', 0))},
                "rigidity": {"value": data.get('rigidity_score', 0), "scale": "0-4", "interpretation": self._interpret_motor_score(data.get('rigidity_score', 0))},
                "bradykinesia": {"value": data.get('bradykinesia_score', 0), "scale": "0-4", "interpretation": self._interpret_motor_score(data.get('bradykinesia_score', 0))},
                "postural_instability": {"value": data.get('postural_instability', 0), "scale": "0-4", "interpretation": self._interpret_motor_score(data.get('postural_instability', 0))},
                "updrs_motor_equivalent": {"value": updrs_motor_score, "max_score": 68, "severity": self._interpret_updrs_score(updrs_motor_score)}
            },
            "voice_analysis": {
                "frequency_stability": {
                    "jitter_percent": {"value": data.get('mdvp_jitter_percent', 0), "normal_range": "<1.0%", "status": "abnormal" if data.get('mdvp_jitter_percent', 0) > 1.0 else "normal"},
                    "fundamental_frequency": {"value": data.get('mdvp_fo', 0), "unit": "Hz", "interpretation": self._interpret_fundamental_frequency(data.get('mdvp_fo', 0), data.get('gender', 0))}
                },
                "amplitude_stability": {
                    "shimmer": {"value": data.get('mdvp_shimmer', 0), "normal_range": "<0.03", "status": "abnormal" if data.get('mdvp_shimmer', 0) > 0.03 else "normal"},
                    "shimmer_db": {"value": data.get('mdvp_shimmer_db', 0), "normal_range": "<0.35 dB"}
                },
                "voice_quality": {
                    "nhr": {"value": data.get('nhr', 0), "normal_range": "<0.03", "status": "abnormal" if data.get('nhr', 0) > 0.03 else "normal"},
                    "hnr": {"value": data.get('hnr', 30), "normal_range": ">20 dB", "status": "abnormal" if data.get('hnr', 30) < 20 else "normal"}
                },
                "voice_impairment_score": {"value": voice_impairment_score, "interpretation": self._interpret_voice_impairment(voice_impairment_score)}
            },
            "disease_progression": {
                "estimated_stage": {"stage": disease_stage, "description": self._describe_disease_stage(disease_stage)},
                "progression_markers": self._assess_progression_markers(data),
                "functional_impact": self._assess_functional_impact(data)
            }
        }
    
    def assess_lifestyle_impact(self, data: Dict[str, Any]) -> str:
        """Assess lifestyle impact on Parkinson's progression"""
        impact_factors = []
        
        # Motor symptoms impact
        motor_total = data.get('tremor_severity', 0) + data.get('rigidity_score', 0) + data.get('bradykinesia_score', 0) + data.get('postural_instability', 0)
        if motor_total > 4:
            impact_factors.append(f"physical therapy and exercise (current motor symptoms score {motor_total}/16 - exercise can improve mobility by 25%)")
        
        # Voice therapy needs
        if data.get('mdvp_jitter_percent', 0) > 1.0 or data.get('mdvp_shimmer', 0) > 0.03:
            impact_factors.append("speech therapy (voice abnormalities detected - LSVT LOUD therapy can improve voice quality by 40%)")
        
        # Age-related considerations
        age = data.get('age', 0)
        if age > 65:
            impact_factors.append(f"age-appropriate exercise modifications (age {age} - balance training reduces fall risk by 50%)")
        
        # Early intervention opportunities
        if motor_total <= 4 and motor_total > 0:
            impact_factors.append("early intervention strategies (mild symptoms detected - early treatment can slow progression)")
        
        if impact_factors:
            return f"Your condition significantly benefits from targeted interventions. Key recommendations: {', '.join(impact_factors)}. Combined therapies can improve quality of life by 60% and slow progression."
        else:
            return "Current assessment shows minimal Parkinson's indicators. Continue regular exercise, maintain social activities, and monitor for any motor or voice changes."
    
    def calculate_field_risk_contribution(self, field_name: str, value: Any, normalized_value: float) -> float:
        """Calculate Parkinson's-specific risk contribution"""
        risk_weights = {
            'tremor_severity': 0.9,
            'rigidity_score': 0.85,
            'bradykinesia_score': 0.9,
            'postural_instability': 0.8,
            'mdvp_jitter_percent': 0.8,
            'mdvp_shimmer': 0.75,
            'nhr': 0.7,
            'hnr': 0.65,
            'rpde': 0.6,
            'dfa': 0.6,
            'age': 0.5,
            'family_history': 0.6,
            'mdvp_fo': 0.4,
            'ppe': 0.5
        }
        
        base_contribution = abs(normalized_value - 0.5) * 2
        weight = risk_weights.get(field_name, 0.5)
        return base_contribution * weight
    
    def explain_field_risk(self, field_name: str, value: Any) -> str:
        """Explain Parkinson's-specific field risk"""
        explanations = {
            'tremor_severity': f"Tremor severity {value}/4 - resting tremor is a cardinal sign of Parkinson's disease",
            'rigidity_score': f"Rigidity score {value}/4 - muscle stiffness indicates dopaminergic pathway dysfunction",
            'bradykinesia_score': f"Bradykinesia score {value}/4 - slowness of movement is the most disabling Parkinson's symptom",
            'postural_instability': f"Postural instability {value}/4 - balance problems indicate advanced disease progression",
            'mdvp_jitter_percent': f"Voice jitter {value}% - vocal frequency instability reflects laryngeal muscle rigidity",
            'mdvp_shimmer': f"Voice shimmer {value} - amplitude variations indicate reduced respiratory control",
            'nhr': f"Noise-to-harmonics ratio {value} - increased vocal noise suggests vocal fold irregularities",
            'hnr': f"Harmonics-to-noise ratio {value} dB - reduced voice clarity indicates dysarthria",
            'age': f"Age {value} years - Parkinson's incidence increases exponentially after age 60",
            'family_history': "Family history indicates genetic predisposition through LRRK2, SNCA, or PARK gene mutations",
            'rpde': f"RPDE {value} - altered voice complexity suggests disrupted neural control",
            'dfa': f"DFA {value} - abnormal voice dynamics indicate motor control deterioration"
        }
        return explanations.get(field_name, f"Field {field_name} with value {value} contributes to Parkinson's disease risk assessment")
    
    def get_factor_specific_recommendation(self, factor: Dict[str, Any]) -> str:
        """Get Parkinson's-specific recommendations"""
        factor_name = factor['factor'].lower()
        
        if 'motor symptoms' in factor_name:
            return "URGENT: Neurologist consultation for motor symptom evaluation. Consider dopaminergic therapy and physical therapy"
        elif 'voice frequency' in factor_name or 'voice amplitude' in factor_name:
            return "Speech-language pathology evaluation and LSVT LOUD therapy for voice rehabilitation"
        elif 'voice quality' in factor_name or 'voice clarity' in factor_name:
            return "Comprehensive voice assessment and targeted speech therapy interventions"
        elif 'voice pattern' in factor_name:
            return "Advanced voice analysis and specialized speech therapy for motor speech disorders"
        elif 'age-related' in factor_name:
            return "Age-appropriate exercise program, fall prevention strategies, and regular neurological monitoring"
        elif 'genetic' in factor_name:
            return "Genetic counseling, family screening, and enhanced monitoring for early disease detection"
        else:
            return "Comprehensive Parkinson's management: medication optimization, physical therapy, speech therapy, and lifestyle modifications"
    
    def generate_health_metrics_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Parkinson's-specific chart data"""
        return {
            "labels": ["Motor Symptoms", "Voice Stability", "Voice Quality", "Movement Control", "Overall Function"],
            "data": [
                (data.get('tremor_severity', 0) + data.get('rigidity_score', 0) + data.get('bradykinesia_score', 0)) / 12 * 100,
                min(100, (data.get('mdvp_jitter_percent', 0) / 5 + data.get('mdvp_shimmer', 0) / 0.1) * 50),
                min(100, max(0, 100 - (data.get('hnr', 30) / 30 * 100)) + (data.get('nhr', 0) / 0.1 * 50)),
                data.get('postural_instability', 0) / 4 * 100,
                (data.get('tremor_severity', 0) + data.get('rigidity_score', 0) + data.get('bradykinesia_score', 0) + data.get('postural_instability', 0)) / 16 * 100
            ],
            "normal_ranges": [10, 15, 20, 10, 15],
            "chart_type": "radar",
            "colors": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"]
        }
    
    def _calculate_updrs_motor_score(self, data: Dict[str, Any]) -> int:
        """Calculate equivalent UPDRS motor score"""
        return (data.get('tremor_severity', 0) + data.get('rigidity_score', 0) + 
                data.get('bradykinesia_score', 0) + data.get('postural_instability', 0)) * 4
    
    def _calculate_voice_impairment_score(self, data: Dict[str, Any]) -> float:
        """Calculate voice impairment composite score"""
        jitter_score = min(1.0, data.get('mdvp_jitter_percent', 0) / 5.0)
        shimmer_score = min(1.0, data.get('mdvp_shimmer', 0) / 0.1)
        nhr_score = min(1.0, data.get('nhr', 0) / 0.1)
        hnr_score = max(0, 1.0 - data.get('hnr', 30) / 30)
        
        return round((jitter_score + shimmer_score + nhr_score + hnr_score) / 4, 2)
    
    def _estimate_disease_stage(self, data: Dict[str, Any]) -> int:
        """Estimate Hoehn and Yahr disease stage"""
        motor_total = (data.get('tremor_severity', 0) + data.get('rigidity_score', 0) + 
                      data.get('bradykinesia_score', 0) + data.get('postural_instability', 0))
        
        if motor_total == 0: return 0
        elif motor_total <= 4: return 1
        elif motor_total <= 8: return 2
        elif motor_total <= 12: return 3
        else: return 4
    
    def _interpret_motor_score(self, score: int) -> str:
        """Interpret individual motor symptom score"""
        if score == 0: return "Normal"
        elif score == 1: return "Slight"
        elif score == 2: return "Mild"
        elif score == 3: return "Moderate"
        else: return "Severe"
    
    def _interpret_updrs_score(self, score: int) -> str:
        """Interpret UPDRS motor score"""
        if score <= 8: return "Minimal motor impairment"
        elif score <= 20: return "Mild motor impairment"
        elif score <= 40: return "Moderate motor impairment"
        else: return "Severe motor impairment"
    
    def _interpret_fundamental_frequency(self, fo: float, gender: int) -> str:
        """Interpret fundamental frequency based on gender"""
        if gender == 1:  # Male
            if fo < 85: return "Below normal male range"
            elif fo > 180: return "Above normal male range"
            else: return "Normal male range"
        else:  # Female
            if fo < 165: return "Below normal female range"
            elif fo > 265: return "Above normal female range"
            else: return "Normal female range"
    
    def _interpret_voice_impairment(self, score: float) -> str:
        """Interpret voice impairment score"""
        if score < 0.2: return "Minimal voice impairment"
        elif score < 0.4: return "Mild voice impairment"
        elif score < 0.6: return "Moderate voice impairment"
        else: return "Severe voice impairment"
    
    def _describe_disease_stage(self, stage: int) -> str:
        """Describe Hoehn and Yahr stage"""
        descriptions = {
            0: "No signs of disease",
            1: "Unilateral symptoms only",
            2: "Bilateral symptoms without impairment of balance",
            3: "Bilateral symptoms with mild to moderate disability; some postural instability",
            4: "Severe disability; still able to walk or stand unassisted",
            5: "Wheelchair bound or bedridden unless aided"
        }
        return descriptions.get(stage, "Unknown stage")
    
    def _assess_progression_markers(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Assess disease progression markers"""
        markers = {}
        
        if data.get('postural_instability', 0) > 0:
            markers['balance'] = "Postural instability present - indicates disease progression"
        
        if data.get('mdvp_jitter_percent', 0) > 2.0:
            markers['voice'] = "Significant voice changes - may indicate advancing disease"
        
        motor_asymmetry = abs(data.get('tremor_severity', 0) - data.get('rigidity_score', 0))
        if motor_asymmetry > 1:
            markers['asymmetry'] = "Motor symptom asymmetry typical of early Parkinson's"
        
        return markers
    
    def _assess_functional_impact(self, data: Dict[str, Any]) -> str:
        """Assess functional impact of symptoms"""
        motor_total = (data.get('tremor_severity', 0) + data.get('rigidity_score', 0) + 
                      data.get('bradykinesia_score', 0) + data.get('postural_instability', 0))
        
        if motor_total <= 2: return "Minimal functional impact"
        elif motor_total <= 6: return "Mild functional limitations"
        elif motor_total <= 10: return "Moderate functional impairment"
        else: return "Significant functional disability"
    
    def identify_contributing_factors(self, data: Dict[str, Any]) -> List[str]:
        """Identify key kidney disease risk factors"""
        factors = []
        
        # Age factor
        age = data.get('age', 0)
        if age > 65:
            factors.append(f"Advanced age ({age} years) - kidney function naturally declines with age")
        elif age > 50:
            factors.append(f"Mature age ({age} years) - increased risk of chronic kidney disease")
        
        # Blood pressure
        bp = data.get('bp', 80)
        if bp > 140:
            factors.append(f"Severe hypertension ({bp} mmHg) - major cause of kidney damage")
        elif bp > 120:
            factors.append(f"Elevated blood pressure ({bp} mmHg) - contributes to kidney disease progression")
        
        # Specific gravity
        sg = data.get('sg', 1.020)
        if sg < 1.010 or sg > 1.030:
            factors.append(f"Abnormal urine specific gravity ({sg}) - indicates kidney concentration problems")
        
        # Albumin in urine
        albumin = data.get('al', 0)
        if albumin >= 4:
            factors.append("Severe proteinuria - significant kidney damage indicator")
        elif albumin >= 2:
            factors.append("Moderate proteinuria - early kidney disease sign")
        elif albumin >= 1:
            factors.append("Mild proteinuria - possible kidney involvement")
        
        # Sugar in urine
        sugar = data.get('su', 0)
        if sugar >= 3:
            factors.append("Severe glycosuria - uncontrolled diabetes affecting kidneys")
        elif sugar >= 1:
            factors.append("Glycosuria present - diabetes-related kidney risk")
        
        # Red blood cells
        rbc = data.get('rbc', 0)
        if rbc == 1:
            factors.append("Hematuria present - possible kidney inflammation or damage")
        
        # Pus cells
        pc = data.get('pc', 0)
        if pc == 1:
            factors.append("Pyuria present - kidney or urinary tract inflammation")
        
        # Bacteria
        ba = data.get('ba', 0)
        if ba == 1:
            factors.append("Bacteriuria present - urinary tract infection affecting kidney function")
        
        # Blood glucose
        bgr = data.get('bgr', 120)
        if bgr > 180:
            factors.append(f"Severe hyperglycemia ({bgr} mg/dL) - diabetic nephropathy risk")
        elif bgr > 140:
            factors.append(f"Moderate hyperglycemia ({bgr} mg/dL) - diabetes-related kidney damage")
        
        # Blood urea
        bu = data.get('bu', 30)
        if bu > 50:
            factors.append(f"Elevated blood urea ({bu} mg/dL) - reduced kidney filtration")
        
        # Serum creatinine
        sc = data.get('sc', 1.0)
        if sc > 2.0:
            factors.append(f"Severely elevated creatinine ({sc} mg/dL) - significant kidney impairment")
        elif sc > 1.3:
            factors.append(f"Elevated creatinine ({sc} mg/dL) - reduced kidney function")
        
        # Sodium and potassium
        sod = data.get('sod', 140)
        if sod < 135 or sod > 145:
            factors.append(f"Abnormal sodium levels ({sod} mEq/L) - kidney electrolyte regulation issues")
        
        pot = data.get('pot', 4.0)
        if pot > 5.5:
            factors.append(f"Hyperkalemia ({pot} mEq/L) - dangerous kidney function decline")
        elif pot < 3.5:
            factors.append(f"Hypokalemia ({pot} mEq/L) - kidney electrolyte imbalance")
        
        # Hemoglobin
        hemo = data.get('hemo', 12)
        if hemo < 10:
            factors.append(f"Severe anemia (Hb: {hemo} g/dL) - chronic kidney disease complication")
        elif hemo < 12:
            factors.append(f"Mild anemia (Hb: {hemo} g/dL) - possible kidney disease")
        
        return factors
    
    def analyze_health_metrics(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Analyze kidney-related health metrics"""
        analysis = {}
        
        # Kidney function assessment
        sc = data.get('sc', 1.0)
        bu = data.get('bu', 30)
        if sc > 2.0 or bu > 50:
            analysis['kidney_function'] = f"Severely impaired (Creatinine: {sc}, Urea: {bu}) - Stage 3-4 CKD likely"
        elif sc > 1.3 or bu > 40:
            analysis['kidney_function'] = f"Moderately impaired (Creatinine: {sc}, Urea: {bu}) - Stage 2-3 CKD"
        else:
            analysis['kidney_function'] = f"Normal range (Creatinine: {sc}, Urea: {bu}) - good kidney function"
        
        # Proteinuria assessment
        albumin = data.get('al', 0)
        if albumin >= 4:
            analysis['proteinuria'] = "Severe proteinuria - significant glomerular damage"
        elif albumin >= 2:
            analysis['proteinuria'] = "Moderate proteinuria - early diabetic nephropathy or glomerulonephritis"
        elif albumin >= 1:
            analysis['proteinuria'] = "Mild proteinuria - monitor for progression"
        else:
            analysis['proteinuria'] = "No proteinuria - good glomerular function"
        
        # Electrolyte balance
        sod = data.get('sod', 140)
        pot = data.get('pot', 4.0)
        if pot > 5.5 or sod < 130:
            analysis['electrolytes'] = f"Critical imbalance (Na: {sod}, K: {pot}) - immediate medical attention needed"
        elif pot > 5.0 or pot < 3.5 or sod < 135 or sod > 145:
            analysis['electrolytes'] = f"Mild imbalance (Na: {sod}, K: {pot}) - kidney regulation affected"
        else:
            analysis['electrolytes'] = f"Normal balance (Na: {sod}, K: {pot}) - good kidney regulation"
        
        # Anemia assessment
        hemo = data.get('hemo', 12)
        if hemo < 10:
            analysis['anemia'] = f"Severe anemia (Hb: {hemo}) - chronic kidney disease complication"
        elif hemo < 12:
            analysis['anemia'] = f"Mild anemia (Hb: {hemo}) - possible CKD or other causes"
        else:
            analysis['anemia'] = f"Normal hemoglobin (Hb: {hemo}) - no anemia present"
        
        # Diabetes impact
        bgr = data.get('bgr', 120)
        sugar = data.get('su', 0)
        if bgr > 180 or sugar >= 3:
            analysis['diabetes_impact'] = f"Severe diabetes (Glucose: {bgr}, Urine sugar: {sugar}) - high nephropathy risk"
        elif bgr > 140 or sugar >= 1:
            analysis['diabetes_impact'] = f"Moderate diabetes (Glucose: {bgr}, Urine sugar: {sugar}) - monitor kidney function"
        
        return analysis
    
    def assess_lifestyle_impact(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Assess lifestyle factors impact on kidney health"""
        impact = {}
        
        # Blood pressure control
        bp = data.get('bp', 80)
        if bp > 140:
            impact['blood_pressure'] = f"Hypertension ({bp} mmHg) accelerates kidney damage - strict BP control essential"
        elif bp > 120:
            impact['blood_pressure'] = f"Elevated BP ({bp} mmHg) - lifestyle modifications can prevent kidney damage"
        else:
            impact['blood_pressure'] = f"Normal BP ({bp} mmHg) - protective for kidney health"
        
        # Diabetes management
        bgr = data.get('bgr', 120)
        if bgr > 180:
            impact['diabetes_control'] = f"Poor glucose control ({bgr} mg/dL) - urgent diabetes management needed"
        elif bgr > 140:
            impact['diabetes_control'] = f"Suboptimal glucose control ({bgr} mg/dL) - improve diabetes management"
        else:
            impact['diabetes_control'] = f"Good glucose control ({bgr} mg/dL) - continue current management"
        
        # Hydration status
        sg = data.get('sg', 1.020)
        if sg > 1.025:
            impact['hydration'] = f"Concentrated urine (SG: {sg}) - increase fluid intake for kidney health"
        elif sg < 1.010:
            impact['hydration'] = f"Dilute urine (SG: {sg}) - may indicate kidney concentration problems"
        else:
            impact['hydration'] = f"Normal urine concentration (SG: {sg}) - adequate hydration"
        
        # Infection prevention
        ba = data.get('ba', 0)
        pc = data.get('pc', 0)
        if ba == 1 or pc == 1:
            impact['infection_control'] = "UTI present - proper hygiene and complete antibiotic treatment essential"
        
        return impact
    
    def calculate_field_risk_contribution(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate individual field contributions to kidney disease risk"""
        contributions = {}
        
        # Creatinine contribution (0-30%)
        sc = data.get('sc', 1.0)
        contributions['creatinine'] = min((sc - 0.8) / 2.0 * 30, 30) if sc > 0.8 else 0
        
        # Blood urea contribution (0-25%)
        bu = data.get('bu', 30)
        contributions['blood_urea'] = min((bu - 20) / 50 * 25, 25) if bu > 20 else 0
        
        # Proteinuria contribution (0-25%)
        albumin = data.get('al', 0)
        contributions['proteinuria'] = albumin * 6.25  # 0-25%
        
        # Blood pressure contribution (0-20%)
        bp = data.get('bp', 80)
        contributions['blood_pressure'] = min((bp - 120) / 60 * 20, 20) if bp > 120 else 0
        
        # Age contribution (0-15%)
        age = data.get('age', 0)
        contributions['age'] = min(age / 80 * 15, 15)
        
        # Diabetes contribution (0-20%)
        bgr = data.get('bgr', 120)
        sugar = data.get('su', 0)
        diabetes_score = min((bgr - 100) / 100 * 15, 15) + sugar * 2.5
        contributions['diabetes'] = min(diabetes_score, 20)
        
        return contributions
    
    def explain_field_risk(self, field: str, value: Any) -> str:
        """Explain how specific field affects kidney disease risk"""
        explanations = {
            'age': f"Age {value}: Kidney function naturally declines ~1% per year after age 40",
            'bp': f"Blood pressure {value} mmHg: Hypertension damages kidney blood vessels and filtration units",
            'sg': f"Specific gravity {value}: Abnormal values indicate kidney concentration problems",
            'al': f"Albumin level {value}: Protein in urine indicates glomerular damage and filtration problems",
            'su': f"Sugar level {value}: Glucose in urine indicates diabetes affecting kidney function",
            'rbc': "Red blood cells in urine: May indicate kidney inflammation, stones, or damage",
            'pc': "Pus cells in urine: Indicates infection or inflammation affecting kidney function",
            'ba': "Bacteria in urine: UTI can lead to kidney infection and permanent damage if untreated",
            'bgr': f"Blood glucose {value} mg/dL: High glucose damages kidney blood vessels (diabetic nephropathy)",
            'bu': f"Blood urea {value} mg/dL: Elevated levels indicate reduced kidney filtration capacity",
            'sc': f"Serum creatinine {value} mg/dL: Best marker of kidney function - higher levels indicate damage",
            'sod': f"Sodium {value} mEq/L: Abnormal levels indicate kidney electrolyte regulation problems",
            'pot': f"Potassium {value} mEq/L: Dangerous when elevated due to kidney failure",
            'hemo': f"Hemoglobin {value} g/dL: Low levels common in chronic kidney disease due to reduced EPO production"
        }
        return explanations.get(field, f"Field {field} with value {value} contributes to kidney disease risk assessment")
    
    def get_factor_specific_recommendation(self, factor: str, data: Dict[str, Any]) -> str:
        """Get specific recommendations based on kidney risk factors"""
        recommendations = {
            'hypertension': "Strict blood pressure control <130/80 mmHg with ACE inhibitors or ARBs preferred",
            'diabetes': "Tight glycemic control (HbA1c <7%) with diabetes medications and lifestyle modifications",
            'proteinuria': "ACE inhibitor or ARB therapy to reduce protein loss and slow kidney disease progression",
            'infection': "Complete antibiotic course and maintain proper urinary hygiene to prevent recurrence",
            'dehydration': "Maintain adequate hydration (8-10 glasses water daily) unless fluid restricted",
            'electrolyte_imbalance': "Dietary modifications and possible medications to correct sodium/potassium levels",
            'anemia': "Iron supplementation and possible EPO therapy for CKD-related anemia",
            'high_creatinine': "Nephrology referral for CKD staging and management planning",
            'lifestyle': "Low-sodium diet (<2g/day), regular exercise, avoid NSAIDs, limit protein if advanced CKD"
        }
        return recommendations.get(factor, "Regular monitoring of kidney function and follow-up with healthcare provider")
    
    def generate_health_metrics_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive kidney health visualization data"""
        chart_data = {
            'kidney_function_radar': {
                'labels': ['Filtration', 'Proteinuria', 'Electrolytes', 'Blood Pressure', 'Diabetes Control'],
                'datasets': [{
                    'label': 'Current Kidney Health',
                    'data': [
                        max(0, 100 - (data.get('sc', 1.0) - 0.8) / 2.0 * 100),
                        max(0, 100 - data.get('al', 0) * 25),
                        self._calculate_electrolyte_score(data),
                        max(0, 100 - max(0, data.get('bp', 80) - 120) / 60 * 100),
                        max(0, 100 - max(0, data.get('bgr', 120) - 100) / 100 * 100)
                    ],
                    'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                    'borderColor': 'rgba(54, 162, 235, 1)'
                }]
            },
            'ckd_stage_assessment': {
                'current_stage': self._determine_ckd_stage(data),
                'gfr_estimate': self._estimate_gfr(data),
                'progression_risk': self._assess_progression_risk(data)
            },
            'lab_values_trend': {
                'labels': ['Creatinine', 'BUN', 'Albumin', 'Hemoglobin', 'Potassium'],
                'current_values': [
                    data.get('sc', 1.0),
                    data.get('bu', 30),
                    data.get('al', 0),
                    data.get('hemo', 12),
                    data.get('pot', 4.0)
                ],
                'normal_ranges': [1.2, 40, 0, 13, 4.5],
                'critical_thresholds': [2.0, 60, 3, 10, 5.5]
            }
        }
        return chart_data
    
    def _calculate_electrolyte_score(self, data: Dict[str, Any]) -> float:
        """Calculate electrolyte balance score"""
        sod = data.get('sod', 140)
        pot = data.get('pot', 4.0)
        
        sod_score = 100 - abs(sod - 140) / 10 * 20
        pot_score = 100 - abs(pot - 4.0) / 2 * 50
        
        return max(0, (sod_score + pot_score) / 2)
    
    def _determine_ckd_stage(self, data: Dict[str, Any]) -> str:
        """Determine CKD stage based on creatinine and other factors"""
        sc = data.get('sc', 1.0)
        albumin = data.get('al', 0)
        
        if sc < 1.2 and albumin == 0:
            return "Normal kidney function"
        elif sc < 1.4 and albumin <= 1:
            return "Stage 1 CKD (mild)"
        elif sc < 1.8 and albumin <= 2:
            return "Stage 2 CKD (mild to moderate)"
        elif sc < 2.5:
            return "Stage 3 CKD (moderate to severe)"
        elif sc < 4.0:
            return "Stage 4 CKD (severe)"
        else:
            return "Stage 5 CKD (kidney failure)"
    
    def _estimate_gfr(self, data: Dict[str, Any]) -> float:
        """Estimate GFR based on creatinine and age"""
        sc = data.get('sc', 1.0)
        age = data.get('age', 50)
        
        # Simplified GFR estimation
        gfr = max(15, 140 - age) * (1.0 / sc) * 0.85
        return round(gfr, 1)
    
    def _assess_progression_risk(self, data: Dict[str, Any]) -> str:
        """Assess risk of CKD progression"""
        risk_factors = 0
        
        if data.get('bp', 80) > 140:
            risk_factors += 1
        if data.get('bgr', 120) > 140:
            risk_factors += 1
        if data.get('al', 0) >= 2:
            risk_factors += 1
        if data.get('sc', 1.0) > 1.5:
            risk_factors += 1
        
        if risk_factors >= 3:
            return "High risk of progression"
        elif risk_factors >= 2:
            return "Moderate risk of progression"
        else:
            return "Low risk of progression"
    
    def identify_contributing_factors(self, data: Dict[str, Any]) -> List[str]:
        """Identify key contributing factors for heart disease"""
        factors = []
        
        if data.get('age', 0) > 65:
            factors.append("Advanced age (>65 years) significantly increases cardiovascular risk")
        elif data.get('age', 0) > 45:
            factors.append("Middle age (45-65 years) is a moderate risk factor")
            
        if data.get('cholesterol', 0) > 240:
            factors.append("High cholesterol levels (>240 mg/dL) contribute to arterial plaque buildup")
        elif data.get('cholesterol', 0) > 200:
            factors.append("Borderline high cholesterol (200-240 mg/dL) requires monitoring")
            
        if data.get('resting_bp', 0) > 140:
            factors.append("High blood pressure (>140 mmHg) strains the cardiovascular system")
        elif data.get('resting_bp', 0) > 120:
            factors.append("Elevated blood pressure (120-140 mmHg) indicates prehypertension")
            
        if data.get('max_heart_rate', 220) < (220 - data.get('age', 50)) * 0.7:
            factors.append("Low maximum heart rate suggests poor cardiovascular fitness")
            
        if data.get('exercise_angina', 0) == 1:
            factors.append("Exercise-induced angina indicates compromised coronary circulation")
            
        if data.get('st_depression', 0) > 2.0:
            factors.append("Significant ST depression suggests myocardial ischemia")
            
        if data.get('chest_pain_type', 0) in [1, 2]:
            factors.append("Atypical or non-anginal chest pain patterns")
            
        if data.get('fasting_blood_sugar', 0) == 1:
            factors.append("Elevated fasting blood sugar increases cardiovascular risk")
            
        return factors
    
    def analyze_health_metrics(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Analyze heart health metrics"""
        metrics = {}
        
        # Blood Pressure Analysis
        bp = data.get('resting_bp', 0)
        if bp < 90:
            metrics["Blood Pressure"] = "Low (may indicate hypotension)"
        elif bp < 120:
            metrics["Blood Pressure"] = "Normal (optimal cardiovascular health)"
        elif bp < 140:
            metrics["Blood Pressure"] = "Elevated (prehypertension stage)"
        elif bp < 160:
            metrics["Blood Pressure"] = "High Stage 1 (requires intervention)"
        else:
            metrics["Blood Pressure"] = "High Stage 2 (urgent medical attention needed)"
            
        # Cholesterol Analysis
        chol = data.get('cholesterol', 0)
        if chol < 200:
            metrics["Cholesterol"] = "Desirable (low cardiovascular risk)"
        elif chol < 240:
            metrics["Cholesterol"] = "Borderline high (lifestyle modifications needed)"
        else:
            metrics["Cholesterol"] = "High (medical intervention recommended)"
            
        # Heart Rate Analysis
        max_hr = data.get('max_heart_rate', 0)
        age = data.get('age', 50)
        predicted_max = 220 - age
        if max_hr > predicted_max * 0.9:
            metrics["Heart Rate Response"] = "Excellent (good cardiovascular fitness)"
        elif max_hr > predicted_max * 0.8:
            metrics["Heart Rate Response"] = "Good (adequate fitness level)"
        elif max_hr > predicted_max * 0.7:
            metrics["Heart Rate Response"] = "Fair (room for improvement)"
        else:
            metrics["Heart Rate Response"] = "Poor (cardiovascular conditioning needed)"
            
        # ST Depression Analysis
        st_dep = data.get('st_depression', 0)
        if st_dep < 1.0:
            metrics["ECG ST Depression"] = "Normal (no significant ischemia)"
        elif st_dep < 2.0:
            metrics["ECG ST Depression"] = "Mild (possible minor ischemia)"
        elif st_dep < 3.0:
            metrics["ECG ST Depression"] = "Moderate (significant ischemia likely)"
        else:
            metrics["ECG ST Depression"] = "Severe (major coronary compromise)"
            
        return metrics
    
    def assess_lifestyle_impact(self, data: Dict[str, Any]) -> str:
        """Assess lifestyle impact on heart disease risk"""
        impact_factors = []
        
        if data.get('exercise_angina', 0) == 1:
            impact_factors.append("exercise limitations due to chest pain")
            
        if data.get('resting_bp', 0) > 140:
            impact_factors.append("hypertension requiring dietary and lifestyle changes")
            
        if data.get('cholesterol', 0) > 200:
            impact_factors.append("elevated cholesterol needing dietary modifications")
            
        if data.get('fasting_blood_sugar', 0) == 1:
            impact_factors.append("blood sugar control through diet and exercise")
            
        if impact_factors:
            return f"Your lifestyle significantly impacts heart health through: {', '.join(impact_factors)}. Comprehensive lifestyle modifications including diet, exercise, stress management, and regular monitoring are essential for risk reduction."
        else:
            return "Your current health metrics suggest good lifestyle habits. Continue maintaining a heart-healthy diet, regular exercise, stress management, and avoid smoking to preserve cardiovascular health."
    
    def calculate_field_risk_contribution(self, field_name: str, value: Any, normalized_value: float) -> float:
        """Calculate heart disease specific risk contribution"""
        risk_weights = {
            'age': 0.8,
            'cholesterol': 0.9,
            'resting_bp': 0.85,
            'max_heart_rate': 0.7,
            'exercise_angina': 0.9,
            'st_depression': 0.8,
            'chest_pain_type': 0.6,
            'fasting_blood_sugar': 0.7,
            'resting_ecg': 0.5,
            'st_slope': 0.6,
            'ca': 0.85,
            'thal': 0.8,
            'sex': 0.3
        }
        
        base_contribution = abs(normalized_value - 0.5) * 2
        weight = risk_weights.get(field_name, 0.5)
        return base_contribution * weight
    
    def explain_field_risk(self, field_name: str, value: Any) -> str:
        """Explain heart disease specific field risk"""
        explanations = {
            'age': f"Age {value} years - cardiovascular risk increases with age due to arterial stiffening and accumulated damage",
            'cholesterol': f"Cholesterol {value} mg/dL - elevated levels contribute to atherosclerotic plaque formation",
            'resting_bp': f"Blood pressure {value} mmHg - high pressure damages arterial walls and increases cardiac workload",
            'max_heart_rate': f"Maximum heart rate {value} bpm - lower values may indicate poor cardiovascular fitness",
            'exercise_angina': "Exercise-induced chest pain suggests inadequate coronary blood flow during exertion",
            'st_depression': f"ST depression {value} mm - indicates myocardial ischemia during stress testing",
            'chest_pain_type': "Chest pain pattern provides clues about coronary artery involvement",
            'fasting_blood_sugar': "Elevated fasting blood sugar increases cardiovascular risk through multiple mechanisms",
            'ca': f"Number of major vessels ({value}) with significant blockage affects prognosis",
            'thal': "Thallium stress test results indicate perfusion defects in heart muscle"
        }
        return explanations.get(field_name, f"The value {value} for {field_name} contributes to overall cardiovascular risk assessment.")
    
    def get_factor_specific_recommendation(self, factor: Dict[str, Any]) -> str:
        """Get heart disease specific recommendations"""
        factor_name = factor['factor'].lower()
        
        if 'cholesterol' in factor_name:
            return "Follow a heart-healthy diet low in saturated fats, consider statin therapy if prescribed"
        elif 'blood pressure' in factor_name or 'bp' in factor_name:
            return "Reduce sodium intake, maintain healthy weight, practice stress reduction techniques"
        elif 'age' in factor_name:
            return "Focus on modifiable risk factors through lifestyle changes and regular cardiac screening"
        elif 'heart rate' in factor_name:
            return "Engage in regular aerobic exercise to improve cardiovascular fitness and heart rate response"
        elif 'angina' in factor_name or 'chest pain' in factor_name:
            return "Avoid overexertion, carry prescribed nitroglycerin, seek immediate care for worsening symptoms"
        elif 'depression' in factor_name or 'ecg' in factor_name:
            return "Follow up with cardiology for further evaluation and possible cardiac catheterization"
        elif 'blood sugar' in factor_name or 'diabetes' in factor_name or 'fasting_blood_sugar' in factor_name:
            return "Maintain strict blood glucose control through diet, exercise, and medication compliance"
        else:
            return "Work with your healthcare provider to address this specific risk factor"
    
    def generate_health_metrics_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate heart health specific chart data"""
        return {
            "labels": ["Blood Pressure", "Cholesterol", "Heart Rate", "ST Depression", "Exercise Tolerance"],
            "data": [
                min(100, (data.get('resting_bp', 120) / 140) * 100),
                min(100, (data.get('cholesterol', 200) / 240) * 100),
                100 - min(100, (data.get('max_heart_rate', 150) / (220 - data.get('age', 50))) * 100),
                min(100, data.get('st_depression', 0) * 25),
                100 if data.get('exercise_angina', 0) == 0 else 30
            ],
            "normal_ranges": [60, 60, 80, 0, 100],
            "colors": ["#ef4444", "#f97316", "#eab308", "#84cc16", "#22c55e"]
        }

class StrokeRiskPredictor(BasePredictor):
    """Predicts stroke risk based on blood pressure, cholesterol, lifestyle, and family history"""
    
    def __init__(self):
        super().__init__(
            name="Stroke Risk Predictor",
            description="Analyzes blood pressure, cholesterol, lifestyle, and family history to predict stroke risk"
        )
    
    def get_required_fields(self) -> Dict[str, str]:
        return {
            "age": "int",
            "gender": "int",  # 1 = male, 0 = female
            "hypertension": "int",  # 1 = yes, 0 = no
            "heart_disease": "int",  # 1 = yes, 0 = no
            "ever_married": "int",  # 1 = yes, 0 = no
            "work_type": "int",  # 0-4 (private, self-employed, govt, children, never worked)
            "residence_type": "int",  # 1 = urban, 0 = rural
            "avg_glucose_level": "float",
            "bmi": "float",
            "smoking_status": "int",  # 0-3 (never, formerly, smokes, unknown)
            "alcohol_consumption": "int",  # 0-3 (never, occasional, moderate, heavy)
            "physical_activity": "int",  # 0-3 (sedentary, light, moderate, vigorous)
            "family_history_stroke": "int"  # 1 = yes, 0 = no
        }
    
    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            "age": "Age in years",
            "gender": "Gender (1 = Male, 0 = Female)",
            "hypertension": "Hypertension (1 = Yes, 0 = No)",
            "heart_disease": "Heart disease (1 = Yes, 0 = No)",
            "ever_married": "Ever married (1 = Yes, 0 = No)",
            "work_type": "Work type (0 = Private, 1 = Self-employed, 2 = Government, 3 = Children, 4 = Never worked)",
            "residence_type": "Residence type (1 = Urban, 0 = Rural)",
            "avg_glucose_level": "Average glucose level (mg/dL)",
            "bmi": "Body Mass Index",
            "smoking_status": "Smoking status (0 = Never smoked, 1 = Formerly smoked, 2 = Smokes, 3 = Unknown)",
            "alcohol_consumption": "Alcohol consumption (0 = Never, 1 = Occasional, 2 = Moderate, 3 = Heavy)",
            "physical_activity": "Physical activity level (0 = Sedentary, 1 = Light, 2 = Moderate, 3 = Vigorous)",
            "family_history_stroke": "Family history of stroke (1 = Yes, 0 = No)"
        }
    
    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        features = [
            data["age"] / 100.0,
            data["gender"],
            data["hypertension"],
            data["heart_disease"],
            data["ever_married"],
            data["work_type"] / 4.0,
            data["residence_type"],
            data["avg_glucose_level"] / 300.0,
            data["bmi"] / 50.0,
            data["smoking_status"] / 3.0,
            data["alcohol_consumption"] / 3.0,
            data["physical_activity"] / 3.0,
            data["family_history_stroke"]
        ]
        return np.array(features)
    
    def identify_contributing_factors(self, data: Dict[str, Any]) -> List[str]:
        """Identify key contributing factors for stroke risk"""
        factors = []
        
        if data.get('age', 0) > 75:
            factors.append("Advanced age (>75 years) significantly increases stroke risk")
        elif data.get('age', 0) > 55:
            factors.append("Older age (55-75 years) is a major stroke risk factor")
            
        if data.get('hypertension', 0) == 1:
            factors.append("Hypertension is the leading modifiable risk factor for stroke")
            
        if data.get('heart_disease', 0) == 1:
            factors.append("Existing heart disease significantly increases stroke risk")
            
        if data.get('avg_glucose_level', 0) > 140:
            factors.append("Elevated glucose levels (>140 mg/dL) indicate diabetes risk")
        elif data.get('avg_glucose_level', 0) > 100:
            factors.append("Borderline glucose levels (100-140 mg/dL) require monitoring")
            
        if data.get('bmi', 0) > 30:
            factors.append("Obesity (BMI >30) increases stroke risk through multiple pathways")
        elif data.get('bmi', 0) > 25:
            factors.append("Overweight status (BMI 25-30) contributes to stroke risk")
            
        if data.get('smoking_status', 0) == 2:
            factors.append("Current smoking dramatically increases stroke risk")
        elif data.get('smoking_status', 0) == 1:
            factors.append("Former smoking history still carries residual stroke risk")
            
        if data.get('alcohol_consumption', 0) == 3:
            factors.append("Heavy alcohol consumption increases hemorrhagic stroke risk")
            
        if data.get('physical_activity', 0) == 0:
            factors.append("Sedentary lifestyle significantly increases stroke risk")
            
        if data.get('family_history_stroke', 0) == 1:
            factors.append("Family history of stroke indicates genetic predisposition")
            
        return factors
    
    def analyze_health_metrics(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Analyze stroke-related health metrics"""
        metrics = {}
        
        # Blood Pressure Analysis (inferred from hypertension)
        if data.get('hypertension', 0) == 1:
            metrics["Blood Pressure"] = "Hypertensive (major stroke risk factor requiring control)"
        else:
            metrics["Blood Pressure"] = "Normal (protective against stroke)"
            
        # Glucose Analysis
        glucose = data.get('avg_glucose_level', 0)
        if glucose < 100:
            metrics["Blood Glucose"] = "Normal (optimal metabolic health)"
        elif glucose < 126:
            metrics["Blood Glucose"] = "Prediabetic range (increased stroke risk)"
        else:
            metrics["Blood Glucose"] = "Diabetic range (significant stroke risk factor)"
            
        # BMI Analysis
        bmi = data.get('bmi', 0)
        if bmi < 18.5:
            metrics["Body Mass Index"] = "Underweight (may indicate other health issues)"
        elif bmi < 25:
            metrics["Body Mass Index"] = "Normal weight (optimal for stroke prevention)"
        elif bmi < 30:
            metrics["Body Mass Index"] = "Overweight (moderate stroke risk increase)"
        else:
            metrics["Body Mass Index"] = "Obese (significant stroke risk factor)"
            
        # Smoking Status Analysis
        smoking = data.get('smoking_status', 0)
        if smoking == 0:
            metrics["Smoking Status"] = "Never smoked (protective factor)"
        elif smoking == 1:
            metrics["Smoking Status"] = "Former smoker (risk decreases over time)"
        elif smoking == 2:
            metrics["Smoking Status"] = "Current smoker (major modifiable risk factor)"
        else:
            metrics["Smoking Status"] = "Unknown smoking history"
            
        # Physical Activity Analysis
        activity = data.get('physical_activity', 0)
        if activity == 0:
            metrics["Physical Activity"] = "Sedentary (significant stroke risk)"
        elif activity == 1:
            metrics["Physical Activity"] = "Light activity (some protective benefit)"
        elif activity == 2:
            metrics["Physical Activity"] = "Moderate activity (good stroke protection)"
        else:
            metrics["Physical Activity"] = "Vigorous activity (excellent stroke protection)"
            
        return metrics
    
    def assess_lifestyle_impact(self, data: Dict[str, Any]) -> str:
        """Assess lifestyle impact on stroke risk"""
        impact_factors = []
        
        if data.get('smoking_status', 0) == 2:
            impact_factors.append("smoking cessation (can reduce risk by 50% within 2 years)")
            
        if data.get('physical_activity', 0) == 0:
            impact_factors.append("regular physical activity (30 minutes daily can reduce risk by 25%)")
            
        if data.get('bmi', 0) > 25:
            impact_factors.append("weight management (losing 10 pounds can significantly reduce risk)")
            
        if data.get('alcohol_consumption', 0) == 3:
            impact_factors.append("alcohol moderation (limiting to 1-2 drinks daily)")
            
        if data.get('avg_glucose_level', 0) > 100:
            impact_factors.append("blood sugar control through diet and exercise")
            
        if impact_factors:
            return f"Your lifestyle significantly impacts stroke risk. Key areas for improvement include: {', '.join(impact_factors)}. These modifications can reduce your stroke risk by up to 80%."
        else:
            return "Your lifestyle factors show good stroke prevention habits. Continue maintaining healthy weight, regular exercise, no smoking, and moderate alcohol consumption."
    
    def calculate_field_risk_contribution(self, field_name: str, value: Any, normalized_value: float) -> float:
        """Calculate stroke-specific risk contribution"""
        risk_weights = {
            'age': 0.9,
            'hypertension': 0.95,
            'heart_disease': 0.8,
            'avg_glucose_level': 0.7,
            'bmi': 0.6,
            'smoking_status': 0.85,
            'alcohol_consumption': 0.5,
            'physical_activity': 0.6,
            'family_history_stroke': 0.7,
            'gender': 0.4,
            'ever_married': 0.2,
            'work_type': 0.3,
            'residence_type': 0.1
        }
        
        base_contribution = abs(normalized_value - 0.5) * 2
        weight = risk_weights.get(field_name, 0.5)
        return base_contribution * weight
    
    def explain_field_risk(self, field_name: str, value: Any) -> str:
        """Explain stroke-specific field risk"""
        explanations = {
            'age': f"Age {value} years - stroke risk doubles every decade after age 55",
            'hypertension': "Hypertension damages blood vessels and is the #1 modifiable stroke risk factor",
            'heart_disease': "Heart disease increases stroke risk through embolic events and shared risk factors",
            'avg_glucose_level': f"Glucose {value} mg/dL - diabetes increases stroke risk 2-4 times through vascular damage",
            'bmi': f"BMI {value} - excess weight contributes to hypertension, diabetes, and direct vascular effects",
            'smoking_status': "Smoking accelerates atherosclerosis and increases blood clotting tendency",
            'alcohol_consumption': "Heavy alcohol use increases hemorrhagic stroke risk and blood pressure",
            'physical_activity': "Sedentary lifestyle contributes to multiple stroke risk factors",
            'family_history_stroke': "Genetic factors account for 40% of stroke risk through inherited predisposition",
            'gender': "Gender influences stroke risk patterns and hormone-related factors"
        }
        return explanations.get(field_name, f"The value {value} for {field_name} contributes to overall stroke risk assessment.")
    
    def get_factor_specific_recommendation(self, factor: Dict[str, Any]) -> str:
        """Get stroke-specific recommendations"""
        factor_name = factor['factor'].lower()
        
        if 'hypertension' in factor_name or 'blood pressure' in factor_name:
            return "Monitor blood pressure daily, take medications as prescribed, reduce sodium intake"
        elif 'glucose' in factor_name or 'diabetes' in factor_name:
            return "Maintain HbA1c <7%, monitor blood sugar regularly, follow diabetic diet"
        elif 'smoking' in factor_name:
            return "Quit smoking immediately - use nicotine replacement, counseling, or prescription aids"
        elif 'bmi' in factor_name or 'weight' in factor_name:
            return "Achieve healthy weight through caloric restriction and increased physical activity"
        elif 'physical activity' in factor_name or 'exercise' in factor_name:
            return "Engage in 150 minutes moderate aerobic activity weekly plus strength training"
        elif 'alcohol' in factor_name:
            return "Limit alcohol to 1 drink daily for women, 2 for men; consider complete abstinence"
        elif 'heart disease' in factor_name:
            return "Optimize cardiac medications, consider anticoagulation if indicated by cardiologist"
        elif 'age' in factor_name:
            return "Focus on aggressive management of all modifiable risk factors"
        else:
            return "Discuss this risk factor with your healthcare provider for personalized management"
    
    def generate_health_metrics_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate stroke risk specific chart data"""
        return {
            "labels": ["Blood Pressure", "Blood Sugar", "BMI", "Smoking Risk", "Activity Level"],
            "data": [
                100 if data.get('hypertension', 0) == 1 else 20,
                min(100, (data.get('avg_glucose_level', 90) / 200) * 100),
                min(100, (data.get('bmi', 22) / 35) * 100),
                data.get('smoking_status', 0) * 33.33,
                100 - (data.get('physical_activity', 3) * 25)
            ],
            "normal_ranges": [20, 45, 60, 0, 25],
            "colors": ["#ef4444", "#f97316", "#eab308", "#84cc16", "#22c55e"]
        }

class CancerDetectionPredictor(BasePredictor):
    """Predicts cancer risk for breast, lung, prostate, skin, and cervical cancers"""
    
    def __init__(self):
        super().__init__(
            name="Cancer Detection & Risk Predictor",
            description="Detects and predicts risk for breast, lung, prostate, skin, and cervical cancers"
        )
    
    def get_required_fields(self) -> Dict[str, str]:
        return {
            "age": "int",
            "gender": "int",  # 1 = male, 0 = female
            "cancer_type": "int",  # 0 = breast, 1 = lung, 2 = prostate, 3 = skin, 4 = cervical
            "family_history": "int",  # 1 = yes, 0 = no
            "smoking_history": "int",  # 0-3 (never, light, moderate, heavy)
            "alcohol_consumption": "int",  # 0-3
            "bmi": "float",
            "physical_activity": "int",  # 0-3
            "diet_quality": "int",  # 0-3 (poor, fair, good, excellent)
            "sun_exposure": "int",  # 0-3 (minimal, moderate, high, extreme)
            "occupational_exposure": "int",  # 1 = yes, 0 = no
            "hormonal_factors": "int",  # 1 = yes, 0 = no (for breast/cervical)
            "previous_cancer": "int"  # 1 = yes, 0 = no
        }
    
    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            "age": "Age in years",
            "gender": "Gender (1 = Male, 0 = Female)",
            "cancer_type": "Cancer type to assess (0 = Breast, 1 = Lung, 2 = Prostate, 3 = Skin, 4 = Cervical)",
            "family_history": "Family history of cancer (1 = Yes, 0 = No)",
            "smoking_history": "Smoking history (0 = Never, 1 = Light, 2 = Moderate, 3 = Heavy)",
            "alcohol_consumption": "Alcohol consumption (0 = Never, 1 = Light, 2 = Moderate, 3 = Heavy)",
            "bmi": "Body Mass Index",
            "physical_activity": "Physical activity level (0 = Sedentary, 1 = Light, 2 = Moderate, 3 = Vigorous)",
            "diet_quality": "Diet quality (0 = Poor, 1 = Fair, 2 = Good, 3 = Excellent)",
            "sun_exposure": "Sun exposure level (0 = Minimal, 1 = Moderate, 2 = High, 3 = Extreme)",
            "occupational_exposure": "Occupational exposure to carcinogens (1 = Yes, 0 = No)",
            "hormonal_factors": "Hormonal factors (relevant for breast/cervical cancer) (1 = Yes, 0 = No)",
            "previous_cancer": "Previous cancer diagnosis (1 = Yes, 0 = No)"
        }
    
    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        features = [
            data["age"] / 100.0,
            data["gender"],
            data["cancer_type"] / 4.0,
            data["family_history"],
            data["smoking_history"] / 3.0,
            data["alcohol_consumption"] / 3.0,
            data["bmi"] / 50.0,
            data["physical_activity"] / 3.0,
            data["diet_quality"] / 3.0,
            data["sun_exposure"] / 3.0,
            data["occupational_exposure"],
            data["hormonal_factors"],
            data["previous_cancer"]
        ]
        return np.array(features)
    
    def identify_contributing_factors(self, data: Dict[str, Any]) -> List[str]:
        """Identify key cancer risk factors"""
        factors = []
        
        # Age factor
        age = data.get('age', 0)
        if age > 65:
            factors.append(f"Advanced age ({age} years) - significantly increases cancer risk")
        elif age > 50:
            factors.append(f"Mature age ({age} years) - moderately increases cancer risk")
        
        # Lifestyle factors
        smoking = data.get('smoking_history', 0)
        if smoking >= 3:
            factors.append("Heavy smoking history - major lung and multiple cancer risk")
        elif smoking >= 2:
            factors.append("Moderate smoking history - elevated cancer risk")
        
        # Family history
        if data.get('family_history', 0) == 1:
            factors.append("Family history of cancer - genetic predisposition")
        
        # BMI and lifestyle
        bmi = data.get('bmi', 25)
        if bmi > 30:
            factors.append(f"Obesity (BMI: {bmi}) - increases multiple cancer risks")
        
        # Occupational exposure
        if data.get('occupational_exposure', 0) == 1:
            factors.append("Occupational carcinogen exposure - environmental risk factor")
        
        # Sun exposure for skin cancer
        if data.get('sun_exposure', 0) >= 3:
            factors.append("Extreme sun exposure - high skin cancer risk")
        
        # Previous cancer
        if data.get('previous_cancer', 0) == 1:
            factors.append("Previous cancer diagnosis - increased risk of recurrence or secondary cancers")
        
        return factors
    
    def analyze_health_metrics(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Analyze cancer-related health metrics"""
        metrics = {}
        
        # BMI Analysis
        bmi = data.get('bmi', 25)
        if bmi < 18.5:
            metrics["Body Mass Index"] = "Underweight (may indicate underlying health issues)"
        elif bmi < 25:
            metrics["Body Mass Index"] = "Normal weight (optimal for cancer prevention)"
        elif bmi < 30:
            metrics["Body Mass Index"] = "Overweight (moderate cancer risk increase)"
        else:
            metrics["Body Mass Index"] = "Obese (significant cancer risk factor)"
        
        # Smoking Analysis
        smoking = data.get('smoking_history', 0)
        if smoking == 0:
            metrics["Smoking Status"] = "Never smoked (protective factor)"
        elif smoking == 1:
            metrics["Smoking Status"] = "Light smoking history (low-moderate risk)"
        elif smoking == 2:
            metrics["Smoking Status"] = "Moderate smoking history (significant risk)"
        else:
            metrics["Smoking Status"] = "Heavy smoking history (major cancer risk factor)"
        
        # Physical Activity Analysis
        activity = data.get('physical_activity', 0)
        if activity == 0:
            metrics["Physical Activity"] = "Sedentary (increased cancer risk)"
        elif activity == 1:
            metrics["Physical Activity"] = "Light activity (some protective benefit)"
        elif activity == 2:
            metrics["Physical Activity"] = "Moderate activity (good cancer protection)"
        else:
            metrics["Physical Activity"] = "Vigorous activity (excellent cancer protection)"
        
        # Diet Quality Analysis
        diet = data.get('diet_quality', 0)
        if diet == 0:
            metrics["Diet Quality"] = "Poor diet (increased cancer risk)"
        elif diet == 1:
            metrics["Diet Quality"] = "Fair diet (moderate cancer risk)"
        elif diet == 2:
            metrics["Diet Quality"] = "Good diet (protective against cancer)"
        else:
            metrics["Diet Quality"] = "Excellent diet (strong cancer protection)"
        
        return metrics
    
    def assess_lifestyle_impact(self, data: Dict[str, Any]) -> str:
        """Assess lifestyle impact on cancer risk"""
        impact_factors = []
        
        if data.get('smoking_history', 0) >= 2:
            impact_factors.append("smoking cessation (can reduce risk by 50% within 5 years)")
        
        if data.get('physical_activity', 0) == 0:
            impact_factors.append("regular physical activity (can reduce risk by 20-30%)")
        
        if data.get('bmi', 25) > 25:
            impact_factors.append("weight management (maintaining healthy BMI reduces multiple cancer risks)")
        
        if data.get('diet_quality', 0) <= 1:
            impact_factors.append("improved diet quality (fruits, vegetables, whole grains provide cancer protection)")
        
        if data.get('sun_exposure', 0) >= 3:
            impact_factors.append("sun protection measures (can prevent 90% of skin cancers)")
        
        if impact_factors:
            return f"Your lifestyle significantly impacts cancer risk. Key areas for improvement include: {', '.join(impact_factors)}. These modifications can reduce your overall cancer risk by up to 40%."
        else:
            return "Your lifestyle factors show good cancer prevention habits. Continue maintaining healthy weight, regular exercise, no smoking, and protective sun practices."
    
    def calculate_field_risk_contribution(self, field_name: str, value: Any, normalized_value: float) -> float:
        """Calculate cancer-specific risk contribution"""
        risk_weights = {
            'age': 0.9,
            'family_history': 0.8,
            'smoking_history': 0.85,
            'previous_cancer': 0.9,
            'occupational_exposure': 0.7,
            'bmi': 0.6,
            'sun_exposure': 0.7,
            'alcohol_consumption': 0.5,
            'physical_activity': 0.4,
            'diet_quality': 0.4,
            'hormonal_factors': 0.6,
            'gender': 0.3,
            'cancer_type': 0.2
        }
        
        base_contribution = abs(normalized_value - 0.5) * 2
        weight = risk_weights.get(field_name, 0.5)
        return base_contribution * weight
    
    def explain_field_risk(self, field_name: str, value: Any) -> str:
        """Explain cancer-specific field risk"""
        explanations = {
            'age': f"Age {value} years - cancer incidence increases exponentially with age due to cellular damage accumulation",
            'smoking_history': f"Smoking level {value} - tobacco contains 70+ carcinogens causing DNA damage in multiple organs",
            'family_history': "Family history - inherited genetic mutations (BRCA1/2, Lynch syndrome) significantly increase risk",
            'bmi': f"BMI {value} - obesity promotes inflammation, hormone imbalances, and insulin resistance",
            'occupational_exposure': "Occupational exposure - workplace carcinogens cause cumulative DNA damage",
            'sun_exposure': f"Sun exposure level {value} - UV radiation causes skin DNA damage leading to melanoma",
            'alcohol_consumption': f"Alcohol level {value} - ethanol metabolites damage DNA and impair immune surveillance",
            'previous_cancer': "Previous cancer - indicates genetic susceptibility and treatment-related secondary cancer risk",
            'hormonal_factors': "Hormonal factors - estrogen exposure increases breast and endometrial cancer risk"
        }
        return explanations.get(field_name, f"Field {field_name} with value {value} contributes to overall cancer risk assessment")
    
    def get_factor_specific_recommendation(self, factor: Dict[str, Any]) -> str:
        """Get cancer-specific recommendations"""
        factor_name = factor['factor'].lower()
        
        if 'smoking' in factor_name:
            return "URGENT: Complete smoking cessation with nicotine replacement therapy and counseling support"
        elif 'family history' in factor_name:
            return "Genetic counseling and enhanced screening protocols (earlier/more frequent screening)"
        elif 'bmi' in factor_name or 'weight' in factor_name:
            return "Weight reduction through caloric restriction and increased physical activity (target BMI <25)"
        elif 'sun exposure' in factor_name:
            return "Sun protection: SPF 30+ sunscreen, protective clothing, avoid peak UV hours (10am-4pm)"
        elif 'alcohol' in factor_name:
            return "Reduce alcohol consumption to recommended limits (<7 units/week for women, <14 for men)"
        elif 'occupational' in factor_name:
            return "Workplace safety measures: proper PPE, ventilation, regular occupational health monitoring"
        elif 'diet' in factor_name:
            return "Adopt cancer-protective diet: increase fruits/vegetables, reduce processed meats, limit refined sugars"
        elif 'physical activity' in factor_name:
            return "Engage in 150 minutes moderate aerobic activity weekly plus strength training"
        else:
            return "Maintain healthy lifestyle and regular medical follow-up with age-appropriate cancer screening"
    
    def generate_health_metrics_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate cancer risk specific chart data"""
        return {
            "labels": ["Age Risk", "Genetic Risk", "Lifestyle Risk", "Environmental Risk", "Previous History"],
            "data": [
                min(100, (data.get('age', 0) / 80) * 100),
                100 if data.get('family_history', 0) == 1 else 20,
                (data.get('smoking_history', 0) * 25 + (4 - data.get('physical_activity', 2)) * 15 + (4 - data.get('diet_quality', 2)) * 10),
                (data.get('occupational_exposure', 0) * 40 + data.get('sun_exposure', 0) * 15),
                100 if data.get('previous_cancer', 0) == 1 else 10
            ],
            "normal_ranges": [30, 20, 30, 20, 10],
            "colors": ["#ef4444", "#f97316", "#eab308", "#84cc16", "#22c55e"]
        }

class KidneyDiseasePredictor(BasePredictor):
    """Predicts chronic kidney disease from blood and urine data"""
    
    def __init__(self):
        super().__init__(
            name="Kidney Disease Predictor",
            description="Detects chronic kidney disease from blood and urine test data"
        )
    
    def get_required_fields(self) -> Dict[str, str]:
        return {
            "age": "int",
            "blood_pressure": "float",
            "specific_gravity": "float",
            "albumin": "int",  # 0-5
            "sugar": "int",  # 0-5
            "red_blood_cells": "int",  # 1 = normal, 0 = abnormal
            "pus_cell": "int",  # 1 = normal, 0 = abnormal
            "pus_cell_clumps": "int",  # 1 = present, 0 = not present
            "bacteria": "int",  # 1 = present, 0 = not present
            "blood_glucose_random": "float",
            "blood_urea": "float",
            "serum_creatinine": "float",
            "sodium": "float",
            "potassium": "float",
            "hemoglobin": "float",
            "packed_cell_volume": "float",
            "white_blood_cell_count": "float",
            "red_blood_cell_count": "float",
            "hypertension": "int",  # 1 = yes, 0 = no
            "diabetes_mellitus": "int",  # 1 = yes, 0 = no
            "coronary_artery_disease": "int",  # 1 = yes, 0 = no
            "appetite": "int",  # 1 = good, 0 = poor
            "pedal_edema": "int",  # 1 = yes, 0 = no
            "anemia": "int"  # 1 = yes, 0 = no
        }
    
    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            "age": "Age in years",
            "blood_pressure": "Blood pressure (mm Hg)",
            "specific_gravity": "Specific gravity of urine",
            "albumin": "Albumin level (0-5 scale)",
            "sugar": "Sugar level (0-5 scale)",
            "red_blood_cells": "Red blood cells in urine (1 = Normal, 0 = Abnormal)",
            "pus_cell": "Pus cells in urine (1 = Normal, 0 = Abnormal)",
            "pus_cell_clumps": "Pus cell clumps (1 = Present, 0 = Not present)",
            "bacteria": "Bacteria in urine (1 = Present, 0 = Not present)",
            "blood_glucose_random": "Random blood glucose (mg/dL)",
            "blood_urea": "Blood urea (mg/dL)",
            "serum_creatinine": "Serum creatinine (mg/dL)",
            "sodium": "Sodium level (mEq/L)",
            "potassium": "Potassium level (mEq/L)",
            "hemoglobin": "Hemoglobin (g/dL)",
            "packed_cell_volume": "Packed cell volume (%)",
            "white_blood_cell_count": "White blood cell count (cells/cumm)",
            "red_blood_cell_count": "Red blood cell count (millions/cmm)",
            "hypertension": "Hypertension (1 = Yes, 0 = No)",
            "diabetes_mellitus": "Diabetes mellitus (1 = Yes, 0 = No)",
            "coronary_artery_disease": "Coronary artery disease (1 = Yes, 0 = No)",
            "appetite": "Appetite (1 = Good, 0 = Poor)",
            "pedal_edema": "Pedal edema (1 = Yes, 0 = No)",
            "anemia": "Anemia (1 = Yes, 0 = No)"
        }
    
    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        features = [
            data["age"] / 100.0,
            data["blood_pressure"] / 200.0,
            data["specific_gravity"],
            data["albumin"] / 5.0,
            data["sugar"] / 5.0,
            data["red_blood_cells"],
            data["pus_cell"],
            data["pus_cell_clumps"],
            data["bacteria"],
            data["blood_glucose_random"] / 500.0,
            data["blood_urea"] / 200.0,
            data["serum_creatinine"] / 10.0,
            data["sodium"] / 200.0,
            data["potassium"] / 10.0,
            data["hemoglobin"] / 20.0,
            data["packed_cell_volume"] / 100.0,
            data["white_blood_cell_count"] / 20000.0,
            data["red_blood_cell_count"] / 10.0,
            data["hypertension"],
            data["diabetes_mellitus"],
            data["coronary_artery_disease"],
            data["appetite"],
            data["pedal_edema"],
            data["anemia"]
        ]
        return np.array(features)

class LiverDiseasePredictor(BasePredictor):
    """Predicts liver disease including hepatitis, cirrhosis, and fatty liver from lab tests"""
    
    def __init__(self):
        super().__init__(
            name="Liver Disease Predictor",
            description="Detects hepatitis, cirrhosis, and fatty liver disease from laboratory test results"
        )
    
    def get_required_fields(self) -> Dict[str, str]:
        return {
            "age": "int",
            "gender": "int",  # 1 = male, 0 = female
            "total_bilirubin": "float",
            "direct_bilirubin": "float",
            "alkaline_phosphotase": "float",
            "alamine_aminotransferase": "float",
            "aspartate_aminotransferase": "float",
            "total_proteins": "float",
            "albumin": "float",
            "albumin_globulin_ratio": "float",
            "alcohol_consumption": "int",  # 0-3
            "smoking": "int",  # 1 = yes, 0 = no
            "bmi": "float",
            "diabetes": "int",  # 1 = yes, 0 = no
            "family_history": "int"  # 1 = yes, 0 = no
        }
    
    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            "age": "Age in years",
            "gender": "Gender (1 = Male, 0 = Female)",
            "total_bilirubin": "Total bilirubin (mg/dL)",
            "direct_bilirubin": "Direct bilirubin (mg/dL)",
            "alkaline_phosphotase": "Alkaline phosphatase (IU/L)",
            "alamine_aminotransferase": "Alanine aminotransferase (IU/L)",
            "aspartate_aminotransferase": "Aspartate aminotransferase (IU/L)",
            "total_proteins": "Total proteins (g/dL)",
            "albumin": "Albumin (g/dL)",
            "albumin_globulin_ratio": "Albumin/Globulin ratio",
            "alcohol_consumption": "Alcohol consumption (0 = Never, 1 = Light, 2 = Moderate, 3 = Heavy)",
            "smoking": "Smoking status (1 = Yes, 0 = No)",
            "bmi": "Body Mass Index",
            "diabetes": "Diabetes (1 = Yes, 0 = No)",
            "family_history": "Family history of liver disease (1 = Yes, 0 = No)"
        }
    
    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        features = [
            data["age"] / 100.0,
            data["gender"],
            data["total_bilirubin"] / 10.0,
            data["direct_bilirubin"] / 5.0,
            data["alkaline_phosphotase"] / 1000.0,
            data["alamine_aminotransferase"] / 200.0,
            data["aspartate_aminotransferase"] / 200.0,
            data["total_proteins"] / 10.0,
            data["albumin"] / 5.0,
            data["albumin_globulin_ratio"] / 3.0,
            data["alcohol_consumption"] / 3.0,
            data["smoking"],
            data["bmi"] / 50.0,
            data["diabetes"],
            data["family_history"]
        ]
        return np.array(features)
    
    def identify_contributing_factors(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify liver disease contributing factors with detailed analysis"""
        factors = []
        
        # Liver enzyme analysis
        alt = data.get('alamine_aminotransferase', 0)
        ast = data.get('aspartate_aminotransferase', 0)
        if alt > 40 or ast > 40:
            severity = "severe" if max(alt, ast) > 120 else "moderate" if max(alt, ast) > 80 else "mild"
            factors.append({
                "factor": "Elevated liver enzymes",
                "value": f"ALT: {alt} IU/L, AST: {ast} IU/L",
                "severity": severity,
                "impact": "high",
                "description": f"Liver enzymes are {severity}ly elevated, indicating hepatocellular damage. AST/ALT ratio: {round(ast/alt if alt > 0 else 0, 2)}"
            })
        
        # Bilirubin analysis
        total_bili = data.get('total_bilirubin', 0)
        direct_bili = data.get('direct_bilirubin', 0)
        if total_bili > 1.2:
            indirect_bili = total_bili - direct_bili
            bili_type = "conjugated" if direct_bili > indirect_bili else "unconjugated"
            factors.append({
                "factor": "Elevated bilirubin",
                "value": f"Total: {total_bili} mg/dL, Direct: {direct_bili} mg/dL",
                "severity": "severe" if total_bili > 3.0 else "moderate" if total_bili > 2.0 else "mild",
                "impact": "high",
                "description": f"Predominantly {bili_type} hyperbilirubinemia suggesting {'hepatocellular dysfunction' if bili_type == 'conjugated' else 'hemolysis or Gilbert syndrome'}"
            })
        
        # Protein synthesis analysis
        albumin = data.get('albumin', 0)
        total_protein = data.get('total_proteins', 0)
        if albumin < 3.5:
            factors.append({
                "factor": "Hypoalbuminemia",
                "value": f"Albumin: {albumin} g/dL",
                "severity": "severe" if albumin < 2.5 else "moderate" if albumin < 3.0 else "mild",
                "impact": "high",
                "description": "Reduced albumin synthesis indicating impaired liver synthetic function and potential portal hypertension"
            })
        
        # Alkaline phosphatase analysis
        alp = data.get('alkaline_phosphotase', 0)
        if alp > 147:
            factors.append({
                "factor": "Elevated alkaline phosphatase",
                "value": f"ALP: {alp} IU/L",
                "severity": "severe" if alp > 400 else "moderate" if alp > 250 else "mild",
                "impact": "moderate",
                "description": "Elevated ALP suggests cholestatic liver injury, bile duct obstruction, or infiltrative liver disease"
            })
        
        # Lifestyle risk factors
        alcohol = data.get('alcohol_consumption', 0)
        if alcohol >= 2:
            factors.append({
                "factor": "Alcohol consumption",
                "value": f"Level {alcohol}/3",
                "severity": "severe" if alcohol == 3 else "moderate",
                "impact": "high",
                "description": f"{'Heavy' if alcohol == 3 else 'Moderate'} alcohol use increases risk of alcoholic liver disease, steatosis, and cirrhosis"
            })
        
        # Metabolic factors
        bmi = data.get('bmi', 0)
        diabetes = data.get('diabetes', 0)
        if bmi > 30 or diabetes:
            factors.append({
                "factor": "Metabolic risk factors",
                "value": f"BMI: {bmi}, Diabetes: {'Yes' if diabetes else 'No'}",
                "severity": "moderate",
                "impact": "moderate",
                "description": "Obesity and diabetes increase risk of non-alcoholic fatty liver disease (NAFLD) and steatohepatitis"
            })
        
        return factors
    
    def analyze_health_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze liver-specific health metrics"""
        alt = data.get('alamine_aminotransferase', 0)
        ast = data.get('aspartate_aminotransferase', 0)
        total_bili = data.get('total_bilirubin', 0)
        albumin = data.get('albumin', 0)
        
        # Calculate liver function scores
        child_pugh_score = self._calculate_child_pugh_score(data)
        meld_score = self._calculate_meld_score(data)
        fibrosis_score = self._calculate_fibrosis_score(data)
        
        return {
            "liver_enzymes": {
                "alt": {"value": alt, "normal_range": "7-40 IU/L", "status": "elevated" if alt > 40 else "normal"},
                "ast": {"value": ast, "normal_range": "10-40 IU/L", "status": "elevated" if ast > 40 else "normal"},
                "ast_alt_ratio": {"value": round(ast/alt if alt > 0 else 0, 2), "interpretation": self._interpret_ast_alt_ratio(ast, alt)}
            },
            "bilirubin_metabolism": {
                "total_bilirubin": {"value": total_bili, "normal_range": "0.2-1.2 mg/dL", "status": "elevated" if total_bili > 1.2 else "normal"},
                "direct_bilirubin": {"value": data.get('direct_bilirubin', 0), "normal_range": "0.0-0.3 mg/dL"},
                "jaundice_risk": "high" if total_bili > 2.5 else "moderate" if total_bili > 1.5 else "low"
            },
            "synthetic_function": {
                "albumin": {"value": albumin, "normal_range": "3.5-5.0 g/dL", "status": "low" if albumin < 3.5 else "normal"},
                "total_proteins": {"value": data.get('total_proteins', 0), "normal_range": "6.0-8.3 g/dL"},
                "albumin_globulin_ratio": {"value": data.get('albumin_globulin_ratio', 0), "normal_range": "1.1-2.5"}
            },
            "liver_function_scores": {
                "child_pugh_score": {"value": child_pugh_score, "class": self._get_child_pugh_class(child_pugh_score)},
                "meld_score": {"value": meld_score, "interpretation": self._interpret_meld_score(meld_score)},
                "fibrosis_score": {"value": fibrosis_score, "stage": self._get_fibrosis_stage(fibrosis_score)}
            }
        }
    
    def assess_lifestyle_impact(self, data: Dict[str, Any]) -> str:
        """Assess lifestyle impact on liver health"""
        impact_factors = []
        
        alcohol = data.get('alcohol_consumption', 0)
        if alcohol >= 2:
            impact_factors.append(f"alcohol reduction (current level {alcohol}/3 significantly increases liver damage risk)")
        
        if data.get('smoking', 0) == 1:
            impact_factors.append("smoking cessation (smoking accelerates liver fibrosis progression)")
        
        bmi = data.get('bmi', 25)
        if bmi > 30:
            impact_factors.append(f"weight management (BMI {bmi} increases NAFLD risk by 300%)")
        
        if data.get('diabetes', 0) == 1:
            impact_factors.append("diabetes control (uncontrolled diabetes accelerates liver disease progression)")
        
        if impact_factors:
            return f"Your lifestyle significantly impacts liver health. Priority interventions: {', '.join(impact_factors)}. These changes can reduce liver disease progression by 60-80%."
        else:
            return "Your lifestyle factors support good liver health. Continue avoiding excessive alcohol, maintaining healthy weight, and regular medical monitoring."
    
    def calculate_field_risk_contribution(self, field_name: str, value: Any, normalized_value: float) -> float:
        """Calculate liver disease-specific risk contribution"""
        risk_weights = {
            'alamine_aminotransferase': 0.9,
            'aspartate_aminotransferase': 0.9,
            'total_bilirubin': 0.85,
            'albumin': 0.8,
            'alkaline_phosphotase': 0.7,
            'alcohol_consumption': 0.85,
            'family_history': 0.6,
            'diabetes': 0.5,
            'bmi': 0.6,
            'age': 0.4,
            'smoking': 0.4
        }
        
        base_contribution = abs(normalized_value - 0.5) * 2
        weight = risk_weights.get(field_name, 0.5)
        return base_contribution * weight
    
    def explain_field_risk(self, field_name: str, value: Any) -> str:
        """Explain liver disease-specific field risk"""
        explanations = {
            'alamine_aminotransferase': f"ALT {value} IU/L - elevated levels indicate hepatocellular damage and inflammation",
            'aspartate_aminotransferase': f"AST {value} IU/L - elevated levels suggest liver cell injury or muscle damage",
            'total_bilirubin': f"Total bilirubin {value} mg/dL - elevated levels indicate impaired bilirubin processing or hemolysis",
            'albumin': f"Albumin {value} g/dL - low levels indicate impaired liver synthetic function",
            'alkaline_phosphotase': f"ALP {value} IU/L - elevated levels suggest cholestatic liver injury or bile duct problems",
            'alcohol_consumption': f"Alcohol level {value} - chronic consumption causes hepatocyte damage and fibrosis",
            'family_history': "Family history increases genetic predisposition to liver diseases like hemochromatosis",
            'diabetes': "Diabetes increases risk of non-alcoholic fatty liver disease and steatohepatitis",
            'bmi': f"BMI {value} - obesity promotes hepatic steatosis and inflammatory liver disease",
            'smoking': "Smoking accelerates liver fibrosis progression and increases oxidative stress"
        }
        return explanations.get(field_name, f"Field {field_name} with value {value} contributes to liver disease risk assessment")
    
    def get_factor_specific_recommendation(self, factor: Dict[str, Any]) -> str:
        """Get liver disease-specific recommendations"""
        factor_name = factor['factor'].lower()
        
        if 'liver enzymes' in factor_name:
            return "URGENT: Hepatology consultation for elevated liver enzymes. Avoid hepatotoxic medications and alcohol"
        elif 'bilirubin' in factor_name:
            return "Investigate cause of hyperbilirubinemia: imaging studies, viral hepatitis panel, autoimmune markers"
        elif 'albumin' in factor_name:
            return "Address hypoalbuminemia: nutritional assessment, protein supplementation, treat underlying liver disease"
        elif 'alkaline phosphatase' in factor_name:
            return "Evaluate cholestatic pattern: MRCP/ERCP, autoimmune markers, medication review"
        elif 'alcohol' in factor_name:
            return "CRITICAL: Complete alcohol cessation with addiction counseling and liver-protective therapy"
        elif 'metabolic' in factor_name:
            return "Metabolic optimization: diabetes control, weight loss, Mediterranean diet, regular exercise"
        else:
            return "Regular liver function monitoring and lifestyle modifications to prevent disease progression"
    
    def generate_health_metrics_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate liver disease-specific chart data"""
        return {
            "labels": ["Liver Enzymes", "Bilirubin Metabolism", "Synthetic Function", "Lifestyle Risk", "Metabolic Risk"],
            "data": [
                min(100, max(data.get('alamine_aminotransferase', 0), data.get('aspartate_aminotransferase', 0)) / 200 * 100),
                min(100, data.get('total_bilirubin', 0) / 5 * 100),
                max(0, 100 - (data.get('albumin', 4) / 4 * 100)),
                data.get('alcohol_consumption', 0) * 33 + data.get('smoking', 0) * 20,
                (data.get('bmi', 25) / 40 * 50) + (data.get('diabetes', 0) * 50)
            ],
            "normal_ranges": [20, 15, 20, 10, 25],
            "chart_type": "radar",
            "colors": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"]
        }
    
    def _calculate_child_pugh_score(self, data: Dict[str, Any]) -> int:
        """Calculate Child-Pugh score for cirrhosis severity"""
        score = 0
        
        # Bilirubin
        bili = data.get('total_bilirubin', 0)
        if bili < 2: score += 1
        elif bili <= 3: score += 2
        else: score += 3
        
        # Albumin
        albumin = data.get('albumin', 0)
        if albumin > 3.5: score += 1
        elif albumin >= 2.8: score += 2
        else: score += 3
        
        # Assume moderate values for missing clinical data
        score += 2  # Ascites (assume mild)
        score += 2  # Encephalopathy (assume mild)
        score += 2  # PT/INR (assume moderate)
        
        return score
    
    def _calculate_meld_score(self, data: Dict[str, Any]) -> int:
        """Calculate MELD score for liver transplant priority"""
        import math
        
        bili = max(1.0, data.get('total_bilirubin', 1.0))
        # Assume moderate values for missing lab data
        creatinine = 1.2  # mg/dL
        inr = 1.5
        
        meld = 3.78 * math.log(bili) + 11.2 * math.log(inr) + 9.57 * math.log(creatinine) + 6.43
        return max(6, min(40, int(meld)))
    
    def _calculate_fibrosis_score(self, data: Dict[str, Any]) -> float:
        """Calculate fibrosis risk score"""
        score = 0
        
        # Age factor
        age = data.get('age', 0)
        if age > 50: score += 1
        
        # AST/ALT ratio
        ast = data.get('aspartate_aminotransferase', 0)
        alt = data.get('alamine_aminotransferase', 0)
        if alt > 0 and ast/alt > 1: score += 1
        
        # Platelet count (assume normal if not provided)
        # if platelets < 150: score += 1
        
        # Albumin
        if data.get('albumin', 4) < 3.5: score += 1
        
        return score / 4.0
    
    def _interpret_ast_alt_ratio(self, ast: float, alt: float) -> str:
        """Interpret AST/ALT ratio"""
        if alt == 0: return "Cannot calculate"
        ratio = ast / alt
        
        if ratio < 1:
            return "Suggests hepatocellular injury (viral hepatitis, drug toxicity)"
        elif ratio > 2:
            return "Suggests alcoholic liver disease or advanced fibrosis"
        else:
            return "Non-specific pattern, requires further evaluation"
    
    def _get_child_pugh_class(self, score: int) -> str:
        """Get Child-Pugh class from score"""
        if score <= 6: return "Class A (mild)"
        elif score <= 9: return "Class B (moderate)"
        else: return "Class C (severe)"
    
    def _interpret_meld_score(self, score: int) -> str:
        """Interpret MELD score"""
        if score < 10: return "Low mortality risk"
        elif score < 15: return "Moderate mortality risk"
        elif score < 20: return "High mortality risk"
        else: return "Very high mortality risk - transplant evaluation needed"
    
    def _get_fibrosis_stage(self, score: float) -> str:
        """Get fibrosis stage from score"""
        if score < 0.25: return "F0-F1 (minimal fibrosis)"
        elif score < 0.5: return "F2 (moderate fibrosis)"
        elif score < 0.75: return "F3 (advanced fibrosis)"
        else: return "F4 (cirrhosis)"

class AlzheimerPredictor(BasePredictor):
    """Predicts Alzheimer's and dementia risk using memory and behavioral data"""
    
    def __init__(self):
        super().__init__(
            name="Alzheimer's / Dementia Predictor",
            description="Early detection of Alzheimer's and dementia using memory and behavioral assessment data"
        )
    
    def get_required_fields(self) -> Dict[str, str]:
        return {
            "age": "int",
            "gender": "int",  # 1 = male, 0 = female
            "education_years": "int",
            "mmse_score": "int",  # Mini-Mental State Examination (0-30)
            "memory_complaints": "int",  # 1 = yes, 0 = no
            "functional_assessment": "int",  # 0-10 scale
            "depression_score": "int",  # 0-15 scale
            "anxiety_level": "int",  # 0-10 scale
            "sleep_quality": "int",  # 0-10 scale
            "social_isolation": "int",  # 0-10 scale
            "physical_activity": "int",  # 0-3
            "family_history_dementia": "int",  # 1 = yes, 0 = no
            "cardiovascular_disease": "int",  # 1 = yes, 0 = no
            "diabetes": "int",  # 1 = yes, 0 = no
            "hypertension": "int",  # 1 = yes, 0 = no
            "smoking_history": "int",  # 0-3
            "alcohol_consumption": "int"  # 0-3
        }
    
    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            "age": "Age in years",
            "gender": "Gender (1 = Male, 0 = Female)",
            "education_years": "Years of education",
            "mmse_score": "Mini-Mental State Examination score (0-30, higher is better)",
            "memory_complaints": "Subjective memory complaints (1 = Yes, 0 = No)",
            "functional_assessment": "Functional assessment score (0-10, higher is better)",
            "depression_score": "Depression assessment score (0-15, higher indicates more depression)",
            "anxiety_level": "Anxiety level (0-10, higher indicates more anxiety)",
            "sleep_quality": "Sleep quality (0-10, higher is better)",
            "social_isolation": "Social isolation level (0-10, higher indicates more isolation)",
            "physical_activity": "Physical activity level (0 = Sedentary, 1 = Light, 2 = Moderate, 3 = Vigorous)",
            "family_history_dementia": "Family history of dementia (1 = Yes, 0 = No)",
            "cardiovascular_disease": "Cardiovascular disease (1 = Yes, 0 = No)",
            "diabetes": "Diabetes (1 = Yes, 0 = No)",
            "hypertension": "Hypertension (1 = Yes, 0 = No)",
            "smoking_history": "Smoking history (0 = Never, 1 = Light, 2 = Moderate, 3 = Heavy)",
            "alcohol_consumption": "Alcohol consumption (0 = Never, 1 = Light, 2 = Moderate, 3 = Heavy)"
        }
    
    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        features = [
            data["age"] / 100.0,
            data["gender"],
            data["education_years"] / 20.0,
            data["mmse_score"] / 30.0,
            data["memory_complaints"],
            data["functional_assessment"] / 10.0,
            data["depression_score"] / 15.0,
            data["anxiety_level"] / 10.0,
            data["sleep_quality"] / 10.0,
            data["social_isolation"] / 10.0,
            data["physical_activity"] / 3.0,
            data["family_history_dementia"],
            data["cardiovascular_disease"],
            data["diabetes"],
            data["hypertension"],
            data["smoking_history"] / 3.0,
            data["alcohol_consumption"] / 3.0
        ]
        return np.array(features)
    
    def identify_contributing_factors(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify Alzheimer's/dementia contributing factors with detailed analysis"""
        factors = []
        
        # Cognitive assessment
        mmse = data.get('mmse_score', 30)
        if mmse < 24:
            severity = "severe" if mmse < 18 else "moderate" if mmse < 21 else "mild"
            factors.append({
                "factor": "Cognitive impairment",
                "value": f"MMSE: {mmse}/30",
                "severity": severity,
                "impact": "high",
                "description": f"Mini-Mental State Examination score indicates {severity} cognitive impairment. Normal: 24-30, MCI: 18-23, Dementia: <18"
            })
        
        # Functional assessment
        functional = data.get('functional_assessment', 10)
        if functional < 7:
            factors.append({
                "factor": "Functional decline",
                "value": f"Functional score: {functional}/10",
                "severity": "severe" if functional < 4 else "moderate" if functional < 6 else "mild",
                "impact": "high",
                "description": "Reduced ability to perform activities of daily living, indicating progressive functional impairment"
            })
        
        # Memory complaints
        if data.get('memory_complaints', 0) == 1:
            factors.append({
                "factor": "Subjective memory complaints",
                "value": "Present",
                "severity": "moderate",
                "impact": "moderate",
                "description": "Self-reported memory problems may indicate early cognitive decline or mild cognitive impairment"
            })
        
        # Depression and anxiety
        depression = data.get('depression_score', 0)
        anxiety = data.get('anxiety_level', 0)
        if depression > 7 or anxiety > 6:
            factors.append({
                "factor": "Mood disorders",
                "value": f"Depression: {depression}/15, Anxiety: {anxiety}/10",
                "severity": "moderate",
                "impact": "moderate",
                "description": "Depression and anxiety can accelerate cognitive decline and may be early symptoms of dementia"
            })
        
        # Sleep quality
        sleep = data.get('sleep_quality', 10)
        if sleep < 6:
            factors.append({
                "factor": "Poor sleep quality",
                "value": f"Sleep quality: {sleep}/10",
                "severity": "moderate",
                "impact": "moderate",
                "description": "Poor sleep disrupts memory consolidation and increases amyloid-beta accumulation in the brain"
            })
        
        # Social isolation
        isolation = data.get('social_isolation', 0)
        if isolation > 6:
            factors.append({
                "factor": "Social isolation",
                "value": f"Isolation level: {isolation}/10",
                "severity": "moderate",
                "impact": "moderate",
                "description": "Social isolation accelerates cognitive decline and increases dementia risk by 50%"
            })
        
        # Cardiovascular risk factors
        cv_factors = []
        if data.get('cardiovascular_disease', 0): cv_factors.append("CVD")
        if data.get('diabetes', 0): cv_factors.append("diabetes")
        if data.get('hypertension', 0): cv_factors.append("hypertension")
        
        if cv_factors:
            factors.append({
                "factor": "Cardiovascular risk factors",
                "value": ", ".join(cv_factors),
                "severity": "moderate",
                "impact": "high",
                "description": "Vascular risk factors contribute to vascular dementia and accelerate Alzheimer's progression"
            })
        
        # Lifestyle factors
        activity = data.get('physical_activity', 3)
        if activity < 2:
            factors.append({
                "factor": "Physical inactivity",
                "value": f"Activity level: {activity}/3",
                "severity": "moderate",
                "impact": "moderate",
                "description": "Regular physical activity reduces dementia risk by 30% through improved brain blood flow"
            })
        
        return factors
    
    def analyze_health_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze Alzheimer's/dementia-specific health metrics"""
        mmse = data.get('mmse_score', 30)
        functional = data.get('functional_assessment', 10)
        
        # Calculate cognitive domain scores
        cognitive_reserve = self._calculate_cognitive_reserve(data)
        dementia_risk_score = self._calculate_dementia_risk_score(data)
        
        return {
            "cognitive_assessment": {
                "mmse_score": {"value": mmse, "normal_range": "24-30", "interpretation": self._interpret_mmse(mmse)},
                "functional_assessment": {"value": functional, "normal_range": "8-10", "status": "impaired" if functional < 7 else "normal"},
                "cognitive_reserve": {"value": cognitive_reserve, "interpretation": self._interpret_cognitive_reserve(cognitive_reserve)}
            },
            "behavioral_symptoms": {
                "depression_score": {"value": data.get('depression_score', 0), "normal_range": "0-4", "status": "elevated" if data.get('depression_score', 0) > 7 else "normal"},
                "anxiety_level": {"value": data.get('anxiety_level', 0), "normal_range": "0-3", "status": "elevated" if data.get('anxiety_level', 0) > 6 else "normal"},
                "sleep_quality": {"value": data.get('sleep_quality', 10), "normal_range": "7-10", "status": "poor" if data.get('sleep_quality', 10) < 6 else "good"}
            },
            "risk_factors": {
                "age_risk": {"value": data.get('age', 0), "risk_level": "high" if data.get('age', 0) > 75 else "moderate" if data.get('age', 0) > 65 else "low"},
                "family_history": {"present": bool(data.get('family_history_dementia', 0)), "risk_multiplier": 2.5 if data.get('family_history_dementia', 0) else 1.0},
                "vascular_risk": {"factors": self._count_vascular_factors(data), "impact": "high" if self._count_vascular_factors(data) >= 2 else "moderate"}
            },
            "dementia_risk_assessment": {
                "overall_risk_score": {"value": dementia_risk_score, "interpretation": self._interpret_risk_score(dementia_risk_score)},
                "estimated_risk_reduction": {"lifestyle_changes": "30-40%", "cognitive_training": "20-25%", "social_engagement": "15-20%"}
            }
        }
    
    def assess_lifestyle_impact(self, data: Dict[str, Any]) -> str:
        """Assess lifestyle impact on dementia risk"""
        impact_factors = []
        
        activity = data.get('physical_activity', 3)
        if activity < 2:
            impact_factors.append(f"increased physical activity (current level {activity}/3 - regular exercise reduces dementia risk by 30%)")
        
        isolation = data.get('social_isolation', 0)
        if isolation > 6:
            impact_factors.append(f"enhanced social engagement (current isolation {isolation}/10 increases risk by 50%)")
        
        sleep = data.get('sleep_quality', 10)
        if sleep < 6:
            impact_factors.append(f"improved sleep hygiene (current quality {sleep}/10 - poor sleep increases amyloid accumulation)")
        
        education = data.get('education_years', 12)
        if education < 12:
            impact_factors.append("lifelong learning and cognitive stimulation (low education reduces cognitive reserve)")
        
        smoking = data.get('smoking_history', 0)
        if smoking >= 2:
            impact_factors.append("smoking cessation (smoking doubles dementia risk through vascular damage)")
        
        if impact_factors:
            return f"Your lifestyle significantly impacts dementia risk. Key interventions: {', '.join(impact_factors)}. Combined lifestyle modifications can reduce dementia risk by up to 40%."
        else:
            return "Your lifestyle factors support brain health. Continue regular exercise, social engagement, quality sleep, and cognitive stimulation."
    
    def calculate_field_risk_contribution(self, field_name: str, value: Any, normalized_value: float) -> float:
        """Calculate Alzheimer's/dementia-specific risk contribution"""
        risk_weights = {
            'mmse_score': 0.9,
            'functional_assessment': 0.85,
            'age': 0.8,
            'family_history_dementia': 0.75,
            'memory_complaints': 0.7,
            'depression_score': 0.6,
            'cardiovascular_disease': 0.65,
            'diabetes': 0.6,
            'hypertension': 0.55,
            'social_isolation': 0.5,
            'sleep_quality': 0.5,
            'physical_activity': 0.45,
            'education_years': 0.4,
            'smoking_history': 0.4
        }
        
        base_contribution = abs(normalized_value - 0.5) * 2
        weight = risk_weights.get(field_name, 0.5)
        return base_contribution * weight
    
    def explain_field_risk(self, field_name: str, value: Any) -> str:
        """Explain Alzheimer's/dementia-specific field risk"""
        explanations = {
            'mmse_score': f"MMSE score {value}/30 - lower scores indicate progressive cognitive decline and dementia",
            'functional_assessment': f"Functional score {value}/10 - reduced ability to perform daily activities indicates dementia progression",
            'age': f"Age {value} years - dementia risk doubles every 5 years after age 65",
            'family_history_dementia': "Family history increases genetic risk through inherited mutations (APP, PSEN1, PSEN2, APOE4)",
            'memory_complaints': "Subjective memory complaints may indicate mild cognitive impairment, a dementia precursor",
            'depression_score': f"Depression score {value}/15 - depression accelerates cognitive decline and may be early dementia symptom",
            'cardiovascular_disease': "Cardiovascular disease reduces brain blood flow and increases vascular dementia risk",
            'diabetes': "Diabetes causes brain insulin resistance and accelerates Alzheimer's pathology",
            'social_isolation': f"Isolation level {value}/10 - lack of social stimulation accelerates cognitive decline",
            'sleep_quality': f"Sleep quality {value}/10 - poor sleep impairs memory consolidation and increases amyloid accumulation",
            'physical_activity': f"Activity level {value}/3 - exercise promotes neuroplasticity and reduces dementia risk",
            'education_years': f"Education {value} years - higher education builds cognitive reserve protecting against dementia"
        }
        return explanations.get(field_name, f"Field {field_name} with value {value} contributes to dementia risk assessment")
    
    def get_factor_specific_recommendation(self, factor: Dict[str, Any]) -> str:
        """Get Alzheimer's/dementia-specific recommendations"""
        factor_name = factor['factor'].lower()
        
        if 'cognitive impairment' in factor_name:
            return "URGENT: Comprehensive neuropsychological evaluation, brain imaging (MRI/PET), and specialist consultation"
        elif 'functional decline' in factor_name:
            return "Occupational therapy assessment, adaptive equipment, caregiver support, and safety evaluation"
        elif 'memory complaints' in factor_name:
            return "Cognitive assessment, memory training programs, and regular monitoring for progression"
        elif 'mood disorders' in factor_name:
            return "Mental health evaluation, antidepressant therapy if appropriate, counseling, and mood monitoring"
        elif 'sleep' in factor_name:
            return "Sleep study evaluation, sleep hygiene education, and treatment of sleep disorders"
        elif 'social isolation' in factor_name:
            return "Social engagement programs, community activities, family involvement, and support groups"
        elif 'cardiovascular' in factor_name:
            return "Aggressive cardiovascular risk management: blood pressure control, diabetes management, cholesterol reduction"
        elif 'physical inactivity' in factor_name:
            return "Structured exercise program: 150 minutes moderate aerobic activity weekly, strength training, balance exercises"
        else:
            return "Comprehensive dementia prevention strategy: cognitive training, social engagement, physical activity, and regular monitoring"
    
    def generate_health_metrics_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Alzheimer's/dementia-specific chart data"""
        return {
            "labels": ["Cognitive Function", "Functional Ability", "Mood/Behavior", "Vascular Risk", "Lifestyle Protection"],
            "data": [
                (data.get('mmse_score', 30) / 30) * 100,
                (data.get('functional_assessment', 10) / 10) * 100,
                max(0, 100 - ((data.get('depression_score', 0) / 15 + data.get('anxiety_level', 0) / 10) * 50)),
                max(0, 100 - (self._count_vascular_factors(data) * 25)),
                ((data.get('physical_activity', 0) / 3 * 30) + (max(0, 10 - data.get('social_isolation', 0)) / 10 * 30) + (data.get('sleep_quality', 0) / 10 * 40))
            ],
            "normal_ranges": [80, 80, 70, 75, 70],
            "chart_type": "radar",
            "colors": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"]
        }
    
    def _calculate_cognitive_reserve(self, data: Dict[str, Any]) -> float:
        """Calculate cognitive reserve score"""
        education = data.get('education_years', 12)
        activity = data.get('physical_activity', 0)
        social = 10 - data.get('social_isolation', 0)
        
        reserve_score = (education / 20 * 0.4) + (activity / 3 * 0.3) + (social / 10 * 0.3)
        return round(reserve_score, 2)
    
    def _calculate_dementia_risk_score(self, data: Dict[str, Any]) -> float:
        """Calculate overall dementia risk score"""
        risk_score = 0
        
        # Age risk
        age = data.get('age', 0)
        if age > 85: risk_score += 3
        elif age > 75: risk_score += 2
        elif age > 65: risk_score += 1
        
        # Cognitive factors
        if data.get('mmse_score', 30) < 24: risk_score += 3
        if data.get('memory_complaints', 0): risk_score += 1
        if data.get('functional_assessment', 10) < 7: risk_score += 2
        
        # Genetic/family factors
        if data.get('family_history_dementia', 0): risk_score += 2
        
        # Vascular factors
        risk_score += self._count_vascular_factors(data)
        
        # Protective factors (subtract from risk)
        if data.get('education_years', 12) > 16: risk_score -= 1
        if data.get('physical_activity', 0) >= 2: risk_score -= 1
        if data.get('social_isolation', 0) < 3: risk_score -= 1
        
        return max(0, risk_score)
    
    def _interpret_mmse(self, score: int) -> str:
        """Interpret MMSE score"""
        if score >= 24: return "Normal cognition"
        elif score >= 18: return "Mild cognitive impairment"
        elif score >= 10: return "Moderate dementia"
        else: return "Severe dementia"
    
    def _interpret_cognitive_reserve(self, score: float) -> str:
        """Interpret cognitive reserve score"""
        if score > 0.7: return "High cognitive reserve - strong protection against dementia"
        elif score > 0.5: return "Moderate cognitive reserve - some protection against dementia"
        else: return "Low cognitive reserve - increased vulnerability to cognitive decline"
    
    def _count_vascular_factors(self, data: Dict[str, Any]) -> int:
        """Count vascular risk factors"""
        factors = 0
        if data.get('cardiovascular_disease', 0): factors += 1
        if data.get('diabetes', 0): factors += 1
        if data.get('hypertension', 0): factors += 1
        if data.get('smoking_history', 0) >= 2: factors += 1
        return factors
    
    def _interpret_risk_score(self, score: float) -> str:
        """Interpret overall dementia risk score"""
        if score <= 2: return "Low risk - continue preventive measures"
        elif score <= 5: return "Moderate risk - implement risk reduction strategies"
        elif score <= 8: return "High risk - comprehensive intervention needed"
        else: return "Very high risk - urgent specialist evaluation required"

class ParkinsonPredictor(BasePredictor):
    """Predicts Parkinson's disease using voice patterns, tremor, and movement analysis"""
    
    def __init__(self):
        super().__init__(
            name="Parkinson's Disease Predictor",
            description="Detects Parkinson's disease using voice patterns, tremor analysis, and movement assessment"
        )
    
    def get_required_fields(self) -> Dict[str, str]:
        return {
            "age": "int",
            "gender": "int",  # 1 = male, 0 = female
            "mdvp_fo": "float",  # Average vocal fundamental frequency
            "mdvp_fhi": "float",  # Maximum vocal fundamental frequency
            "mdvp_flo": "float",  # Minimum vocal fundamental frequency
            "mdvp_jitter_percent": "float",  # Jitter percentage
            "mdvp_jitter_abs": "float",  # Absolute jitter
            "mdvp_rap": "float",  # Relative amplitude perturbation
            "mdvp_ppq": "float",  # Pitch period perturbation quotient
            "jitter_ddp": "float",  # Jitter DDP
            "mdvp_shimmer": "float",  # Shimmer
            "mdvp_shimmer_db": "float",  # Shimmer in dB
            "shimmer_apq3": "float",  # Shimmer APQ3
            "shimmer_apq5": "float",  # Shimmer APQ5
            "mdvp_apq": "float",  # Amplitude perturbation quotient
            "shimmer_dda": "float",  # Shimmer DDA
            "nhr": "float",  # Noise-to-harmonics ratio
            "hnr": "float",  # Harmonics-to-noise ratio
            "rpde": "float",  # Recurrence period density entropy
            "dfa": "float",  # Detrended fluctuation analysis
            "spread1": "float",  # Nonlinear measure of fundamental frequency variation
            "spread2": "float",  # Nonlinear measure of fundamental frequency variation
            "d2": "float",  # Correlation dimension
            "ppe": "float",  # Pitch period entropy
            "tremor_severity": "int",  # 0-4 scale
            "rigidity_score": "int",  # 0-4 scale
            "bradykinesia_score": "int",  # 0-4 scale
            "postural_instability": "int",  # 0-4 scale
            "family_history": "int"  # 1 = yes, 0 = no
        }
    
    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            "age": "Age in years",
            "gender": "Gender (1 = Male, 0 = Female)",
            "mdvp_fo": "Average vocal fundamental frequency (Hz)",
            "mdvp_fhi": "Maximum vocal fundamental frequency (Hz)",
            "mdvp_flo": "Minimum vocal fundamental frequency (Hz)",
            "mdvp_jitter_percent": "Jitter percentage (%)",
            "mdvp_jitter_abs": "Absolute jitter (ms)",
            "mdvp_rap": "Relative amplitude perturbation",
            "mdvp_ppq": "Pitch period perturbation quotient",
            "jitter_ddp": "Jitter DDP",
            "mdvp_shimmer": "Shimmer",
            "mdvp_shimmer_db": "Shimmer in dB",
            "shimmer_apq3": "Shimmer APQ3",
            "shimmer_apq5": "Shimmer APQ5",
            "mdvp_apq": "Amplitude perturbation quotient",
            "shimmer_dda": "Shimmer DDA",
            "nhr": "Noise-to-harmonics ratio",
            "hnr": "Harmonics-to-noise ratio",
            "rpde": "Recurrence period density entropy",
            "dfa": "Detrended fluctuation analysis",
            "spread1": "Nonlinear measure of fundamental frequency variation",
            "spread2": "Nonlinear measure of fundamental frequency variation",
            "d2": "Correlation dimension",
            "ppe": "Pitch period entropy",
            "tremor_severity": "Tremor severity (0 = None, 1 = Slight, 2 = Mild, 3 = Moderate, 4 = Severe)",
            "rigidity_score": "Rigidity score (0 = None, 1 = Slight, 2 = Mild, 3 = Moderate, 4 = Severe)",
            "bradykinesia_score": "Bradykinesia score (0 = None, 1 = Slight, 2 = Mild, 3 = Moderate, 4 = Severe)",
            "postural_instability": "Postural instability (0 = None, 1 = Slight, 2 = Mild, 3 = Moderate, 4 = Severe)",
            "family_history": "Family history of Parkinson's (1 = Yes, 0 = No)"
        }
    
    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        features = [
            data["age"] / 100.0,
            data["gender"],
            data["mdvp_fo"] / 300.0,
            data["mdvp_fhi"] / 500.0,
            data["mdvp_flo"] / 200.0,
            data["mdvp_jitter_percent"] / 10.0,
            data["mdvp_jitter_abs"] / 0.1,
            data["mdvp_rap"] / 0.1,
            data["mdvp_ppq"] / 0.1,
            data["jitter_ddp"] / 0.1,
            data["mdvp_shimmer"] / 0.1,
            data["mdvp_shimmer_db"] / 2.0,
            data["shimmer_apq3"] / 0.1,
            data["shimmer_apq5"] / 0.1,
            data["mdvp_apq"] / 0.1,
            data["shimmer_dda"] / 0.1,
            data["nhr"] / 0.1,
            data["hnr"] / 50.0,
            data["rpde"] / 1.0,
            data["dfa"] / 1.0,
            data["spread1"] / 1.0,
            data["spread2"] / 1.0,
            data["d2"] / 5.0,
            data["ppe"] / 1.0,
            data["tremor_severity"] / 4.0,
            data["rigidity_score"] / 4.0,
            data["bradykinesia_score"] / 4.0,
            data["postural_instability"] / 4.0,
            data["family_history"]
        ]
        return np.array(features)