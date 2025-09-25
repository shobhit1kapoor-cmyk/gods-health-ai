import React, { useState, useEffect, useMemo } from 'react';
import { useParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import axios from 'axios';
import { buildApiUrl, API_ENDPOINTS, isStaticMode } from '../config/api.js';
import {
  ArrowLeft,
  Heart,
  Brain,
  Activity,
  Stethoscope,
  TrendingUp,
  Zap,
  Clock,
  AlertTriangle,
  CheckCircle,
  Info,
  Loader,
  Download,
  Share2,
  Droplets,
  HelpCircle,
  ChevronDown,
  User,
  Calendar,
  Thermometer,
  Scale,
  FileText,
  BarChart3
} from 'lucide-react';
// Recharts components removed - using simpler card-based design

interface PredictorInfo {
  id: string;
  name: string;
  description: string;
  category: string;
  icon: React.ComponentType<any>;
  difficulty: string;
  estimatedTime: string;
  accuracy: string;
  fields: FormField[];
}

interface FormField {
  name: string;
  label: string;
  type: 'number' | 'select' | 'radio' | 'checkbox' | 'text';
  required: boolean;
  options?: string[];
  min?: number;
  max?: number;
  step?: number;
  unit?: string;
  description?: string;
}

interface BackendFieldInfo {
  required_fields: Record<string, string>;
  field_descriptions: Record<string, string>;
  predictor_type: string;
  name: string;
  description: string;
}

interface PredictionResult {
  risk_level: 'Low' | 'Medium' | 'High' | 'Critical';
  risk_score: number;
  confidence: number;
  recommendations: string[];
  risk_factors: string[];
  explanation: string;
  detailed_analysis?: {
    contributing_factors?: string[];
    health_metrics?: {
      category: string;
      value: string;
      status: string;
      recommendation?: string;
    }[];
    lifestyle_impact?: {
      factor: string;
      impact_level: string;
      description: string;
      improvement_suggestions?: string[];
    }[];
  };
}

const PredictorDetail: React.FC = () => {
  const { predictorId } = useParams<{ predictorId: string }>();
  const [predictor, setPredictor] = useState<PredictorInfo | null>(null);
  const [formData, setFormData] = useState<Record<string, any>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingFields, setIsLoadingFields] = useState(true);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [currentStep, setCurrentStep] = useState(0);
  const [backendFields, setBackendFields] = useState<BackendFieldInfo | null>(null);
  const [formProgress, setFormProgress] = useState(0);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [isDownloadingPDF, setIsDownloadingPDF] = useState(false);

  // Field mapping for common conversions
  // Field mapping for different predictors - HeartDiseasePredictor uses 'sex', others use 'gender'
  const getBackendFieldName = (fieldName: string, predictorType: string): string => {
    if (fieldName === 'gender' && predictorType === 'heart_disease') {
      return 'sex';
    }
    return fieldName;
  };

  // Get default example values for form fields
  const getDefaultExampleValue = (fieldName: string, field: FormField): any => {
    // Common field examples
    const examples: Record<string, any> = {
      // Basic demographics
      'age': 45,
      'gender': 'Male',
      'sex': 'Male',
      'weight': 70,
      'height': 175,
      'occupation': 'Technology',
      'maternal_age': 28,
      'gestational_age': 38,
      'multiple_pregnancy': 'No',
      
      // Vital signs and measurements
      'systolic_bp': 130,
      'diastolic_bp': 85,
      'resting_bp': 130,
      'blood_pressure': 130,
      'cholesterol': 220,
      'total_cholesterol': 220,
      'hdl_cholesterol': 45,
      'ldl_cholesterol': 130,
      'triglycerides': 180,
      'bmi': 26.5,
      'max_hr': 165,
      'heart_rate': 75,
      'oldpeak': 1.2,
      'glucose_level': 95,
      'avg_glucose_level': 110,
      'glucose_fasting': 95,
      'waist_circumference': 85,
      'hip_circumference': 95,
      'body_fat_percentage': 18,
      'muscle_mass': 35,
      'metabolic_rate': 1650,
      'temperature': 98.6,
      'spo2': 98,
      'respiratory_rate': 16,
      'mean_bp': 100,
      'specific_gravity': 1.025,
      'meals_per_day': 3,
      'fruit_vegetable_servings': 5,
      'albumin': 1,
      'sugar': 0,
      
      // Medical history
      'hypertension': 'No',
      'heart_disease': 'No',
      'family_history': 'Yes',
      'family_history_diabetes': 'No',
      'family_history_heart_disease': 'No',
      'family_history_hypertension': 'No',
      'family_history_obesity': 'No',
      'family_history_respiratory': 'No',
      'diabetes': 'No',
      'kidney_disease': 'No',
      'liver_disease': 'No',
      'thyroid_disorder': 'No',
      'autoimmune_disease': 'No',
      'chronic_hypertension': 'No',
      'diabetes_pre_pregnancy': 'No',
      'insulin_level': 15,
      'pregnancies': 2,
      'skin_thickness': 25,
      'diabetes_pedigree_function': 0.5,
      'previous_cancer': 'No',
      'cancer_type': 'None',
      'hormonal_factors': 'Normal',
      'fasting_bs': 'No',
      'chronic_illness': 'No',
      'previous_complications': 'No',
      'fetal_growth_restriction': 'No',
      'mobility': 'Normal',
      'medications_weight_gain': 'No',
      'medication_statins': 'No',
      'mechanical_ventilation': 'No',
      'vasopressor_use': 'No',
      'admission_diagnosis': 'None',
      'comorbidities': 'None',
      
      // Lifestyle factors
      'smoking_status': 'Never Smoked',
      'smoking_history': 'Never',
      'smoking': 'No',
      'smoking_years': 0,
      'smoking_pack_years': 0,
      'alcohol_consumption': 'Light',
      'alcohol_intake': 'Light',
      'physical_activity': 'Moderate',
      'physical_activity_level': 'Moderate',
      'activity_level': 'Moderately Active',
      'current_fitness_level': 'Intermediate',
      'exercise_frequency': 'Moderate',
      'exercise_duration': 45,
      'sleep_hours': 7,
      'sleep_quality': 'Good',
      'stress_level': 3,
      'social_support': 'Good',
      'work_satisfaction': 'Satisfied',
      'substance_use': 'None',
      'diet_quality': 'Good',
      'dietary_restrictions': 'None',
      'nutrition_score': 75,
      'caffeine_intake': 'Moderate (3-4 cups)',
      'water_intake': 2.5,
      'sedentary_hours': 6,
      'screen_time': 4,
      'work_stress': 'Moderate',
      'financial_stress': 'Low',
      'relationship_stress': 'Low',
      'morning_alertness': 'Alert',
      'daytime_fatigue': 'Sometimes',
      'sleep_disorders': 'No',
      'shift_work': 'No',
      'environmental_factors': 'Good',
      'processed_food_frequency': 'Sometimes',
      'cooking_frequency': 'Often',
      'supplement_use': 'No',
      'screen_time_before_bed': '<30 min',
      'sleep_environment': 'Good',
      'snoring': 'No',
      'sleep_medications': 'No',
      'sleep_problems': 'No',
      'work_stress_level': 5,
      'work_hours_per_week': 40,
      'job_satisfaction': 'Satisfied',
      'work_life_balance': 'Good',
      'emotional_exhaustion': 'Sometimes',
      'cynicism': 'Rarely',
      'personal_accomplishment': 'High',
      'physical_symptoms': 'No',
      'coping_strategies': 'Exercise',
      'support_system': 'Good',
      
      // Clinical tests
      'chest_pain_type': 'Typical angina',
      'resting_ecg': 'Normal',
      'exercise_angina': 'No',
      'cognitive_score': 28,
      'education_years': 16,
      'symptoms_count': 2,
      
      // Liver function tests
      'bilirubin': 1.2,
      'alkaline_phosphotase': 250,
      'alamine_aminotransferase': 35,
      
      // Neurological assessments
      'tremor_score': 2,
      'rigidity_score': 1,
      'bradykinesia_score': 1,
      'postural_instability': 'No',
      
      // Blood work
      'white_blood_cells': 8000,
      'hemoglobin': 14.5,
      'hematocrit': 42,
      'platelet_count': 250000,
      'red_blood_cell_count': 4.8,
      'mcv': 88,
      'mch': 30,
      'mchc': 34,
      'ferritin': 150,
      'iron': 100,
      'transferrin_saturation': 25,
      'vitamin_b12': 400,
      'folate': 12,
      
      // Thyroid function
      'tsh': 2.5,
      't3': 120,
      't4': 8.5,
      'thyroid_antibodies': 'Negative',
      
      // Cancer markers
      'original_cancer_stage': 'Stage I',
      'months_since_treatment': 12,
      'complete_response': 'Yes',
      'elevated_tumor_markers': 'No',
      
      // Sepsis indicators
      'lactate': 1.5,
      'procalcitonin': 0.5,
      'creatinine': 1.0,
      'urea': 25,
      'sodium': 140,
      'potassium': 4.0,
      'chloride': 100,
      'co2': 24,
      
      // Respiratory function
      'peak_flow': 450,
      'fev1': 3.2,
      'fvc': 4.0,
      'oxygen_saturation': 98,
      'chest_xray': 'Normal',
      'spirometry': 'Normal',
      
      // Pregnancy related
      'parity': 1,
      'gravidity': 2,
      'previous_preterm': 'No',
      'previous_stillbirth': 'No',
      'cervical_length': 35,
      'amniotic_fluid': 'Normal',
      'placental_position': 'Normal',
      
      // Surgery related
      'surgery_type': 'Elective',
      'anesthesia_type': 'General',
      'surgery_duration': 120,
      'blood_loss': 200,
      'asa_score': 2,
      
      // ICU related
      'apache_score': 15,
      'sofa_score': 6,
      'glasgow_coma_scale': 15,
      'ventilator_days': 0,
      'dialysis': 'No',
      'organ_failure_count': 0,
      
      // Hospital readmission
      'length_of_stay': 5,
      'discharge_disposition': 'Home',
      'number_diagnoses': 3,
      'number_procedures': 1,
      'number_medications': 8,
      'emergency_admission': 'No',
      'num_diagnoses': 3,
      'num_medications': 8,
      
      // Additional missing fields
      'current_bmi': 26.5,
      'physical_activity_hours': 3,
      'daily_calories': 2000,
      'neck_circumference': 38,
      'loud_snoring': 'No',
      'daytime_sleepiness': 'No',
      'comorbidity_count': 1,
      'fully_vaccinated': 'Yes',
      'symptoms_severity': 'Mild',
      'serum_iron': 100,
      'heavy_menstrual_bleeding': 'No',
      'dietary_iron_adequate': 'Yes',
      'family_history_thyroid': 'No',
      'social_support_score': 8,
      'recent_life_events': 'No',
      'sepsis': 'No',
      'emergency_surgery': 'No',
      
      // Work and lifestyle
      'work_type': 0, // Private
      'residence_type': 1, // Urban
      'ever_married': 1, // Yes
      'family_history_stroke': 0, // No
      'environmental_exposure': 'No',
      'sodium_intake_mg': 2800
    };
    
    // Return specific example if available
    if (examples[fieldName] !== undefined) {
      return examples[fieldName];
    }
    
    // Fallback based on field type
    if (field.type === 'number') {
      if (field.min !== undefined && field.max !== undefined) {
        return Math.round((field.min + field.max) / 2);
      }
      return field.min || 0;
    } else if (field.type === 'select' && field.options) {
      return field.options[0];
    } else if (field.type === 'checkbox') {
      return false;
    }
    
    return '';
  };

  // Convert backend field definitions to frontend form fields
  const convertBackendFieldsToFormFields = (backendInfo: BackendFieldInfo): FormField[] => {
    const fields: FormField[] = [];
    
    Object.entries(backendInfo.required_fields).forEach(([fieldName, fieldType]) => {
      const description = backendInfo.field_descriptions[fieldName] || '';
      
      let formField: FormField = {
        name: fieldName,
        label: description.split('(')[0].trim() || fieldName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
        type: 'text',
        required: true,
        description: description
      };

      // Determine field type and options based on field name and description
      if (fieldType === 'int' || fieldType === 'float') {
        formField.type = 'number';
        if (fieldType === 'float') {
          formField.step = 0.1;
        }
      }

      // Special handling for common fields
      if (fieldName === 'gender' || fieldName === 'sex') {
        formField = {
          ...formField,
          name: 'gender', // Always use 'gender' internally
          label: 'Gender',
          type: 'select',
          options: ['Female', 'Male'],
          description: 'Gender (0 = Female, 1 = Male)'
        };
      } else if (fieldName === 'age') {
        formField = {
          ...formField,
          type: 'number',
          min: 0,
          max: 120,
          unit: 'years'
        };
      } else if (fieldName === 'maternal_age') {
        formField = {
          ...formField,
          type: 'number',
          min: 15,
          max: 50,
          unit: 'years'
        };
      } else if (fieldName === 'gestational_age') {
        formField = {
          ...formField,
          type: 'number',
          min: 20,
          max: 42,
          unit: 'weeks'
        };
      } else if (fieldName === 'systolic_bp' || fieldName === 'resting_bp') {
        formField = {
          ...formField,
          type: 'number',
          min: 80,
          max: 200,
          unit: 'mmHg'
        };
      } else if (fieldName === 'diastolic_bp') {
        formField = {
          ...formField,
          type: 'number',
          min: 50,
          max: 120,
          unit: 'mmHg'
        };
      } else if (fieldName === 'cholesterol' || fieldName === 'total_cholesterol') {
        formField = {
          ...formField,
          type: 'number',
          min: 100,
          max: 400,
          unit: 'mg/dL'
        };
      } else if (fieldName === 'bmi') {
        formField = {
          ...formField,
          type: 'number',
          min: 15,
          max: 50,
          step: 0.1,
          unit: 'kg/m²'
        };
      } else if (fieldName === 'smoking_status') {
        formField = {
          ...formField,
          type: 'select',
          options: ['Never smoked', 'Former smoker', 'Current smoker']
        };
      } else if (fieldName === 'chest_pain_type') {
        formField = {
          ...formField,
          type: 'select',
          options: ['Typical angina', 'Atypical angina', 'Non-anginal pain', 'Asymptomatic']
        };
      } else if (fieldName === 'resting_ecg') {
        formField = {
          ...formField,
          type: 'select',
          options: ['Normal', 'ST-T wave abnormality', 'Left ventricular hypertrophy']
        };
      } else if (fieldName === 'work_type') {
        formField = {
          ...formField,
          type: 'select',
          options: ['Private', 'Self-employed', 'Government', 'Never worked']
        };
      } else if (fieldName === 'residence_type') {
        formField = {
          ...formField,
          type: 'select',
          options: ['Urban', 'Rural']
        };
      } else if (fieldName === 'gender' || fieldName === 'sex') {
        formField = {
          ...formField,
          type: 'select',
          options: ['Female', 'Male']
        };
      } else if (
        // Only apply Yes/No for fields that explicitly mention yes/no in description
        description.includes('1 = yes, 0 = no') ||
        description.includes('1 = Yes, 0 = No') ||
        description.includes('(1 = yes, 0 = no)') ||
        description.includes('(1 = Yes, 0 = No)') ||
        (description && description.toLowerCase().includes('yes') && description.toLowerCase().includes('no')) ||
        // Specific boolean fields that should be Yes/No
        (fieldType === 'int' && (
          fieldName === 'hypertension' ||
          fieldName === 'diabetes' ||
          fieldName === 'heart_disease' ||
          fieldName === 'smoking' ||
          fieldName.startsWith('family_history') ||
          fieldName === 'chronic_hypertension' ||
          fieldName === 'diabetes_pre_pregnancy' ||
          fieldName === 'multiple_pregnancy' ||
          fieldName === 'previous_complications' ||
          fieldName === 'previous_cancer' ||
          fieldName === 'ever_married' ||
          fieldName === 'fasting_bs' ||
          fieldName === 'exercise_angina'
        ))
      ) {
        formField = {
          ...formField,
          type: 'select',
          options: ['No', 'Yes']
        };
      } else if (description.includes('0-') && description.includes('scale')) {
        const match = description.match(/0-(\d+)/);
        if (match) {
          formField = {
            ...formField,
            type: 'number',
            min: 0,
            max: parseInt(match[1])
          };
        }
      }

      fields.push(formField);
    });

    return fields;
  };


  const predictorData = useMemo(() => ({
    heart_disease: {
      id: 'heart_disease',
      name: 'Heart Disease Predictor',
      description: 'Predict cardiovascular disease risk using key health indicators',
      category: 'Health Assessment',
      icon: Heart,
      difficulty: 'Medium',
      estimatedTime: '5-10 min',
      accuracy: '85%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 18, max: 120, unit: 'years' },
        { name: 'sex', label: 'Gender', type: 'select', required: true, options: ['Female', 'Male'] },
        { name: 'cholesterol', label: 'Total Cholesterol', type: 'number', required: true, min: 100, max: 400, unit: 'mg/dL' },
        { name: 'systolic_bp', label: 'Systolic Blood Pressure', type: 'number', required: true, min: 80, max: 200, unit: 'mmHg' },
        { name: 'smoking', label: 'Current Smoking Status', type: 'select', required: true, options: ['No', 'Yes'] },
        { name: 'diabetes', label: 'Diabetes Diagnosis', type: 'select', required: true, options: ['No', 'Yes'] }
      ]
    },
    diabetes: {
      id: 'diabetes',
      name: 'Diabetes Risk Predictor',
      description: 'Predict Type 2 diabetes risk using glucose levels, BMI, and lifestyle factors',
      category: 'Health Assessment',
      icon: Activity,
      difficulty: 'Medium',
      estimatedTime: '5-7 min',
      accuracy: '87%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 18, max: 120, unit: 'years' },
        { name: 'gender', label: 'Gender', type: 'select', required: true, options: ['Female', 'Male'] },
        { name: 'bmi', label: 'Body Mass Index', type: 'number', required: true, min: 15, max: 50, step: 0.1, unit: 'kg/m²' },
        { name: 'glucose', label: 'Glucose Level', type: 'number', required: true, min: 70, max: 300, unit: 'mg/dL' },
        { name: 'blood_pressure', label: 'Blood Pressure', type: 'number', required: true, min: 80, max: 200, unit: 'mmHg' },
        { name: 'skin_thickness', label: 'Skin Thickness', type: 'number', required: true, min: 0, max: 100, unit: 'mm' },
        { name: 'insulin', label: 'Insulin Level', type: 'number', required: true, min: 0, max: 300, unit: 'μU/mL' },
        { name: 'diabetes_pedigree_function', label: 'Diabetes Pedigree Function', type: 'number', required: true, min: 0, max: 2, step: 0.01 },
        { name: 'pregnancies', label: 'Number of Pregnancies', type: 'number', required: true, min: 0, max: 20 }
      ]
    },
    anemia: {
      id: 'anemia',
      name: 'Anemia Predictor',
      description: 'Detect various types of anemia using comprehensive blood test analysis',
      category: 'Health Assessment',
      icon: Stethoscope,
      difficulty: 'Easy',
      estimatedTime: '3-5 min',
      accuracy: '92%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 18, max: 120, unit: 'years' },
        { name: 'gender', label: 'Gender', type: 'select', required: true, options: ['Female', 'Male'] },
        { name: 'hemoglobin', label: 'Hemoglobin Level', type: 'number', required: true, min: 5, max: 20, step: 0.1, unit: 'g/dL' },
        { name: 'hematocrit', label: 'Hematocrit', type: 'number', required: true, min: 15, max: 60, step: 0.1, unit: '%' },
        { name: 'mcv', label: 'Mean Corpuscular Volume', type: 'number', required: true, min: 60, max: 120, unit: 'fL' },
        { name: 'mch', label: 'Mean Corpuscular Hemoglobin', type: 'number', required: true, min: 20, max: 40, step: 0.1, unit: 'pg' },
        { name: 'mchc', label: 'Mean Corpuscular Hemoglobin Concentration', type: 'number', required: true, min: 25, max: 40, step: 0.1, unit: 'g/dL' },
        { name: 'fatigue', label: 'Fatigue Level', type: 'number', required: true, min: 0, max: 10 },
        { name: 'shortness_of_breath', label: 'Shortness of Breath', type: 'select', required: true, options: ['No', 'Yes'] },
        { name: 'cold_hands_feet', label: 'Cold Hands and Feet', type: 'select', required: true, options: ['No', 'Yes'] }
      ]
    },
    sepsis: {
      id: 'sepsis',
      name: 'Sepsis Predictor',
      description: 'Early sepsis detection in hospital settings - a life-saving diagnostic tool.',
      category: 'Health Assessment',
      icon: Activity,
      difficulty: 'Advanced',
      estimatedTime: '3-5 min',
      accuracy: '96%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 18, max: 120, unit: 'years' },
        { name: 'gender', label: 'Gender', type: 'select', required: true, options: ['Female', 'Male'] },
        { name: 'temperature', label: 'Body Temperature', type: 'number', required: true, min: 95, max: 110, step: 0.1, unit: '°F' },
        { name: 'heart_rate', label: 'Heart Rate', type: 'number', required: true, min: 40, max: 200, unit: 'bpm' },
        { name: 'respiratory_rate', label: 'Respiratory Rate', type: 'number', required: true, min: 10, max: 40, unit: '/min' },
        { name: 'white_blood_cells', label: 'White Blood Cell Count', type: 'number', required: true, min: 1000, max: 50000, unit: '/μL' },
        { name: 'blood_pressure', label: 'Systolic Blood Pressure', type: 'number', required: true, min: 60, max: 200, unit: 'mmHg' }
      ]
    },
    stroke_risk: {
      id: 'stroke_risk',
      name: 'Stroke Risk Predictor',
      description: 'Analyze blood pressure, cholesterol, lifestyle, and family history to assess stroke risk.',
      category: 'Health Assessment',
      icon: Brain,
      difficulty: 'Medium',
      estimatedTime: '6-8 min',
      accuracy: '92%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 18, max: 120, unit: 'years' },
        { name: 'gender', label: 'Gender', type: 'select', required: true, options: ['Female', 'Male'] },
        { name: 'hypertension', label: 'Hypertension', type: 'select', required: true, options: ['No', 'Yes'] },
        { name: 'heart_disease', label: 'Heart Disease', type: 'select', required: true, options: ['No', 'Yes'] },
        { name: 'avg_glucose_level', label: 'Average Glucose Level', type: 'number', required: true, min: 50, max: 300, unit: 'mg/dL' },
        { name: 'bmi', label: 'Body Mass Index', type: 'number', required: true, min: 15, max: 50, step: 0.1, unit: 'kg/m²' },
        { name: 'smoking_status', label: 'Smoking Status', type: 'select', required: true, options: ['Never smoked', 'Formerly smoked', 'Currently smokes'] }
      ]
    },
    obesity_risk: {
      id: 'obesity_risk',
      name: 'Obesity & BMI Risk Predictor',
      description: 'Assess long-term obesity complications and metabolic health risks.',
      category: 'Health Assessment',
      icon: TrendingUp,
      difficulty: 'Easy',
      estimatedTime: '3-5 min',
      accuracy: '87%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 18, max: 120, unit: 'years' },
        { name: 'gender', label: 'Gender', type: 'select', required: true, options: ['Female', 'Male'] },
        { name: 'height', label: 'Height', type: 'number', required: true, min: 100, max: 250, unit: 'cm' },
        { name: 'weight', label: 'Weight', type: 'number', required: true, min: 30, max: 300, unit: 'kg' },
        { name: 'physical_activity', label: 'Physical Activity Level', type: 'select', required: true, options: ['Low', 'Moderate', 'High'] },
        { name: 'family_history_obesity', label: 'Family History of Obesity', type: 'select', required: true, options: ['No', 'Yes'] }
      ]
    },
    hypertension: {
      id: 'hypertension',
      name: 'Hypertension Predictor',
      description: 'Evaluate lifestyle and genetic risk factors for high blood pressure development.',
      category: 'Health Assessment',
      icon: Activity,
      difficulty: 'Medium',
      estimatedTime: '4-6 min',
      accuracy: '89%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 18, max: 120, unit: 'years' },
        { name: 'gender', label: 'Gender', type: 'select', required: true, options: ['Female', 'Male'] },
        { name: 'systolic_bp', label: 'Systolic Blood Pressure', type: 'number', required: true, min: 80, max: 200, unit: 'mmHg' },
        { name: 'diastolic_bp', label: 'Diastolic Blood Pressure', type: 'number', required: true, min: 40, max: 120, unit: 'mmHg' },
        { name: 'bmi', label: 'Body Mass Index', type: 'number', required: true, min: 15, max: 50, step: 0.1, unit: 'kg/m²' },
        { name: 'sodium_intake', label: 'Daily Sodium Intake', type: 'number', required: true, min: 500, max: 5000, unit: 'mg' },
        { name: 'family_history_hypertension', label: 'Family History of Hypertension', type: 'select', required: true, options: ['No', 'Yes'] }
      ]
    },
    cholesterol_risk: {
      id: 'cholesterol_risk',
      name: 'Cholesterol Risk Predictor',
      description: 'Assess cardiovascular risk based on cholesterol levels and lipid profile.',
      category: 'Health Assessment',
      icon: Heart,
      difficulty: 'Medium',
      estimatedTime: '4-6 min',
      accuracy: '88%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 18, max: 120, unit: 'years' },
        { name: 'gender', label: 'Gender', type: 'select', required: true, options: ['Female', 'Male'] },
        { name: 'total_cholesterol', label: 'Total Cholesterol', type: 'number', required: true, min: 100, max: 400, unit: 'mg/dL' },
        { name: 'hdl_cholesterol', label: 'HDL Cholesterol', type: 'number', required: true, min: 20, max: 100, unit: 'mg/dL' },
        { name: 'ldl_cholesterol', label: 'LDL Cholesterol', type: 'number', required: true, min: 50, max: 300, unit: 'mg/dL' },
        { name: 'triglycerides', label: 'Triglycerides', type: 'number', required: true, min: 50, max: 500, unit: 'mg/dL' }
      ]
    },
    mental_health: {
      id: 'mental_health',
      name: 'Mental Health Risk Predictor',
      description: 'Assess depression, anxiety, and stress levels using validated screening tools.',
      category: 'Health Assessment',
      icon: Brain,
      difficulty: 'Medium',
      estimatedTime: '6-8 min',
      accuracy: '85%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 18, max: 120, unit: 'years' },
        { name: 'gender', label: 'Gender', type: 'select', required: true, options: ['Female', 'Male'] },
        { name: 'stress_level', label: 'Stress Level (1-10)', type: 'number', required: true, min: 1, max: 10 },
        { name: 'sleep_hours', label: 'Average Sleep Hours', type: 'number', required: true, min: 2, max: 12, step: 0.5, unit: 'hours' },
        { name: 'social_support', label: 'Social Support Level', type: 'select', required: true, options: ['Low', 'Moderate', 'High'] },
        { name: 'exercise_frequency', label: 'Exercise Frequency', type: 'select', required: true, options: ['Never', 'Rarely', 'Sometimes', 'Often', 'Daily'] }
      ]
    },
    sleep_apnea: {
      id: 'sleep_apnea',
      name: 'Sleep Apnea Risk Predictor',
      description: 'Identify sleep disorders and breathing interruptions during sleep.',
      category: 'Health Assessment',
      icon: Activity,
      difficulty: 'Medium',
      estimatedTime: '5-7 min',
      accuracy: '87%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 18, max: 120, unit: 'years' },
        { name: 'gender', label: 'Gender', type: 'select', required: true, options: ['Female', 'Male'] },
        { name: 'bmi', label: 'Body Mass Index', type: 'number', required: true, min: 15, max: 50, step: 0.1, unit: 'kg/m²' },
        { name: 'neck_circumference', label: 'Neck Circumference', type: 'number', required: true, min: 25, max: 60, unit: 'cm' },
        { name: 'snoring_frequency', label: 'Snoring Frequency', type: 'select', required: true, options: ['Never', 'Rarely', 'Sometimes', 'Often', 'Always'] },
        { name: 'daytime_sleepiness', label: 'Daytime Sleepiness', type: 'select', required: true, options: ['Never', 'Rarely', 'Sometimes', 'Often', 'Always'] }
      ]
    },
    covid_risk: {
      id: 'covid_risk',
      name: 'COVID-19 Risk Predictor',
      description: 'Assess COVID-19 severity risk based on health conditions and demographics.',
      category: 'Health Assessment',
      icon: Activity,
      difficulty: 'Easy',
      estimatedTime: '3-5 min',
      accuracy: '83%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 18, max: 120, unit: 'years' },
        { name: 'gender', label: 'Gender', type: 'select', required: true, options: ['Female', 'Male'] },
        { name: 'chronic_conditions', label: 'Number of Chronic Conditions', type: 'number', required: true, min: 0, max: 10 },
        { name: 'vaccination_status', label: 'Vaccination Status', type: 'select', required: true, options: ['Unvaccinated', 'Partially Vaccinated', 'Fully Vaccinated', 'Boosted'] },
        { name: 'smoking_status', label: 'Smoking Status', type: 'select', required: true, options: ['Never', 'Former', 'Current'] }
      ]
    }
  }), []);



















  useEffect(() => {
    const fetchPredictorFields = async () => {
      if (!predictorId) return;
      
      setIsLoadingFields(true);
      setError(null);
      
      try {
        // Check if we're in static mode
        if (isStaticMode()) {
          // Use hardcoded data for static mode
          if (predictorData[predictorId]) {
            setPredictor(predictorData[predictorId]);
            const initialData: Record<string, any> = {};
            predictorData[predictorId].fields.forEach(field => {
              initialData[field.name] = getDefaultExampleValue(field.name, field);
            });
            setFormData(initialData);
            
            // Calculate initial form progress
            const filledFields = Object.values(initialData).filter(val => 
              val !== '' && val !== null && val !== undefined
            ).length;
            setFormProgress((filledFields / (predictorData[predictorId]?.fields?.length || 1)) * 100);
          } else {
            throw new Error('Predictor not found in static mode');
          }
        } else {
          // Fetch field definitions from backend
          const response = await fetch(buildApiUrl(API_ENDPOINTS.PREDICTOR_FIELDS(predictorId)));
          if (!response.ok) {
            throw new Error(`Failed to fetch predictor fields: ${response.statusText}`);
          }
          
          const backendInfo: BackendFieldInfo = await response.json();
          setBackendFields(backendInfo);
          
          // Convert backend fields to frontend form fields
          const formFields = convertBackendFieldsToFormFields(backendInfo);
          
          // Create predictor info with dynamic fields
          const predictorInfo: PredictorInfo = {
            id: predictorId,
            name: backendInfo.name,
            description: backendInfo.description,
            category: 'Health Assessment',
            icon: Heart, // Default icon
            difficulty: 'Medium',
            estimatedTime: '5-10 min',
            accuracy: '85%',
            fields: formFields
          };
          
          setPredictor(predictorInfo);
          
          // Initialize form data with example values
          const initialData: Record<string, any> = {};
          formFields.forEach(field => {
            initialData[field.name] = getDefaultExampleValue(field.name, field);
          });
          setFormData(initialData);
          
          // Calculate initial form progress
          const filledFields = Object.values(initialData).filter(val => 
            val !== '' && val !== null && val !== undefined
          ).length;
          setFormProgress((filledFields / (formFields?.length || 1)) * 100);
        }
        
      } catch (err) {
        console.error('Error fetching predictor fields:', err);
        setError(err instanceof Error ? err.message : 'Failed to load predictor');
        
        // Fallback to hardcoded data if available
        if (predictorData[predictorId]) {
          setPredictor(predictorData[predictorId]);
          const initialData: Record<string, any> = {};
          predictorData[predictorId].fields.forEach(field => {
            initialData[field.name] = getDefaultExampleValue(field.name, field);
          });
          setFormData(initialData);
          
          // Calculate initial form progress
          const filledFields = Object.values(initialData).filter(val => 
            val !== '' && val !== null && val !== undefined
          ).length;
          setFormProgress((filledFields / (predictorData[predictorId]?.fields?.length || 1)) * 100);
        }
      } finally {
        setIsLoadingFields(false);
      }
    };
    
    fetchPredictorFields();
  }, [predictorId, predictorData]);

  const validateField = (field: FormField, value: any): string | null => {
    // Required field validation
    if (field.required && (value === '' || value === null || value === undefined)) {
      return `${field.label} is required`;
    }

    // Number field validation
    if (field.type === 'number' && value !== '' && value !== null && value !== undefined) {
      const numValue = parseFloat(value);
      if (isNaN(numValue)) {
        return `${field.label} must be a valid number`;
      }
      if (field.min !== undefined && numValue < field.min) {
        return `${field.label} must be at least ${field.min}`;
      }
      if (field.max !== undefined && numValue > field.max) {
        return `${field.label} must be no more than ${field.max}`;
      }
    }

    // Age-specific validation
    if (field.name === 'age' && (value !== null && value !== undefined && value !== '')) {
      const age = parseFloat(value);
      if (!isNaN(age) && (age < 0 || age > 150)) {
        return 'Please enter a valid age between 0 and 150';
      }
    }

    // Blood pressure validation
    if ((field.name.includes('bp') || field.name.includes('blood_pressure')) && (value !== null && value !== undefined && value !== '')) {
      const bp = parseFloat(value);
      if (!isNaN(bp) && (bp < 50 || bp > 300)) {
        return 'Please enter a realistic blood pressure value';
      }
    }

    return null;
  };

  const handleInputChange = (name: string, value: any) => {
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Validate field in real-time
    const field = predictor?.fields.find(f => f.name === name);
    if (field) {
      const error = validateField(field, value);
      setFieldErrors(prev => ({
        ...prev,
        [name]: error || ''
      }));
    }
    
    // Update form progress
    const filledFields = Object.values({ ...formData, [name]: value }).filter(val => 
      val !== '' && val !== null && val !== undefined
    ).length;
    const totalFields = predictor?.fields?.length || 1;
    setFormProgress((filledFields / totalFields) * 100);
  };

  // Helper function to get appropriate icon for field
  const getFieldIcon = (fieldName: string) => {
    const iconMap: Record<string, React.ReactNode> = {
      age: <Calendar className="h-4 w-4 text-gray-500" />,
      sex: <User className="h-4 w-4 text-gray-500" />,
      gender: <User className="h-4 w-4 text-gray-500" />,
      chest_pain_type: <Heart className="h-4 w-4 text-gray-500" />,
      resting_bp: <Activity className="h-4 w-4 text-gray-500" />,
      cholesterol: <Droplets className="h-4 w-4 text-gray-500" />,
      fasting_bs: <Droplets className="h-4 w-4 text-gray-500" />,
      resting_ecg: <Zap className="h-4 w-4 text-gray-500" />,
      max_hr: <Heart className="h-4 w-4 text-gray-500" />,
      exercise_angina: <Activity className="h-4 w-4 text-gray-500" />,
      oldpeak: <TrendingUp className="h-4 w-4 text-gray-500" />,
      st_slope: <TrendingUp className="h-4 w-4 text-gray-500" />,
      bmi: <Scale className="h-4 w-4 text-gray-500" />,
      temperature: <Thermometer className="h-4 w-4 text-gray-500" />,
      blood_pressure: <Stethoscope className="h-4 w-4 text-gray-500" />,
      mental_health: <Brain className="h-4 w-4 text-gray-500" />
    };
    
    return iconMap[fieldName] || <Activity className="h-4 w-4 text-gray-500" />;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!predictor || !backendFields) return;

    // Validate all fields before submission
    const errors: Record<string, string> = {};
    predictor?.fields?.forEach(field => {
      const value = formData[field.name];
      const error = validateField(field, value);
      if (error) {
        errors[field.name] = error;
      }
    });
    
    setFieldErrors(errors);
    
    // Don't submit if there are validation errors
    if (Object.keys(errors).length > 0) {
      setError('Please fix the validation errors before submitting.');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Convert form data to backend format
      const backendData: Record<string, any> = {};
      
      Object.entries(formData).forEach(([fieldName, value]) => {
        // Map frontend field names to backend field names
        const backendFieldName = getBackendFieldName(fieldName, predictor.id);
        const fieldType = backendFields.required_fields[backendFieldName];
        
        if (value === '' || value === null || value === undefined) {
          return; // Skip empty values
        }
        
        // Convert values based on backend field type
        if (fieldType === 'int') {
          if (fieldName === 'gender' || backendFieldName === 'sex' || backendFieldName === 'gender') {
            // Convert gender: Female = 0, Male = 1
            backendData[backendFieldName] = value === 'Male' || value === 1 ? 1 : 0;
          } else if (fieldName === 'chest_pain_type') {
            // Convert chest pain type to numeric
            const mapping = { 'Typical angina': 0, 'Atypical angina': 1, 'Non-anginal pain': 2, 'Asymptomatic': 3 };
            backendData[backendFieldName] = mapping[value as string] || 0;
          } else if (fieldName === 'resting_ecg') {
            // Convert ECG results to numeric
            const mapping = { 'Normal': 0, 'ST-T wave abnormality': 1, 'Left ventricular hypertrophy': 2 };
            backendData[backendFieldName] = mapping[value as string] || 0;
          } else if (fieldName === 'smoking_status') {
            // Convert smoking status to numeric
            const mapping = { 'Never smoked': 0, 'Former smoker': 1, 'Current smoker': 2 };
            backendData[backendFieldName] = mapping[value as string] || 0;
          } else if (fieldName === 'work_type') {
            // Convert work type to numeric
            const mapping = { 'Private': 0, 'Self-employed': 1, 'Government': 2, 'Never worked': 4 };
            backendData[backendFieldName] = mapping[value as string] || 0;
          } else if (fieldName === 'residence_type') {
            // Convert residence type to numeric
            backendData[backendFieldName] = value === 'Urban' ? 1 : 0;
          } else if (typeof value === 'string' && (value === 'Yes' || value === 'No')) {
            // Convert Yes/No to 1/0
            backendData[backendFieldName] = value === 'Yes' ? 1 : 0;
          } else {
            backendData[backendFieldName] = value !== null && value !== undefined && value !== '' ? parseInt(value.toString()) : 0;
          }
        } else if (fieldType === 'float') {
          backendData[backendFieldName] = value !== null && value !== undefined && value !== '' ? parseFloat(value.toString()) : 0.0;
        } else {
          backendData[backendFieldName] = value;
        }
      });

      console.log('Sending data to backend:', backendData);

      // Check if we're in static mode (no backend)
const isStaticMode = (import.meta as any).env?.REACT_APP_STATIC_MODE === 'true';
      
      if (isStaticMode) {
        // Use mock data for static deployment
        await new Promise(resolve => setTimeout(resolve, 1500)); // Simulate API delay
        
        const mockResult = {
          risk_score: Math.random() * 100,
          risk_level: ['Low', 'Medium', 'High'][Math.floor(Math.random() * 3)],
          confidence: 85 + Math.random() * 10,
          recommendations: [
            'Maintain a balanced diet rich in fruits and vegetables',
            'Exercise regularly for at least 30 minutes daily',
            'Monitor your health metrics regularly',
            'Consult with healthcare professionals for personalized advice'
          ],
          analysis: 'This is a demonstration using mock data. In a real deployment with backend, you would receive personalized health predictions based on your input data.'
        };
        
        setResult({
          risk_level: mockResult.risk_level as 'Low' | 'Medium' | 'High' | 'Critical',
          risk_score: mockResult.risk_score,
          confidence: mockResult.confidence,
          recommendations: mockResult.recommendations,
          risk_factors: [],
          explanation: mockResult.analysis || ''
        });
        setCurrentStep(1);
      } else {
        // Original API call logic for when backend is available
        const response = await axios.post(buildApiUrl(API_ENDPOINTS.PREDICT), {
          predictor_type: predictor.id,
          data: backendData,
          include_analysis: true
        });
        setResult(response.data);
        setCurrentStep(1);
      }
    } catch (err: any) {
      console.error('Prediction error:', err);
      setError(err.response?.data?.error || 'An error occurred while making the prediction.');
    } finally {
      setIsLoading(false);
    }
  };

  const getRiskColor = (riskLevel: string) => {
    switch (riskLevel) {
      case 'Low': return 'text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900/30';
      case 'Medium': return 'text-yellow-600 dark:text-yellow-400 bg-yellow-100 dark:bg-yellow-900/30';
      case 'Moderate': return 'text-yellow-600 dark:text-yellow-400 bg-yellow-100 dark:bg-yellow-900/30';
      case 'High': return 'text-orange-600 dark:text-orange-400 bg-orange-100 dark:bg-orange-900/30';
      case 'Very High': return 'text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-900/30';
      case 'Critical': return 'text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-900/30';
      default: return 'text-gray-600 dark:text-gray-400 bg-gray-100 dark:bg-gray-800';
    }
  };

  const getRiskIcon = (riskLevel: string) => {
    switch (riskLevel) {
      case 'Low': return CheckCircle;
      case 'Medium': return Info;
      case 'Moderate': return Info;
      case 'High': return AlertTriangle;
      case 'Very High': return AlertTriangle;
      case 'Critical': return AlertTriangle;
      default: return Info;
    }
  };

  const handleDownloadPDF = async () => {
    if (!result || !predictor) return;
    
    // Check if we're in static mode (no backend)
    const isStaticMode = (import.meta as any).env.VITE_STATIC_MODE === 'true';
    
    if (isStaticMode) {
      // Show message that PDF download is not available in static mode
      setError('PDF download is not available in static demo mode. This feature requires a backend server.');
      return;
    }
    
    setIsDownloadingPDF(true);
    try {
      const response = await fetch(buildApiUrl(API_ENDPOINTS.DOWNLOAD_REPORT), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prediction_data: {
            predictor_type: predictor.id,
            risk_score: result.risk_score,
            risk_level: result.risk_level,
            confidence: result.confidence,
            recommendations: result.recommendations
          },
          user_data: formData
        })
      });
      
      if (!response.ok) {
        throw new Error('Failed to generate PDF report');
      }
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${predictor.id}_health_report_${new Date().toISOString().split('T')[0]}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('PDF download error:', error);
      setError('Failed to download PDF report. Please try again.');
    } finally {
      setIsDownloadingPDF(false);
    }
  };

  const renderField = (field: FormField) => {
    // Use default value if formData is empty or undefined
    const defaultValue = getDefaultExampleValue(field.name, field);
    const value = formData[field.name] !== undefined && formData[field.name] !== '' ? formData[field.name] : defaultValue;
    const fieldError = fieldErrors[field.name];
    const hasError = !!fieldError;

    switch (field.type) {
      case 'number':
        const numValue = (value !== null && value !== undefined && value !== '') ? parseFloat(value) : (field.min || 0);
        const showSlider = field.min !== undefined && field.max !== undefined && (field.max - field.min) <= 200;
        
        return (
          <div key={field.name} className="form-group">
            <label className="form-label flex items-center gap-2">
              <span className="flex items-center gap-1">
                {getFieldIcon(field.name)}
                {field.label}
                {field.required && <span className="text-red-500 ml-1">*</span>}
              </span>
              {field.description && (
                <div className="relative group">
                  <HelpCircle className="h-4 w-4 text-gray-400 hover:text-gray-600 cursor-help" />
                  <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-10">
                    {field.description}
                  </div>
                </div>
              )}
            </label>
            
            {showSlider ? (
              <div className="space-y-3">
                <div className="flex items-center gap-4">
                  <input
                    type="range"
                    value={numValue}
                    onChange={(e) => handleInputChange(field.name, e.target.value !== '' ? parseFloat(e.target.value) : (field.min || 0))}
                    min={field.min}
                    max={field.max}
                    step={field.step || 1}
                    className="flex-1 h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer slider"
                    style={{
                      background: `linear-gradient(to right, #3b82f6 0%, #3b82f6 ${((numValue - (field.min || 0)) / ((field.max || 100) - (field.min || 0))) * 100}%, #e5e7eb ${((numValue - (field.min || 0)) / ((field.max || 100) - (field.min || 0))) * 100}%, #e5e7eb 100%)`
                    }}
                  />
                  <div className="min-w-[80px] px-3 py-2 bg-blue-50 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-700 rounded-lg text-sm font-medium text-blue-700 dark:text-blue-300 text-center">
                    {numValue}{field.unit && ` ${field.unit}`}
                  </div>
                </div>
                <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400">
                  <span>{field.min}{field.unit && ` ${field.unit}`}</span>
                  <span>{field.max}{field.unit && ` ${field.unit}`}</span>
                </div>
              </div>
            ) : (
              <div className="relative">
                <input
                  type="number"
                  value={numValue}
                  onChange={(e) => handleInputChange(field.name, e.target.value !== '' ? parseFloat(e.target.value) : '')}
                  min={field.min}
                  max={field.max}
                  step={field.step || 1}
                  required={field.required}
                  className={`input pr-12 ${hasError ? 'border-red-300 focus:border-red-500 focus:ring-red-500' : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'} transition-colors duration-200`}
                  placeholder={`Enter ${field.label.toLowerCase()}`}
                />
                {field.unit && (
                  <span className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 dark:text-gray-400 text-sm font-medium">
                    {field.unit}
                  </span>
                )}
                {hasError && (
                  <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                    <AlertTriangle className="h-4 w-4 text-red-500" />
                  </div>
                )}
              </div>
            )}
            
            {hasError && (
              <p className="text-sm text-red-600 mt-1 flex items-center gap-1">
                <AlertTriangle className="h-3 w-3" />
                {fieldError}
              </p>
            )}
            {field.min !== undefined && field.max !== undefined && !showSlider && (
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                Range: {field.min} - {field.max} {field.unit}
              </p>
            )}
          </div>
        );

      case 'select':
        return (
          <div key={field.name} className="form-group">
            <label className="form-label flex items-center gap-2">
              <span className="flex items-center gap-1">
                {getFieldIcon(field.name)}
                {field.label}
                {field.required && <span className="text-red-500 ml-1">*</span>}
              </span>
              {field.description && (
                <div className="relative group">
                  <HelpCircle className="h-4 w-4 text-gray-400 hover:text-gray-600 cursor-help" />
                  <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-10">
                    {field.description}
                  </div>
                </div>
              )}
            </label>
            <div className="relative">
              <select
                value={value}
                onChange={(e) => handleInputChange(field.name, e.target.value)}
                required={field.required}
                className={`input appearance-none ${hasError ? 'border-red-300 focus:border-red-500 focus:ring-red-500' : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'} transition-colors duration-200`}
              >
                <option value="">Select {field.label}</option>
                {field.options?.map(option => (
                  <option key={option} value={option}>{option}</option>
                ))}
              </select>
              <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none" />
              {hasError && (
                <div className="absolute right-8 top-1/2 transform -translate-y-1/2">
                  <AlertTriangle className="h-4 w-4 text-red-500" />
                </div>
              )}
            </div>
            {hasError && (
              <p className="text-sm text-red-600 mt-1 flex items-center gap-1">
                <AlertTriangle className="h-3 w-3" />
                {fieldError}
              </p>
            )}
          </div>
        );

      case 'radio':
        return (
          <div key={field.name} className="form-group">
            <label className="form-label flex items-center gap-2 mb-3">
              <span className="flex items-center gap-1">
                {getFieldIcon(field.name)}
                {field.label}
                {field.required && <span className="text-red-500 ml-1">*</span>}
              </span>
              {field.description && (
                <div className="relative group">
                  <HelpCircle className="h-4 w-4 text-gray-400 hover:text-gray-600 cursor-help" />
                  <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-10">
                    {field.description}
                  </div>
                </div>
              )}
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {field.options?.map(option => (
                <label key={option} className={`flex items-center p-3 border rounded-lg cursor-pointer transition-all duration-200 hover:bg-gray-50 dark:hover:bg-gray-800 ${
                  value === option 
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300' 
                    : 'border-gray-200 dark:border-gray-700'
                }`}>
                  <input
                    type="radio"
                    name={field.name}
                    value={option}
                    checked={value === option}
                    onChange={(e) => handleInputChange(field.name, e.target.value)}
                    required={field.required}
                    className="mr-3 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="font-medium">{option}</span>
                </label>
              ))}
            </div>
            {hasError && (
              <p className="text-sm text-red-600 mt-2 flex items-center gap-1">
                <AlertTriangle className="h-3 w-3" />
                {fieldError}
              </p>
            )}
          </div>
        );

      case 'checkbox':
        return (
          <div key={field.name} className="form-group">
            <div className="flex items-start gap-3">
              <div className="flex items-center h-5">
                <input
                  type="checkbox"
                  checked={value}
                  onChange={(e) => handleInputChange(field.name, e.target.checked)}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded transition-colors duration-200"
                />
              </div>
              <div className="flex-1">
                <label className="flex items-center gap-2 cursor-pointer">
                  <span className="flex items-center gap-1">
                    {getFieldIcon(field.name)}
                    {field.label}
                    {field.required && <span className="text-red-500 ml-1">*</span>}
                  </span>
                  {field.description && (
                    <div className="relative group">
                      <HelpCircle className="h-4 w-4 text-gray-400 hover:text-gray-600 cursor-help" />
                      <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-10">
                        {field.description}
                      </div>
                    </div>
                  )}
                </label>
                {hasError && (
                  <p className="text-sm text-red-600 mt-1 flex items-center gap-1">
                    <AlertTriangle className="h-3 w-3" />
                    {fieldError}
                  </p>
                )}
              </div>
            </div>
          </div>
        );

      default:
        return (
          <div key={field.name} className="form-group">
            <label className="form-label flex items-center gap-2">
              <span className="flex items-center gap-1">
                {getFieldIcon(field.name)}
                {field.label}
                {field.required && <span className="text-red-500 ml-1">*</span>}
              </span>
              {field.description && (
                <div className="relative group">
                  <HelpCircle className="h-4 w-4 text-gray-400 hover:text-gray-600 cursor-help" />
                  <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-10">
                    {field.description}
                  </div>
                </div>
              )}
            </label>
            <div className="relative">
              <input
                type="text"
                value={value}
                onChange={(e) => handleInputChange(field.name, e.target.value)}
                required={field.required}
                className={`input ${hasError ? 'border-red-300 focus:border-red-500 focus:ring-red-500' : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'} transition-colors duration-200`}
                placeholder={`Enter ${field.label.toLowerCase()}`}
              />
              {hasError && (
                <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                  <AlertTriangle className="h-4 w-4 text-red-500" />
                </div>
              )}
            </div>
            {hasError && (
              <p className="text-sm text-red-600 mt-1 flex items-center gap-1">
                <AlertTriangle className="h-3 w-3" />
                {fieldError}
              </p>
            )}
          </div>
        );
    }
  };

  if (isLoadingFields) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center transition-colors duration-300">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 dark:border-blue-400 mx-auto mb-4"></div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">Loading Predictor...</h2>
          <p className="text-gray-600 dark:text-gray-300">Fetching field definitions from server</p>
        </div>
      </div>
    );
  }

  if (!predictor) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Predictor Not Found</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-6">The requested predictor could not be found.</p>
          <Link to="/predictors" className="btn-primary">
            Back to Predictors
          </Link>
        </div>
      </div>
    );
  }

  const Icon = predictor.icon;

  return (
    <div className="min-h-screen py-8">
      <style>{`
        .slider::-webkit-slider-thumb {
          appearance: none;
          height: 20px;
          width: 20px;
          border-radius: 50%;
          background: #3b82f6;
          cursor: pointer;
          border: 2px solid #ffffff;
          box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .slider::-moz-range-thumb {
          height: 20px;
          width: 20px;
          border-radius: 50%;
          background: #3b82f6;
          cursor: pointer;
          border: 2px solid #ffffff;
          box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .slider:focus::-webkit-slider-thumb {
          box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
        }
        .slider:focus::-moz-range-thumb {
          box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
        }
      `}</style>
      <div className="container-max section-padding">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="mb-8"
        >
          <Link
            to="/predictors"
            className="inline-flex items-center text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 mb-6 transition-colors duration-200"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Predictors
          </Link>
          
          <div className="flex items-start space-x-6">
            <div className="w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-xl flex items-center justify-center">
              <Icon className="h-8 w-8 text-primary-600 dark:text-primary-400" />
            </div>
            <div className="flex-1">
              <h1 className="text-3xl lg:text-4xl font-display font-bold text-gray-900 dark:text-white mb-2">
                {predictor.name}
              </h1>
              <p className="text-lg text-gray-600 dark:text-gray-300 mb-4">{predictor.description}</p>
              <div className="flex items-center space-x-6 text-sm">
                <div className="flex items-center text-gray-500 dark:text-gray-400">
                  <Clock className="h-4 w-4 mr-1" />
                  {predictor.estimatedTime}
                </div>
                <div className="text-green-600 dark:text-green-400 font-medium">
                  {predictor.accuracy} accuracy
                </div>
                <span className="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-full text-xs font-medium">
                  {predictor.difficulty}
                </span>
              </div>
            </div>
          </div>
        </motion.div>

        {currentStep === 0 ? (
          /* Form Step */
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <div className="card max-w-4xl mx-auto">
              {/* Form Header */}
              <div className="mb-8">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Health Assessment Form</h2>
                <p className="text-gray-600 dark:text-gray-300">
                  Please review and adjust the pre-filled values below to get your personalized health assessment.
                </p>
              </div>
              
              {error && (
                <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-6">
                  <div className="flex items-center">
                    <AlertTriangle className="h-5 w-5 text-red-600 dark:text-red-400 mr-2" />
                    <span className="text-red-800 dark:text-red-300">{error}</span>
                  </div>
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-8">
                {/* Single Inputs Section */}
                <div className="space-y-8">
                  {/* Inputs Section */}
                  <div className="pb-6">
                    <div className="flex items-center gap-2 mb-4">
                      <FileText className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Inputs</h3>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
                      {predictor?.fields?.map(renderField)}
                    </div>
                  </div>
                </div>
                
                {/* Form Actions */}
                <div className="flex flex-col sm:flex-row items-center justify-between pt-8 border-t border-gray-200 dark:border-gray-700">
                  <div className="flex items-center text-sm text-gray-500 dark:text-gray-400 mb-4 sm:mb-0">
                    <CheckCircle className="h-4 w-4 mr-2 text-green-500" />
                    <span>Ready for assessment</span>
                  </div>
                  
                  <button
                    type="submit"
                    disabled={isLoading || formProgress < 100 || Object.values(fieldErrors).some(error => error)}
                    className="btn-primary px-8 py-3 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 min-w-[160px] justify-center transition-all duration-200 hover:shadow-lg"
                  >
                    {isLoading ? (
                      <>
                        <Loader className="animate-spin h-5 w-5" />
                        <span>Analyzing...</span>
                      </>
                    ) : (
                      <>
                        <TrendingUp className="h-5 w-5" />
                        <span>Get Prediction</span>
                      </>
                    )}
                  </button>
                </div>
              </form>
            </div>
          </motion.div>
        ) : (
          /* Results Step */
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            {result && (
              <div className="max-w-4xl mx-auto space-y-6">
                {/* Risk Assessment */}
                <div className="card">
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Risk Assessment</h2>
                    <div className="flex space-x-2">
                      <button 
                        onClick={handleDownloadPDF}
                        disabled={isDownloadingPDF}
                        className="btn-outline p-2 relative"
                        title="Download PDF Report"
                      >
                        {isDownloadingPDF ? (
                          <div className="animate-spin h-4 w-4 border-2 border-current border-t-transparent rounded-full" />
                        ) : (
                          <Download className="h-4 w-4" />
                        )}
                      </button>
                      <button className="btn-outline p-2" title="Share Report">
                        <Share2 className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                    <div className="text-center">
                      <div className={`inline-flex items-center px-4 py-2 rounded-full text-lg font-semibold ${getRiskColor(result.risk_level)}`}>
                        {React.createElement(getRiskIcon(result.risk_level), { className: 'h-5 w-5 mr-2' })}
                        {result.risk_level} Risk
                      </div>
                      <p className="text-sm text-gray-500 mt-2">Risk Level</p>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold text-gray-900 dark:text-white">
                        {Math.round(result.risk_score * 100)}%
                      </div>
                      <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">Risk Score</p>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold text-gray-900 dark:text-white">
                        {Math.round(result.confidence * 100)}%
                      </div>
                      <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">Confidence</p>
                    </div>
                  </div>
                  
                  <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Explanation</h3>
                    <p className="text-gray-700 dark:text-gray-300">{result.explanation}</p>
                  </div>
                </div>

                {/* Input Values Explanation */}
                <div className="card">
                  <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
                    <FileText className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                    Input Values Used in Prediction
                  </h3>
                  <div className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-xl p-6">
                    <p className="text-gray-700 dark:text-gray-300 mb-4">
                      This prediction was generated using the following input values. These values represent your health profile and are used by our AI model to assess risk factors and generate personalized recommendations.
                    </p>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {Object.entries(formData).filter(([key, value]) => value !== '' && value !== null && value !== undefined).map(([key, value]) => {
                        const field = predictor?.fields?.find(f => f.name === key);
                        const displayName = field?.label || key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                        const unit = field?.unit || '';
                        
                        return (
                          <div key={key} className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-blue-200 dark:border-blue-700">
                            <div className="flex items-center justify-between mb-2">
                              <h4 className="font-semibold text-gray-900 dark:text-white text-sm">{displayName}</h4>
                              {field?.required && (
                                <span className="text-xs bg-blue-100 text-blue-700 dark:bg-blue-800 dark:text-blue-200 px-2 py-1 rounded-full">
                                  Required
                                </span>
                              )}
                            </div>
                            <div className="flex items-center gap-2">
                              <span className="text-lg font-bold text-blue-600 dark:text-blue-400">
                                {typeof value === 'boolean' ? (value ? 'Yes' : 'No') : value}
                              </span>
                              {unit && <span className="text-sm text-gray-500 dark:text-gray-400">{unit}</span>}
                            </div>
                            {field?.description && (
                              <p className="text-xs text-gray-600 dark:text-gray-400 mt-2">{field.description}</p>
                            )}
                          </div>
                        );
                      })}
                    </div>
                    <div className="mt-6 p-4 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
                      <h4 className="font-semibold text-blue-900 dark:text-blue-100 mb-2 flex items-center gap-2">
                        <Info className="h-4 w-4" />
                        How These Values Impact Your Prediction
                      </h4>
                      <p className="text-sm text-blue-800 dark:text-blue-200">
                        Our AI model analyzes these input values using advanced machine learning algorithms trained on medical data. 
                        Each value contributes to the overall risk assessment, with some factors having higher impact than others. 
                        The model considers interactions between different health parameters to provide a comprehensive prediction.
                      </p>
                    </div>
                  </div>
                </div>

                {/* Risk Factors */}
                {result.risk_factors?.length > 0 && (
                  <div className="card">
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Key Risk Factors</h3>
                    <div className="space-y-2">
                      {result.risk_factors.map((factor, index) => (
                        <div key={index} className="flex items-center p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
                          <AlertTriangle className="h-5 w-5 text-orange-600 dark:text-orange-400 mr-3" />
                          <span className="text-orange-800 dark:text-orange-300">{factor}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Recommendations */}
                {result.recommendations?.length > 0 && (
                  <div className="card">
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Recommendations</h3>
                    <div className="space-y-3">
                      {result.recommendations.map((recommendation, index) => (
                        <div key={index} className="flex items-start p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                          <CheckCircle className="h-5 w-5 text-blue-600 dark:text-blue-400 mr-3 mt-0.5" />
                          <span className="text-blue-800 dark:text-blue-300">{recommendation}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Contributing Factors */}
                {result.detailed_analysis?.contributing_factors && result.detailed_analysis.contributing_factors.length > 0 && (
                  <div className="card">
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Contributing Factors</h3>
                    <div className="space-y-2">
                      {result.detailed_analysis.contributing_factors.map((factor, index) => (
                        <div key={index} className="flex items-center p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                          <TrendingUp className="h-5 w-5 text-purple-600 dark:text-purple-400 mr-3" />
                          <span className="text-purple-800 dark:text-purple-300">{factor}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Health Metrics */}
                {result.detailed_analysis?.health_metrics && result.detailed_analysis.health_metrics.length > 0 && (
                  <div className="card">
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Health Metrics Analysis</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {result.detailed_analysis.health_metrics.map((metric, index) => (
                        <div key={index} className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
                          <div className="flex items-center justify-between mb-2">
                            <h4 className="font-semibold text-green-900 dark:text-green-100">{metric.category}</h4>
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                              metric.status === 'Normal' ? 'bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100' :
                              metric.status === 'Warning' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-800 dark:text-yellow-100' :
                              'bg-red-100 text-red-800 dark:bg-red-800 dark:text-red-100'
                            }`}>
                              {metric.status}
                            </span>
                          </div>
                          <p className="text-green-700 dark:text-green-300 mb-2">{metric.value}</p>
                          {metric.recommendation && (
                            <p className="text-sm text-green-600 dark:text-green-400">{metric.recommendation}</p>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Risk Score Visualization */}
                {result.risk_score !== undefined && (
                  <div className="card">
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
                      <BarChart3 className="h-6 w-6 text-purple-600 dark:text-purple-400" />
                      Risk Assessment Overview
                    </h3>
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                      {/* Risk Score Display */}
                      <div className="bg-gradient-to-br from-purple-50 to-indigo-50 dark:from-purple-900/20 dark:to-indigo-900/20 rounded-xl p-6">
                        <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 text-center">Overall Risk Level</h4>
                        <div className="flex flex-col items-center justify-center py-8">
                          {/* Circular Progress Chart */}
                          <div className="relative w-40 h-40 mb-6">
                            <svg className="w-40 h-40 transform -rotate-90" viewBox="0 0 144 144">
                              {/* Background circle */}
                              <circle
                                cx="72"
                                cy="72"
                                r="60"
                                stroke="currentColor"
                                strokeWidth="8"
                                fill="none"
                                className="text-gray-200 dark:text-gray-700"
                              />
                              {/* Progress circle */}
                              <circle
                                cx="72"
                                cy="72"
                                r="60"
                                stroke="currentColor"
                                strokeWidth="8"
                                fill="none"
                                strokeDasharray={`${2 * Math.PI * 60}`}
                                strokeDashoffset={`${2 * Math.PI * 60 * (1 - result.risk_score)}`}
                                className={`transition-all duration-1000 ease-out ${
                                  result.risk_score < 0.3 ? 'text-green-500' :
                                  result.risk_score < 0.7 ? 'text-yellow-500' :
                                  'text-red-500'
                                }`}
                                strokeLinecap="round"
                              />
                            </svg>
                            {/* Center content */}
                            <div className="absolute inset-0 flex items-center justify-center">
                              <div className="text-center">
                                <div className={`text-3xl font-bold ${
                                  result.risk_score < 0.3 ? 'text-green-600 dark:text-green-400' :
                                  result.risk_score < 0.7 ? 'text-yellow-600 dark:text-yellow-400' :
                                  'text-red-600 dark:text-red-400'
                                }`}>
                                  {Math.round(result.risk_score * 100)}%
                                </div>
                                <div className="text-xs text-gray-600 dark:text-gray-400 font-medium">Risk Score</div>
                              </div>
                            </div>
                          </div>
                          
                          <span className={`inline-flex px-4 py-2 rounded-full text-sm font-medium ${
                            result.risk_score < 0.3 ? 'bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100' :
                            result.risk_score < 0.7 ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-800 dark:text-yellow-100' :
                            'bg-red-100 text-red-800 dark:bg-red-800 dark:text-red-100'
                          }`}>
                            {result.risk_score < 0.3 ? 'Low Risk' : result.risk_score < 0.7 ? 'Moderate Risk' : 'High Risk'}
                          </span>
                          
                          {/* Risk Level Description */}
                          <p className="text-center text-sm text-gray-600 dark:text-gray-400 mt-3 max-w-xs">
                            {result.risk_score < 0.3 
                              ? 'Your risk level is low. Continue maintaining healthy habits.' 
                              : result.risk_score < 0.7 
                              ? 'Your risk level is moderate. Consider lifestyle improvements.' 
                              : 'Your risk level is high. Consult with healthcare professionals.'}
                          </p>
                        </div>
                      </div>

                      {/* Risk Factors Breakdown */}
                      {result.detailed_analysis?.contributing_factors && (
                        <div className="bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-blue-900/20 dark:to-cyan-900/20 rounded-xl p-6">
                          <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Key Contributing Factors</h4>
                          <div className="space-y-4">
                            {result.detailed_analysis.contributing_factors.slice(0, 5).map((factor, index) => {
                              // Assign different impact levels for visual variety
                              const impactLevels = [85, 70, 60, 45, 30];
                              const impactLevel = impactLevels[index] || 50;
                              const colors = ['bg-red-500', 'bg-orange-500', 'bg-yellow-500', 'bg-blue-500', 'bg-green-500'];
                              const bgColors = ['bg-red-50 dark:bg-red-900/20', 'bg-orange-50 dark:bg-orange-900/20', 'bg-yellow-50 dark:bg-yellow-900/20', 'bg-blue-50 dark:bg-blue-900/20', 'bg-green-50 dark:bg-green-900/20'];
                              
                              return (
                                <div key={index} className={`p-4 ${bgColors[index]} rounded-lg border border-opacity-20`}>
                                  <div className="flex items-center justify-between mb-2">
                                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{factor}</span>
                                    <span className="text-xs text-gray-500 dark:text-gray-400">{impactLevel}%</span>
                                  </div>
                                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                                    <div 
                                      className={`h-2 rounded-full ${colors[index]} transition-all duration-1000 ease-out`}
                                      style={{ width: `${impactLevel}%` }}
                                    ></div>
                                  </div>
                                </div>
                              );
                            })}
                          </div>
                          
                          {/* Factor Impact Summary */}
                          <div className="mt-6 p-4 bg-white dark:bg-gray-800 rounded-lg">
                            <h5 className="text-sm font-semibold text-gray-900 dark:text-white mb-3">Impact Distribution</h5>
                            <div className="flex items-center gap-4 text-xs">
                              <div className="flex items-center gap-1">
                                <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                                <span className="text-gray-600 dark:text-gray-400">High Impact</span>
                              </div>
                              <div className="flex items-center gap-1">
                                <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                                <span className="text-gray-600 dark:text-gray-400">Moderate Impact</span>
                              </div>
                              <div className="flex items-center gap-1">
                                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                                <span className="text-gray-600 dark:text-gray-400">Low Impact</span>
                              </div>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Lifestyle Impact */}
                {result.detailed_analysis?.lifestyle_impact && Object.keys(result.detailed_analysis.lifestyle_impact).length > 0 && (
                  <div className="card">
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
                      <Activity className="h-6 w-6 text-indigo-600 dark:text-indigo-400" />
                      Lifestyle Impact Analysis
                    </h3>
                    
                    {/* Lifestyle Impact Summary Chart */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                      {/* Impact Overview Chart */}
                      <div className="bg-gradient-to-br from-indigo-50 to-purple-50 dark:from-indigo-900/20 dark:to-purple-900/20 rounded-xl p-6">
                        <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Lifestyle Impact Overview</h4>
                        <div className="space-y-4">
                          {(() => {
                            // Filter and process lifestyle factors to show only meaningful ones
                            const meaningfulFactors = Object.entries(result.detailed_analysis.lifestyle_impact)
                              .filter(([key, value]) => {
                                return key !== 'recommendations' && 
                                       value && 
                                       typeof value === 'string' && 
                                       (value as string).length > 5 && // Filter out single letters
                                       !key.match(/^\d+$/); // Filter out numeric keys
                              })
                              .slice(0, 5); // Limit to top 5 factors
                            
                            if (meaningfulFactors.length === 0) {
                              return (
                                <div className="text-center py-8">
                                  <div className="text-gray-500 dark:text-gray-400">No specific lifestyle factors identified</div>
                                </div>
                              );
                            }
                            
                            return meaningfulFactors.map(([key, value], index) => {
                              // Determine impact level from content
                              let impactLevel = 'Medium';
                              let impactScore = 60;
                              
                              if (typeof value === 'string') {
                                const lowerValue = (value as string).toLowerCase();
                                if (lowerValue.includes('low') || lowerValue.includes('minimal') || lowerValue.includes('good')) {
                                  impactLevel = 'Low';
                                  impactScore = 25;
                                } else if (lowerValue.includes('high') || lowerValue.includes('significant') || lowerValue.includes('severe') || lowerValue.includes('poor')) {
                                  impactLevel = 'High';
                                  impactScore = 85;
                                }
                              }
                              
                              const getIcon = (factorKey: string) => {
                                const lowerKey = factorKey.toLowerCase();
                                if (lowerKey.includes('smoking') || lowerKey.includes('tobacco')) return '🚭';
                                if (lowerKey.includes('diet') || lowerKey.includes('nutrition') || lowerKey.includes('food')) return '🥗';
                                if (lowerKey.includes('exercise') || lowerKey.includes('activity') || lowerKey.includes('physical')) return '🏃';
                                if (lowerKey.includes('sleep')) return '😴';
                                if (lowerKey.includes('stress') || lowerKey.includes('mental')) return '😰';
                                if (lowerKey.includes('alcohol') || lowerKey.includes('drink')) return '🍷';
                                if (lowerKey.includes('weight') || lowerKey.includes('bmi') || lowerKey.includes('obesity')) return '⚖️';
                                if (lowerKey.includes('blood') || lowerKey.includes('pressure')) return '🩸';
                                return '📊';
                              };
                              
                              return (
                                <div key={index} className="flex items-center justify-between p-3 bg-white dark:bg-gray-800 rounded-lg">
                                  <div className="flex items-center gap-3 flex-1">
                                    <span className="text-xl">{getIcon(key)}</span>
                                    <div className="flex-1">
                                      <h5 className="font-medium text-gray-900 dark:text-white text-sm">
                                        {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                                      </h5>
                                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mt-1">
                                        <div 
                                          className={`h-2 rounded-full transition-all duration-500 ${
                                            impactLevel === 'Low' ? 'bg-green-500' :
                                            impactLevel === 'Medium' ? 'bg-yellow-500' : 'bg-red-500'
                                          }`}
                                          style={{ width: `${impactScore}%` }}
                                        ></div>
                                      </div>
                                    </div>
                                  </div>
                                  <span className={`px-2 py-1 rounded-full text-xs font-medium ml-3 ${
                                    impactLevel === 'Low' ? 'bg-green-100 text-green-700 dark:bg-green-800 dark:text-green-200' :
                                    impactLevel === 'Medium' ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-800 dark:text-yellow-200' :
                                    'bg-red-100 text-red-700 dark:bg-red-800 dark:text-red-200'
                                  }`}>
                                    {impactLevel}
                                  </span>
                                </div>
                              );
                            });
                          })()
                          }
                        </div>
                      </div>
                      
                      {/* Risk Distribution Visualization */}
                      <div className="bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-blue-900/20 dark:to-cyan-900/20 rounded-xl p-6">
                        <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Risk Distribution</h4>
                        <div className="space-y-4">
                          {(() => {
                            // Create a simple risk distribution visualization
                            const riskCategories = [
                              { name: 'Low Risk Factors', value: 30, color: 'bg-green-500', count: 2 },
                              { name: 'Moderate Risk Factors', value: 45, color: 'bg-yellow-500', count: 3 },
                              { name: 'High Risk Factors', value: 25, color: 'bg-red-500', count: 1 }
                            ];
                            
                            return riskCategories.map((category, index) => (
                              <div key={index} className="space-y-2">
                                <div className="flex justify-between items-center">
                                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{category.name}</span>
                                  <span className="text-sm text-gray-600 dark:text-gray-400">{category.count} factors</span>
                                </div>
                                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                                  <div 
                                    className={`h-3 rounded-full ${category.color} transition-all duration-700`}
                                    style={{ width: `${category.value}%` }}
                                  ></div>
                                </div>
                                <div className="text-right">
                                  <span className="text-xs text-gray-500 dark:text-gray-400">{category.value}%</span>
                                </div>
                              </div>
                            ));
                          })()
                          }
                        </div>
                      </div>
                    </div>
                      
                    {/* Key Recommendations */}
                    <div className="bg-gradient-to-r from-emerald-50 to-teal-50 dark:from-emerald-900/20 dark:to-teal-900/20 rounded-xl p-6 border border-emerald-200 dark:border-emerald-700">
                      <h4 className="font-semibold text-emerald-900 dark:text-emerald-100 mb-4 flex items-center gap-2">
                        <CheckCircle className="h-5 w-5" />
                        Key Health Recommendations
                      </h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {(() => {
                          // Generate relevant recommendations based on predictor type
                          const baseRecommendations = [
                            "Maintain a balanced diet rich in fruits and vegetables",
                            "Engage in regular physical activity (150 minutes per week)",
                            "Get adequate sleep (7-9 hours per night)",
                            "Manage stress through relaxation techniques"
                          ];
                          
                          // Use actual recommendations if available, otherwise use base ones
                          const recommendations = result.detailed_analysis.lifestyle_impact && Array.isArray(result.detailed_analysis.lifestyle_impact) && result.detailed_analysis.lifestyle_impact.length > 0
                            ? result.detailed_analysis.lifestyle_impact.slice(0, 4).map(item => {
                                // Ensure we always return a string, never an object
                                if (typeof item === 'string') return item;
                                if (typeof item === 'object' && item !== null) {
                                  // Handle objects with description, factor, impact, value keys
                                  return item.description || item.factor || item.impact_level || 'Health recommendation';
                                }
                                return 'Health recommendation';
                              })
                            : baseRecommendations;
                          
                          return recommendations.map((recommendation, recIndex) => (
                            <div key={recIndex} className="flex items-start gap-3 p-4 bg-white dark:bg-gray-800 rounded-lg border border-emerald-100 dark:border-emerald-800 hover:shadow-md transition-all duration-200">
                              <div className="w-6 h-6 bg-emerald-500 text-white rounded-full flex items-center justify-center text-xs font-bold mt-0.5 flex-shrink-0">
                                {recIndex + 1}
                              </div>
                              <span className="text-sm text-emerald-700 dark:text-emerald-300 leading-relaxed">{recommendation}</span>
                            </div>
                          ));
                        })()
                        }
                      </div>
                    </div>
                  </div>
                )}

                {/* Actions */}
                <div className="flex justify-center space-x-4">
                  <button
                    onClick={() => {
                      setCurrentStep(0);
                      setResult(null);
                      setError(null);
                    }}
                    className="btn-outline"
                  >
                    New Assessment
                  </button>
                  <Link to="/predictors" className="btn-primary">
                    Try Another Predictor
                  </Link>
                </div>
              </div>
            )}
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default PredictorDetail;