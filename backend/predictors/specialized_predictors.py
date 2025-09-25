import numpy as np
from typing import Dict, List, Any
from .base_predictor import BasePredictor

class CovidRiskPredictor(BasePredictor):
    """Predicts COVID-19 severity and hospitalization risk"""
    
    def __init__(self):
        super().__init__(
            name="COVID-19 / Infectious Disease Predictor",
            description="Predicts COVID-19 severity, hospitalization risk, and outcomes for infectious diseases"
        )
    
    def get_required_fields(self) -> Dict[str, str]:
        return {
            "age": "int",
            "gender": "int",  # 1 = male, 0 = female
            "bmi": "float",
            "temperature": "float",  # Celsius
            "oxygen_saturation": "float",  # percentage
            "heart_rate": "float",
            "respiratory_rate": "float",
            "blood_pressure_systolic": "float",
            "blood_pressure_diastolic": "float",
            "cough": "int",  # 1 = yes, 0 = no
            "shortness_of_breath": "int",  # 1 = yes, 0 = no
            "fatigue": "int",  # 0-10 scale
            "fever_duration_days": "int",
            "loss_of_taste_smell": "int",  # 1 = yes, 0 = no
            "chest_pain": "int",  # 1 = yes, 0 = no
            "headache": "int",  # 1 = yes, 0 = no
            "muscle_aches": "int",  # 1 = yes, 0 = no
            "diabetes": "int",  # 1 = yes, 0 = no
            "hypertension": "int",  # 1 = yes, 0 = no
            "heart_disease": "int",  # 1 = yes, 0 = no
            "lung_disease": "int",  # 1 = yes, 0 = no
            "kidney_disease": "int",  # 1 = yes, 0 = no
            "liver_disease": "int",  # 1 = yes, 0 = no
            "cancer": "int",  # 1 = yes, 0 = no
            "immunocompromised": "int",  # 1 = yes, 0 = no
            "vaccination_status": "int",  # 0 = none, 1 = partial, 2 = full, 3 = boosted
            "smoking_status": "int",  # 0 = never, 1 = former, 2 = current
            "white_blood_cells": "float",  # cells/μL
            "lymphocytes": "float",  # cells/μL
            "platelets": "float",  # cells/μL
            "c_reactive_protein": "float",  # mg/L
            "d_dimer": "float",  # mg/L
            "lactate_dehydrogenase": "float",  # U/L
            "ferritin": "float",  # ng/mL
            "procalcitonin": "float"  # ng/mL
        }
    
    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            "age": "Age in years",
            "gender": "Gender (1 = Male, 0 = Female)",
            "bmi": "Body Mass Index",
            "temperature": "Body temperature (Celsius)",
            "oxygen_saturation": "Oxygen saturation (%)",
            "heart_rate": "Heart rate (bpm)",
            "respiratory_rate": "Respiratory rate (breaths per minute)",
            "blood_pressure_systolic": "Systolic blood pressure (mmHg)",
            "blood_pressure_diastolic": "Diastolic blood pressure (mmHg)",
            "cough": "Presence of cough (1 = Yes, 0 = No)",
            "shortness_of_breath": "Shortness of breath (1 = Yes, 0 = No)",
            "fatigue": "Fatigue level (0-10)",
            "fever_duration_days": "Duration of fever (days)",
            "loss_of_taste_smell": "Loss of taste or smell (1 = Yes, 0 = No)",
            "chest_pain": "Chest pain (1 = Yes, 0 = No)",
            "headache": "Headache (1 = Yes, 0 = No)",
            "muscle_aches": "Muscle aches (1 = Yes, 0 = No)",
            "diabetes": "Diabetes (1 = Yes, 0 = No)",
            "hypertension": "Hypertension (1 = Yes, 0 = No)",
            "heart_disease": "Heart disease (1 = Yes, 0 = No)",
            "lung_disease": "Lung disease (1 = Yes, 0 = No)",
            "kidney_disease": "Kidney disease (1 = Yes, 0 = No)",
            "liver_disease": "Liver disease (1 = Yes, 0 = No)",
            "cancer": "Cancer diagnosis (1 = Yes, 0 = No)",
            "immunocompromised": "Immunocompromised status (1 = Yes, 0 = No)",
            "vaccination_status": "COVID-19 vaccination status (0 = None, 1 = Partial, 2 = Full, 3 = Boosted)",
            "smoking_status": "Smoking status (0 = Never, 1 = Former, 2 = Current)",
            "white_blood_cells": "White blood cell count (cells/μL)",
            "lymphocytes": "Lymphocyte count (cells/μL)",
            "platelets": "Platelet count (cells/μL)",
            "c_reactive_protein": "C-reactive protein (mg/L)",
            "d_dimer": "D-dimer (mg/L)",
            "lactate_dehydrogenase": "Lactate dehydrogenase (U/L)",
            "ferritin": "Ferritin (ng/mL)",
            "procalcitonin": "Procalcitonin (ng/mL)"
        }
    
    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        features = [
            data["age"] / 100.0,
            data["gender"],
            data["bmi"] / 50.0,
            data["temperature"] / 42.0,
            data["oxygen_saturation"] / 100.0,
            data["heart_rate"] / 150.0,
            data["respiratory_rate"] / 40.0,
            data["blood_pressure_systolic"] / 200.0,
            data["blood_pressure_diastolic"] / 120.0,
            data["cough"],
            data["shortness_of_breath"],
            data["fatigue"] / 10.0,
            data["fever_duration_days"] / 14.0,
            data["loss_of_taste_smell"],
            data["chest_pain"],
            data["headache"],
            data["muscle_aches"],
            data["diabetes"],
            data["hypertension"],
            data["heart_disease"],
            data["lung_disease"],
            data["kidney_disease"],
            data["liver_disease"],
            data["cancer"],
            data["immunocompromised"],
            data["vaccination_status"] / 3.0,
            data["smoking_status"] / 2.0,
            data["white_blood_cells"] / 15000.0,
            data["lymphocytes"] / 4000.0,
            data["platelets"] / 500000.0,
            data["c_reactive_protein"] / 200.0,
            data["d_dimer"] / 10.0,
            data["lactate_dehydrogenase"] / 1000.0,
            data["ferritin"] / 5000.0,
            data["procalcitonin"] / 10.0
        ]
        return np.array(features)
    
    def identify_contributing_factors(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify key factors contributing to cancer recurrence risk"""
        factors = []
        
        # Cancer stage
        stage = data["cancer_stage"]
        if stage >= 3:
            factors.append({
                "factor": "Advanced Cancer Stage",
                "value": f"Stage {stage}",
                "impact": "High",
                "description": "Advanced stage cancers have higher recurrence risk"
            })
        elif stage == 2:
            factors.append({
                "factor": "Intermediate Cancer Stage",
                "value": f"Stage {stage}",
                "impact": "Medium",
                "description": "Stage 2 cancers have moderate recurrence risk"
            })
        
        # Tumor grade
        grade = data["tumor_grade"]
        if grade >= 3:
            factors.append({
                "factor": "High-Grade Tumor",
                "value": f"Grade {grade}",
                "impact": "High",
                "description": "High-grade tumors are more aggressive and likely to recur"
            })
        
        # Lymph node involvement
        if data["lymph_nodes_positive"] > 0:
            factors.append({
                "factor": "Lymph Node Involvement",
                "value": f"{data['lymph_nodes_positive']} positive nodes",
                "impact": "High",
                "description": "Positive lymph nodes indicate cancer spread and higher recurrence risk"
            })
        
        # Tumor size
        tumor_size = data["tumor_size_cm"]
        if tumor_size > 5:
            factors.append({
                "factor": "Large Tumor Size",
                "value": f"{tumor_size} cm",
                "impact": "High",
                "description": "Large tumors are associated with higher recurrence risk"
            })
        elif tumor_size > 2:
            factors.append({
                "factor": "Moderate Tumor Size",
                "value": f"{tumor_size} cm",
                "impact": "Medium",
                "description": "Moderate tumor size increases recurrence risk"
            })
        
        # Hormone receptor status (for applicable cancers)
        if data["hormone_receptor_positive"] == 0:
            factors.append({
                "factor": "Hormone Receptor Negative",
                "value": "Negative",
                "impact": "Medium",
                "description": "Hormone receptor negative cancers may have different recurrence patterns"
            })
        
        # HER2 status (for applicable cancers)
        if data["her2_positive"]:
            factors.append({
                "factor": "HER2 Positive",
                "value": "Positive",
                "impact": "Medium",
                "description": "HER2 positive cancers may have higher recurrence risk without targeted therapy"
            })
        
        # Treatment completion
        if not data["completed_treatment"]:
            factors.append({
                "factor": "Incomplete Treatment",
                "value": "Not completed",
                "impact": "High",
                "description": "Incomplete treatment significantly increases recurrence risk"
            })
        
        # Age factor
        age = data["age"]
        if age < 40:
            factors.append({
                "factor": "Young Age",
                "value": f"{age} years",
                "impact": "Medium",
                "description": "Younger patients may have more aggressive cancers"
            })
        
        # Family history
        if data["family_history_cancer"]:
            factors.append({
                "factor": "Family History",
                "value": "Present",
                "impact": "Medium",
                "description": "Family history may indicate genetic predisposition"
            })
        
        return factors
    
    def analyze_health_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze health metrics for cancer recurrence assessment"""
        metrics = {
            "tumor_characteristics": self._assess_tumor_characteristics(data),
            "treatment_response": self._assess_treatment_response(data),
            "biomarker_status": self._assess_biomarker_status(data),
            "surveillance_metrics": self._assess_surveillance_metrics(data)
        }
        
        # Overall recurrence risk score
        risk_score = (
            metrics["tumor_characteristics"]["score"] * 0.4 +
            metrics["treatment_response"]["score"] * 0.3 +
            metrics["biomarker_status"]["score"] * 0.2 +
            metrics["surveillance_metrics"]["score"] * 0.1
        )
        
        metrics["overall_risk"] = {
            "score": round(risk_score, 2),
            "category": "High risk" if risk_score >= 7 else "Moderate risk" if risk_score >= 4 else "Low risk"
        }
        
        return metrics
    
    def assess_lifestyle_impact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess lifestyle factors impact on cancer recurrence risk"""
        impact = {
            "lifestyle_factors": self._assess_lifestyle_factors(data),
            "immune_support": self._assess_immune_support(data),
            "stress_management": self._assess_stress_management(data),
            "recommendations": []
        }
        
        # Generate recommendations
        if data["smoking"]:
            impact["recommendations"].append("Smoking cessation is crucial for reducing recurrence risk")
        
        if data["alcohol_consumption"] >= 3:
            impact["recommendations"].append("Limit alcohol consumption to reduce recurrence risk")
        
        if data["bmi"] > 30:
            impact["recommendations"].append("Maintain healthy weight through diet and exercise")
        
        if data["physical_activity_hours"] < 2:
            impact["recommendations"].append("Increase physical activity to at least 150 minutes per week")
        
        if data["stress_level"] >= 7:
            impact["recommendations"].append("Implement stress management techniques and consider counseling")
        
        return impact
    
    def _assess_tumor_characteristics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess tumor characteristics impact on recurrence risk"""
        score = 0
        characteristics = []
        
        # Stage assessment
        stage = data["cancer_stage"]
        if stage == 4:
            score += 5
            characteristics.append("Stage 4 (Metastatic)")
        elif stage == 3:
            score += 4
            characteristics.append("Stage 3 (Locally Advanced)")
        elif stage == 2:
            score += 2
            characteristics.append("Stage 2 (Regional)")
        
        # Grade assessment
        grade = data["tumor_grade"]
        if grade == 3:
            score += 3
            characteristics.append("High-grade (Grade 3)")
        elif grade == 2:
            score += 2
            characteristics.append("Intermediate-grade (Grade 2)")
        
        # Size assessment
        size = data["tumor_size_cm"]
        if size > 5:
            score += 2
            characteristics.append(f"Large tumor ({size} cm)")
        elif size > 2:
            score += 1
            characteristics.append(f"Moderate tumor ({size} cm)")
        
        # Lymph node involvement
        positive_nodes = data["lymph_nodes_positive"]
        if positive_nodes > 10:
            score += 3
            characteristics.append(f"Extensive nodal involvement ({positive_nodes} nodes)")
        elif positive_nodes > 3:
            score += 2
            characteristics.append(f"Multiple positive nodes ({positive_nodes} nodes)")
        elif positive_nodes > 0:
            score += 1
            characteristics.append(f"Limited nodal involvement ({positive_nodes} nodes)")
        
        return {
            "score": min(score, 10),
            "characteristics": characteristics,
            "risk_category": "High risk" if score >= 7 else "Moderate risk" if score >= 4 else "Low risk"
        }
    
    def _assess_treatment_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess treatment response and completion"""
        score = 0
        factors = []
        
        # Treatment completion
        if not data["completed_treatment"]:
            score += 5
            factors.append("Treatment not completed")
        
        # Response to treatment
        if data["treatment_response"] == "poor":
            score += 4
            factors.append("Poor response to treatment")
        elif data["treatment_response"] == "partial":
            score += 2
            factors.append("Partial response to treatment")
        
        # Time since treatment
        time_since_treatment = data["months_since_treatment"]
        if time_since_treatment < 12:
            score += 1
            factors.append("Recent treatment completion")
        
        return {
            "score": min(score, 10),
            "factors": factors,
            "response_category": "Poor response" if score >= 6 else "Moderate response" if score >= 3 else "Good response"
        }
    
    def _assess_biomarker_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess biomarker status impact on recurrence"""
        score = 0
        markers = []
        
        # Hormone receptor status
        if data["hormone_receptor_positive"] == 0:
            score += 2
            markers.append("Hormone receptor negative")
        
        # HER2 status
        if data["her2_positive"]:
            score += 2
            markers.append("HER2 positive")
        
        # Tumor markers (if elevated)
        if data["tumor_markers_elevated"]:
            score += 3
            markers.append("Elevated tumor markers")
        
        # Genetic mutations
        if data["high_risk_mutations"]:
            score += 3
            markers.append("High-risk genetic mutations")
        
        return {
            "score": min(score, 10),
            "markers": markers,
            "risk_level": "High risk" if score >= 6 else "Moderate risk" if score >= 3 else "Low risk"
        }
    
    def _assess_surveillance_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess surveillance and monitoring metrics"""
        score = 0
        issues = []
        
        # Follow-up compliance
        if not data["regular_followup"]:
            score += 3
            issues.append("Irregular follow-up appointments")
        
        # Imaging surveillance
        if not data["regular_imaging"]:
            score += 2
            issues.append("Irregular imaging surveillance")
        
        # Self-monitoring
        if not data["self_monitoring"]:
            score += 1
            issues.append("Poor self-monitoring")
        
        return {
            "score": min(score, 10),
            "issues": issues,
            "surveillance_quality": "Poor" if score >= 4 else "Adequate" if score >= 2 else "Good"
        }
    
    def _assess_lifestyle_factors(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess lifestyle factors impact on recurrence"""
        risk_factors = []
        score = 0
        
        # Smoking
        if data["smoking"]:
            score += 4
            risk_factors.append("Smoking significantly increases recurrence risk")
        
        # Alcohol consumption
        alcohol = data["alcohol_consumption"]
        if alcohol >= 4:
            score += 3
            risk_factors.append("Heavy alcohol consumption increases risk")
        elif alcohol >= 2:
            score += 2
            risk_factors.append("Moderate alcohol consumption may increase risk")
        
        # BMI
        bmi = data["bmi"]
        if bmi > 35:
            score += 3
            risk_factors.append("Severe obesity increases recurrence risk")
        elif bmi > 30:
            score += 2
            risk_factors.append("Obesity increases recurrence risk")
        
        # Physical activity
        activity = data["physical_activity_hours"]
        if activity < 1:
            score += 2
            risk_factors.append("Sedentary lifestyle increases recurrence risk")
        
        return {
            "risk_level": "High" if score >= 6 else "Medium" if score >= 3 else "Low",
            "risk_factors": risk_factors,
            "description": "Lifestyle factors affecting cancer recurrence risk"
        }
    
    def _assess_immune_support(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess immune system support factors"""
        support_factors = []
        score = 0
        
        # Sleep quality
        sleep_hours = data["sleep_hours"]
        if sleep_hours < 6:
            score += 2
            support_factors.append("Poor sleep may compromise immune function")
        elif sleep_hours >= 7:
            score -= 1
            support_factors.append("Adequate sleep supports immune function")
        
        # Nutrition
        if data["healthy_diet"]:
            score -= 2
            support_factors.append("Healthy diet supports immune function")
        else:
            score += 2
            support_factors.append("Poor diet may compromise immune function")
        
        # Supplements
        if data["immune_supplements"]:
            score -= 1
            support_factors.append("Immune-supporting supplements")
        
        return {
            "support_level": "Good" if score <= 0 else "Moderate" if score <= 3 else "Poor",
            "factors": support_factors,
            "description": "Factors supporting immune system function"
        }
    
    def _assess_stress_management(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess stress management and psychological factors"""
        stress_level = data["stress_level"]
        
        if stress_level >= 8:
            impact_level = "High"
            description = "High stress levels may negatively impact immune function and recovery"
        elif stress_level >= 5:
            impact_level = "Medium"
            description = "Moderate stress levels may affect recovery"
        else:
            impact_level = "Low"
            description = "Low stress levels support optimal recovery"
        
        support_factors = []
        if data["psychological_support"]:
            support_factors.append("Receiving psychological support")
        if data["social_support"]:
            support_factors.append("Strong social support system")
        if data["stress_management_techniques"]:
            support_factors.append("Using stress management techniques")
        
        return {
            "stress_impact": impact_level,
            "stress_score": stress_level,
            "support_factors": support_factors,
            "description": description
        }
    
    def identify_contributing_factors(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify key factors contributing to COVID-19 risk"""
        factors = []
        
        # Age risk assessment
        age = data["age"]
        if age >= 65:
            factors.append({
                "factor": "Advanced Age",
                "value": f"{age} years",
                "impact": "High",
                "description": "Age 65+ significantly increases COVID-19 severity risk"
            })
        elif age >= 50:
            factors.append({
                "factor": "Moderate Age Risk",
                "value": f"{age} years",
                "impact": "Medium",
                "description": "Age 50+ moderately increases COVID-19 risk"
            })
        
        # Comorbidity assessment
        comorbidities = []
        if data["diabetes"]: comorbidities.append("Diabetes")
        if data["hypertension"]: comorbidities.append("Hypertension")
        if data["heart_disease"]: comorbidities.append("Heart Disease")
        if data["lung_disease"]: comorbidities.append("Lung Disease")
        if data["kidney_disease"]: comorbidities.append("Kidney Disease")
        if data["cancer"]: comorbidities.append("Cancer")
        if data["immunocompromised"]: comorbidities.append("Immunocompromised")
        
        if comorbidities:
            factors.append({
                "factor": "Underlying Conditions",
                "value": ", ".join(comorbidities),
                "impact": "High",
                "description": "Multiple comorbidities significantly increase COVID-19 severity risk"
            })
        
        # Vaccination status
        vax_status = data["vaccination_status"]
        if vax_status == 0:
            factors.append({
                "factor": "Unvaccinated",
                "value": "No vaccination",
                "impact": "High",
                "description": "Lack of vaccination increases hospitalization risk"
            })
        elif vax_status == 1:
            factors.append({
                "factor": "Partial Vaccination",
                "value": "Partially vaccinated",
                "impact": "Medium",
                "description": "Incomplete vaccination provides limited protection"
            })
        
        # Vital signs assessment
        if data["oxygen_saturation"] < 95:
            factors.append({
                "factor": "Low Oxygen Saturation",
                "value": f"{data['oxygen_saturation']}%",
                "impact": "High",
                "description": "Oxygen saturation below 95% indicates severe respiratory compromise"
            })
        
        # Inflammatory markers
        if data["c_reactive_protein"] > 10:
            factors.append({
                "factor": "Elevated CRP",
                "value": f"{data['c_reactive_protein']} mg/L",
                "impact": "Medium",
                "description": "High C-reactive protein indicates significant inflammation"
            })
        
        return factors
    
    def analyze_health_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze health metrics for COVID-19 assessment"""
        metrics = {
            "vital_signs": self._assess_vital_signs(data),
            "respiratory_status": self._assess_respiratory_status(data),
            "inflammatory_markers": self._assess_inflammatory_markers(data),
            "symptom_severity": self._assess_symptom_severity(data)
        }
        
        # Overall severity score
        severity_score = (
            metrics["vital_signs"]["score"] * 0.3 +
            metrics["respiratory_status"]["score"] * 0.4 +
            metrics["inflammatory_markers"]["score"] * 0.2 +
            metrics["symptom_severity"]["score"] * 0.1
        )
        
        metrics["overall_severity"] = {
            "score": round(severity_score, 2),
            "category": "Severe" if severity_score >= 7 else "Moderate" if severity_score >= 4 else "Mild"
        }
        
        return metrics
    
    def assess_lifestyle_impact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess lifestyle factors impact on COVID-19 risk"""
        impact = {
            "smoking_impact": self._assess_smoking_impact(data),
            "bmi_impact": self._assess_bmi_impact(data),
            "vaccination_protection": self._assess_vaccination_protection(data),
            "recommendations": []
        }
        
        # Generate recommendations
        if data["smoking_status"] == 2:
            impact["recommendations"].append("Smoking cessation is crucial for reducing COVID-19 severity risk")
        
        if data["bmi"] >= 30:
            impact["recommendations"].append("Weight management can help reduce COVID-19 complications")
        
        if data["vaccination_status"] < 3:
            impact["recommendations"].append("Consider booster vaccination for optimal protection")
        
        return impact
    
    def _assess_vital_signs(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess vital signs severity"""
        score = 0
        issues = []
        
        # Temperature
        if data["temperature"] >= 39:
            score += 3
            issues.append("High fever")
        elif data["temperature"] >= 38:
            score += 2
            issues.append("Moderate fever")
        
        # Oxygen saturation
        if data["oxygen_saturation"] < 90:
            score += 4
            issues.append("Severe hypoxemia")
        elif data["oxygen_saturation"] < 95:
            score += 2
            issues.append("Mild hypoxemia")
        
        # Heart rate
        if data["heart_rate"] > 120:
            score += 2
            issues.append("Tachycardia")
        
        # Respiratory rate
        if data["respiratory_rate"] > 30:
            score += 3
            issues.append("Severe tachypnea")
        elif data["respiratory_rate"] > 24:
            score += 2
            issues.append("Mild tachypnea")
        
        return {
            "score": min(score, 10),
            "issues": issues,
            "category": "Critical" if score >= 8 else "Concerning" if score >= 4 else "Stable"
        }
    
    def _assess_respiratory_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess respiratory status"""
        score = 0
        symptoms = []
        
        if data["shortness_of_breath"]:
            score += 3
            symptoms.append("Shortness of breath")
        
        if data["cough"]:
            score += 1
            symptoms.append("Cough")
        
        if data["chest_pain"]:
            score += 2
            symptoms.append("Chest pain")
        
        # Oxygen saturation impact
        if data["oxygen_saturation"] < 90:
            score += 4
        elif data["oxygen_saturation"] < 95:
            score += 2
        
        return {
            "score": min(score, 10),
            "symptoms": symptoms,
            "category": "Severe" if score >= 7 else "Moderate" if score >= 3 else "Mild"
        }
    
    def _assess_inflammatory_markers(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess inflammatory markers"""
        score = 0
        elevated_markers = []
        
        if data["c_reactive_protein"] > 100:
            score += 4
            elevated_markers.append("Severely elevated CRP")
        elif data["c_reactive_protein"] > 10:
            score += 2
            elevated_markers.append("Elevated CRP")
        
        if data["d_dimer"] > 1:
            score += 2
            elevated_markers.append("Elevated D-dimer")
        
        if data["ferritin"] > 1000:
            score += 2
            elevated_markers.append("Elevated ferritin")
        
        if data["lactate_dehydrogenase"] > 500:
            score += 2
            elevated_markers.append("Elevated LDH")
        
        return {
            "score": min(score, 10),
            "elevated_markers": elevated_markers,
            "category": "Severe inflammation" if score >= 6 else "Moderate inflammation" if score >= 3 else "Mild inflammation"
        }
    
    def _assess_symptom_severity(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall symptom severity"""
        score = 0
        symptoms = []
        
        if data["fatigue"] >= 7:
            score += 2
            symptoms.append("Severe fatigue")
        elif data["fatigue"] >= 4:
            score += 1
            symptoms.append("Moderate fatigue")
        
        if data["fever_duration_days"] > 7:
            score += 2
            symptoms.append("Prolonged fever")
        
        if data["headache"]:
            score += 1
            symptoms.append("Headache")
        
        if data["muscle_aches"]:
            score += 1
            symptoms.append("Muscle aches")
        
        return {
            "score": min(score, 10),
            "symptoms": symptoms,
            "category": "Severe" if score >= 5 else "Moderate" if score >= 3 else "Mild"
        }
    
    def _assess_smoking_impact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess smoking impact on COVID-19 risk"""
        smoking_status = data["smoking_status"]
        
        if smoking_status == 2:  # Current smoker
            return {
                "risk_level": "High",
                "description": "Current smoking significantly increases COVID-19 severity risk",
                "recommendation": "Immediate smoking cessation recommended"
            }
        elif smoking_status == 1:  # Former smoker
            return {
                "risk_level": "Medium",
                "description": "Former smoking history may increase COVID-19 risk",
                "recommendation": "Continue avoiding tobacco products"
            }
        else:
            return {
                "risk_level": "Low",
                "description": "No smoking history is protective",
                "recommendation": "Continue avoiding tobacco products"
            }
    
    def _assess_bmi_impact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess BMI impact on COVID-19 risk"""
        bmi = data["bmi"]
        
        if bmi >= 40:
            return {
                "category": "Severely obese",
                "risk_level": "Very High",
                "description": "Severe obesity significantly increases COVID-19 complications"
            }
        elif bmi >= 30:
            return {
                "category": "Obese",
                "risk_level": "High",
                "description": "Obesity increases COVID-19 severity risk"
            }
        elif bmi >= 25:
            return {
                "category": "Overweight",
                "risk_level": "Medium",
                "description": "Overweight may moderately increase COVID-19 risk"
            }
        else:
            return {
                "category": "Normal weight",
                "risk_level": "Low",
                "description": "Normal weight is protective against severe COVID-19"
            }
    
    def _assess_vaccination_protection(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess vaccination protection level"""
        vax_status = data["vaccination_status"]
        
        if vax_status == 3:
            return {
                "protection_level": "High",
                "status": "Boosted",
                "description": "Booster vaccination provides optimal protection"
            }
        elif vax_status == 2:
            return {
                "protection_level": "Good",
                "status": "Fully vaccinated",
                "description": "Full vaccination provides good protection, consider booster"
            }
        elif vax_status == 1:
            return {
                "protection_level": "Limited",
                "status": "Partially vaccinated",
                "description": "Partial vaccination provides limited protection"
            }
        else:
            return {
                "protection_level": "None",
                "status": "Unvaccinated",
                "description": "No vaccination protection, immediate vaccination recommended"
            }

class AsthmaCopdPredictor(BasePredictor):
    """Predicts asthma and COPD progression and exacerbation risk"""
    
    def __init__(self):
        super().__init__(
            name="Asthma & COPD Predictor",
            description="Predicts respiratory disease progression and exacerbation risk for asthma and COPD"
        )
    
    def get_required_fields(self) -> Dict[str, str]:
        return {
            "age": "int",
            "gender": "int",  # 1 = male, 0 = female
            "smoking_pack_years": "float",
            "current_smoking_status": "int",  # 0 = never, 1 = former, 2 = current
            "occupational_exposure": "int",  # 1 = yes, 0 = no
            "family_history_respiratory": "int",  # 1 = yes, 0 = no
            "fev1_percent_predicted": "float",  # Forced Expiratory Volume
            "fvc_percent_predicted": "float",  # Forced Vital Capacity
            "fev1_fvc_ratio": "float",
            "peak_flow_rate": "float",  # L/min
            "oxygen_saturation_rest": "float",
            "oxygen_saturation_exercise": "float",
            "shortness_of_breath_scale": "int",  # 0-4 mMRC scale
            "cough_frequency": "int",  # 0-4 scale
            "sputum_production": "int",  # 0-4 scale
            "wheezing_frequency": "int",  # 0-4 scale
            "chest_tightness": "int",  # 0-4 scale
            "exercise_tolerance": "int",  # 0-4 scale
            "sleep_disturbance": "int",  # 0-4 scale
            "rescue_inhaler_use": "int",  # uses per week
            "exacerbations_last_year": "int",
            "hospitalizations_last_year": "int",
            "steroid_courses_last_year": "int",
            "allergies": "int",  # 1 = yes, 0 = no
            "eosinophil_count": "float",  # cells/μL
            "ige_level": "float",  # IU/mL
            "vitamin_d_level": "float",  # ng/mL
            "bmi": "float",
            "air_quality_exposure": "int",  # 0-4 scale
            "seasonal_variation": "int",  # 1 = yes, 0 = no
            "medication_adherence": "int"  # 0-4 scale
        }
    
    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            "age": "Age in years",
            "gender": "Gender (1 = Male, 0 = Female)",
            "smoking_pack_years": "Smoking history (pack-years)",
            "current_smoking_status": "Current smoking status (0 = Never, 1 = Former, 2 = Current)",
            "occupational_exposure": "Occupational exposure to irritants (1 = Yes, 0 = No)",
            "family_history_respiratory": "Family history of respiratory disease (1 = Yes, 0 = No)",
            "fev1_percent_predicted": "FEV1 as percentage of predicted value (%)",
            "fvc_percent_predicted": "FVC as percentage of predicted value (%)",
            "fev1_fvc_ratio": "FEV1/FVC ratio",
            "peak_flow_rate": "Peak expiratory flow rate (L/min)",
            "oxygen_saturation_rest": "Oxygen saturation at rest (%)",
            "oxygen_saturation_exercise": "Oxygen saturation during exercise (%)",
            "shortness_of_breath_scale": "mMRC Dyspnea Scale (0-4)",
            "cough_frequency": "Cough frequency (0 = None, 1 = Rare, 2 = Occasional, 3 = Frequent, 4 = Constant)",
            "sputum_production": "Sputum production (0-4 scale)",
            "wheezing_frequency": "Wheezing frequency (0-4 scale)",
            "chest_tightness": "Chest tightness (0-4 scale)",
            "exercise_tolerance": "Exercise tolerance (0 = Poor, 4 = Excellent)",
            "sleep_disturbance": "Sleep disturbance due to symptoms (0-4 scale)",
            "rescue_inhaler_use": "Rescue inhaler uses per week",
            "exacerbations_last_year": "Number of exacerbations in the last year",
            "hospitalizations_last_year": "Hospitalizations in the last year",
            "steroid_courses_last_year": "Oral steroid courses in the last year",
            "allergies": "Known allergies (1 = Yes, 0 = No)",
            "eosinophil_count": "Eosinophil count (cells/μL)",
            "ige_level": "Total IgE level (IU/mL)",
            "vitamin_d_level": "Vitamin D level (ng/mL)",
            "bmi": "Body Mass Index",
            "air_quality_exposure": "Air quality exposure (0 = Excellent, 4 = Very Poor)",
            "seasonal_variation": "Seasonal symptom variation (1 = Yes, 0 = No)",
            "medication_adherence": "Medication adherence (0 = Poor, 4 = Excellent)"
        }
    
    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        features = [
            data["age"] / 100.0,
            data["gender"],
            data["smoking_pack_years"] / 100.0,
            data["current_smoking_status"] / 2.0,
            data["occupational_exposure"],
            data["family_history_respiratory"],
            data["fev1_percent_predicted"] / 100.0,
            data["fvc_percent_predicted"] / 100.0,
            data["fev1_fvc_ratio"],
            data["peak_flow_rate"] / 600.0,
            data["oxygen_saturation_rest"] / 100.0,
            data["oxygen_saturation_exercise"] / 100.0,
            data["shortness_of_breath_scale"] / 4.0,
            data["cough_frequency"] / 4.0,
            data["sputum_production"] / 4.0,
            data["wheezing_frequency"] / 4.0,
            data["chest_tightness"] / 4.0,
            data["exercise_tolerance"] / 4.0,
            data["sleep_disturbance"] / 4.0,
            data["rescue_inhaler_use"] / 20.0,
            data["exacerbations_last_year"] / 10.0,
            data["hospitalizations_last_year"] / 5.0,
            data["steroid_courses_last_year"] / 10.0,
            data["allergies"],
            data["eosinophil_count"] / 1000.0,
            data["ige_level"] / 1000.0,
            data["vitamin_d_level"] / 100.0,
            data["bmi"] / 50.0,
            data["air_quality_exposure"] / 4.0,
            data["seasonal_variation"],
            data["medication_adherence"] / 4.0
        ]
        return np.array(features)
    
    def identify_contributing_factors(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify key factors contributing to asthma/COPD risk"""
        factors = []
        
        # Smoking assessment
        pack_years = data["smoking_pack_years"]
        smoking_status = data["current_smoking_status"]
        
        if smoking_status == 2:  # Current smoker
            factors.append({
                "factor": "Active Smoking",
                "value": f"{pack_years} pack-years",
                "impact": "High",
                "description": "Active smoking is the primary risk factor for COPD and worsens asthma"
            })
        elif pack_years > 20:
            factors.append({
                "factor": "Heavy Smoking History",
                "value": f"{pack_years} pack-years",
                "impact": "High",
                "description": "Significant smoking history increases COPD risk"
            })
        
        # Lung function assessment
        if data["fev1_percent_predicted"] < 50:
            factors.append({
                "factor": "Severe Airflow Obstruction",
                "value": f"{data['fev1_percent_predicted']}% predicted",
                "impact": "High",
                "description": "Severely reduced lung function indicates advanced disease"
            })
        elif data["fev1_percent_predicted"] < 80:
            factors.append({
                "factor": "Reduced Lung Function",
                "value": f"{data['fev1_percent_predicted']}% predicted",
                "impact": "Medium",
                "description": "Reduced lung function indicates respiratory impairment"
            })
        
        # Symptom severity
        if data["shortness_of_breath_scale"] >= 3:
            factors.append({
                "factor": "Severe Dyspnea",
                "value": f"mMRC Grade {data['shortness_of_breath_scale']}",
                "impact": "High",
                "description": "Severe shortness of breath significantly impacts daily activities"
            })
        
        # Exacerbation history
        if data["exacerbations_last_year"] >= 2:
            factors.append({
                "factor": "Frequent Exacerbations",
                "value": f"{data['exacerbations_last_year']} in last year",
                "impact": "High",
                "description": "Frequent exacerbations indicate poor disease control"
            })
        
        # Environmental factors
        if data["occupational_exposure"]:
            factors.append({
                "factor": "Occupational Exposure",
                "value": "Present",
                "impact": "Medium",
                "description": "Workplace irritants can worsen respiratory symptoms"
            })
        
        return factors
    
    def analyze_health_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze health metrics for asthma/COPD assessment"""
        metrics = {
            "lung_function": self._assess_lung_function(data),
            "symptom_control": self._assess_symptom_control(data),
            "exacerbation_risk": self._assess_exacerbation_risk(data),
            "quality_of_life": self._assess_quality_of_life(data)
        }
        
        # Overall disease severity
        severity_score = (
            metrics["lung_function"]["score"] * 0.4 +
            metrics["symptom_control"]["score"] * 0.3 +
            metrics["exacerbation_risk"]["score"] * 0.2 +
            metrics["quality_of_life"]["score"] * 0.1
        )
        
        metrics["overall_severity"] = {
            "score": round(severity_score, 2),
            "category": "Severe" if severity_score >= 7 else "Moderate" if severity_score >= 4 else "Mild"
        }
        
        return metrics
    
    def assess_lifestyle_impact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess lifestyle factors impact on respiratory health"""
        impact = {
            "smoking_impact": self._assess_smoking_impact(data),
            "environmental_impact": self._assess_environmental_impact(data),
            "medication_adherence": self._assess_medication_adherence(data),
            "recommendations": []
        }
        
        # Generate recommendations
        if data["current_smoking_status"] == 2:
            impact["recommendations"].append("Smoking cessation is the most important intervention for respiratory health")
        
        if data["air_quality_exposure"] >= 3:
            impact["recommendations"].append("Minimize exposure to air pollution and environmental irritants")
        
        if data["medication_adherence"] < 3:
            impact["recommendations"].append("Improve medication adherence for better symptom control")
        
        if data["exercise_tolerance"] < 2:
            impact["recommendations"].append("Consider pulmonary rehabilitation to improve exercise capacity")
        
        return impact
    
    def _assess_lung_function(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess lung function parameters"""
        score = 0
        issues = []
        
        # FEV1 assessment
        fev1 = data["fev1_percent_predicted"]
        if fev1 < 30:
            score += 5
            issues.append("Very severe airflow obstruction")
        elif fev1 < 50:
            score += 4
            issues.append("Severe airflow obstruction")
        elif fev1 < 80:
            score += 2
            issues.append("Moderate airflow obstruction")
        
        # FEV1/FVC ratio
        if data["fev1_fvc_ratio"] < 0.5:
            score += 3
            issues.append("Severe obstruction pattern")
        elif data["fev1_fvc_ratio"] < 0.7:
            score += 2
            issues.append("Obstruction pattern present")
        
        # Oxygen saturation
        if data["oxygen_saturation_rest"] < 90:
            score += 3
            issues.append("Hypoxemia at rest")
        elif data["oxygen_saturation_exercise"] < 90:
            score += 2
            issues.append("Exercise-induced hypoxemia")
        
        return {
            "score": min(score, 10),
            "issues": issues,
            "category": "Severe impairment" if score >= 7 else "Moderate impairment" if score >= 4 else "Mild impairment"
        }
    
    def _assess_symptom_control(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess symptom control"""
        score = 0
        symptoms = []
        
        # Dyspnea scale
        dyspnea = data["shortness_of_breath_scale"]
        if dyspnea >= 4:
            score += 4
            symptoms.append("Severe dyspnea")
        elif dyspnea >= 2:
            score += 2
            symptoms.append("Moderate dyspnea")
        
        # Cough and sputum
        if data["cough_frequency"] >= 3:
            score += 2
            symptoms.append("Frequent cough")
        
        if data["sputum_production"] >= 3:
            score += 2
            symptoms.append("Significant sputum production")
        
        # Rescue inhaler use
        if data["rescue_inhaler_use"] > 14:  # More than twice daily
            score += 3
            symptoms.append("Frequent rescue inhaler use")
        elif data["rescue_inhaler_use"] > 7:
            score += 2
            symptoms.append("Regular rescue inhaler use")
        
        return {
            "score": min(score, 10),
            "symptoms": symptoms,
            "category": "Poor control" if score >= 7 else "Partial control" if score >= 4 else "Good control"
        }
    
    def _assess_exacerbation_risk(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess exacerbation risk"""
        score = 0
        risk_factors = []
        
        # Exacerbation history
        exacerbations = data["exacerbations_last_year"]
        if exacerbations >= 3:
            score += 4
            risk_factors.append("Frequent exacerbations")
        elif exacerbations >= 2:
            score += 3
            risk_factors.append("Recurrent exacerbations")
        elif exacerbations >= 1:
            score += 2
            risk_factors.append("Previous exacerbations")
        
        # Hospitalizations
        if data["hospitalizations_last_year"] >= 1:
            score += 3
            risk_factors.append("Recent hospitalizations")
        
        # Steroid courses
        if data["steroid_courses_last_year"] >= 3:
            score += 2
            risk_factors.append("Frequent steroid use")
        
        # Poor lung function
        if data["fev1_percent_predicted"] < 50:
            score += 2
            risk_factors.append("Severe airflow obstruction")
        
        return {
            "score": min(score, 10),
            "risk_factors": risk_factors,
            "category": "High risk" if score >= 7 else "Moderate risk" if score >= 4 else "Low risk"
        }
    
    def _assess_quality_of_life(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess quality of life impact"""
        score = 0
        impacts = []
        
        # Exercise tolerance
        if data["exercise_tolerance"] <= 1:
            score += 3
            impacts.append("Severe exercise limitation")
        elif data["exercise_tolerance"] <= 2:
            score += 2
            impacts.append("Moderate exercise limitation")
        
        # Sleep disturbance
        if data["sleep_disturbance"] >= 3:
            score += 2
            impacts.append("Significant sleep disruption")
        
        # Dyspnea impact
        if data["shortness_of_breath_scale"] >= 3:
            score += 2
            impacts.append("Daily activities limited by breathlessness")
        
        return {
            "score": min(score, 10),
            "impacts": impacts,
            "category": "Severely impacted" if score >= 6 else "Moderately impacted" if score >= 3 else "Minimally impacted"
        }
    
    def _assess_smoking_impact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess smoking impact on respiratory health"""
        smoking_status = data["current_smoking_status"]
        pack_years = data["smoking_pack_years"]
        
        if smoking_status == 2:  # Current smoker
            return {
                "risk_level": "Very High",
                "description": f"Active smoking ({pack_years} pack-years) is severely damaging respiratory health",
                "recommendation": "Immediate smoking cessation is critical"
            }
        elif smoking_status == 1 and pack_years > 20:  # Heavy former smoker
            return {
                "risk_level": "High",
                "description": f"Heavy smoking history ({pack_years} pack-years) has caused permanent lung damage",
                "recommendation": "Continue avoiding tobacco, monitor lung function regularly"
            }
        elif smoking_status == 1:  # Former smoker
            return {
                "risk_level": "Medium",
                "description": f"Former smoking ({pack_years} pack-years) may have caused some lung damage",
                "recommendation": "Continue avoiding tobacco products"
            }
        else:
            return {
                "risk_level": "Low",
                "description": "No smoking history is protective for respiratory health",
                "recommendation": "Continue avoiding tobacco products"
            }
    
    def _assess_environmental_impact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess environmental factors impact"""
        score = 0
        factors = []
        
        if data["occupational_exposure"]:
            score += 3
            factors.append("Occupational irritants")
        
        air_quality = data["air_quality_exposure"]
        if air_quality >= 3:
            score += 2
            factors.append("Poor air quality")
        
        if data["allergies"] and data["seasonal_variation"]:
            score += 2
            factors.append("Seasonal allergens")
        
        return {
            "risk_level": "High" if score >= 5 else "Medium" if score >= 3 else "Low",
            "factors": factors,
            "description": "Environmental factors contributing to respiratory symptoms"
        }
    
    def _assess_medication_adherence(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess medication adherence impact"""
        adherence = data["medication_adherence"]
        
        if adherence >= 4:
            return {
                "level": "Excellent",
                "description": "Excellent medication adherence supports optimal disease control",
                "recommendation": "Continue current medication regimen"
            }
        elif adherence >= 3:
            return {
                "level": "Good",
                "description": "Good medication adherence with room for improvement",
                "recommendation": "Work with healthcare provider to optimize adherence"
            }
        elif adherence >= 2:
            return {
                "level": "Fair",
                "description": "Fair medication adherence may compromise disease control",
                "recommendation": "Address barriers to medication adherence"
            }
        else:
            return {
                "level": "Poor",
                "description": "Poor medication adherence significantly impacts disease control",
                "recommendation": "Urgent need to improve medication adherence"
            }

class AnemiaPredictor(BasePredictor):
    """Predicts anemia using blood test values and clinical data"""
    
    def __init__(self):
        super().__init__(
            name="Anemia Predictor",
            description="Predicts anemia and its type using blood test values and clinical indicators"
        )
    
    def get_required_fields(self) -> Dict[str, str]:
        return {
            "age": "int",
            "gender": "int",  # 1 = male, 0 = female
            "hemoglobin": "float",  # g/dL
            "hematocrit": "float",  # percentage
            "red_blood_cell_count": "float",  # million cells/μL
            "mean_corpuscular_volume": "float",  # fL
            "mean_corpuscular_hemoglobin": "float",  # pg
            "mean_corpuscular_hemoglobin_concentration": "float",  # g/dL
            "red_cell_distribution_width": "float",  # percentage
            "reticulocyte_count": "float",  # percentage
            "serum_iron": "float",  # μg/dL
            "total_iron_binding_capacity": "float",  # μg/dL
            "transferrin_saturation": "float",  # percentage
            "ferritin": "float",  # ng/mL
            "vitamin_b12": "float",  # pg/mL
            "folate": "float",  # ng/mL
            "lactate_dehydrogenase": "float",  # U/L
            "bilirubin_total": "float",  # mg/dL
            "bilirubin_indirect": "float",  # mg/dL
            "haptoglobin": "float",  # mg/dL
            "fatigue_level": "int",  # 0-10 scale
            "shortness_of_breath": "int",  # 1 = yes, 0 = no
            "pale_skin": "int",  # 1 = yes, 0 = no
            "cold_hands_feet": "int",  # 1 = yes, 0 = no
            "brittle_nails": "int",  # 1 = yes, 0 = no
            "strange_cravings": "int",  # 1 = yes, 0 = no (ice, starch, etc.)
            "heavy_menstrual_periods": "int",  # 1 = yes, 0 = no/not applicable
            "gastrointestinal_bleeding": "int",  # 1 = yes, 0 = no
            "chronic_kidney_disease": "int",  # 1 = yes, 0 = no
            "chronic_inflammatory_disease": "int",  # 1 = yes, 0 = no
            "family_history_anemia": "int",  # 1 = yes, 0 = no
            "vegetarian_diet": "int",  # 1 = yes, 0 = no
            "alcohol_consumption": "int"  # 0-4 scale
        }
    
    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            "age": "Age in years",
            "gender": "Gender (1 = Male, 0 = Female)",
            "hemoglobin": "Hemoglobin level (g/dL)",
            "hematocrit": "Hematocrit percentage (%)",
            "red_blood_cell_count": "Red blood cell count (million cells/μL)",
            "mean_corpuscular_volume": "Mean corpuscular volume (fL)",
            "mean_corpuscular_hemoglobin": "Mean corpuscular hemoglobin (pg)",
            "mean_corpuscular_hemoglobin_concentration": "MCHC (g/dL)",
            "red_cell_distribution_width": "Red cell distribution width (%)",
            "reticulocyte_count": "Reticulocyte count (%)",
            "serum_iron": "Serum iron level (μg/dL)",
            "total_iron_binding_capacity": "Total iron binding capacity (μg/dL)",
            "transferrin_saturation": "Transferrin saturation (%)",
            "ferritin": "Ferritin level (ng/mL)",
            "vitamin_b12": "Vitamin B12 level (pg/mL)",
            "folate": "Folate level (ng/mL)",
            "lactate_dehydrogenase": "LDH level (U/L)",
            "bilirubin_total": "Total bilirubin (mg/dL)",
            "bilirubin_indirect": "Indirect bilirubin (mg/dL)",
            "haptoglobin": "Haptoglobin level (mg/dL)",
            "fatigue_level": "Fatigue level (0-10)",
            "shortness_of_breath": "Shortness of breath (1 = Yes, 0 = No)",
            "pale_skin": "Pale skin (1 = Yes, 0 = No)",
            "cold_hands_feet": "Cold hands and feet (1 = Yes, 0 = No)",
            "brittle_nails": "Brittle or spoon-shaped nails (1 = Yes, 0 = No)",
            "strange_cravings": "Cravings for ice, starch, or non-food items (1 = Yes, 0 = No)",
            "heavy_menstrual_periods": "Heavy menstrual periods (1 = Yes, 0 = No/Not applicable)",
            "gastrointestinal_bleeding": "History of GI bleeding (1 = Yes, 0 = No)",
            "chronic_kidney_disease": "Chronic kidney disease (1 = Yes, 0 = No)",
            "chronic_inflammatory_disease": "Chronic inflammatory disease (1 = Yes, 0 = No)",
            "family_history_anemia": "Family history of anemia (1 = Yes, 0 = No)",
            "vegetarian_diet": "Vegetarian or vegan diet (1 = Yes, 0 = No)",
            "alcohol_consumption": "Alcohol consumption (0-4 scale)"
        }
    
    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        # Calculate iron saturation if not provided
        iron_saturation = data["transferrin_saturation"] / 100.0 if data["transferrin_saturation"] > 1 else data["transferrin_saturation"]
        
        features = [
            data["age"] / 100.0,
            data["gender"],
            data["hemoglobin"] / 20.0,
            data["hematocrit"] / 100.0,
            data["red_blood_cell_count"] / 6.0,
            data["mean_corpuscular_volume"] / 120.0,
            data["mean_corpuscular_hemoglobin"] / 40.0,
            data["mean_corpuscular_hemoglobin_concentration"] / 40.0,
            data["red_cell_distribution_width"] / 20.0,
            data["reticulocyte_count"] / 5.0,
            data["serum_iron"] / 200.0,
            data["total_iron_binding_capacity"] / 500.0,
            iron_saturation,
            data["ferritin"] / 500.0,
            data["vitamin_b12"] / 1000.0,
            data["folate"] / 20.0,
            data["lactate_dehydrogenase"] / 1000.0,
            data["bilirubin_total"] / 5.0,
            data["bilirubin_indirect"] / 5.0,
            data["haptoglobin"] / 300.0,
            data["fatigue_level"] / 10.0,
            data["shortness_of_breath"],
            data["pale_skin"],
            data["cold_hands_feet"],
            data["brittle_nails"],
            data["strange_cravings"],
            data["heavy_menstrual_periods"],
            data["gastrointestinal_bleeding"],
            data["chronic_kidney_disease"],
            data["chronic_inflammatory_disease"],
            data["family_history_anemia"],
            data["vegetarian_diet"],
            data["alcohol_consumption"] / 4.0
        ]
        return np.array(features)
    
    def identify_contributing_factors(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify key factors contributing to anemia risk"""
        factors = []
        
        # Hemoglobin assessment
        hemoglobin = data["hemoglobin"]
        gender = data["gender"]
        
        # Gender-specific hemoglobin thresholds
        if gender == 1:  # Male
            if hemoglobin < 12:
                factors.append({
                    "factor": "Low Hemoglobin (Male)",
                    "value": f"{hemoglobin} g/dL",
                    "impact": "High",
                    "description": "Hemoglobin below 12 g/dL indicates anemia in males"
                })
        else:  # Female
            if hemoglobin < 11:
                factors.append({
                    "factor": "Low Hemoglobin (Female)",
                    "value": f"{hemoglobin} g/dL",
                    "impact": "High",
                    "description": "Hemoglobin below 11 g/dL indicates anemia in females"
                })
        
        # Iron deficiency markers
        if data["ferritin"] < 15:
            factors.append({
                "factor": "Iron Deficiency",
                "value": f"Ferritin {data['ferritin']} ng/mL",
                "impact": "High",
                "description": "Low ferritin indicates iron deficiency anemia"
            })
        
        if data["transferrin_saturation"] < 16:
            factors.append({
                "factor": "Low Iron Saturation",
                "value": f"{data['transferrin_saturation']}%",
                "impact": "High",
                "description": "Low transferrin saturation suggests iron deficiency"
            })
        
        # B12/Folate deficiency
        if data["vitamin_b12"] < 200:
            factors.append({
                "factor": "B12 Deficiency",
                "value": f"{data['vitamin_b12']} pg/mL",
                "impact": "High",
                "description": "Low B12 can cause megaloblastic anemia"
            })
        
        if data["folate"] < 3:
            factors.append({
                "factor": "Folate Deficiency",
                "value": f"{data['folate']} ng/mL",
                "impact": "High",
                "description": "Low folate can cause megaloblastic anemia"
            })
        
        # Chronic conditions
        chronic_conditions = []
        if data["chronic_kidney_disease"]: chronic_conditions.append("Chronic Kidney Disease")
        if data["chronic_inflammatory_disease"]: chronic_conditions.append("Chronic Inflammatory Disease")
        
        if chronic_conditions:
            factors.append({
                "factor": "Chronic Disease",
                "value": ", ".join(chronic_conditions),
                "impact": "Medium",
                "description": "Chronic diseases can cause anemia of chronic disease"
            })
        
        # Bleeding sources
        if data["gastrointestinal_bleeding"]:
            factors.append({
                "factor": "GI Bleeding",
                "value": "Present",
                "impact": "High",
                "description": "Gastrointestinal bleeding can cause iron deficiency anemia"
            })
        
        if data["heavy_menstrual_periods"] and gender == 0:
            factors.append({
                "factor": "Heavy Menstrual Bleeding",
                "value": "Present",
                "impact": "High",
                "description": "Heavy menstrual periods are a common cause of iron deficiency in women"
            })
        
        return factors
    
    def analyze_health_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze health metrics for anemia assessment"""
        metrics = {
            "anemia_severity": self._assess_anemia_severity(data),
            "anemia_type": self._determine_anemia_type(data),
            "iron_status": self._assess_iron_status(data),
            "symptom_severity": self._assess_symptom_severity(data)
        }
        
        # Overall anemia risk score
        risk_score = (
            metrics["anemia_severity"]["score"] * 0.4 +
            metrics["iron_status"]["score"] * 0.3 +
            metrics["symptom_severity"]["score"] * 0.2 +
            (5 if metrics["anemia_type"]["type"] != "Normal" else 0) * 0.1
        )
        
        metrics["overall_risk"] = {
            "score": round(risk_score, 2),
            "category": "High risk" if risk_score >= 7 else "Moderate risk" if risk_score >= 4 else "Low risk"
        }
        
        return metrics
    
    def assess_lifestyle_impact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess lifestyle factors impact on anemia risk"""
        impact = {
            "dietary_impact": self._assess_dietary_impact(data),
            "bleeding_risk": self._assess_bleeding_risk(data),
            "absorption_factors": self._assess_absorption_factors(data),
            "recommendations": []
        }
        
        # Generate recommendations
        if data["vegetarian_diet"]:
            impact["recommendations"].append("Ensure adequate iron intake through plant-based sources and consider supplementation")
        
        if data["gastrointestinal_bleeding"]:
            impact["recommendations"].append("Address underlying cause of GI bleeding")
        
        if data["heavy_menstrual_periods"] and data["gender"] == 0:
            impact["recommendations"].append("Consider gynecological evaluation for heavy menstrual bleeding")
        
        if data["alcohol_consumption"] >= 3:
            impact["recommendations"].append("Reduce alcohol consumption to improve nutrient absorption")
        
        return impact
    
    def _assess_anemia_severity(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess anemia severity based on hemoglobin levels"""
        hemoglobin = data["hemoglobin"]
        gender = data["gender"]
        
        # Gender-specific thresholds
        if gender == 1:  # Male
            if hemoglobin < 8:
                severity = "Severe"
                score = 10
            elif hemoglobin < 10:
                severity = "Moderate"
                score = 7
            elif hemoglobin < 12:
                severity = "Mild"
                score = 4
            else:
                severity = "Normal"
                score = 0
        else:  # Female
            if hemoglobin < 8:
                severity = "Severe"
                score = 10
            elif hemoglobin < 10:
                severity = "Moderate"
                score = 7
            elif hemoglobin < 11:
                severity = "Mild"
                score = 4
            else:
                severity = "Normal"
                score = 0
        
        return {
            "score": score,
            "severity": severity,
            "hemoglobin": hemoglobin,
            "description": f"Hemoglobin level indicates {severity.lower()} anemia" if score > 0 else "Normal hemoglobin level"
        }
    
    def _determine_anemia_type(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Determine the type of anemia based on lab values"""
        mcv = data["mean_corpuscular_volume"]
        ferritin = data["ferritin"]
        b12 = data["vitamin_b12"]
        folate = data["folate"]
        
        if mcv < 80:  # Microcytic
            if ferritin < 15:
                anemia_type = "Iron Deficiency Anemia"
                description = "Small red blood cells with low iron stores"
            else:
                anemia_type = "Anemia of Chronic Disease (Microcytic)"
                description = "Small red blood cells with normal/high iron stores"
        elif mcv > 100:  # Macrocytic
            if b12 < 200 or folate < 3:
                anemia_type = "Megaloblastic Anemia"
                description = "Large red blood cells due to B12/folate deficiency"
            else:
                anemia_type = "Non-megaloblastic Macrocytic Anemia"
                description = "Large red blood cells, non-B12/folate related"
        else:  # Normocytic
            if data["chronic_kidney_disease"] or data["chronic_inflammatory_disease"]:
                anemia_type = "Anemia of Chronic Disease"
                description = "Normal-sized red blood cells with chronic disease"
            else:
                anemia_type = "Normocytic Anemia"
                description = "Normal-sized red blood cells, cause unclear"
        
        # Check if actually anemic
        hemoglobin = data["hemoglobin"]
        gender = data["gender"]
        threshold = 12 if gender == 1 else 11
        
        if hemoglobin >= threshold:
            anemia_type = "Normal"
            description = "No anemia detected"
        
        return {
            "type": anemia_type,
            "description": description,
            "mcv": mcv
        }
    
    def _assess_iron_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess iron status"""
        score = 0
        issues = []
        
        # Ferritin assessment
        ferritin = data["ferritin"]
        if ferritin < 15:
            score += 4
            issues.append("Severely low ferritin")
        elif ferritin < 30:
            score += 3
            issues.append("Low ferritin")
        elif ferritin > 300:
            score += 2
            issues.append("Elevated ferritin")
        
        # Transferrin saturation
        tsat = data["transferrin_saturation"]
        if tsat < 16:
            score += 3
            issues.append("Low transferrin saturation")
        elif tsat > 45:
            score += 2
            issues.append("High transferrin saturation")
        
        # Serum iron
        iron = data["serum_iron"]
        if iron < 60:
            score += 2
            issues.append("Low serum iron")
        
        return {
            "score": min(score, 10),
            "issues": issues,
            "category": "Severe deficiency" if score >= 7 else "Moderate deficiency" if score >= 4 else "Normal"
        }
    
    def _assess_symptom_severity(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess anemia symptom severity"""
        score = 0
        symptoms = []
        
        # Fatigue
        fatigue = data["fatigue_level"]
        if fatigue >= 7:
            score += 3
            symptoms.append("Severe fatigue")
        elif fatigue >= 4:
            score += 2
            symptoms.append("Moderate fatigue")
        
        # Other symptoms
        if data["shortness_of_breath"]:
            score += 2
            symptoms.append("Shortness of breath")
        
        if data["pale_skin"]:
            score += 1
            symptoms.append("Pale skin")
        
        if data["cold_hands_feet"]:
            score += 1
            symptoms.append("Cold hands and feet")
        
        if data["brittle_nails"]:
            score += 1
            symptoms.append("Brittle nails")
        
        if data["strange_cravings"]:
            score += 2
            symptoms.append("Pica (strange cravings)")
        
        return {
            "score": min(score, 10),
            "symptoms": symptoms,
            "category": "Severe symptoms" if score >= 7 else "Moderate symptoms" if score >= 4 else "Mild symptoms"
        }
    
    def _assess_dietary_impact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess dietary factors impact on anemia"""
        risk_factors = []
        score = 0
        
        if data["vegetarian_diet"]:
            score += 2
            risk_factors.append("Vegetarian diet may limit iron absorption")
        
        if data["alcohol_consumption"] >= 3:
            score += 2
            risk_factors.append("High alcohol consumption impairs nutrient absorption")
        
        return {
            "risk_level": "High" if score >= 3 else "Medium" if score >= 2 else "Low",
            "risk_factors": risk_factors,
            "description": "Dietary factors affecting iron and vitamin absorption"
        }
    
    def _assess_bleeding_risk(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess bleeding risk factors"""
        bleeding_sources = []
        score = 0
        
        if data["gastrointestinal_bleeding"]:
            score += 4
            bleeding_sources.append("Gastrointestinal bleeding")
        
        if data["heavy_menstrual_periods"] and data["gender"] == 0:
            score += 3
            bleeding_sources.append("Heavy menstrual periods")
        
        return {
            "risk_level": "High" if score >= 4 else "Medium" if score >= 2 else "Low",
            "bleeding_sources": bleeding_sources,
            "description": "Sources of blood loss contributing to anemia"
        }
    
    def _assess_absorption_factors(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess factors affecting nutrient absorption"""
        factors = []
        score = 0
        
        if data["chronic_inflammatory_disease"]:
            score += 2
            factors.append("Chronic inflammation affects iron utilization")
        
        if data["alcohol_consumption"] >= 3:
            score += 2
            factors.append("Alcohol impairs B12 and folate absorption")
        
        return {
            "impact_level": "High" if score >= 3 else "Medium" if score >= 2 else "Low",
            "factors": factors,
            "description": "Factors affecting nutrient absorption and utilization"
        }

class ThyroidDisorderPredictor(BasePredictor):
    """Predicts thyroid disorders including hyperthyroidism and hypothyroidism"""
    
    def __init__(self):
        super().__init__(
            name="Thyroid Disorder Predictor",
            description="Predicts hyperthyroidism and hypothyroidism using clinical and laboratory data"
        )
    
    def get_required_fields(self) -> Dict[str, str]:
        return {
            "age": "int",
            "gender": "int",  # 1 = male, 0 = female
            "tsh": "float",  # mIU/L
            "free_t4": "float",  # ng/dL
            "free_t3": "float",  # pg/mL
            "total_t4": "float",  # μg/dL
            "total_t3": "float",  # ng/dL
            "thyroid_peroxidase_antibody": "float",  # IU/mL
            "thyroglobulin_antibody": "float",  # IU/mL
            "tsh_receptor_antibody": "float",  # IU/L
            "weight_change_kg": "float",  # positive = gain, negative = loss
            "heart_rate": "float",
            "blood_pressure_systolic": "float",
            "blood_pressure_diastolic": "float",
            "body_temperature": "float",  # Celsius
            "fatigue_level": "int",  # 0-10 scale
            "anxiety_level": "int",  # 0-10 scale
            "depression_symptoms": "int",  # 0-10 scale
            "sleep_quality": "int",  # 0-10 scale
            "hair_loss": "int",  # 1 = yes, 0 = no
            "dry_skin": "int",  # 1 = yes, 0 = no
            "cold_intolerance": "int",  # 1 = yes, 0 = no
            "heat_intolerance": "int",  # 1 = yes, 0 = no
            "constipation": "int",  # 1 = yes, 0 = no
            "diarrhea": "int",  # 1 = yes, 0 = no
            "muscle_weakness": "int",  # 1 = yes, 0 = no
            "tremor": "int",  # 1 = yes, 0 = no
            "goiter": "int",  # 1 = yes, 0 = no
            "eye_problems": "int",  # 1 = yes, 0 = no
            "menstrual_irregularities": "int",  # 1 = yes, 0 = no/not applicable
            "family_history_thyroid": "int",  # 1 = yes, 0 = no
            "autoimmune_disease": "int",  # 1 = yes, 0 = no
            "iodine_intake": "int",  # 0-4 scale
            "stress_level": "int",  # 0-10 scale
            "smoking_status": "int"  # 0 = never, 1 = former, 2 = current
        }
    
    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            "age": "Age in years",
            "gender": "Gender (1 = Male, 0 = Female)",
            "tsh": "Thyroid Stimulating Hormone (mIU/L)",
            "free_t4": "Free T4 (ng/dL)",
            "free_t3": "Free T3 (pg/mL)",
            "total_t4": "Total T4 (μg/dL)",
            "total_t3": "Total T3 (ng/dL)",
            "thyroid_peroxidase_antibody": "Anti-TPO antibody (IU/mL)",
            "thyroglobulin_antibody": "Anti-thyroglobulin antibody (IU/mL)",
            "tsh_receptor_antibody": "TSH receptor antibody (IU/L)",
            "weight_change_kg": "Weight change in last 6 months (kg, + = gain, - = loss)",
            "heart_rate": "Resting heart rate (bpm)",
            "blood_pressure_systolic": "Systolic blood pressure (mmHg)",
            "blood_pressure_diastolic": "Diastolic blood pressure (mmHg)",
            "body_temperature": "Average body temperature (Celsius)",
            "fatigue_level": "Fatigue level (0-10)",
            "anxiety_level": "Anxiety level (0-10)",
            "depression_symptoms": "Depression symptoms (0-10)",
            "sleep_quality": "Sleep quality (0-10, higher is better)",
            "hair_loss": "Hair loss or thinning (1 = Yes, 0 = No)",
            "dry_skin": "Dry skin (1 = Yes, 0 = No)",
            "cold_intolerance": "Cold intolerance (1 = Yes, 0 = No)",
            "heat_intolerance": "Heat intolerance (1 = Yes, 0 = No)",
            "constipation": "Constipation (1 = Yes, 0 = No)",
            "diarrhea": "Diarrhea (1 = Yes, 0 = No)",
            "muscle_weakness": "Muscle weakness (1 = Yes, 0 = No)",
            "tremor": "Hand tremor (1 = Yes, 0 = No)",
            "goiter": "Enlarged thyroid (goiter) (1 = Yes, 0 = No)",
            "eye_problems": "Eye problems (bulging, dryness) (1 = Yes, 0 = No)",
            "menstrual_irregularities": "Menstrual irregularities (1 = Yes, 0 = No/Not applicable)",
            "family_history_thyroid": "Family history of thyroid disease (1 = Yes, 0 = No)",
            "autoimmune_disease": "Other autoimmune diseases (1 = Yes, 0 = No)",
            "iodine_intake": "Iodine intake level (0 = Low, 1 = Normal, 2 = High, 3 = Very High, 4 = Excessive)",
            "stress_level": "Stress level (0-10)",
            "smoking_status": "Smoking status (0 = Never, 1 = Former, 2 = Current)"
        }
    
    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        features = [
            data["age"] / 100.0,
            data["gender"],
            data["tsh"] / 20.0,
            data["free_t4"] / 3.0,
            data["free_t3"] / 5.0,
            data["total_t4"] / 15.0,
            data["total_t3"] / 200.0,
            data["thyroid_peroxidase_antibody"] / 100.0,
            data["thyroglobulin_antibody"] / 100.0,
            data["tsh_receptor_antibody"] / 10.0,
            (data["weight_change_kg"] + 20.0) / 40.0,  # normalize -20 to +20 kg range
            data["heart_rate"] / 150.0,
            data["blood_pressure_systolic"] / 200.0,
            data["blood_pressure_diastolic"] / 120.0,
            data["body_temperature"] / 40.0,
            data["fatigue_level"] / 10.0,
            data["anxiety_level"] / 10.0,
            data["depression_symptoms"] / 10.0,
            data["sleep_quality"] / 10.0,
            data["hair_loss"],
            data["dry_skin"],
            data["cold_intolerance"],
            data["heat_intolerance"],
            data["constipation"],
            data["diarrhea"],
            data["muscle_weakness"],
            data["tremor"],
            data["goiter"],
            data["eye_problems"],
            data["menstrual_irregularities"],
            data["family_history_thyroid"],
            data["autoimmune_disease"],
            data["iodine_intake"] / 4.0,
            data["stress_level"] / 10.0,
            data["smoking_status"] / 2.0
        ]
        return np.array(features)
    
    def identify_contributing_factors(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify key factors contributing to thyroid disorder risk"""
        factors = []
        
        # TSH assessment
        tsh = data["tsh"]
        if tsh > 4.5:
            factors.append({
                "factor": "Elevated TSH",
                "value": f"{tsh} mIU/L",
                "impact": "High",
                "description": "High TSH suggests hypothyroidism"
            })
        elif tsh < 0.4:
            factors.append({
                "factor": "Suppressed TSH",
                "value": f"{tsh} mIU/L",
                "impact": "High",
                "description": "Low TSH suggests hyperthyroidism"
            })
        
        # T4 assessment
        t4 = data["free_t4"]
        if t4 < 0.8:
            factors.append({
                "factor": "Low Free T4",
                "value": f"{t4} ng/dL",
                "impact": "High",
                "description": "Low T4 indicates hypothyroidism"
            })
        elif t4 > 1.8:
            factors.append({
                "factor": "High Free T4",
                "value": f"{t4} ng/dL",
                "impact": "High",
                "description": "High T4 indicates hyperthyroidism"
            })
        
        # T3 assessment
        t3 = data["free_t3"]
        if t3 < 2.3:
            factors.append({
                "factor": "Low Free T3",
                "value": f"{t3} pg/mL",
                "impact": "Medium",
                "description": "Low T3 may indicate thyroid dysfunction"
            })
        elif t3 > 4.2:
            factors.append({
                "factor": "High Free T3",
                "value": f"{t3} pg/mL",
                "impact": "High",
                "description": "High T3 indicates hyperthyroidism"
            })
        
        # Antibody assessment
        if data["anti_tpo"] > 35:
            factors.append({
                "factor": "Elevated Anti-TPO",
                "value": f"{data['anti_tpo']} IU/mL",
                "impact": "High",
                "description": "High anti-TPO antibodies suggest autoimmune thyroid disease"
            })
        
        if data["anti_thyroglobulin"] > 40:
            factors.append({
                "factor": "Elevated Anti-Thyroglobulin",
                "value": f"{data['anti_thyroglobulin']} IU/mL",
                "impact": "Medium",
                "description": "High anti-thyroglobulin antibodies suggest autoimmune thyroid disease"
            })
        
        # Family history
        if data["family_history_thyroid"]:
            factors.append({
                "factor": "Family History",
                "value": "Present",
                "impact": "Medium",
                "description": "Family history increases thyroid disorder risk"
            })
        
        # Gender factor
        if data["gender"] == 0:  # Female
            factors.append({
                "factor": "Female Gender",
                "value": "Female",
                "impact": "Low",
                "description": "Women are at higher risk for thyroid disorders"
            })
        
        # Age factor
        age = data["age"]
        if age > 60:
            factors.append({
                "factor": "Advanced Age",
                "value": f"{age} years",
                "impact": "Medium",
                "description": "Thyroid disorders are more common with age"
            })
        
        return factors
    
    def analyze_health_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze health metrics for thyroid assessment"""
        metrics = {
            "thyroid_function": self._assess_thyroid_function(data),
            "autoimmune_markers": self._assess_autoimmune_markers(data),
            "symptom_severity": self._assess_symptom_severity(data),
            "metabolic_impact": self._assess_metabolic_impact(data)
        }
        
        # Overall thyroid disorder risk score
        risk_score = (
            metrics["thyroid_function"]["score"] * 0.4 +
            metrics["autoimmune_markers"]["score"] * 0.3 +
            metrics["symptom_severity"]["score"] * 0.2 +
            metrics["metabolic_impact"]["score"] * 0.1
        )
        
        metrics["overall_risk"] = {
            "score": round(risk_score, 2),
            "category": "High risk" if risk_score >= 7 else "Moderate risk" if risk_score >= 4 else "Low risk"
        }
        
        return metrics
    
    def assess_lifestyle_impact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess lifestyle factors impact on thyroid health"""
        impact = {
            "dietary_impact": self._assess_dietary_impact(data),
            "stress_impact": self._assess_stress_impact(data),
            "environmental_factors": self._assess_environmental_factors(data),
            "recommendations": []
        }
        
        # Generate recommendations
        if data["iodine_deficiency"]:
            impact["recommendations"].append("Ensure adequate iodine intake through iodized salt or supplements")
        
        if data["high_stress_level"] >= 7:
            impact["recommendations"].append("Implement stress management techniques as stress can affect thyroid function")
        
        if data["smoking"]:
            impact["recommendations"].append("Consider smoking cessation as smoking can worsen thyroid eye disease")
        
        if data["excessive_soy_consumption"]:
            impact["recommendations"].append("Moderate soy intake as it may interfere with thyroid hormone absorption")
        
        return impact
    
    def _assess_thyroid_function(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess thyroid function based on hormone levels"""
        tsh = data["tsh"]
        t4 = data["free_t4"]
        t3 = data["free_t3"]
        
        score = 0
        issues = []
        
        # TSH assessment
        if tsh > 10:
            score += 5
            issues.append("Severely elevated TSH")
            function_type = "Severe Hypothyroidism"
        elif tsh > 4.5:
            score += 3
            issues.append("Elevated TSH")
            function_type = "Mild Hypothyroidism"
        elif tsh < 0.1:
            score += 5
            issues.append("Severely suppressed TSH")
            function_type = "Severe Hyperthyroidism"
        elif tsh < 0.4:
            score += 3
            issues.append("Suppressed TSH")
            function_type = "Mild Hyperthyroidism"
        else:
            function_type = "Normal"
        
        # T4 assessment
        if t4 < 0.6:
            score += 4
            issues.append("Severely low T4")
        elif t4 < 0.8:
            score += 2
            issues.append("Low T4")
        elif t4 > 2.0:
            score += 4
            issues.append("Severely high T4")
        elif t4 > 1.8:
            score += 2
            issues.append("High T4")
        
        # T3 assessment
        if t3 < 2.0:
            score += 2
            issues.append("Low T3")
        elif t3 > 4.5:
            score += 3
            issues.append("High T3")
        
        return {
            "score": min(score, 10),
            "function_type": function_type,
            "issues": issues,
            "tsh": tsh,
            "free_t4": t4,
            "free_t3": t3
        }
    
    def _assess_autoimmune_markers(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess autoimmune thyroid markers"""
        score = 0
        markers = []
        
        # Anti-TPO
        anti_tpo = data["anti_tpo"]
        if anti_tpo > 100:
            score += 4
            markers.append("Severely elevated Anti-TPO")
        elif anti_tpo > 35:
            score += 3
            markers.append("Elevated Anti-TPO")
        
        # Anti-Thyroglobulin
        anti_tg = data["anti_thyroglobulin"]
        if anti_tg > 100:
            score += 3
            markers.append("Severely elevated Anti-Thyroglobulin")
        elif anti_tg > 40:
            score += 2
            markers.append("Elevated Anti-Thyroglobulin")
        
        autoimmune_risk = "High" if score >= 5 else "Medium" if score >= 3 else "Low"
        
        return {
            "score": min(score, 10),
            "risk_level": autoimmune_risk,
            "markers": markers,
            "description": "Autoimmune markers indicating Hashimoto's or Graves' disease risk"
        }
    
    def _assess_symptom_severity(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess thyroid-related symptom severity"""
        score = 0
        symptoms = []
        
        # Fatigue
        fatigue = data["fatigue_level"]
        if fatigue >= 7:
            score += 3
            symptoms.append("Severe fatigue")
        elif fatigue >= 4:
            score += 2
            symptoms.append("Moderate fatigue")
        
        # Weight changes
        if data["unexplained_weight_gain"]:
            score += 2
            symptoms.append("Unexplained weight gain")
        
        if data["unexplained_weight_loss"]:
            score += 2
            symptoms.append("Unexplained weight loss")
        
        # Temperature sensitivity
        if data["cold_intolerance"]:
            score += 1
            symptoms.append("Cold intolerance")
        
        if data["heat_intolerance"]:
            score += 1
            symptoms.append("Heat intolerance")
        
        # Other symptoms
        if data["hair_loss"]:
            score += 1
            symptoms.append("Hair loss")
        
        if data["dry_skin"]:
            score += 1
            symptoms.append("Dry skin")
        
        if data["heart_palpitations"]:
            score += 2
            symptoms.append("Heart palpitations")
        
        if data["muscle_weakness"]:
            score += 1
            symptoms.append("Muscle weakness")
        
        return {
            "score": min(score, 10),
            "symptoms": symptoms,
            "category": "Severe symptoms" if score >= 7 else "Moderate symptoms" if score >= 4 else "Mild symptoms"
        }
    
    def _assess_metabolic_impact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess metabolic impact of thyroid dysfunction"""
        score = 0
        impacts = []
        
        # Cholesterol impact
        cholesterol = data["total_cholesterol"]
        if cholesterol > 240:
            score += 2
            impacts.append("High cholesterol (may be thyroid-related)")
        
        # Heart rate impact
        heart_rate = data["resting_heart_rate"]
        if heart_rate > 100:
            score += 2
            impacts.append("Elevated heart rate")
        elif heart_rate < 60:
            score += 1
            impacts.append("Low heart rate")
        
        # Blood pressure
        systolic_bp = data["systolic_bp"]
        if systolic_bp > 140:
            score += 1
            impacts.append("High blood pressure")
        
        return {
            "score": min(score, 10),
            "impacts": impacts,
            "category": "Significant impact" if score >= 4 else "Moderate impact" if score >= 2 else "Minimal impact"
        }
    
    def _assess_dietary_impact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess dietary factors affecting thyroid health"""
        risk_factors = []
        score = 0
        
        if data["iodine_deficiency"]:
            score += 3
            risk_factors.append("Iodine deficiency can cause hypothyroidism")
        
        if data["excessive_soy_consumption"]:
            score += 2
            risk_factors.append("Excessive soy may interfere with thyroid hormone absorption")
        
        if data["cruciferous_vegetables_excess"]:
            score += 1
            risk_factors.append("Excessive raw cruciferous vegetables may affect thyroid function")
        
        return {
            "risk_level": "High" if score >= 4 else "Medium" if score >= 2 else "Low",
            "risk_factors": risk_factors,
            "description": "Dietary factors affecting thyroid hormone production and absorption"
        }
    
    def _assess_stress_impact(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess stress impact on thyroid function"""
        stress_level = data["high_stress_level"]
        
        if stress_level >= 8:
            impact_level = "High"
            description = "Chronic high stress can significantly affect thyroid function"
        elif stress_level >= 5:
            impact_level = "Medium"
            description = "Moderate stress may contribute to thyroid dysfunction"
        else:
            impact_level = "Low"
            description = "Low stress levels have minimal impact on thyroid function"
        
        return {
            "impact_level": impact_level,
            "stress_score": stress_level,
            "description": description
        }
    
    def _assess_environmental_factors(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess environmental factors affecting thyroid health"""
        factors = []
        score = 0
        
        if data["smoking"]:
            score += 2
            factors.append("Smoking can worsen thyroid eye disease and affect hormone levels")
        
        if data["radiation_exposure"]:
            score += 3
            factors.append("Radiation exposure increases thyroid cancer and dysfunction risk")
        
        return {
            "risk_level": "High" if score >= 4 else "Medium" if score >= 2 else "Low",
            "factors": factors,
            "description": "Environmental factors that may affect thyroid health"
        }

class CancerRecurrencePredictor(BasePredictor):
    """Predicts cancer recurrence risk after treatment"""
    
    def __init__(self):
        super().__init__(
            name="Cancer Recurrence Predictor",
            description="Predicts the likelihood of cancer recurrence after treatment completion"
        )
    
    def get_required_fields(self) -> Dict[str, str]:
        return {
            "age_at_diagnosis": "int",
            "gender": "int",  # 1 = male, 0 = female
            "cancer_type": "int",  # 0 = breast, 1 = lung, 2 = colon, 3 = prostate, 4 = other
            "cancer_stage": "int",  # 1-4
            "tumor_size_cm": "float",
            "lymph_nodes_positive": "int",
            "lymph_nodes_examined": "int",
            "histologic_grade": "int",  # 1-3
            "hormone_receptor_positive": "int",  # 1 = yes, 0 = no/not applicable
            "her2_positive": "int",  # 1 = yes, 0 = no/not applicable
            "ki67_percentage": "float",  # proliferation marker
            "months_since_treatment": "int",
            "treatment_surgery": "int",  # 1 = yes, 0 = no
            "treatment_chemotherapy": "int",  # 1 = yes, 0 = no
            "treatment_radiation": "int",  # 1 = yes, 0 = no
            "treatment_hormone_therapy": "int",  # 1 = yes, 0 = no
            "treatment_immunotherapy": "int",  # 1 = yes, 0 = no
            "treatment_targeted_therapy": "int",  # 1 = yes, 0 = no
            "complete_response": "int",  # 1 = yes, 0 = no
            "cea_level": "float",  # ng/mL (carcinoembryonic antigen)
            "ca_125_level": "float",  # U/mL
            "ca_19_9_level": "float",  # U/mL
            "psa_level": "float",  # ng/mL (for prostate cancer)
            "circulating_tumor_cells": "int",  # cells per 7.5 mL
            "family_history_cancer": "int",  # 1 = yes, 0 = no
            "genetic_mutations": "int",  # 1 = yes, 0 = no (BRCA, p53, etc.)
            "smoking_status": "int",  # 0 = never, 1 = former, 2 = current
            "alcohol_consumption": "int",  # 0-4 scale
            "bmi": "float",
            "physical_activity_level": "int",  # 0-4 scale
            "stress_level": "int",  # 0-10 scale
            "sleep_quality": "int",  # 0-10 scale
            "immune_function_score": "int",  # 0-10 scale
            "comorbidities_count": "int",
            "medication_adherence": "int"  # 0-4 scale
        }
    
    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            "age_at_diagnosis": "Age at initial cancer diagnosis",
            "gender": "Gender (1 = Male, 0 = Female)",
            "cancer_type": "Cancer type (0 = Breast, 1 = Lung, 2 = Colon, 3 = Prostate, 4 = Other)",
            "cancer_stage": "Cancer stage at diagnosis (1-4)",
            "tumor_size_cm": "Primary tumor size (cm)",
            "lymph_nodes_positive": "Number of positive lymph nodes",
            "lymph_nodes_examined": "Total lymph nodes examined",
            "histologic_grade": "Histologic grade (1 = Well differentiated, 2 = Moderately differentiated, 3 = Poorly differentiated)",
            "hormone_receptor_positive": "Hormone receptor positive (1 = Yes, 0 = No/Not applicable)",
            "her2_positive": "HER2 positive (1 = Yes, 0 = No/Not applicable)",
            "ki67_percentage": "Ki-67 proliferation index (%)",
            "months_since_treatment": "Months since treatment completion",
            "treatment_surgery": "Received surgery (1 = Yes, 0 = No)",
            "treatment_chemotherapy": "Received chemotherapy (1 = Yes, 0 = No)",
            "treatment_radiation": "Received radiation therapy (1 = Yes, 0 = No)",
            "treatment_hormone_therapy": "Received hormone therapy (1 = Yes, 0 = No)",
            "treatment_immunotherapy": "Received immunotherapy (1 = Yes, 0 = No)",
            "treatment_targeted_therapy": "Received targeted therapy (1 = Yes, 0 = No)",
            "complete_response": "Achieved complete response (1 = Yes, 0 = No)",
            "cea_level": "CEA tumor marker level (ng/mL)",
            "ca_125_level": "CA-125 tumor marker level (U/mL)",
            "ca_19_9_level": "CA 19-9 tumor marker level (U/mL)",
            "psa_level": "PSA level for prostate cancer (ng/mL)",
            "circulating_tumor_cells": "Circulating tumor cells count (per 7.5 mL)",
            "family_history_cancer": "Family history of cancer (1 = Yes, 0 = No)",
            "genetic_mutations": "Known cancer-related genetic mutations (1 = Yes, 0 = No)",
            "smoking_status": "Smoking status (0 = Never, 1 = Former, 2 = Current)",
            "alcohol_consumption": "Alcohol consumption (0-4 scale)",
            "bmi": "Body Mass Index",
            "physical_activity_level": "Physical activity level (0-4 scale)",
            "stress_level": "Stress level (0-10)",
            "sleep_quality": "Sleep quality (0-10)",
            "immune_function_score": "Immune function assessment (0-10)",
            "comorbidities_count": "Number of comorbid conditions",
            "medication_adherence": "Medication adherence (0-4 scale)"
        }
    
    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        # Calculate lymph node ratio
        ln_ratio = data["lymph_nodes_positive"] / max(data["lymph_nodes_examined"], 1)
        
        features = [
            data["age_at_diagnosis"] / 100.0,
            data["gender"],
            data["cancer_type"] / 4.0,
            data["cancer_stage"] / 4.0,
            data["tumor_size_cm"] / 10.0,
            ln_ratio,
            data["lymph_nodes_positive"] / 20.0,
            data["histologic_grade"] / 3.0,
            data["hormone_receptor_positive"],
            data["her2_positive"],
            data["ki67_percentage"] / 100.0,
            data["months_since_treatment"] / 60.0,
            data["treatment_surgery"],
            data["treatment_chemotherapy"],
            data["treatment_radiation"],
            data["treatment_hormone_therapy"],
            data["treatment_immunotherapy"],
            data["treatment_targeted_therapy"],
            data["complete_response"],
            data["cea_level"] / 20.0,
            data["ca_125_level"] / 100.0,
            data["ca_19_9_level"] / 100.0,
            data["psa_level"] / 20.0,
            data["circulating_tumor_cells"] / 10.0,
            data["family_history_cancer"],
            data["genetic_mutations"],
            data["smoking_status"] / 2.0,
            data["alcohol_consumption"] / 4.0,
            data["bmi"] / 50.0,
            data["physical_activity_level"] / 4.0,
            data["stress_level"] / 10.0,
            data["sleep_quality"] / 10.0,
            data["immune_function_score"] / 10.0,
            data["comorbidities_count"] / 10.0,
            data["medication_adherence"] / 4.0
        ]
        return np.array(features)