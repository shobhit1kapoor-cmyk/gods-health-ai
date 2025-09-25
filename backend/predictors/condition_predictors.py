import numpy as np
from typing import Dict, List, Any
from .base_predictor import BasePredictor

class SepsisPredictor(BasePredictor):
    """Predicts sepsis risk for early detection in hospitals - life-saving use case"""
    
    def __init__(self):
        super().__init__(
            name="Sepsis Predictor",
            description="Early detection of sepsis in hospitals using vital signs and laboratory data"
        )
    
    def get_required_fields(self) -> Dict[str, str]:
        return {
            "age": "int",
            "heart_rate": "float",
            "systolic_bp": "float",
            "mean_arterial_pressure": "float",
            "diastolic_bp": "float",
            "respiratory_rate": "float",
            "temperature": "float",  # Celsius
            "spo2": "float",  # Oxygen saturation
            "white_blood_cells": "float",
            "immature_granulocytes": "float",
            "platelets": "float",
            "creatinine": "float",
            "bun": "float",  # Blood urea nitrogen
            "lactate": "float",
            "glucose": "float",
            "magnesium": "float",
            "calcium": "float",
            "phosphate": "float",
            "potassium": "float",
            "sodium": "float",
            "chloride": "float",
            "hematocrit": "float",
            "hemoglobin": "float",
            "ptt": "float",  # Partial thromboplastin time
            "wbc_count": "float",
            "fibrinogen": "float",
            "troponin": "float"
        }
    
    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            "age": "Patient age in years",
            "heart_rate": "Heart rate (beats per minute)",
            "systolic_bp": "Systolic blood pressure (mmHg)",
            "mean_arterial_pressure": "Mean arterial pressure (mmHg)",
            "diastolic_bp": "Diastolic blood pressure (mmHg)",
            "respiratory_rate": "Respiratory rate (breaths per minute)",
            "temperature": "Body temperature (°C)",
            "spo2": "Oxygen saturation (%)",
            "white_blood_cells": "White blood cell count (K/uL)",
            "immature_granulocytes": "Immature granulocytes (%)",
            "platelets": "Platelet count (K/uL)",
            "creatinine": "Serum creatinine (mg/dL)",
            "bun": "Blood urea nitrogen (mg/dL)",
            "lactate": "Lactate level (mmol/L)",
            "glucose": "Blood glucose (mg/dL)",
            "magnesium": "Magnesium level (mg/dL)",
            "calcium": "Calcium level (mg/dL)",
            "phosphate": "Phosphate level (mg/dL)",
            "potassium": "Potassium level (mEq/L)",
            "sodium": "Sodium level (mEq/L)",
            "chloride": "Chloride level (mEq/L)",
            "hematocrit": "Hematocrit (%)",
            "hemoglobin": "Hemoglobin (g/dL)",
            "ptt": "Partial thromboplastin time (seconds)",
            "wbc_count": "White blood cell count (cells/μL)",
            "fibrinogen": "Fibrinogen level (mg/dL)",
            "troponin": "Troponin level (ng/mL)"
        }
    
    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        features = [
            data["age"] / 100.0,
            data["heart_rate"] / 200.0,
            data["systolic_bp"] / 200.0,
            data["mean_arterial_pressure"] / 150.0,
            data["diastolic_bp"] / 120.0,
            data["respiratory_rate"] / 50.0,
            data["temperature"] / 45.0,
            data["spo2"] / 100.0,
            data["white_blood_cells"] / 50.0,
            data["immature_granulocytes"] / 100.0,
            data["platelets"] / 1000.0,
            data["creatinine"] / 10.0,
            data["bun"] / 100.0,
            data["lactate"] / 20.0,
            data["glucose"] / 500.0,
            data["magnesium"] / 5.0,
            data["calcium"] / 15.0,
            data["phosphate"] / 10.0,
            data["potassium"] / 10.0,
            data["sodium"] / 200.0,
            data["chloride"] / 150.0,
            data["hematocrit"] / 100.0,
            data["hemoglobin"] / 20.0,
            data["ptt"] / 100.0,
            data["wbc_count"] / 50000.0,
            data["fibrinogen"] / 1000.0,
            data["troponin"] / 50.0
        ]
        return np.array(features)
    
    def identify_contributing_factors(self, data: Dict[str, Any]) -> List[str]:
        """Identify key factors contributing to sepsis risk"""
        factors = []
        
        # Age factors
        if data.get("age", 0) > 65:
            factors.append("Advanced age increasing sepsis risk and mortality")
        elif data.get("age", 0) < 1:
            factors.append("Very young age with immature immune system")
        
        # Vital signs abnormalities
        if data.get("heart_rate", 0) > 100:
            factors.append("Tachycardia suggesting systemic inflammatory response")
        elif data.get("heart_rate", 0) < 60:
            factors.append("Bradycardia potentially indicating severe sepsis")
        
        if data.get("respiratory_rate", 0) > 22:
            factors.append("Tachypnea indicating respiratory distress or compensation")
        
        if data.get("temperature", 0) > 38.3 or data.get("temperature", 0) < 36.0:
            factors.append("Abnormal body temperature suggesting infection")
        
        # Blood pressure concerns
        if data.get("systolic_bp", 0) < 90 or data.get("mean_arterial_pressure", 0) < 65:
            factors.append("Hypotension indicating possible septic shock")
        
        # Oxygen saturation
        if data.get("spo2", 0) < 95:
            factors.append("Low oxygen saturation suggesting respiratory compromise")
        
        # Laboratory abnormalities
        if data.get("white_blood_cells", 0) > 12 or data.get("white_blood_cells", 0) < 4:
            factors.append("Abnormal white blood cell count indicating immune response")
        
        if data.get("lactate", 0) > 2.0:
            factors.append("Elevated lactate suggesting tissue hypoperfusion")
        
        if data.get("creatinine", 0) > 1.5:
            factors.append("Elevated creatinine indicating kidney dysfunction")
        
        if data.get("platelets", 0) < 100:
            factors.append("Low platelet count suggesting coagulation dysfunction")
        
        # Glucose abnormalities
        if data.get("glucose", 0) > 180:
            factors.append("Hyperglycemia associated with stress response and poor outcomes")
        
        # Electrolyte imbalances
        if data.get("sodium", 0) < 135 or data.get("sodium", 0) > 145:
            factors.append("Sodium imbalance indicating fluid and electrolyte disturbance")
        
        if data.get("potassium", 0) < 3.5 or data.get("potassium", 0) > 5.0:
            factors.append("Potassium imbalance affecting cardiac and muscle function")
        
        # Coagulation abnormalities
        if data.get("ptt", 0) > 40:
            factors.append("Prolonged clotting time suggesting coagulopathy")
        
        # Cardiac markers
        if data.get("troponin", 0) > 0.1:
            factors.append("Elevated troponin indicating cardiac stress or damage")
        
        return factors
    
    def analyze_health_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze key health metrics for sepsis risk assessment"""
        analysis = {
            "sepsis_risk": "low",
            "monitoring_level": "routine",
            "risk_indicators": [],
            "intervention_needs": []
        }
        
        # Risk stratification
        risk_factors = 0
        
        # Age risk (elderly and very young at higher risk)
        age = data.get("age", 0)
        if age > 65 or age < 1:
            risk_factors += 2
        elif age > 75:
            risk_factors += 3
        
        # Vital signs abnormalities
        temp = data.get("temperature", 98.6)
        if temp > 101.3 or temp < 96.8:  # Fever or hypothermia
            risk_factors += 2
        
        heart_rate = data.get("heart_rate", 70)
        if heart_rate > 90:  # Tachycardia
            risk_factors += 1
        
        respiratory_rate = data.get("respiratory_rate", 16)
        if respiratory_rate > 20:  # Tachypnea
            risk_factors += 1
        
        # Blood pressure abnormalities
        systolic_bp = data.get("systolic_bp", 120)
        if systolic_bp < 90:  # Hypotension
            risk_factors += 2
        
        # Oxygen saturation
        oxygen_sat = data.get("oxygen_saturation", 98)
        if oxygen_sat < 95:
            risk_factors += 2
        
        # Laboratory abnormalities
        wbc = data.get("white_blood_cell_count", 7000)
        if wbc > 12000 or wbc < 4000:
            risk_factors += 2
        
        lactate = data.get("lactate", 1.0)
        if lactate > 2.0:
            risk_factors += 2
        
        # Organ dysfunction indicators
        creatinine = data.get("creatinine", 1.0)
        if creatinine > 2.0:
            risk_factors += 2
        
        bilirubin = data.get("bilirubin", 1.0)
        if bilirubin > 2.0:
            risk_factors += 1
        
        # Risk level assignment
        if risk_factors >= 6:
            analysis["sepsis_risk"] = "high"
            analysis["monitoring_level"] = "intensive"
        elif risk_factors >= 3:
            analysis["sepsis_risk"] = "moderate"
            analysis["monitoring_level"] = "increased"
        
        # Specific risk indicators
        if temp > 101.3 or temp < 96.8:
            analysis["risk_indicators"].append("Temperature dysregulation")
        
        if heart_rate > 90 and respiratory_rate > 20:
            analysis["risk_indicators"].append("SIRS criteria met")
        
        if systolic_bp < 90:
            analysis["risk_indicators"].append("Hypotension/shock")
        
        if lactate > 2.0:
            analysis["risk_indicators"].append("Elevated lactate")
        
        if wbc > 12000 or wbc < 4000:
            analysis["risk_indicators"].append("Abnormal white blood cell count")
        
        # Intervention needs
        if analysis["sepsis_risk"] == "high":
            analysis["intervention_needs"].append("Immediate antibiotic therapy")
            analysis["intervention_needs"].append("Fluid resuscitation")
            analysis["intervention_needs"].append("ICU monitoring")
        elif analysis["sepsis_risk"] == "moderate":
            analysis["intervention_needs"].append("Close monitoring")
            analysis["intervention_needs"].append("Consider antibiotic therapy")
        
        if systolic_bp < 90:
            analysis["intervention_needs"].append("Vasopressor support")
        
        return analysis
    
    def assess_lifestyle_impact(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Assess lifestyle factors affecting sepsis risk and prevention"""
        recommendations = {}
        
        # Immune system support
        age = data.get("age", 0)
        if age > 65:
            recommendations["immune_support"] = "Maintain vaccinations up to date, especially pneumonia and flu vaccines to prevent infections"
        
        # Chronic disease management
        if data.get("diabetes", 0) == 1:
            recommendations["diabetes_management"] = "Maintain strict blood sugar control to reduce infection risk and improve immune function"
        
        if data.get("chronic_kidney_disease", 0) == 1:
            recommendations["kidney_care"] = "Follow nephrology care plan and monitor for signs of infection or complications"
        
        if data.get("immunocompromised", 0) == 1:
            recommendations["infection_prevention"] = "Practice strict hygiene, avoid crowds during illness seasons, and seek immediate care for any signs of infection"
        
        # Wound and catheter care
        if data.get("recent_surgery", 0) == 1:
            recommendations["wound_care"] = "Follow proper wound care instructions, keep surgical sites clean and dry, and monitor for signs of infection"
        
        if data.get("indwelling_catheter", 0) == 1:
            recommendations["catheter_care"] = "Maintain proper catheter hygiene and follow healthcare provider instructions for care and monitoring"
        
        # General infection prevention
        recommendations["hygiene"] = "Practice frequent hand washing, maintain good personal hygiene, and avoid contact with sick individuals"
        recommendations["medical_care"] = "Seek prompt medical attention for any signs of infection, fever, or unusual symptoms"
        recommendations["medication_compliance"] = "Take all prescribed medications as directed and complete full courses of antibiotics when prescribed"
        
        return recommendations
        
        # Length of stay analysis
        if data.get("time_in_hospital", 0) < 3:
            factors.append("Short hospital stay may indicate incomplete treatment or early discharge")
        elif data.get("time_in_hospital", 0) > 7:
            factors.append("Extended hospital stay suggesting complex medical condition")
        
        # Previous healthcare utilization
        if data.get("number_emergency", 0) > 2:
            factors.append("Multiple emergency visits in past year indicating unstable health")
        
        if data.get("number_inpatient", 0) > 1:
            factors.append("Previous hospitalizations suggesting chronic or recurring conditions")
        
        # Admission characteristics
        if data.get("admission_type", 0) == 1:  # Emergency
            factors.append("Emergency admission indicating acute health crisis")
        
        # Medication management
        if data.get("change", 0) == 1:
            factors.append("Recent medication changes requiring monitoring and adjustment")
        
        if data.get("num_medications", 0) > 15:
            factors.append("High number of medications increasing complexity of care")
        
        # Comorbidity burden
        if data.get("comorbidity_score", 0) > 5:
            factors.append("High comorbidity burden requiring comprehensive care coordination")
        
        # Age factor
        if data.get("age", 0) > 70:
            factors.append("Advanced age associated with higher readmission risk")
        
        # Diabetes management
        if data.get("diabetesMed", 0) == 1 and data.get("a1c_result", 0) in [1, 2]:
            factors.append("Poorly controlled diabetes requiring intensive management")
        
        return factors
    
    def analyze_health_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze key health metrics for readmission assessment"""
        analysis = {
            "care_complexity": "low",
            "medication_burden": "manageable",
            "comorbidity_status": "stable",
            "risk_indicators": []
        }
        
        # Care complexity assessment
        complexity_score = 0
        if data.get("num_procedures", 0) > 3:
            complexity_score += 1
        if data.get("num_lab_procedures", 0) > 50:
            complexity_score += 1
        if data.get("number_diagnoses", 0) > 5:
            complexity_score += 1
        
        if complexity_score >= 2:
            analysis["care_complexity"] = "high"
            analysis["risk_indicators"].append("Complex medical care requirements")
        
        # Medication burden
        if data.get("num_medications", 0) > 10:
            analysis["medication_burden"] = "high"
            analysis["risk_indicators"].append("High medication burden")
        
        # Comorbidity assessment
        if data.get("comorbidity_score", 0) > 3:
            analysis["comorbidity_status"] = "complex"
            analysis["risk_indicators"].append("Multiple comorbidities")
        
        # Healthcare utilization pattern
        if data.get("number_emergency", 0) + data.get("number_inpatient", 0) > 3:
            analysis["risk_indicators"].append("High healthcare utilization pattern")
        
        return analysis
    
    def assess_lifestyle_impact(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Assess lifestyle factors affecting readmission risk"""
        recommendations = {}
        
        # Medication adherence
        if data.get("num_medications", 0) > 5:
            recommendations["medication_management"] = "Use pill organizers, set reminders, and maintain updated medication lists"
        
        # Diabetes management
        if data.get("diabetesMed", 0) == 1:
            recommendations["diabetes_care"] = "Monitor blood sugar regularly, follow dietary guidelines, and maintain regular follow-up appointments"
        
        # Follow-up care
        recommendations["follow_up"] = "Schedule and attend all follow-up appointments with healthcare providers"
        recommendations["symptom_monitoring"] = "Learn to recognize warning signs and when to seek medical attention"
        
        # Support system
        if data.get("age", 0) > 65:
            recommendations["support_system"] = "Engage family members or caregivers in discharge planning and ongoing care"
        
        # Emergency preparedness
        recommendations["emergency_plan"] = "Have a clear plan for accessing healthcare services and emergency contacts readily available"
        
        return recommendations
        
        # Vital signs analysis
        if data.get("temperature", 0) > 38.3 or data.get("temperature", 0) < 36.0:
            factors.append("Abnormal body temperature indicating possible infection")
        
        if data.get("heart_rate", 0) > 90:
            factors.append("Elevated heart rate (tachycardia) suggesting systemic response")
        
        if data.get("respiratory_rate", 0) > 20:
            factors.append("Increased respiratory rate indicating respiratory distress")
        
        if data.get("systolic_bp", 0) < 90:
            factors.append("Low blood pressure suggesting septic shock risk")
        
        # Laboratory values
        if data.get("white_blood_cells", 0) > 12 or data.get("white_blood_cells", 0) < 4:
            factors.append("Abnormal white blood cell count indicating immune response")
        
        if data.get("lactate", 0) > 2.0:
            factors.append("Elevated lactate levels suggesting tissue hypoperfusion")
        
        if data.get("creatinine", 0) > 1.2:
            factors.append("Elevated creatinine indicating potential kidney dysfunction")
        
        if data.get("platelets", 0) < 100:
            factors.append("Low platelet count suggesting coagulation issues")
        
        # Age factor
        if data.get("age", 0) > 65:
            factors.append("Advanced age increasing infection susceptibility")
        
        return factors
    
    def analyze_health_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze key health metrics for sepsis assessment"""
        analysis = {
            "vital_signs_status": "normal",
            "infection_markers": "normal",
            "organ_function": "normal",
            "severity_indicators": []
        }
        
        # Vital signs assessment
        vital_abnormalities = 0
        if data.get("temperature", 0) > 38.3 or data.get("temperature", 0) < 36.0:
            vital_abnormalities += 1
        if data.get("heart_rate", 0) > 90:
            vital_abnormalities += 1
        if data.get("respiratory_rate", 0) > 20:
            vital_abnormalities += 1
        if data.get("systolic_bp", 0) < 90:
            vital_abnormalities += 1
        
        if vital_abnormalities >= 2:
            analysis["vital_signs_status"] = "concerning"
            analysis["severity_indicators"].append("Multiple vital sign abnormalities")
        
        # Infection markers
        if data.get("white_blood_cells", 0) > 12 or data.get("white_blood_cells", 0) < 4:
            analysis["infection_markers"] = "abnormal"
        
        # Organ function assessment
        organ_issues = []
        if data.get("creatinine", 0) > 1.2:
            organ_issues.append("kidney")
        if data.get("lactate", 0) > 2.0:
            organ_issues.append("tissue_perfusion")
        if data.get("platelets", 0) < 100:
            organ_issues.append("coagulation")
        
        if organ_issues:
            analysis["organ_function"] = "impaired"
            analysis["severity_indicators"].extend([f"{organ} dysfunction" for organ in organ_issues])
        
        return analysis
    
    def assess_lifestyle_impact(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Assess lifestyle factors affecting sepsis risk"""
        recommendations = {}
        
        # Age-related recommendations
        if data.get("age", 0) > 65:
            recommendations["age_factor"] = "Older adults have higher sepsis risk - maintain good hygiene and seek prompt medical care for infections"
        
        # General prevention recommendations
        recommendations["infection_prevention"] = "Practice good hand hygiene, keep wounds clean, and stay up-to-date with vaccinations"
        recommendations["early_recognition"] = "Learn to recognize early signs of infection and seek immediate medical attention"
        recommendations["chronic_conditions"] = "Manage chronic conditions like diabetes to reduce infection risk"
        recommendations["immune_support"] = "Maintain a healthy diet, regular exercise, and adequate sleep to support immune function"
        
        return recommendations

class HospitalReadmissionPredictor(BasePredictor):
    """Predicts if a patient will need to return to hospital soon after discharge"""
    
    def __init__(self):
        super().__init__(
            name="Hospital Readmission Predictor",
            description="Predicts likelihood of patient readmission within 30 days of discharge"
        )
    
    def get_required_fields(self) -> Dict[str, str]:
        return {
            "age": "int",
            "gender": "int",  # 1 = male, 0 = female
            "admission_type": "int",  # 1 = emergency, 2 = urgent, 3 = elective
            "discharge_disposition": "int",  # 1 = home, 2 = other facility, 3 = expired
            "admission_source": "int",  # 1 = emergency, 2 = referral, 3 = transfer
            "time_in_hospital": "int",  # days
            "num_lab_procedures": "int",
            "num_procedures": "int",
            "num_medications": "int",
            "number_outpatient": "int",
            "number_emergency": "int",
            "number_inpatient": "int",
            "diag_1": "int",  # Primary diagnosis category
            "diag_2": "int",  # Secondary diagnosis category
            "diag_3": "int",  # Additional diagnosis category
            "number_diagnoses": "int",
            "max_glu_serum": "int",  # 0 = none, 1 = >200, 2 = >300, 3 = normal
            "a1c_result": "int",  # 0 = none, 1 = >7, 2 = >8, 3 = normal
            "metformin": "int",  # 0 = no, 1 = steady, 2 = up, 3 = down
            "insulin": "int",  # 0 = no, 1 = steady, 2 = up, 3 = down
            "change": "int",  # 1 = change in medication, 0 = no change
            "diabetesMed": "int",  # 1 = yes, 0 = no
            "comorbidity_score": "int",  # 0-10 scale
            "previous_admissions": "int"  # Number of previous admissions in last year
        }
    
    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            "age": "Patient age in years",
            "gender": "Gender (1 = Male, 0 = Female)",
            "admission_type": "Type of admission (1 = Emergency, 2 = Urgent, 3 = Elective)",
            "discharge_disposition": "Discharge disposition (1 = Home, 2 = Other facility, 3 = Expired)",
            "admission_source": "Source of admission (1 = Emergency, 2 = Referral, 3 = Transfer)",
            "time_in_hospital": "Length of stay in days",
            "num_lab_procedures": "Number of lab procedures performed",
            "num_procedures": "Number of procedures performed",
            "num_medications": "Number of medications administered",
            "number_outpatient": "Number of outpatient visits in previous year",
            "number_emergency": "Number of emergency visits in previous year",
            "number_inpatient": "Number of inpatient visits in previous year",
            "diag_1": "Primary diagnosis category (1-18)",
            "diag_2": "Secondary diagnosis category (1-18)",
            "diag_3": "Additional diagnosis category (1-18)",
            "number_diagnoses": "Total number of diagnoses",
            "max_glu_serum": "Maximum glucose serum test result (0 = None, 1 = >200, 2 = >300, 3 = Normal)",
            "a1c_result": "A1C test result (0 = None, 1 = >7%, 2 = >8%, 3 = Normal)",
            "metformin": "Metformin prescription (0 = No, 1 = Steady, 2 = Up, 3 = Down)",
            "insulin": "Insulin prescription (0 = No, 1 = Steady, 2 = Up, 3 = Down)",
            "change": "Change in diabetic medication (1 = Yes, 0 = No)",
            "diabetesMed": "Diabetic medication prescribed (1 = Yes, 0 = No)",
            "comorbidity_score": "Comorbidity score (0-10, higher indicates more comorbidities)",
            "previous_admissions": "Number of previous hospital admissions in the last year"
        }
    
    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        features = [
            data["age"] / 100.0,
            data["gender"],
            data["admission_type"] / 3.0,
            data["discharge_disposition"] / 3.0,
            data["admission_source"] / 3.0,
            data["time_in_hospital"] / 30.0,
            data["num_lab_procedures"] / 100.0,
            data["num_procedures"] / 20.0,
            data["num_medications"] / 50.0,
            data["number_outpatient"] / 20.0,
            data["number_emergency"] / 10.0,
            data["number_inpatient"] / 10.0,
            data["diag_1"] / 18.0,
            data["diag_2"] / 18.0,
            data["diag_3"] / 18.0,
            data["number_diagnoses"] / 20.0,
            data["max_glu_serum"] / 3.0,
            data["a1c_result"] / 3.0,
            data["metformin"] / 3.0,
            data["insulin"] / 3.0,
            data["change"],
            data["diabetesMed"],
            data["comorbidity_score"] / 10.0,
            data["previous_admissions"] / 10.0
        ]
        return np.array(features)

class ICUMortalityPredictor(BasePredictor):
    """Predicts survival probability in ICU based on vitals and lab results"""
    
    def __init__(self):
        super().__init__(
            name="ICU Mortality Predictor",
            description="Predicts survival probability in ICU using vital signs and laboratory results"
        )
    
    def get_required_fields(self) -> Dict[str, str]:
        return {
            "age": "int",
            "gender": "int",  # 1 = male, 0 = female
            "apache_score": "int",  # APACHE II score (0-71)
            "glasgow_coma_scale": "int",  # 3-15
            "heart_rate": "float",
            "systolic_bp": "float",
            "diastolic_bp": "float",
            "mean_bp": "float",
            "respiratory_rate": "float",
            "temperature": "float",
            "spo2": "float",
            "urine_output": "float",  # mL/hr
            "mechanical_ventilation": "int",  # 1 = yes, 0 = no
            "vasopressor_use": "int",  # 1 = yes, 0 = no
            "sedation_level": "int",  # 0-4 scale
            "creatinine": "float",
            "bun": "float",
            "glucose": "float",
            "sodium": "float",
            "potassium": "float",
            "chloride": "float",
            "hemoglobin": "float",
            "hematocrit": "float",
            "platelets": "float",
            "white_blood_cells": "float",
            "lactate": "float",
            "ph": "float",
            "pco2": "float",
            "po2": "float",
            "bicarbonate": "float",
            "admission_diagnosis": "int",  # Primary admission diagnosis category
            "comorbidities": "int",  # Number of comorbidities
            "length_of_stay": "int"  # Days in ICU so far
        }
    
    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            "age": "Patient age in years",
            "gender": "Gender (1 = Male, 0 = Female)",
            "apache_score": "APACHE II score (0-71, higher indicates more severe illness)",
            "glasgow_coma_scale": "Glasgow Coma Scale (3-15, higher is better)",
            "heart_rate": "Heart rate (beats per minute)",
            "systolic_bp": "Systolic blood pressure (mmHg)",
            "diastolic_bp": "Diastolic blood pressure (mmHg)",
            "mean_bp": "Mean arterial pressure (mmHg)",
            "respiratory_rate": "Respiratory rate (breaths per minute)",
            "temperature": "Body temperature (°C)",
            "spo2": "Oxygen saturation (%)",
            "urine_output": "Urine output (mL/hr)",
            "mechanical_ventilation": "On mechanical ventilation (1 = Yes, 0 = No)",
            "vasopressor_use": "Using vasopressors (1 = Yes, 0 = No)",
            "sedation_level": "Sedation level (0 = Awake, 1 = Light, 2 = Moderate, 3 = Deep, 4 = Coma)",
            "creatinine": "Serum creatinine (mg/dL)",
            "bun": "Blood urea nitrogen (mg/dL)",
            "glucose": "Blood glucose (mg/dL)",
            "sodium": "Sodium level (mEq/L)",
            "potassium": "Potassium level (mEq/L)",
            "chloride": "Chloride level (mEq/L)",
            "hemoglobin": "Hemoglobin (g/dL)",
            "hematocrit": "Hematocrit (%)",
            "platelets": "Platelet count (K/uL)",
            "white_blood_cells": "White blood cell count (K/uL)",
            "lactate": "Lactate level (mmol/L)",
            "ph": "Blood pH",
            "pco2": "Partial pressure of CO2 (mmHg)",
            "po2": "Partial pressure of O2 (mmHg)",
            "bicarbonate": "Bicarbonate level (mEq/L)",
            "admission_diagnosis": "Primary admission diagnosis category (1-20)",
            "comorbidities": "Number of comorbidities",
            "length_of_stay": "Current length of stay in ICU (days)"
        }
    
    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        features = [
            data["age"] / 100.0,
            data["gender"],
            data["apache_score"] / 71.0,
            data["glasgow_coma_scale"] / 15.0,
            data["heart_rate"] / 200.0,
            data["systolic_bp"] / 200.0,
            data["diastolic_bp"] / 120.0,
            data["mean_bp"] / 150.0,
            data["respiratory_rate"] / 50.0,
            data["temperature"] / 45.0,
            data["spo2"] / 100.0,
            data["urine_output"] / 200.0,
            data["mechanical_ventilation"],
            data["vasopressor_use"],
            data["sedation_level"] / 4.0,
            data["creatinine"] / 10.0,
            data["bun"] / 100.0,
            data["glucose"] / 500.0,
            data["sodium"] / 200.0,
            data["potassium"] / 10.0,
            data["chloride"] / 150.0,
            data["hemoglobin"] / 20.0,
            data["hematocrit"] / 100.0,
            data["platelets"] / 1000.0,
            data["white_blood_cells"] / 50.0,
            data["lactate"] / 20.0,
            data["ph"] / 8.0,
            data["pco2"] / 100.0,
            data["po2"] / 500.0,
            data["bicarbonate"] / 50.0,
            data["admission_diagnosis"] / 20.0,
            data["comorbidities"] / 10.0,
            data["length_of_stay"] / 30.0
        ]
        return np.array(features)
    
    def identify_contributing_factors(self, data: Dict[str, Any], prediction_result: Dict[str, Any]) -> List[str]:
        """Identify key factors contributing to ICU mortality risk"""
        factors = []
        
        # Severity scores
        if data.get("apache_score", 0) > 25:
            factors.append("High APACHE II score indicating severe illness")
        
        if data.get("glasgow_coma_scale", 15) < 8:
            factors.append("Low Glasgow Coma Scale suggesting severe neurological impairment")
        
        # Vital signs instability
        if data.get("systolic_bp", 0) < 90 or data.get("mean_bp", 0) < 65:
            factors.append("Hypotension indicating circulatory shock")
        
        if data.get("heart_rate", 0) > 120 or data.get("heart_rate", 0) < 50:
            factors.append("Abnormal heart rate suggesting cardiac instability")
        
        # Respiratory failure indicators
        if data.get("mechanical_ventilation", 0) == 1:
            factors.append("Mechanical ventilation indicating respiratory failure")
        
        if data.get("spo2", 100) < 90:
            factors.append("Low oxygen saturation indicating respiratory compromise")
        
        # Organ dysfunction markers
        if data.get("creatinine", 0) > 2.0:
            factors.append("Elevated creatinine indicating kidney dysfunction")
        
        if data.get("lactate", 0) > 4.0:
            factors.append("Severely elevated lactate indicating tissue hypoperfusion")
        
        if data.get("platelets", 0) < 50:
            factors.append("Severe thrombocytopenia indicating coagulation dysfunction")
        
        # Support requirements
        if data.get("vasopressor_use", 0) == 1:
            factors.append("Vasopressor requirement indicating hemodynamic instability")
        
        # Age factor
        if data.get("age", 0) > 75:
            factors.append("Advanced age associated with higher mortality risk")
        
        return factors
    
    def analyze_health_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze key health metrics for ICU mortality assessment"""
        analysis = {
            "severity_level": "moderate",
            "organ_function": "stable",
            "hemodynamic_status": "stable",
            "critical_indicators": []
        }
        
        # Severity assessment
        if data.get("apache_score", 0) > 30:
            analysis["severity_level"] = "critical"
            analysis["critical_indicators"].append("Extremely high APACHE II score")
        elif data.get("apache_score", 0) > 20:
            analysis["severity_level"] = "severe"
        
        # Organ function assessment
        organ_failures = 0
        if data.get("creatinine", 0) > 1.5:
            organ_failures += 1
        if data.get("mechanical_ventilation", 0) == 1:
            organ_failures += 1
        if data.get("platelets", 0) < 100:
            organ_failures += 1
        if data.get("glasgow_coma_scale", 15) < 10:
            organ_failures += 1
        
        if organ_failures >= 3:
            analysis["organ_function"] = "multi-organ failure"
            analysis["critical_indicators"].append("Multiple organ dysfunction")
        elif organ_failures >= 1:
            analysis["organ_function"] = "impaired"
        
        # Hemodynamic assessment
        if data.get("vasopressor_use", 0) == 1 or data.get("mean_bp", 0) < 65:
            analysis["hemodynamic_status"] = "unstable"
            analysis["critical_indicators"].append("Hemodynamic instability")
        
        return analysis
    
    def assess_lifestyle_impact(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Assess lifestyle factors affecting ICU outcomes"""
        recommendations = {}
        
        # Family involvement
        recommendations["family_support"] = "Family presence and involvement in care decisions can improve outcomes"
        
        # Recovery planning
        recommendations["recovery_focus"] = "Focus on early mobilization and rehabilitation when medically stable"
        
        # Long-term considerations
        if data.get("age", 0) > 65:
            recommendations["age_considerations"] = "Older patients may require extended recovery time and specialized care planning"
        
        # Preventive measures for future
        recommendations["prevention"] = "Address underlying conditions and risk factors to prevent future critical illness"
        recommendations["follow_up"] = "Ensure comprehensive follow-up care after ICU discharge for optimal recovery"
        
        return recommendations

class PostSurgeryComplicationPredictor(BasePredictor):
    """Predicts risk of complications after major surgeries"""
    
    def __init__(self):
        super().__init__(
            name="Post-Surgery Complication Predictor",
            description="Predicts risk of complications following major surgical procedures"
        )
    
    def get_required_fields(self) -> Dict[str, str]:
        return {
            "age": "int",
            "gender": "int",  # 1 = male, 0 = female
            "bmi": "float",
            "surgery_type": "int",  # 1-10 different surgery categories
            "surgery_duration": "float",  # hours
            "anesthesia_type": "int",  # 1 = general, 2 = regional, 3 = local
            "asa_score": "int",  # ASA physical status (1-5)
            "emergency_surgery": "int",  # 1 = yes, 0 = no
            "preop_hemoglobin": "float",
            "preop_creatinine": "float",
            "preop_albumin": "float",
            "diabetes": "int",  # 1 = yes, 0 = no
            "hypertension": "int",  # 1 = yes, 0 = no
            "heart_disease": "int",  # 1 = yes, 0 = no
            "copd": "int",  # 1 = yes, 0 = no
            "kidney_disease": "int",  # 1 = yes, 0 = no
            "liver_disease": "int",  # 1 = yes, 0 = no
            "smoking_status": "int",  # 0 = never, 1 = former, 2 = current
            "alcohol_use": "int",  # 0-3 scale
            "functional_status": "int",  # 1 = independent, 2 = partially dependent, 3 = dependent
            "blood_loss": "float",  # mL
            "transfusion_required": "int",  # 1 = yes, 0 = no
            "postop_pain_score": "int",  # 0-10 scale
            "mobility_day1": "int",  # 1 = mobile, 0 = immobile
            "wound_class": "int"  # 1 = clean, 2 = clean-contaminated, 3 = contaminated, 4 = dirty
        }
    
    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            "age": "Patient age in years",
            "gender": "Gender (1 = Male, 0 = Female)",
            "bmi": "Body Mass Index",
            "surgery_type": "Type of surgery (1-10 scale based on complexity and risk)",
            "surgery_duration": "Duration of surgery in hours",
            "anesthesia_type": "Type of anesthesia (1 = General, 2 = Regional, 3 = Local)",
            "asa_score": "ASA Physical Status Classification (1-5, higher indicates more risk)",
            "emergency_surgery": "Emergency surgery (1 = Yes, 0 = No)",
            "preop_hemoglobin": "Preoperative hemoglobin level (g/dL)",
            "preop_creatinine": "Preoperative creatinine level (mg/dL)",
            "preop_albumin": "Preoperative albumin level (g/dL)",
            "diabetes": "Diabetes mellitus (1 = Yes, 0 = No)",
            "hypertension": "Hypertension (1 = Yes, 0 = No)",
            "heart_disease": "Heart disease (1 = Yes, 0 = No)",
            "copd": "Chronic obstructive pulmonary disease (1 = Yes, 0 = No)",
            "kidney_disease": "Kidney disease (1 = Yes, 0 = No)",
            "liver_disease": "Liver disease (1 = Yes, 0 = No)",
            "smoking_status": "Smoking status (0 = Never, 1 = Former, 2 = Current)",
            "alcohol_use": "Alcohol use (0 = None, 1 = Light, 2 = Moderate, 3 = Heavy)",
            "functional_status": "Functional status (1 = Independent, 2 = Partially dependent, 3 = Dependent)",
            "blood_loss": "Estimated blood loss during surgery (mL)",
            "transfusion_required": "Blood transfusion required (1 = Yes, 0 = No)",
            "postop_pain_score": "Postoperative pain score (0-10, higher indicates more pain)",
            "mobility_day1": "Mobile on postoperative day 1 (1 = Yes, 0 = No)",
            "wound_class": "Wound classification (1 = Clean, 2 = Clean-contaminated, 3 = Contaminated, 4 = Dirty)"
        }
    
    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        features = [
            data["age"] / 100.0,
            data["gender"],
            data["bmi"] / 50.0,
            data["surgery_type"] / 10.0,
            data["surgery_duration"] / 12.0,
            data["anesthesia_type"] / 3.0,
            data["asa_score"] / 5.0,
            data["emergency_surgery"],
            data["preop_hemoglobin"] / 20.0,
            data["preop_creatinine"] / 5.0,
            data["preop_albumin"] / 5.0,
            data["diabetes"],
            data["hypertension"],
            data["heart_disease"],
            data["copd"],
            data["kidney_disease"],
            data["liver_disease"],
            data["smoking_status"] / 2.0,
            data["alcohol_use"] / 3.0,
            data["functional_status"] / 3.0,
            data["blood_loss"] / 2000.0,
            data["transfusion_required"],
            data["postop_pain_score"] / 10.0,
            data["mobility_day1"],
            data["wound_class"] / 4.0
        ]
        return np.array(features)
    
    def identify_contributing_factors(self, data: Dict[str, Any], prediction_result: Dict[str, Any]) -> List[str]:
        """Identify key factors contributing to post-surgery complication risk"""
        factors = []
        
        # Patient risk factors
        if data.get("age", 0) > 70:
            factors.append("Advanced age increasing surgical risk and recovery time")
        
        if data.get("bmi", 0) > 30:
            factors.append("Obesity increasing risk of wound complications and infections")
        
        if data.get("asa_score", 0) >= 4:
            factors.append("High ASA score indicating severe systemic disease")
        
        # Surgery characteristics
        if data.get("emergency_surgery", 0) == 1:
            factors.append("Emergency surgery with higher complication rates")
        
        if data.get("surgery_duration", 0) > 4:
            factors.append("Prolonged surgery duration increasing infection and complication risk")
        
        # Comorbidities
        comorbidity_count = sum([
            data.get("diabetes", 0),
            data.get("hypertension", 0),
            data.get("heart_disease", 0),
            data.get("copd", 0),
            data.get("kidney_disease", 0),
            data.get("liver_disease", 0)
        ])
        
        if comorbidity_count >= 3:
            factors.append("Multiple comorbidities significantly increasing surgical risk")
        
        # Preoperative status
        if data.get("preop_hemoglobin", 0) < 10:
            factors.append("Low preoperative hemoglobin indicating anemia")
        
        if data.get("preop_albumin", 0) < 3.0:
            factors.append("Low albumin indicating poor nutritional status")
        
        # Lifestyle factors
        if data.get("smoking_status", 0) == 2:
            factors.append("Current smoking significantly impairing wound healing")
        
        if data.get("functional_status", 0) >= 2:
            factors.append("Poor functional status affecting recovery")
        
        # Surgical factors
        if data.get("blood_loss", 0) > 500:
            factors.append("Significant blood loss during surgery")
        
        if data.get("wound_class", 0) >= 3:
            factors.append("Contaminated or dirty wound increasing infection risk")
        
        return factors
    
    def analyze_health_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze key health metrics for post-surgery assessment"""
        analysis = {
            "surgical_risk": "moderate",
            "recovery_outlook": "good",
            "complication_factors": [],
            "monitoring_priorities": []
        }
        
        # Risk stratification
        risk_score = 0
        if data.get("asa_score", 0) >= 3:
            risk_score += 2
        if data.get("emergency_surgery", 0) == 1:
            risk_score += 2
        if data.get("age", 0) > 65:
            risk_score += 1
        if data.get("bmi", 0) > 30:
            risk_score += 1
        
        if risk_score >= 4:
            analysis["surgical_risk"] = "high"
            analysis["recovery_outlook"] = "guarded"
        elif risk_score >= 2:
            analysis["surgical_risk"] = "moderate-high"
        
        # Complication risk factors
        if data.get("diabetes", 0) == 1:
            analysis["complication_factors"].append("Diabetes - wound healing concerns")
            analysis["monitoring_priorities"].append("Blood glucose control")
        
        if data.get("smoking_status", 0) >= 1:
            analysis["complication_factors"].append("Smoking history - impaired healing")
        
        if data.get("preop_albumin", 0) < 3.5:
            analysis["complication_factors"].append("Poor nutritional status")
            analysis["monitoring_priorities"].append("Nutritional support")
        
        # Monitoring priorities
        if data.get("heart_disease", 0) == 1:
            analysis["monitoring_priorities"].append("Cardiac monitoring")
        
        if data.get("kidney_disease", 0) == 1:
            analysis["monitoring_priorities"].append("Renal function")
        
        return analysis
    
    def assess_lifestyle_impact(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Assess lifestyle factors affecting post-surgery recovery"""
        recommendations = {}
        
        # Smoking cessation
        if data.get("smoking_status", 0) >= 1:
            recommendations["smoking"] = "Complete smoking cessation is crucial for optimal wound healing and reduced complications"
        
        # Nutrition
        if data.get("preop_albumin", 0) < 3.5 or data.get("bmi", 0) > 30:
            recommendations["nutrition"] = "Focus on balanced nutrition with adequate protein for healing and weight management"
        
        # Activity and mobility
        recommendations["mobility"] = "Early mobilization as tolerated to prevent complications like blood clots and pneumonia"
        
        # Diabetes management
        if data.get("diabetes", 0) == 1:
            recommendations["diabetes_care"] = "Strict blood sugar control is essential for proper wound healing"
        
        # Pain management
        recommendations["pain_management"] = "Effective pain control to enable mobility and prevent complications"
        
        # Follow-up care
        recommendations["follow_up"] = "Attend all scheduled follow-up appointments for wound monitoring and complication detection"
        
        # Infection prevention
        recommendations["infection_prevention"] = "Follow wound care instructions carefully and watch for signs of infection"
        
        return recommendations

class PregnancyComplicationPredictor(BasePredictor):
    """Predicts pregnancy complications like gestational diabetes and preeclampsia"""
    
    def __init__(self):
        super().__init__(
            name="Pregnancy Complication Predictor",
            description="Predicts pregnancy complications including gestational diabetes and preeclampsia"
        )
    
    def get_required_fields(self) -> Dict[str, str]:
        return {
            "maternal_age": "int",
            "gestational_age": "int",  # weeks
            "pre_pregnancy_bmi": "float",
            "weight_gain": "float",  # kg gained so far
            "systolic_bp": "float",
            "diastolic_bp": "float",
            "proteinuria": "int",  # 0 = none, 1 = trace, 2 = 1+, 3 = 2+, 4 = 3+
            "glucose_tolerance_test": "float",  # mg/dL
            "hemoglobin": "float",
            "platelet_count": "float",
            "creatinine": "float",
            "uric_acid": "float",
            "previous_pregnancies": "int",
            "previous_complications": "int",  # 1 = yes, 0 = no
            "family_history_diabetes": "int",  # 1 = yes, 0 = no
            "family_history_hypertension": "int",  # 1 = yes, 0 = no
            "smoking": "int",  # 1 = yes, 0 = no
            "alcohol_use": "int",  # 1 = yes, 0 = no
            "multiple_pregnancy": "int",  # 1 = twins/multiples, 0 = singleton
            "assisted_reproduction": "int",  # 1 = yes, 0 = no
            "chronic_hypertension": "int",  # 1 = yes, 0 = no
            "diabetes_pre_pregnancy": "int",  # 1 = yes, 0 = no
            "kidney_disease": "int",  # 1 = yes, 0 = no
            "autoimmune_disease": "int",  # 1 = yes, 0 = no
            "fetal_growth_restriction": "int"  # 1 = yes, 0 = no
        }
    
    def get_field_descriptions(self) -> Dict[str, str]:
        return {
            "maternal_age": "Maternal age in years",
            "gestational_age": "Current gestational age in weeks",
            "pre_pregnancy_bmi": "Pre-pregnancy Body Mass Index",
            "weight_gain": "Weight gain during pregnancy so far (kg)",
            "systolic_bp": "Systolic blood pressure (mmHg)",
            "diastolic_bp": "Diastolic blood pressure (mmHg)",
            "proteinuria": "Proteinuria level (0 = None, 1 = Trace, 2 = 1+, 3 = 2+, 4 = 3+)",
            "glucose_tolerance_test": "Glucose tolerance test result (mg/dL)",
            "hemoglobin": "Hemoglobin level (g/dL)",
            "platelet_count": "Platelet count (K/uL)",
            "creatinine": "Serum creatinine (mg/dL)",
            "uric_acid": "Uric acid level (mg/dL)",
            "previous_pregnancies": "Number of previous pregnancies",
            "previous_complications": "Previous pregnancy complications (1 = Yes, 0 = No)",
            "family_history_diabetes": "Family history of diabetes (1 = Yes, 0 = No)",
            "family_history_hypertension": "Family history of hypertension (1 = Yes, 0 = No)",
            "smoking": "Smoking during pregnancy (1 = Yes, 0 = No)",
            "alcohol_use": "Alcohol use during pregnancy (1 = Yes, 0 = No)",
            "multiple_pregnancy": "Multiple pregnancy (1 = Twins/multiples, 0 = Singleton)",
            "assisted_reproduction": "Assisted reproductive technology (1 = Yes, 0 = No)",
            "chronic_hypertension": "Pre-existing chronic hypertension (1 = Yes, 0 = No)",
            "diabetes_pre_pregnancy": "Pre-existing diabetes (1 = Yes, 0 = No)",
            "kidney_disease": "Pre-existing kidney disease (1 = Yes, 0 = No)",
            "autoimmune_disease": "Autoimmune disease (1 = Yes, 0 = No)",
            "fetal_growth_restriction": "Fetal growth restriction detected (1 = Yes, 0 = No)"
        }
    
    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        features = [
            data["maternal_age"] / 50.0,
            data["gestational_age"] / 42.0,
            data["pre_pregnancy_bmi"] / 50.0,
            data["weight_gain"] / 30.0,
            data["systolic_bp"] / 200.0,
            data["diastolic_bp"] / 120.0,
            data["proteinuria"] / 4.0,
            data["glucose_tolerance_test"] / 300.0,
            data["hemoglobin"] / 20.0,
            data["platelet_count"] / 1000.0,
            data["creatinine"] / 5.0,
            data["uric_acid"] / 15.0,
            data["previous_pregnancies"] / 10.0,
            data["previous_complications"],
            data["family_history_diabetes"],
            data["family_history_hypertension"],
            data["smoking"],
            data["alcohol_use"],
            data["multiple_pregnancy"],
            data["assisted_reproduction"],
            data["chronic_hypertension"],
            data["diabetes_pre_pregnancy"],
            data["kidney_disease"],
            data["autoimmune_disease"],
            data["fetal_growth_restriction"]
        ]
        return np.array(features)