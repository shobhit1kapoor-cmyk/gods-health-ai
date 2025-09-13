import numpy as np
from typing import Dict, List, Any
from .base_predictor import BasePredictor

class ObesityRiskPredictor(BasePredictor):
    """Predicts obesity risk and long-term obesity complications"""
    
    def __init__(self):
        super().__init__(
            name="Obesity & BMI Risk Predictor",
            description="Predicts obesity risk and long-term complications related to weight management"
        )
    
    def get_required_fields(self) -> Dict[str, str]:
        return {
            "age": "int",
            "gender": "int",  # 1 = male, 0 = female
            "height": "float",  # cm
            "weight": "float",  # kg
            "waist_circumference": "float",  # cm
            "hip_circumference": "float",  # cm
            "body_fat_percentage": "float",
            "muscle_mass": "float",  # kg
            "metabolic_rate": "float",  # kcal/day
            "physical_activity_level": "int",  # 0-4 scale
            "sedentary_hours_per_day": "int",
            "calories_consumed_daily": "int",
            "fast_food_frequency": "int",  # 0-7 times per week
            "vegetable_servings_daily": "int",
            "fruit_servings_daily": "int",
            "water_intake_liters": "float",
            "sleep_hours_per_night": "float",
            "stress_level": "int",  # 0-10 scale
            "family_history_obesity": "int",  # 1 = yes, 0 = no
            "diabetes": "int",  # 1 = yes, 0 = no
            "hypertension": "int",  # 1 = yes, 0 = no
            "thyroid_disorder": "int",  # 1 = yes, 0 = no
            "medications_weight_gain": "int",  # 1 = yes, 0 = no
            "smoking_status": "int",  # 0 = never, 1 = former, 2 = current
            "alcohol_consumption": "int"  # 0-4 scale
        }
    
    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            "age": "Age in years",
            "gender": "Gender (1 = Male, 0 = Female)",
            "height": "Height in centimeters",
            "weight": "Weight in kilograms",
            "waist_circumference": "Waist circumference in centimeters",
            "hip_circumference": "Hip circumference in centimeters",
            "body_fat_percentage": "Body fat percentage (%)",
            "muscle_mass": "Muscle mass in kilograms",
            "metabolic_rate": "Basal metabolic rate (kcal/day)",
            "physical_activity_level": "Physical activity level (0 = Sedentary, 1 = Light, 2 = Moderate, 3 = Active, 4 = Very Active)",
            "sedentary_hours_per_day": "Hours spent sedentary per day",
            "calories_consumed_daily": "Average daily calorie intake",
            "fast_food_frequency": "Fast food consumption frequency (times per week)",
            "vegetable_servings_daily": "Daily vegetable servings",
            "fruit_servings_daily": "Daily fruit servings",
            "water_intake_liters": "Daily water intake in liters",
            "sleep_hours_per_night": "Average sleep hours per night",
            "stress_level": "Stress level (0-10, higher indicates more stress)",
            "family_history_obesity": "Family history of obesity (1 = Yes, 0 = No)",
            "diabetes": "Diabetes diagnosis (1 = Yes, 0 = No)",
            "hypertension": "Hypertension diagnosis (1 = Yes, 0 = No)",
            "thyroid_disorder": "Thyroid disorder (1 = Yes, 0 = No)",
            "medications_weight_gain": "Taking medications that cause weight gain (1 = Yes, 0 = No)",
            "smoking_status": "Smoking status (0 = Never, 1 = Former, 2 = Current)",
            "alcohol_consumption": "Alcohol consumption (0 = None, 1 = Light, 2 = Moderate, 3 = Heavy, 4 = Very Heavy)"
        }
    
    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        # Calculate BMI
        height_m = data["height"] / 100.0
        bmi = data["weight"] / (height_m ** 2)
        
        # Calculate waist-to-hip ratio
        whr = data["waist_circumference"] / data["hip_circumference"]
        
        features = [
            data["age"] / 100.0,
            data["gender"],
            bmi / 50.0,
            whr,
            data["body_fat_percentage"] / 100.0,
            data["muscle_mass"] / 100.0,
            data["metabolic_rate"] / 3000.0,
            data["physical_activity_level"] / 4.0,
            data["sedentary_hours_per_day"] / 24.0,
            data["calories_consumed_daily"] / 4000.0,
            data["fast_food_frequency"] / 7.0,
            data["vegetable_servings_daily"] / 10.0,
            data["fruit_servings_daily"] / 10.0,
            data["water_intake_liters"] / 5.0,
            data["sleep_hours_per_night"] / 12.0,
            data["stress_level"] / 10.0,
            data["family_history_obesity"],
            data["diabetes"],
            data["hypertension"],
            data["thyroid_disorder"],
            data["medications_weight_gain"],
            data["smoking_status"] / 2.0,
            data["alcohol_consumption"] / 4.0
        ]
        return np.array(features)

    def identify_contributing_factors(self, data: Dict[str, Any], prediction_result: Dict[str, Any]) -> List[str]:
        """Identify key factors contributing to sleep apnea risk"""
        factors = []
        
        # Physical characteristics
        if data["bmi"] >= 30:
            factors.append("Obesity (BMI ≥30)")
        elif data["bmi"] >= 25:
            factors.append("Overweight (BMI 25-29.9)")
        
        if data["neck_circumference"] >= 17 and data["gender"] == 1:  # Male
            factors.append("Large neck circumference (≥17 inches for men)")
        elif data["neck_circumference"] >= 16 and data["gender"] == 0:  # Female
            factors.append("Large neck circumference (≥16 inches for women)")
        
        # Age factor
        if data["age"] >= 65:
            factors.append("Advanced age (≥65 years)")
        elif data["age"] >= 40:
            factors.append("Middle age (40-64 years)")
        
        # Gender
        if data["gender"] == 1:
            factors.append("Male gender (higher risk)")
        
        # Sleep and breathing symptoms
        if data["snoring_frequency"] >= 4:
            factors.append("Frequent snoring (most nights)")
        if data["witnessed_apneas"] >= 3:
            factors.append("Frequent witnessed breathing pauses")
        if data["gasping_choking"] >= 3:
            factors.append("Frequent gasping or choking during sleep")
        
        # Daytime symptoms
        if data["daytime_sleepiness"] >= 3:
            factors.append("Excessive daytime sleepiness")
        if data["morning_headaches"] >= 3:
            factors.append("Frequent morning headaches")
        if data["concentration_problems"] >= 3:
            factors.append("Concentration difficulties")
        
        # Lifestyle factors
        if data["alcohol_consumption"] >= 3:
            factors.append("Heavy alcohol consumption")
        if data["smoking_status"] == 2:
            factors.append("Current smoking")
        if data["sedentary_lifestyle"] >= 3:
            factors.append("Sedentary lifestyle")
        
        # Medical conditions
        if data["hypertension"]:
            factors.append("Hypertension")
        if data["diabetes"]:
            factors.append("Diabetes")
        if data["heart_disease"]:
            factors.append("Heart disease")
        if data["nasal_congestion"] >= 3:
            factors.append("Chronic nasal congestion")
        
        # Family history
        if data["family_history_sleep_apnea"]:
            factors.append("Family history of sleep apnea")
        
        return factors

    def analyze_health_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze health metrics related to sleep apnea risk"""
        return {
            "physical_assessment": {
                "bmi": {
                    "value": data["bmi"],
                    "category": self._get_bmi_category(data["bmi"]),
                    "sleep_apnea_risk": "High" if data["bmi"] >= 30 else "Moderate" if data["bmi"] >= 25 else "Low"
                },
                "neck_circumference": {
                    "value": data["neck_circumference"],
                    "risk_level": self._assess_neck_circumference_risk(data["neck_circumference"], data["gender"])
                },
                "age_risk": "High" if data["age"] >= 65 else "Moderate" if data["age"] >= 40 else "Low"
            },
            "sleep_symptoms": {
                "snoring_severity": ["Never", "Rarely", "Sometimes", "Often", "Always"][data["snoring_frequency"]],
                "apnea_frequency": ["Never", "Rarely", "Sometimes", "Often", "Always"][data["witnessed_apneas"]],
                "gasping_frequency": ["Never", "Rarely", "Sometimes", "Often", "Always"][data["gasping_choking"]],
                "symptom_severity_score": data["snoring_frequency"] + data["witnessed_apneas"] + data["gasping_choking"]
            },
            "daytime_impact": {
                "sleepiness_level": ["None", "Mild", "Moderate", "Severe", "Extreme"][data["daytime_sleepiness"]],
                "morning_headaches": ["Never", "Rarely", "Sometimes", "Often", "Always"][data["morning_headaches"]],
                "concentration_issues": ["None", "Mild", "Moderate", "Severe", "Extreme"][data["concentration_problems"]],
                "quality_of_life_impact": self._assess_qol_impact(data)
            },
            "comorbidity_risk": {
                "cardiovascular_conditions": sum([data["hypertension"], data["heart_disease"]]),
                "metabolic_conditions": data["diabetes"],
                "overall_health_risk": self._calculate_health_risk_score(data)
            },
            "sleep_apnea_risk_score": self._calculate_sleep_apnea_risk_score(data)
        }

    def assess_lifestyle_impact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the impact of lifestyle factors on sleep apnea risk"""
        return {
            "weight_management": {
                "current_bmi": data["bmi"],
                "weight_impact": "Critical" if data["bmi"] >= 35 else "High" if data["bmi"] >= 30 else "Moderate" if data["bmi"] >= 25 else "Low",
                "weight_loss_benefit": "10% weight loss can reduce AHI by 26%" if data["bmi"] >= 30 else "Maintain healthy weight"
            },
            "sleep_hygiene": {
                "sleep_position": "Side sleeping recommended" if data["sleep_position"] != 1 else "Current back sleeping increases risk",
                "alcohol_impact": "Significant negative impact" if data["alcohol_consumption"] >= 3 else "Moderate impact" if data["alcohol_consumption"] >= 2 else "Minimal impact",
                "smoking_impact": "Increases upper airway inflammation" if data["smoking_status"] == 2 else "No negative impact"
            },
            "physical_activity": {
                "current_level": ["Very Active", "Active", "Moderate", "Sedentary", "Very Sedentary"][data["sedentary_lifestyle"]],
                "exercise_benefit": "High" if data["sedentary_lifestyle"] >= 3 else "Moderate",
                "recommended_activity": "150 minutes moderate exercise weekly"
            },
            "environmental_factors": {
                "nasal_breathing": "Impaired" if data["nasal_congestion"] >= 3 else "Normal",
                "airway_optimization": "Consider nasal decongestants" if data["nasal_congestion"] >= 3 else "Maintain clear airways",
                "bedroom_environment": "Optimize humidity and allergen control"
            }
        }

    def _get_bmi_category(self, bmi: float) -> str:
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        elif bmi < 35:
            return "Obese Class I"
        elif bmi < 40:
            return "Obese Class II"
        else:
            return "Obese Class III"

    def _assess_neck_circumference_risk(self, neck_circumference: float, gender: int) -> str:
        if gender == 1:  # Male
            if neck_circumference >= 17:
                return "High Risk"
            elif neck_circumference >= 16:
                return "Moderate Risk"
            else:
                return "Low Risk"
        else:  # Female
            if neck_circumference >= 16:
                return "High Risk"
            elif neck_circumference >= 15:
                return "Moderate Risk"
            else:
                return "Low Risk"

    def _assess_qol_impact(self, data: Dict[str, Any]) -> str:
        impact_score = data["daytime_sleepiness"] + data["morning_headaches"] + data["concentration_problems"]
        if impact_score >= 9:
            return "Severe Impact"
        elif impact_score >= 6:
            return "Moderate Impact"
        elif impact_score >= 3:
            return "Mild Impact"
        else:
            return "Minimal Impact"

    def _calculate_health_risk_score(self, data: Dict[str, Any]) -> int:
        score = 0
        score += 1 if data["hypertension"] else 0
        score += 1 if data["diabetes"] else 0
        score += 1 if data["heart_disease"] else 0
        score += 1 if data["bmi"] >= 30 else 0
        score += 1 if data["age"] >= 65 else 0
        return score

    def _calculate_sleep_apnea_risk_score(self, data: Dict[str, Any]) -> int:
        score = 0
        # BMI contribution
        if data["bmi"] >= 35:
            score += 3
        elif data["bmi"] >= 30:
            score += 2
        elif data["bmi"] >= 25:
            score += 1
        
        # Age contribution
        if data["age"] >= 65:
            score += 2
        elif data["age"] >= 40:
            score += 1
        
        # Gender contribution
        if data["gender"] == 1:
            score += 1
        
        # Symptoms contribution
        score += min(3, data["snoring_frequency"])
        score += min(2, data["witnessed_apneas"])
        score += min(2, data["daytime_sleepiness"])
        
        # Neck circumference
        if (data["gender"] == 1 and data["neck_circumference"] >= 17) or (data["gender"] == 0 and data["neck_circumference"] >= 16):
            score += 2
        
        # Comorbidities
        score += 1 if data["hypertension"] else 0
        score += 1 if data["diabetes"] else 0
        
        return min(20, score)


class CholesterolRiskPredictor(BasePredictor):
    def __init__(self):
        super().__init__()
        self.model_name = "cholesterol_risk_predictor"
        self.required_fields = [
            "age", "gender", "total_cholesterol", "ldl_cholesterol", "hdl_cholesterol",
            "triglycerides", "bmi", "systolic_bp", "diastolic_bp", "smoking_status",
            "diabetes", "family_history_heart_disease", "physical_activity_level",
            "saturated_fat_intake", "trans_fat_intake", "fiber_intake_grams",
            "omega3_intake", "alcohol_consumption", "medication_statins",
            "c_reactive_protein", "homocysteine", "lipoprotein_a"
        ]

    def get_required_fields(self) -> List[str]:
        return self.required_fields

    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            "age": "Age in years",
            "gender": "Gender (0: Female, 1: Male)",
            "total_cholesterol": "Total cholesterol level (mg/dL)",
            "ldl_cholesterol": "LDL cholesterol level (mg/dL)",
            "hdl_cholesterol": "HDL cholesterol level (mg/dL)",
            "triglycerides": "Triglyceride level (mg/dL)",
            "bmi": "Body Mass Index",
            "systolic_bp": "Systolic blood pressure (mmHg)",
            "diastolic_bp": "Diastolic blood pressure (mmHg)",
            "smoking_status": "Smoking status (0: Never, 1: Former, 2: Current)",
            "diabetes": "Diabetes diagnosis (0: No, 1: Yes)",
            "family_history_heart_disease": "Family history of heart disease (0: No, 1: Yes)",
            "physical_activity_level": "Physical activity level (0-4: Sedentary to Very Active)",
            "saturated_fat_intake": "Saturated fat intake level (0-4: Low to Very High)",
            "trans_fat_intake": "Trans fat intake level (0-4: None to Very High)",
            "fiber_intake_grams": "Daily fiber intake in grams",
            "omega3_intake": "Omega-3 fatty acid intake level (0-4: None to Very High)",
            "alcohol_consumption": "Alcohol consumption level (0-4: None to Heavy)",
            "medication_statins": "Taking statin medications (0: No, 1: Yes)",
            "c_reactive_protein": "C-reactive protein level (mg/L)",
            "homocysteine": "Homocysteine level (μmol/L)",
            "lipoprotein_a": "Lipoprotein(a) level (mg/dL)"
        }

    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        features = [
            data["age"] / 100,
            data["gender"],
            data["total_cholesterol"] / 300,
            data["ldl_cholesterol"] / 200,
            data["hdl_cholesterol"] / 100,
            data["triglycerides"] / 400,
            data["bmi"] / 50,
            data["systolic_bp"] / 200,
            data["diastolic_bp"] / 120,
            data["smoking_status"] / 2,
            data["diabetes"],
            data["family_history_heart_disease"],
            data["physical_activity_level"] / 4,
            data["saturated_fat_intake"] / 4,
            data["trans_fat_intake"] / 4,
            min(data["fiber_intake_grams"], 50) / 50,
            data["omega3_intake"] / 4,
            data["alcohol_consumption"] / 4,
            data["medication_statins"],
            min(data["c_reactive_protein"], 10) / 10,
            min(data["homocysteine"], 30) / 30,
            min(data["lipoprotein_a"], 100) / 100
        ]
        return np.array(features)

    def identify_contributing_factors(self, data: Dict[str, Any], prediction_result: Dict[str, Any]) -> List[str]:
        """Identify key factors contributing to cholesterol and atherosclerosis risk"""
        factors = []
        
        # Cholesterol levels
        if data["total_cholesterol"] >= 240:
            factors.append("High total cholesterol (≥240 mg/dL)")
        elif data["total_cholesterol"] >= 200:
            factors.append("Borderline high total cholesterol (200-239 mg/dL)")
        
        if data["ldl_cholesterol"] >= 160:
            factors.append("High LDL cholesterol (≥160 mg/dL)")
        elif data["ldl_cholesterol"] >= 130:
            factors.append("Borderline high LDL cholesterol (130-159 mg/dL)")
        
        if data["hdl_cholesterol"] < 40:
            factors.append("Low HDL cholesterol (<40 mg/dL)")
        
        if data["triglycerides"] >= 200:
            factors.append("High triglycerides (≥200 mg/dL)")
        
        # Lifestyle factors
        if data["saturated_fat_intake"] >= 3:
            factors.append("High saturated fat intake")
        if data["trans_fat_intake"] >= 2:
            factors.append("Significant trans fat consumption")
        if data["fiber_intake_grams"] < 25:
            factors.append("Low fiber intake (<25g/day)")
        if data["physical_activity_level"] <= 1:
            factors.append("Low physical activity level")
        
        # Risk factors
        if data["smoking_status"] == 2:
            factors.append("Current smoking")
        if data["bmi"] >= 30:
            factors.append("Obesity (BMI ≥30)")
        if data["diabetes"]:
            factors.append("Diabetes diagnosis")
        if data["family_history_heart_disease"]:
            factors.append("Family history of heart disease")
        
        # Blood pressure
        if data["systolic_bp"] >= 140 or data["diastolic_bp"] >= 90:
            factors.append("Hypertension")
        
        # Inflammatory markers
        if data["c_reactive_protein"] > 3.0:
            factors.append("Elevated C-reactive protein (>3.0 mg/L)")
        if data["homocysteine"] > 15:
            factors.append("Elevated homocysteine (>15 μmol/L)")
        
        return factors

    def analyze_health_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze health metrics related to cholesterol and atherosclerosis risk"""
        total_hdl_ratio = data["total_cholesterol"] / max(data["hdl_cholesterol"], 1)
        ldl_hdl_ratio = data["ldl_cholesterol"] / max(data["hdl_cholesterol"], 1)
        
        return {
            "cholesterol_profile": {
                "total_cholesterol": {
                    "value": data["total_cholesterol"],
                    "category": self._get_cholesterol_category(data["total_cholesterol"], "total")
                },
                "ldl_cholesterol": {
                    "value": data["ldl_cholesterol"],
                    "category": self._get_cholesterol_category(data["ldl_cholesterol"], "ldl")
                },
                "hdl_cholesterol": {
                    "value": data["hdl_cholesterol"],
                    "category": self._get_cholesterol_category(data["hdl_cholesterol"], "hdl")
                },
                "triglycerides": {
                    "value": data["triglycerides"],
                    "category": self._get_cholesterol_category(data["triglycerides"], "triglycerides")
                }
            },
            "cholesterol_ratios": {
                "total_hdl_ratio": round(total_hdl_ratio, 1),
                "ldl_hdl_ratio": round(ldl_hdl_ratio, 1),
                "risk_assessment": "High" if total_hdl_ratio > 5 else "Moderate" if total_hdl_ratio > 3.5 else "Low"
            },
            "inflammatory_markers": {
                "c_reactive_protein": data["c_reactive_protein"],
                "homocysteine": data["homocysteine"],
                "lipoprotein_a": data["lipoprotein_a"]
            },
            "cardiovascular_risk_score": self._calculate_cv_risk_score(data)
        }

    def assess_lifestyle_impact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the impact of lifestyle factors on cholesterol and atherosclerosis risk"""
        return {
            "dietary_impact": {
                "saturated_fat_level": ["Low", "Moderate", "High", "Very High", "Excessive"][data["saturated_fat_intake"]],
                "trans_fat_level": ["None", "Low", "Moderate", "High", "Very High"][data["trans_fat_intake"]],
                "fiber_adequacy": "Adequate" if data["fiber_intake_grams"] >= 25 else "Insufficient",
                "omega3_level": ["None", "Low", "Moderate", "High", "Very High"][data["omega3_intake"]]
            },
            "activity_impact": {
                "exercise_level": ["Sedentary", "Light", "Moderate", "Active", "Very Active"][data["physical_activity_level"]],
                "hdl_benefit": "Significant" if data["physical_activity_level"] >= 3 else "Moderate" if data["physical_activity_level"] >= 2 else "Minimal"
            },
            "substance_impact": {
                "smoking_effect": "Lowers HDL, increases oxidation" if data["smoking_status"] == 2 else "No negative effect",
                "alcohol_effect": "May raise HDL" if data["alcohol_consumption"] == 1 else "Negative effects" if data["alcohol_consumption"] >= 3 else "Neutral"
            },
            "medication_impact": {
                "statin_use": "Taking statins" if data["medication_statins"] else "Not taking statins",
                "ldl_reduction_potential": "20-50%" if not data["medication_statins"] else "Current therapy"
            }
        }

    def _get_cholesterol_category(self, value: float, cholesterol_type: str) -> str:
        if cholesterol_type == "total":
            if value < 200:
                return "Desirable"
            elif value < 240:
                return "Borderline High"
            else:
                return "High"
        elif cholesterol_type == "ldl":
            if value < 100:
                return "Optimal"
            elif value < 130:
                return "Near Optimal"
            elif value < 160:
                return "Borderline High"
            else:
                return "High"
        elif cholesterol_type == "hdl":
            if value < 40:
                return "Low"
            elif value >= 60:
                return "High (Protective)"
            else:
                return "Normal"
        elif cholesterol_type == "triglycerides":
            if value < 150:
                return "Normal"
            elif value < 200:
                return "Borderline High"
            else:
                return "High"
        return "Unknown"

    def _calculate_cv_risk_score(self, data: Dict[str, Any]) -> int:
        score = 0
        score += 2 if data["total_cholesterol"] >= 240 else 1 if data["total_cholesterol"] >= 200 else 0
        score += 2 if data["ldl_cholesterol"] >= 160 else 1 if data["ldl_cholesterol"] >= 130 else 0
        score += 1 if data["hdl_cholesterol"] < 40 else 0
        score += 1 if data["triglycerides"] >= 200 else 0
        score += 2 if data["smoking_status"] == 2 else 0
        score += 1 if data["diabetes"] else 0
        score += 1 if data["family_history_heart_disease"] else 0
        score += 1 if data["bmi"] >= 30 else 0
        return min(10, score)


class MentalHealthPredictor(BasePredictor):
    def __init__(self):
        super().__init__()
        self.model_name = "mental_health_predictor"
        self.required_fields = [
            "age", "gender", "stress_level", "sleep_hours", "social_support",
            "exercise_frequency", "alcohol_consumption", "smoking_status",
            "chronic_illness", "medication_antidepressants", "therapy_sessions",
            "work_satisfaction", "relationship_status", "financial_stress",
            "trauma_history", "family_history_mental_health"
        ]

    def get_required_fields(self) -> List[str]:
        return self.required_fields

    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            "age": "Age in years",
            "gender": "Gender (0: Female, 1: Male, 2: Other)",
            "stress_level": "Perceived stress level (0-4: None to Extreme)",
            "sleep_hours": "Average hours of sleep per night",
            "social_support": "Level of social support (0-4: None to Excellent)",
            "exercise_frequency": "Exercise frequency per week (0-7 days)",
            "alcohol_consumption": "Alcohol consumption level (0-4: None to Heavy)",
            "smoking_status": "Smoking status (0: Never, 1: Former, 2: Current)",
            "chronic_illness": "Has chronic illness (0: No, 1: Yes)",
            "medication_antidepressants": "Taking antidepressants (0: No, 1: Yes)",
            "therapy_sessions": "Number of therapy sessions per month",
            "work_satisfaction": "Work satisfaction level (0-4: Very Low to Very High)",
            "relationship_status": "Relationship status (0: Single, 1: Partnered, 2: Married, 3: Divorced/Widowed)",
            "financial_stress": "Financial stress level (0-4: None to Extreme)",
            "trauma_history": "History of trauma (0: No, 1: Yes)",
            "family_history_mental_health": "Family history of mental health issues (0: No, 1: Yes)"
        }

    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        features = [
            data["age"] / 100,
            data["gender"] / 2,
            data["stress_level"] / 4,
            min(data["sleep_hours"], 12) / 12,
            data["social_support"] / 4,
            min(data["exercise_frequency"], 7) / 7,
            data["alcohol_consumption"] / 4,
            data["smoking_status"] / 2,
            data["chronic_illness"],
            data["medication_antidepressants"],
            min(data["therapy_sessions"], 20) / 20,
            data["work_satisfaction"] / 4,
            data["relationship_status"] / 3,
            data["financial_stress"] / 4,
            data["trauma_history"],
            data["family_history_mental_health"]
        ]
        return np.array(features)

    def identify_contributing_factors(self, data: Dict[str, Any], prediction_result: Dict[str, Any]) -> List[str]:
        """Identify key factors contributing to mental health risk"""
        factors = []
        
        # Stress and psychological factors
        if data["stress_level"] >= 3:
            factors.append("High stress level")
        if data["financial_stress"] >= 3:
            factors.append("High financial stress")
        if data["work_satisfaction"] <= 1:
            factors.append("Low work satisfaction")
        
        # Sleep and lifestyle
        if data["sleep_hours"] < 6:
            factors.append("Insufficient sleep (<6 hours)")
        elif data["sleep_hours"] > 9:
            factors.append("Excessive sleep (>9 hours)")
        if data["exercise_frequency"] <= 1:
            factors.append("Low physical activity")
        
        # Social and support factors
        if data["social_support"] <= 1:
            factors.append("Poor social support")
        if data["relationship_status"] == 3:  # Divorced/Widowed
            factors.append("Recent relationship loss")
        
        # Substance use
        if data["alcohol_consumption"] >= 3:
            factors.append("Heavy alcohol consumption")
        if data["smoking_status"] == 2:
            factors.append("Current smoking")
        
        # Medical and family history
        if data["chronic_illness"]:
            factors.append("Chronic illness present")
        if data["trauma_history"]:
            factors.append("History of trauma")
        if data["family_history_mental_health"]:
            factors.append("Family history of mental health issues")
        
        # Treatment factors
        if data["medication_antidepressants"]:
            factors.append("Currently on antidepressants")
        if data["therapy_sessions"] == 0:
            factors.append("No therapy sessions")
        
        return factors

    def analyze_health_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze health metrics related to mental health"""
        return {
            "stress_assessment": {
                "overall_stress": ["None", "Mild", "Moderate", "High", "Extreme"][data["stress_level"]],
                "financial_stress": ["None", "Mild", "Moderate", "High", "Extreme"][data["financial_stress"]],
                "work_satisfaction": ["Very Low", "Low", "Moderate", "High", "Very High"][data["work_satisfaction"]]
            },
            "sleep_quality": {
                "hours_per_night": data["sleep_hours"],
                "sleep_adequacy": self._assess_sleep_adequacy(data["sleep_hours"]),
                "sleep_impact": "Negative" if data["sleep_hours"] < 6 or data["sleep_hours"] > 9 else "Positive"
            },
            "social_wellbeing": {
                "support_level": ["None", "Poor", "Fair", "Good", "Excellent"][data["social_support"]],
                "relationship_status": ["Single", "Partnered", "Married", "Divorced/Widowed"][data["relationship_status"]],
                "social_risk": "High" if data["social_support"] <= 1 else "Low"
            },
            "lifestyle_factors": {
                "exercise_frequency": data["exercise_frequency"],
                "exercise_benefit": "High" if data["exercise_frequency"] >= 4 else "Moderate" if data["exercise_frequency"] >= 2 else "Low",
                "substance_use_risk": self._assess_substance_risk(data)
            },
            "mental_health_risk_score": self._calculate_mental_health_risk_score(data)
        }

    def assess_lifestyle_impact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the impact of lifestyle factors on mental health"""
        return {
            "stress_management": {
                "current_stress_level": ["None", "Mild", "Moderate", "High", "Extreme"][data["stress_level"]],
                "coping_resources": "Good" if data["social_support"] >= 3 and data["therapy_sessions"] > 0 else "Limited",
                "stress_reduction_potential": "High" if data["exercise_frequency"] >= 3 and data["sleep_hours"] >= 7 else "Moderate"
            },
            "sleep_impact": {
                "current_sleep": f"{data['sleep_hours']} hours",
                "sleep_quality": self._assess_sleep_adequacy(data["sleep_hours"]),
                "improvement_needed": data["sleep_hours"] < 7 or data["sleep_hours"] > 9
            },
            "social_connection": {
                "support_adequacy": "Adequate" if data["social_support"] >= 2 else "Inadequate",
                "relationship_stability": "Stable" if data["relationship_status"] in [1, 2] else "Unstable",
                "isolation_risk": "High" if data["social_support"] <= 1 else "Low"
            },
            "treatment_engagement": {
                "therapy_utilization": "Active" if data["therapy_sessions"] > 0 else "None",
                "medication_compliance": "On medication" if data["medication_antidepressants"] else "No medication",
                "treatment_adequacy": "Adequate" if data["therapy_sessions"] > 0 or data["medication_antidepressants"] else "Insufficient"
            }
        }

    def _assess_sleep_adequacy(self, sleep_hours: float) -> str:
        if sleep_hours < 6:
            return "Insufficient"
        elif sleep_hours > 9:
            return "Excessive"
        elif 7 <= sleep_hours <= 8:
            return "Optimal"
        else:
            return "Adequate"

    def _assess_substance_risk(self, data: Dict[str, Any]) -> str:
        risk_factors = 0
        if data["alcohol_consumption"] >= 3:
            risk_factors += 2
        elif data["alcohol_consumption"] >= 2:
            risk_factors += 1
        if data["smoking_status"] == 2:
            risk_factors += 2
        
        if risk_factors >= 3:
            return "High"
        elif risk_factors >= 1:
            return "Moderate"
        else:
            return "Low"

    def _calculate_mental_health_risk_score(self, data: Dict[str, Any]) -> int:
        score = 0
        score += data["stress_level"]
        score += data["financial_stress"]
        score += 4 - data["work_satisfaction"]
        score += 2 if data["sleep_hours"] < 6 or data["sleep_hours"] > 9 else 0
        score += 4 - data["social_support"]
        score += 1 if data["alcohol_consumption"] >= 3 else 0
        score += 1 if data["smoking_status"] == 2 else 0
        score += 1 if data["chronic_illness"] else 0
        score += 2 if data["trauma_history"] else 0
        score += 1 if data["family_history_mental_health"] else 0
        score -= 1 if data["therapy_sessions"] > 0 else 0
        score -= 1 if data["exercise_frequency"] >= 3 else 0
        return max(0, min(20, score))
        
        # Blood pressure analysis
        if data["systolic_bp"] >= 140 or data["diastolic_bp"] >= 90:
            factors.append("Current blood pressure indicates hypertension (≥140/90 mmHg)")
        elif data["systolic_bp"] >= 130 or data["diastolic_bp"] >= 80:
            factors.append("Elevated blood pressure (Stage 1 hypertension range)")
        
        # Lifestyle factors
        if data["sodium_intake_mg"] > 2300:
            factors.append("High sodium intake (>2300mg/day)")
        if data["physical_activity_minutes"] < 150:
            factors.append("Insufficient physical activity (<150 minutes/week)")
        if data["bmi"] >= 30:
            factors.append("Obesity (BMI ≥30)")
        elif data["bmi"] >= 25:
            factors.append("Overweight (BMI 25-29.9)")
        
        # Risk factors
        if data["smoking_status"] == 2:
            factors.append("Current smoking")
        if data["alcohol_drinks_per_week"] > 14:
            factors.append("Excessive alcohol consumption (>14 drinks/week)")
        if data["stress_level"] >= 7:
            factors.append("High stress levels")
        if data["sleep_quality"] <= 4:
            factors.append("Poor sleep quality")
        
        # Medical conditions
        if data["family_history_hypertension"]:
            factors.append("Family history of hypertension")
        if data["diabetes"]:
            factors.append("Diabetes diagnosis")
        if data["kidney_disease"]:
            factors.append("Kidney disease")
        
        # Lab values
        if data["cholesterol_total"] > 240:
            factors.append("High total cholesterol (>240 mg/dL)")
        if data["glucose_fasting"] > 126:
            factors.append("Elevated fasting glucose (>126 mg/dL)")
        
        return factors

    def analyze_health_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze health metrics related to hypertension risk"""
        return {
            "blood_pressure": {
                "systolic": data["systolic_bp"],
                "diastolic": data["diastolic_bp"],
                "category": self._get_bp_category(data["systolic_bp"], data["diastolic_bp"]),
                "risk_level": self._assess_bp_risk(data["systolic_bp"], data["diastolic_bp"])
            },
            "cardiovascular_markers": {
                "total_cholesterol": data["cholesterol_total"],
                "hdl_cholesterol": data["hdl_cholesterol"],
                "ldl_cholesterol": data["ldl_cholesterol"],
                "triglycerides": data["triglycerides"],
                "heart_rate": data["heart_rate"]
            },
            "lifestyle_factors": {
                "bmi": data["bmi"],
                "physical_activity_minutes": data["physical_activity_minutes"],
                "sodium_intake_mg": data["sodium_intake_mg"],
                "stress_level": data["stress_level"]
            },
            "risk_score": self._calculate_hypertension_risk_score(data)
        }

    def assess_lifestyle_impact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the impact of lifestyle factors on hypertension risk"""
        return {
            "diet_impact": {
                "sodium_level": "High" if data["sodium_intake_mg"] > 2300 else "Moderate" if data["sodium_intake_mg"] > 1500 else "Low",
                "potassium_adequacy": "Adequate" if data["potassium_intake_mg"] >= 3500 else "Insufficient",
                "sodium_potassium_ratio": data["sodium_intake_mg"] / max(data["potassium_intake_mg"], 1)
            },
            "activity_impact": {
                "exercise_adequacy": "Adequate" if data["physical_activity_minutes"] >= 150 else "Insufficient",
                "bp_reduction_potential": "5-10 mmHg" if data["physical_activity_minutes"] < 150 else "Maintained"
            },
            "substance_impact": {
                "smoking_effect": "Acute BP elevation" if data["smoking_status"] == 2 else "No acute effect",
                "alcohol_effect": "Elevates BP" if data["alcohol_drinks_per_week"] > 14 else "Minimal effect",
                "caffeine_effect": "Temporary elevation" if data["caffeine_intake_mg"] > 400 else "Minimal effect"
            },
            "stress_management": {
                "stress_level": "High" if data["stress_level"] >= 7 else "Moderate" if data["stress_level"] >= 4 else "Low",
                "meditation_benefit": "Significant" if data["meditation_frequency"] >= 3 else "Moderate" if data["meditation_frequency"] >= 1 else "None",
                "work_stress_impact": "High" if data["work_stress_level"] >= 7 else "Moderate" if data["work_stress_level"] >= 4 else "Low"
            }
        }

    def _get_bp_category(self, systolic: float, diastolic: float) -> str:
        if systolic < 120 and diastolic < 80:
            return "Normal"
        elif systolic < 130 and diastolic < 80:
            return "Elevated"
        elif systolic < 140 or diastolic < 90:
            return "Stage 1 Hypertension"
        else:
            return "Stage 2 Hypertension"

    def _assess_bp_risk(self, systolic: float, diastolic: float) -> str:
        if systolic >= 140 or diastolic >= 90:
            return "High"
        elif systolic >= 130 or diastolic >= 80:
            return "Moderate"
        else:
            return "Low"

    def _calculate_hypertension_risk_score(self, data: Dict[str, Any]) -> int:
        score = 0
        score += 2 if data["family_history_hypertension"] else 0
        score += 1 if data["bmi"] >= 25 else 0
        score += 2 if data["smoking_status"] == 2 else 0
        score += 1 if data["alcohol_drinks_per_week"] > 14 else 0
        score += 1 if data["physical_activity_minutes"] < 150 else 0
        score += 1 if data["sodium_intake_mg"] > 2300 else 0
        score += 1 if data["stress_level"] >= 7 else 0
        score += 2 if data["diabetes"] else 0
        return min(10, score)
        
        # BMI analysis
        height_m = data["height"] / 100.0
        bmi = data["weight"] / (height_m ** 2)
        if bmi >= 30:
            factors.append("Current BMI indicates obesity (≥30)")
        elif bmi >= 25:
            factors.append("Current BMI indicates overweight (25-29.9)")
        
        # Body composition
        bf_threshold = 25 if data["gender"] == 1 else 32
        if data["body_fat_percentage"] > bf_threshold:
            factors.append("High body fat percentage")
        waist_threshold = 102 if data["gender"] == 1 else 88
        if data["waist_circumference"] > waist_threshold:
            factors.append("Elevated waist circumference (abdominal obesity)")
        
        # Lifestyle factors
        if data["physical_activity_level"] <= 1:
            factors.append("Low physical activity level")
        if data["sedentary_hours_per_day"] >= 8:
            factors.append("Excessive sedentary time (≥8 hours/day)")
        calorie_threshold = 2500 if data["gender"] == 1 else 2000
        if data["calories_consumed_daily"] > calorie_threshold:
            factors.append("High daily caloric intake")
        if data["fast_food_frequency"] >= 4:
            factors.append("Frequent fast food consumption (≥4 times/week)")
        
        # Sleep and stress
        if data["sleep_hours_per_night"] < 7:
            factors.append("Insufficient sleep (<7 hours/night)")
        if data["stress_level"] >= 7:
            factors.append("High stress levels")
        
        # Medical factors
        if data["family_history_obesity"]:
            factors.append("Family history of obesity")
        if data["diabetes"]:
            factors.append("Diabetes diagnosis")
        if data["thyroid_disorder"]:
            factors.append("Thyroid disorder")
        if data["medications_weight_gain"]:
            factors.append("Taking medications that promote weight gain")
        
        return factors

    def analyze_health_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze health metrics related to obesity risk"""
        height_m = data["height"] / 100.0
        bmi = data["weight"] / (height_m ** 2)
        whr = data["waist_circumference"] / data["hip_circumference"]
        
        whr_threshold = 0.9 if data["gender"] == 1 else 0.85
        
        return {
            "bmi": {
                "value": round(bmi, 1),
                "category": self._get_bmi_category(bmi),
                "risk_level": "High" if bmi >= 30 else "Moderate" if bmi >= 25 else "Normal"
            },
            "waist_hip_ratio": {
                "value": round(whr, 2),
                "risk_level": "High" if whr > whr_threshold else "Normal"
            },
            "body_composition": {
                "body_fat_percentage": data["body_fat_percentage"],
                "muscle_mass_kg": data["muscle_mass"],
                "metabolic_rate": data["metabolic_rate"]
            },
            "lifestyle_score": {
                "physical_activity": data["physical_activity_level"],
                "diet_quality": self._calculate_diet_score(data),
                "sleep_quality": min(10, max(0, 10 - abs(8 - data["sleep_hours_per_night"]) * 2))
            }
        }

    def assess_lifestyle_impact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the impact of lifestyle factors on obesity risk"""
        return {
            "diet_impact": {
                "caloric_balance": "Positive" if data["calories_consumed_daily"] > data["metabolic_rate"] else "Negative",
                "fast_food_risk": "High" if data["fast_food_frequency"] >= 4 else "Moderate" if data["fast_food_frequency"] >= 2 else "Low",
                "nutrition_quality": "Good" if data["vegetable_servings_daily"] >= 5 and data["fruit_servings_daily"] >= 3 else "Poor"
            },
            "activity_impact": {
                "exercise_level": ["Sedentary", "Light", "Moderate", "Active", "Very Active"][data["physical_activity_level"]],
                "sedentary_risk": "High" if data["sedentary_hours_per_day"] >= 8 else "Moderate" if data["sedentary_hours_per_day"] >= 6 else "Low"
            },
            "sleep_impact": {
                "duration_adequacy": "Adequate" if 7 <= data["sleep_hours_per_night"] <= 9 else "Inadequate",
                "weight_impact": "Negative" if data["sleep_hours_per_night"] < 7 or data["sleep_hours_per_night"] > 9 else "Neutral"
            },
            "stress_impact": {
                "level": "High" if data["stress_level"] >= 7 else "Moderate" if data["stress_level"] >= 4 else "Low",
                "weight_impact": "Increases cortisol and appetite" if data["stress_level"] >= 7 else "Minimal impact"
            }
        }

    def _get_bmi_category(self, bmi: float) -> str:
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal weight"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def _calculate_diet_score(self, data: Dict[str, Any]) -> int:
        score = 0
        score += min(3, data["vegetable_servings_daily"])
        score += min(2, data["fruit_servings_daily"])
        score += min(2, data["water_intake_liters"])
        score -= min(3, data["fast_food_frequency"])
        return max(0, min(10, score))

class HypertensionPredictor(BasePredictor):
    """Predicts hypertension risk based on lifestyle and genetic factors"""
    
    def __init__(self):
        super().__init__(
            name="Hypertension (High Blood Pressure) Predictor",
            description="Predicts hypertension risk using lifestyle and genetic risk factors"
        )
    
    def get_required_fields(self) -> Dict[str, str]:
        return {
            "age": "int",
            "gender": "int",  # 1 = male, 0 = female
            "systolic_bp": "float",
            "diastolic_bp": "float",
            "bmi": "float",
            "waist_circumference": "float",
            "family_history_hypertension": "int",  # 1 = yes, 0 = no
            "sodium_intake_mg": "float",  # mg per day
            "potassium_intake_mg": "float",  # mg per day
            "physical_activity_minutes": "int",  # minutes per week
            "smoking_status": "int",  # 0 = never, 1 = former, 2 = current
            "alcohol_drinks_per_week": "int",
            "stress_level": "int",  # 0-10 scale
            "sleep_quality": "int",  # 0-10 scale
            "diabetes": "int",  # 1 = yes, 0 = no
            "kidney_disease": "int",  # 1 = yes, 0 = no
            "heart_rate": "float",
            "cholesterol_total": "float",
            "hdl_cholesterol": "float",
            "ldl_cholesterol": "float",
            "triglycerides": "float",
            "glucose_fasting": "float",
            "caffeine_intake_mg": "float",  # mg per day
            "meditation_frequency": "int",  # 0-7 times per week
            "work_stress_level": "int"  # 0-10 scale
        }
    
    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            "age": "Age in years",
            "gender": "Gender (1 = Male, 0 = Female)",
            "systolic_bp": "Current systolic blood pressure (mmHg)",
            "diastolic_bp": "Current diastolic blood pressure (mmHg)",
            "bmi": "Body Mass Index",
            "waist_circumference": "Waist circumference (cm)",
            "family_history_hypertension": "Family history of hypertension (1 = Yes, 0 = No)",
            "sodium_intake_mg": "Daily sodium intake (mg)",
            "potassium_intake_mg": "Daily potassium intake (mg)",
            "physical_activity_minutes": "Physical activity minutes per week",
            "smoking_status": "Smoking status (0 = Never, 1 = Former, 2 = Current)",
            "alcohol_drinks_per_week": "Alcoholic drinks per week",
            "stress_level": "Overall stress level (0-10)",
            "sleep_quality": "Sleep quality (0-10, higher is better)",
            "diabetes": "Diabetes diagnosis (1 = Yes, 0 = No)",
            "kidney_disease": "Kidney disease (1 = Yes, 0 = No)",
            "heart_rate": "Resting heart rate (bpm)",
            "cholesterol_total": "Total cholesterol (mg/dL)",
            "hdl_cholesterol": "HDL cholesterol (mg/dL)",
            "ldl_cholesterol": "LDL cholesterol (mg/dL)",
            "triglycerides": "Triglycerides (mg/dL)",
            "glucose_fasting": "Fasting glucose (mg/dL)",
            "caffeine_intake_mg": "Daily caffeine intake (mg)",
            "meditation_frequency": "Meditation frequency (times per week)",
            "work_stress_level": "Work-related stress level (0-10)"
        }
    
    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        features = [
            data["age"] / 100.0,
            data["gender"],
            data["systolic_bp"] / 200.0,
            data["diastolic_bp"] / 120.0,
            data["bmi"] / 50.0,
            data["waist_circumference"] / 150.0,
            data["family_history_hypertension"],
            data["sodium_intake_mg"] / 5000.0,
            data["potassium_intake_mg"] / 5000.0,
            data["physical_activity_minutes"] / 300.0,
            data["smoking_status"] / 2.0,
            data["alcohol_drinks_per_week"] / 20.0,
            data["stress_level"] / 10.0,
            data["sleep_quality"] / 10.0,
            data["diabetes"],
            data["kidney_disease"],
            data["heart_rate"] / 120.0,
            data["cholesterol_total"] / 400.0,
            data["hdl_cholesterol"] / 100.0,
            data["ldl_cholesterol"] / 300.0,
            data["triglycerides"] / 500.0,
            data["glucose_fasting"] / 200.0,
            data["caffeine_intake_mg"] / 1000.0,
            data["meditation_frequency"] / 7.0,
            data["work_stress_level"] / 10.0
        ]
        return np.array(features)

class CholesterolRiskPredictor(BasePredictor):
    """Predicts cholesterol and atherosclerosis risk leading to stroke/heart attack"""
    
    def __init__(self):
        super().__init__(
            name="Cholesterol & Atherosclerosis Risk Predictor",
            description="Predicts cholesterol levels and atherosclerosis risk that can lead to stroke or heart attack"
        )
    
    def get_required_fields(self) -> Dict[str, str]:
        return {
            "age": "int",
            "gender": "int",  # 1 = male, 0 = female
            "total_cholesterol": "float",  # mg/dL
            "hdl_cholesterol": "float",  # mg/dL
            "ldl_cholesterol": "float",  # mg/dL
            "triglycerides": "float",  # mg/dL
            "bmi": "float",
            "waist_circumference": "float",
            "systolic_bp": "float",
            "diastolic_bp": "float",
            "smoking_status": "int",  # 0 = never, 1 = former, 2 = current
            "family_history_heart_disease": "int",  # 1 = yes, 0 = no
            "diabetes": "int",  # 1 = yes, 0 = no
            "physical_activity_level": "int",  # 0-4 scale
            "saturated_fat_intake": "int",  # 0-4 scale (low to very high)
            "trans_fat_intake": "int",  # 0-4 scale
            "fiber_intake_grams": "float",  # grams per day
            "omega3_intake": "int",  # 0-4 scale
            "alcohol_consumption": "int",  # 0-4 scale
            "stress_level": "int",  # 0-10 scale
            "sleep_hours": "float",
            "medication_statins": "int",  # 1 = yes, 0 = no
            "c_reactive_protein": "float",  # mg/L
            "homocysteine": "float",  # μmol/L
            "lipoprotein_a": "float"  # mg/dL
        }
    
    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            "age": "Age in years",
            "gender": "Gender (1 = Male, 0 = Female)",
            "total_cholesterol": "Total cholesterol level (mg/dL)",
            "hdl_cholesterol": "HDL (good) cholesterol (mg/dL)",
            "ldl_cholesterol": "LDL (bad) cholesterol (mg/dL)",
            "triglycerides": "Triglycerides level (mg/dL)",
            "bmi": "Body Mass Index",
            "waist_circumference": "Waist circumference (cm)",
            "systolic_bp": "Systolic blood pressure (mmHg)",
            "diastolic_bp": "Diastolic blood pressure (mmHg)",
            "smoking_status": "Smoking status (0 = Never, 1 = Former, 2 = Current)",
            "family_history_heart_disease": "Family history of heart disease (1 = Yes, 0 = No)",
            "diabetes": "Diabetes diagnosis (1 = Yes, 0 = No)",
            "physical_activity_level": "Physical activity level (0-4 scale)",
            "saturated_fat_intake": "Saturated fat intake level (0 = Low, 1 = Moderate, 2 = High, 3 = Very High, 4 = Excessive)",
            "trans_fat_intake": "Trans fat intake level (0 = None, 1 = Low, 2 = Moderate, 3 = High, 4 = Very High)",
            "fiber_intake_grams": "Daily fiber intake (grams)",
            "omega3_intake": "Omega-3 fatty acid intake (0 = None, 1 = Low, 2 = Moderate, 3 = High, 4 = Very High)",
            "alcohol_consumption": "Alcohol consumption (0-4 scale)",
            "stress_level": "Stress level (0-10)",
            "sleep_hours": "Average sleep hours per night",
            "medication_statins": "Taking statin medications (1 = Yes, 0 = No)",
            "c_reactive_protein": "C-reactive protein level (mg/L)",
            "homocysteine": "Homocysteine level (μmol/L)",
            "lipoprotein_a": "Lipoprotein(a) level (mg/dL)"
        }
    
    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        # Calculate cholesterol ratios
        total_hdl_ratio = data["total_cholesterol"] / max(data["hdl_cholesterol"], 1)
        ldl_hdl_ratio = data["ldl_cholesterol"] / max(data["hdl_cholesterol"], 1)
        
        features = [
            data["age"] / 100.0,
            data["gender"],
            data["total_cholesterol"] / 400.0,
            data["hdl_cholesterol"] / 100.0,
            data["ldl_cholesterol"] / 300.0,
            data["triglycerides"] / 500.0,
            total_hdl_ratio / 10.0,
            ldl_hdl_ratio / 8.0,
            data["bmi"] / 50.0,
            data["waist_circumference"] / 150.0,
            data["systolic_bp"] / 200.0,
            data["diastolic_bp"] / 120.0,
            data["smoking_status"] / 2.0,
            data["family_history_heart_disease"],
            data["diabetes"],
            data["physical_activity_level"] / 4.0,
            data["saturated_fat_intake"] / 4.0,
            data["trans_fat_intake"] / 4.0,
            data["fiber_intake_grams"] / 50.0,
            data["omega3_intake"] / 4.0,
            data["alcohol_consumption"] / 4.0,
            data["stress_level"] / 10.0,
            data["sleep_hours"] / 12.0,
            data["medication_statins"],
            data["c_reactive_protein"] / 10.0,
            data["homocysteine"] / 50.0,
            data["lipoprotein_a"] / 100.0
        ]
        return np.array(features)

class MentalHealthPredictor(BasePredictor):
    """Predicts depression and anxiety from surveys, voice, and wearable data"""
    
    def __init__(self):
        super().__init__(
            name="Mental Health Predictor",
            description="Detects depression and anxiety using survey data, voice patterns, and wearable device metrics"
        )
    
    def get_required_fields(self) -> Dict[str, str]:
        return {
            "age": "int",
            "gender": "int",  # 1 = male, 0 = female
            "phq9_score": "int",  # Patient Health Questionnaire-9 (0-27)
            "gad7_score": "int",  # Generalized Anxiety Disorder-7 (0-21)
            "sleep_hours_per_night": "float",
            "sleep_quality_score": "int",  # 0-10 scale
            "physical_activity_minutes": "int",  # per week
            "social_interaction_hours": "float",  # per day
            "work_stress_level": "int",  # 0-10 scale
            "financial_stress_level": "int",  # 0-10 scale
            "relationship_satisfaction": "int",  # 0-10 scale
            "family_history_mental_health": "int",  # 1 = yes, 0 = no
            "chronic_illness": "int",  # 1 = yes, 0 = no
            "medication_antidepressants": "int",  # 1 = yes, 0 = no
            "therapy_sessions": "int",  # sessions per month
            "substance_use": "int",  # 0-4 scale
            "alcohol_consumption": "int",  # 0-4 scale
            "caffeine_intake_mg": "float",  # mg per day
            "screen_time_hours": "float",  # per day
            "outdoor_time_hours": "float",  # per day
            "heart_rate_variability": "float",  # from wearable
            "resting_heart_rate": "float",  # from wearable
            "voice_pitch_variance": "float",  # voice analysis metric
            "speech_rate": "float",  # words per minute
            "pause_frequency": "float"  # pauses per minute in speech
        }
    
    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            "age": "Age in years",
            "gender": "Gender (1 = Male, 0 = Female)",
            "phq9_score": "PHQ-9 Depression Score (0-27, higher indicates more depression)",
            "gad7_score": "GAD-7 Anxiety Score (0-21, higher indicates more anxiety)",
            "sleep_hours_per_night": "Average sleep hours per night",
            "sleep_quality_score": "Sleep quality (0-10, higher is better)",
            "physical_activity_minutes": "Physical activity minutes per week",
            "social_interaction_hours": "Social interaction hours per day",
            "work_stress_level": "Work-related stress (0-10)",
            "financial_stress_level": "Financial stress (0-10)",
            "relationship_satisfaction": "Relationship satisfaction (0-10)",
            "family_history_mental_health": "Family history of mental health issues (1 = Yes, 0 = No)",
            "chronic_illness": "Chronic illness diagnosis (1 = Yes, 0 = No)",
            "medication_antidepressants": "Taking antidepressant medication (1 = Yes, 0 = No)",
            "therapy_sessions": "Therapy sessions per month",
            "substance_use": "Substance use level (0-4 scale)",
            "alcohol_consumption": "Alcohol consumption (0-4 scale)",
            "caffeine_intake_mg": "Daily caffeine intake (mg)",
            "screen_time_hours": "Daily screen time (hours)",
            "outdoor_time_hours": "Daily outdoor time (hours)",
            "heart_rate_variability": "Heart rate variability (from wearable device)",
            "resting_heart_rate": "Resting heart rate (bpm)",
            "voice_pitch_variance": "Voice pitch variance (voice analysis metric)",
            "speech_rate": "Speech rate (words per minute)",
            "pause_frequency": "Speech pause frequency (pauses per minute)"
        }
    
    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        features = [
            data["age"] / 100.0,
            data["gender"],
            data["phq9_score"] / 27.0,
            data["gad7_score"] / 21.0,
            data["sleep_hours_per_night"] / 12.0,
            data["sleep_quality_score"] / 10.0,
            data["physical_activity_minutes"] / 300.0,
            data["social_interaction_hours"] / 12.0,
            data["work_stress_level"] / 10.0,
            data["financial_stress_level"] / 10.0,
            data["relationship_satisfaction"] / 10.0,
            data["family_history_mental_health"],
            data["chronic_illness"],
            data["medication_antidepressants"],
            data["therapy_sessions"] / 10.0,
            data["substance_use"] / 4.0,
            data["alcohol_consumption"] / 4.0,
            data["caffeine_intake_mg"] / 1000.0,
            data["screen_time_hours"] / 16.0,
            data["outdoor_time_hours"] / 8.0,
            data["heart_rate_variability"] / 100.0,
            data["resting_heart_rate"] / 120.0,
            data["voice_pitch_variance"] / 100.0,
            data["speech_rate"] / 200.0,
            data["pause_frequency"] / 20.0
        ]
        return np.array(features)

class SleepApneaPredictor(BasePredictor):
    """Predicts sleep apnea and sleep disorders using wearable or questionnaire data"""
    
    def __init__(self):
        super().__init__(
            name="Sleep Apnea & Sleep Disorder Predictor",
            description="Predicts sleep apnea and other sleep disorders using wearable data or questionnaire responses"
        )
    
    def get_required_fields(self) -> Dict[str, str]:
        return {
            "age": "int",
            "gender": "int",  # 1 = male, 0 = female
            "bmi": "float",
            "neck_circumference": "float",  # cm
            "snoring_frequency": "int",  # 0-7 nights per week
            "snoring_loudness": "int",  # 0-4 scale
            "witnessed_apneas": "int",  # 1 = yes, 0 = no
            "gasping_choking": "int",  # 1 = yes, 0 = no
            "morning_headaches": "int",  # 0-7 days per week
            "daytime_sleepiness": "int",  # Epworth Sleepiness Scale (0-24)
            "fatigue_level": "int",  # 0-10 scale
            "concentration_problems": "int",  # 0-10 scale
            "sleep_duration_hours": "float",
            "sleep_efficiency": "float",  # percentage
            "sleep_latency_minutes": "float",  # time to fall asleep
            "wake_after_sleep_onset": "float",  # minutes
            "rem_sleep_percentage": "float",
            "deep_sleep_percentage": "float",
            "oxygen_saturation_min": "float",  # minimum SpO2 during sleep
            "heart_rate_during_sleep": "float",  # average
            "blood_pressure_systolic": "float",
            "blood_pressure_diastolic": "float",
            "diabetes": "int",  # 1 = yes, 0 = no
            "heart_disease": "int",  # 1 = yes, 0 = no
            "stroke_history": "int",  # 1 = yes, 0 = no
            "family_history_sleep_apnea": "int",  # 1 = yes, 0 = no
            "alcohol_before_bed": "int",  # 1 = yes, 0 = no
            "smoking_status": "int",  # 0 = never, 1 = former, 2 = current
            "nasal_congestion": "int",  # 0-10 scale
            "sleep_position": "int"  # 1 = back, 2 = side, 3 = stomach
        }
    
    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            "age": "Age in years",
            "gender": "Gender (1 = Male, 0 = Female)",
            "bmi": "Body Mass Index",
            "neck_circumference": "Neck circumference (cm)",
            "snoring_frequency": "Snoring frequency (nights per week)",
            "snoring_loudness": "Snoring loudness (0 = None, 1 = Soft, 2 = Moderate, 3 = Loud, 4 = Very Loud)",
            "witnessed_apneas": "Witnessed breathing pauses during sleep (1 = Yes, 0 = No)",
            "gasping_choking": "Gasping or choking during sleep (1 = Yes, 0 = No)",
            "morning_headaches": "Morning headaches frequency (days per week)",
            "daytime_sleepiness": "Epworth Sleepiness Scale score (0-24)",
            "fatigue_level": "Fatigue level (0-10)",
            "concentration_problems": "Concentration problems (0-10)",
            "sleep_duration_hours": "Average sleep duration (hours)",
            "sleep_efficiency": "Sleep efficiency percentage (%)",
            "sleep_latency_minutes": "Time to fall asleep (minutes)",
            "wake_after_sleep_onset": "Wake time after sleep onset (minutes)",
            "rem_sleep_percentage": "REM sleep percentage (%)",
            "deep_sleep_percentage": "Deep sleep percentage (%)",
            "oxygen_saturation_min": "Minimum oxygen saturation during sleep (%)",
            "heart_rate_during_sleep": "Average heart rate during sleep (bpm)",
            "blood_pressure_systolic": "Systolic blood pressure (mmHg)",
            "blood_pressure_diastolic": "Diastolic blood pressure (mmHg)",
            "diabetes": "Diabetes diagnosis (1 = Yes, 0 = No)",
            "heart_disease": "Heart disease (1 = Yes, 0 = No)",
            "stroke_history": "History of stroke (1 = Yes, 0 = No)",
            "family_history_sleep_apnea": "Family history of sleep apnea (1 = Yes, 0 = No)",
            "alcohol_before_bed": "Alcohol consumption before bed (1 = Yes, 0 = No)",
            "smoking_status": "Smoking status (0 = Never, 1 = Former, 2 = Current)",
            "nasal_congestion": "Nasal congestion level (0-10)",
            "sleep_position": "Primary sleep position (1 = Back, 2 = Side, 3 = Stomach)"
        }
    
    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        features = [
            data["age"] / 100.0,
            data["gender"],
            data["bmi"] / 50.0,
            data["neck_circumference"] / 50.0,
            data["snoring_frequency"] / 7.0,
            data["snoring_loudness"] / 4.0,
            data["witnessed_apneas"],
            data["gasping_choking"],
            data["morning_headaches"] / 7.0,
            data["daytime_sleepiness"] / 24.0,
            data["fatigue_level"] / 10.0,
            data["concentration_problems"] / 10.0,
            data["sleep_duration_hours"] / 12.0,
            data["sleep_efficiency"] / 100.0,
            data["sleep_latency_minutes"] / 120.0,
            data["wake_after_sleep_onset"] / 120.0,
            data["rem_sleep_percentage"] / 100.0,
            data["deep_sleep_percentage"] / 100.0,
            data["oxygen_saturation_min"] / 100.0,
            data["heart_rate_during_sleep"] / 120.0,
            data["blood_pressure_systolic"] / 200.0,
            data["blood_pressure_diastolic"] / 120.0,
            data["diabetes"],
            data["heart_disease"],
            data["stroke_history"],
            data["family_history_sleep_apnea"],
            data["alcohol_before_bed"],
            data["smoking_status"] / 2.0,
            data["nasal_congestion"] / 10.0,
            data["sleep_position"] / 3.0
        ]
        return np.array(features)