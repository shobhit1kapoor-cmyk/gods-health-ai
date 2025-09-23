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
  Shield,
  Droplets,
  Apple,
  Dumbbell,
  Moon,
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
      'oldpeak': 1.2,
      'glucose_level': 95,
      'avg_glucose_level': 110,
      'waist_circumference': 85,
      'specific_gravity': 1.025,
      'water_intake': 2.5,
      'meals_per_day': 3,
      'fruit_vegetable_servings': 5,
      'albumin': 1,
      'sugar': 0,
      
      // Medical history
      'hypertension': 'No',
      'heart_disease': 'No',
      'family_history': 'Yes',
      'family_history_diabetes': 'No',
      'family_history_respiratory': 'No',
      'diabetes': 'No',
      'fasting_bs': 'No',
      'chronic_illness': 'No',
      'previous_complications': 'No',
      
      // Lifestyle factors
      'smoking_status': 'Never Smoked',
      'smoking': 'No',
      'smoking_years': 0,
      'smoking_pack_years': 0,
      'physical_activity': 'Moderate',
      'activity_level': 'Moderately Active',
      'current_fitness_level': 'Intermediate',
      'exercise_duration': 45,
      'dietary_restrictions': 'None',
      'processed_food_frequency': 'Sometimes',
      'cooking_frequency': 'Often',
      'supplement_use': 'No',
      'alcohol_consumption': 'Light',
      'exercise_frequency': 'Moderate',
      'sleep_hours': 7,
      'morning_alertness': 'Alert',
      'daytime_fatigue': 'Sometimes',
      'caffeine_intake': 'Moderate (3-4 cups)',
      'screen_time_before_bed': '<30 min',
      'sleep_environment': 'Good',
      'snoring': 'No',
      'sleep_medications': 'No',
      'sleep_problems': 'No',
      'stress_level': 3,
      'work_stress_level': 5,
      'occupation': 'Technology',
      'work_hours_per_week': 40,
      'job_satisfaction': 'Satisfied',
      'work_life_balance': 'Good',
      'emotional_exhaustion': 'Sometimes',
      'cynicism': 'Rarely',
      'personal_accomplishment': 'High',
      'physical_symptoms': 'No',
      'coping_strategies': 'Exercise',
      'support_system': 'Good',
      'social_support': 'Good',
      'work_satisfaction': 'Satisfied',
      'substance_use': 'None',
      
      // Clinical tests
      'chest_pain_type': 'Typical angina',
      'resting_ecg': 'Normal',
      'exercise_angina': 'No',
      'cognitive_score': 28,
      'education_years': 16,
      'symptoms_count': 2,
      
      // Pregnancy-related
      'maternal_age': 28,
      'gestational_age': 38,
      'multiple_pregnancy': 'No',
      
      // Work and lifestyle
      'work_type': 'Private',
      'residence_type': 'Urban',
      'ever_married': 'Yes',
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
        fieldName.includes('yes') || 
        fieldName.includes('no') || 
        description.includes('1 = yes, 0 = no') ||
        description.includes('1 = Yes, 0 = No') ||
        description.includes('(1 = yes, 0 = no)') ||
        description.includes('(1 = Yes, 0 = No)') ||
        (fieldType === 'int' && (
          (description && description.toLowerCase().includes('yes') && description.toLowerCase().includes('no')) ||
          (fieldName.endsWith('_status') && description.includes('1') && description.includes('0')) ||
          fieldName.includes('hypertension') ||
          fieldName.includes('diabetes') ||
          fieldName.includes('heart_disease') ||
          (fieldName.includes('smoking') && !fieldName.includes('status')) ||
          (fieldName.includes('alcohol') && !fieldName.includes('consumption')) ||
          fieldName.includes('family_history') ||
          fieldName.includes('chronic') ||
          fieldName.includes('emergency') ||
          fieldName.includes('transfusion') ||
          fieldName.includes('multiple_pregnancy') ||
          fieldName.includes('assisted_reproduction') ||
          fieldName.includes('previous_complications') ||
          fieldName.includes('occupational_exposure') ||
          fieldName.includes('hormonal_factors') ||
          fieldName.includes('previous_cancer') ||
          fieldName.includes('immunocompromised') ||
          fieldName.includes('ever_married') ||
          fieldName.includes('cough') ||
          fieldName.includes('shortness_of_breath') ||
          fieldName.includes('loss_of_taste_smell') ||
          (fieldName.includes('chest_pain') && !fieldName.includes('type')) ||
          fieldName.includes('headache') ||
          fieldName.includes('muscle_aches') ||
          fieldName.includes('pale_skin') ||
          fieldName.includes('cold_hands_feet') ||
          fieldName.includes('brittle_nails') ||
          fieldName.includes('strange_cravings') ||
          fieldName.includes('change') ||
          fieldName.includes('diabetesMed') ||
          fieldName.includes('copd') ||
          fieldName.includes('kidney_disease') ||
          fieldName.includes('liver_disease') ||
          (fieldName.includes('cancer') && !fieldName.includes('type')) ||
          fieldName.includes('mobility') ||
          fieldName.includes('fetal_growth_restriction') ||
          fieldName.includes('autoimmune_disease') ||
          fieldName.includes('chronic_hypertension') ||
          fieldName.includes('diabetes_pre_pregnancy')
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

  // Mock predictor data - in real app, this would come from API
  const predictorData: Record<string, PredictorInfo> = useMemo(() => ({
    heart_disease: {
      id: 'heart_disease',
      name: 'Heart Disease Predictor',
      description: 'Predict risk of heart attack, arrhythmia, or heart failure using cardiovascular health indicators.',
      category: 'Disease Risk & Diagnosis',
      icon: Heart,
      difficulty: 'Medium',
      estimatedTime: '5-7 min',
      accuracy: '94%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 18, max: 120, unit: 'years' },
        { name: 'sex', label: 'Sex', type: 'select', required: true, options: ['Male', 'Female'] },
        { name: 'chest_pain_type', label: 'Chest Pain Type', type: 'select', required: true, options: ['Typical Angina', 'Atypical Angina', 'Non-Anginal Pain', 'Asymptomatic'] },
        { name: 'resting_bp', label: 'Resting Blood Pressure', type: 'number', required: true, min: 80, max: 200, unit: 'mmHg' },
        { name: 'cholesterol', label: 'Serum Cholesterol', type: 'number', required: true, min: 100, max: 400, unit: 'mg/dl' },
        { name: 'fasting_bs', label: 'Fasting Blood Sugar > 120 mg/dl', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'resting_ecg', label: 'Resting ECG Results', type: 'select', required: true, options: ['Normal', 'ST-T Wave Abnormality', 'Left Ventricular Hypertrophy'] },
        { name: 'max_hr', label: 'Maximum Heart Rate Achieved', type: 'number', required: true, min: 60, max: 220, unit: 'bpm' },
        { name: 'exercise_angina', label: 'Exercise Induced Angina', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'oldpeak', label: 'ST Depression (Oldpeak)', type: 'number', required: true, min: 0, max: 10, step: 0.1, unit: 'mm' }
      ]
    },
    stroke_risk: {
      id: 'stroke_risk',
      name: 'Stroke Risk Predictor',
      description: 'Analyze blood pressure, cholesterol, lifestyle, and family history to assess stroke risk.',
      category: 'Disease Risk & Diagnosis',
      icon: Brain,
      difficulty: 'Medium',
      estimatedTime: '6-8 min',
      accuracy: '92%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 18, max: 120, unit: 'years' },
        { name: 'gender', label: 'Gender', type: 'select', required: true, options: ['Male', 'Female'] },
        { name: 'hypertension', label: 'Hypertension', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'heart_disease', label: 'Heart Disease', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'ever_married', label: 'Ever Married', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'work_type', label: 'Work Type', type: 'select', required: true, options: ['Private', 'Self-employed', 'Government Job', 'Children', 'Never Worked'] },
        { name: 'residence_type', label: 'Residence Type', type: 'select', required: true, options: ['Urban', 'Rural'] },
        { name: 'avg_glucose_level', label: 'Average Glucose Level', type: 'number', required: true, min: 50, max: 300, unit: 'mg/dL' },
        { name: 'bmi', label: 'Body Mass Index (BMI)', type: 'number', required: true, min: 10, max: 50, step: 0.1, unit: 'kg/m²' },
        { name: 'smoking_status', label: 'Smoking Status', type: 'select', required: true, options: ['Never Smoked', 'Formerly Smoked', 'Smokes'] }
      ]
    },
    cancer_detection: {
      id: 'cancer_detection',
      name: 'Cancer Detection & Risk',
      description: 'Comprehensive cancer risk assessment for breast, lung, prostate, skin, and cervical cancers.',
      category: 'Disease Risk & Diagnosis',
      icon: Stethoscope,
      difficulty: 'Advanced',
      estimatedTime: '10-12 min',
      accuracy: '89%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 18, max: 120, unit: 'years' },
        { name: 'gender', label: 'Gender', type: 'select', required: true, options: ['Male', 'Female'] },
        { name: 'family_history', label: 'Family History of Cancer', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'smoking_status', label: 'Smoking Status', type: 'select', required: true, options: ['Never Smoked', 'Former Smoker', 'Current Smoker'] },
        { name: 'alcohol_consumption', label: 'Alcohol Consumption', type: 'select', required: true, options: ['None', 'Light', 'Moderate', 'Heavy'] },
        { name: 'bmi', label: 'Body Mass Index (BMI)', type: 'number', required: true, min: 15, max: 50, step: 0.1, unit: 'kg/m²' },
        { name: 'exercise_frequency', label: 'Exercise Frequency per Week', type: 'number', required: true, min: 0, max: 14, unit: 'times' },
        { name: 'environmental_exposure', label: 'Environmental/Occupational Exposure', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'previous_cancer', label: 'Previous Cancer History', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'hormonal_factors', label: 'Hormonal Risk Factors', type: 'radio', required: true, options: ['Yes', 'No'] }
      ]
    },
    kidney_disease: {
      id: 'kidney_disease',
      name: 'Kidney Disease Predictor',
      description: 'Chronic kidney disease detection using blood and urine test data.',
      category: 'Disease Risk & Diagnosis',
      icon: Activity,
      difficulty: 'Medium',
      estimatedTime: '4-6 min',
      accuracy: '91%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 18, max: 120, unit: 'years' },
        { name: 'blood_pressure', label: 'Blood Pressure', type: 'number', required: true, min: 80, max: 200, unit: 'mmHg' },
        { name: 'specific_gravity', label: 'Specific Gravity', type: 'number', required: true, min: 1.005, max: 1.030, step: 0.001 },
        { name: 'albumin', label: 'Albumin', type: 'number', required: true, min: 0, max: 5 },
        { name: 'sugar', label: 'Sugar', type: 'number', required: true, min: 0, max: 5 },
        { name: 'red_blood_cells', label: 'Red Blood Cells', type: 'select', required: true, options: ['Normal', 'Abnormal'] },
        { name: 'pus_cell', label: 'Pus Cell', type: 'select', required: true, options: ['Normal', 'Abnormal'] },
        { name: 'pus_cell_clumps', label: 'Pus Cell Clumps', type: 'select', required: true, options: ['Present', 'Not Present'] },
        { name: 'bacteria', label: 'Bacteria', type: 'select', required: true, options: ['Present', 'Not Present'] },
        { name: 'blood_glucose_random', label: 'Blood Glucose Random', type: 'number', required: true, min: 50, max: 500, unit: 'mgs/dl' },
        { name: 'blood_urea', label: 'Blood Urea', type: 'number', required: true, min: 1.5, max: 391, unit: 'mgs/dl' },
        { name: 'serum_creatinine', label: 'Serum Creatinine', type: 'number', required: true, min: 0.4, max: 76, step: 0.1, unit: 'mgs/dl' },
        { name: 'sodium', label: 'Sodium', type: 'number', required: true, min: 4.5, max: 163, unit: 'mEq/L' },
        { name: 'potassium', label: 'Potassium', type: 'number', required: true, min: 2.5, max: 47, step: 0.1, unit: 'mEq/L' },
        { name: 'hemoglobin', label: 'Hemoglobin', type: 'number', required: true, min: 3.1, max: 17.8, step: 0.1, unit: 'gms' },
        { name: 'packed_cell_volume', label: 'Packed Cell Volume', type: 'number', required: true, min: 9, max: 54 },
        { name: 'white_blood_cell_count', label: 'White Blood Cell Count', type: 'number', required: true, min: 2200, max: 26400 },
        { name: 'red_blood_cell_count', label: 'Red Blood Cell Count', type: 'number', required: true, min: 2.1, max: 8, step: 0.1, unit: 'millions/cmm' },
        { name: 'hypertension', label: 'Hypertension', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'diabetes_mellitus', label: 'Diabetes Mellitus', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'coronary_artery_disease', label: 'Coronary Artery Disease', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'appetite', label: 'Appetite', type: 'select', required: true, options: ['Good', 'Poor'] },
        { name: 'pedal_edema', label: 'Pedal Edema', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'anemia', label: 'Anemia', type: 'radio', required: true, options: ['Yes', 'No'] }
      ]
    },
    liver_disease: {
      id: 'liver_disease',
      name: 'Liver Disease Predictor',
      description: 'Detect hepatitis, cirrhosis, and fatty liver disease from laboratory test results.',
      category: 'Disease Risk & Diagnosis',
      icon: Stethoscope,
      difficulty: 'Medium',
      estimatedTime: '5-7 min',
      accuracy: '88%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 18, max: 120, unit: 'years' },
        { name: 'gender', label: 'Gender', type: 'select', required: true, options: ['Male', 'Female'] },
        { name: 'total_bilirubin', label: 'Total Bilirubin', type: 'number', required: true, min: 0.1, max: 75, step: 0.1, unit: 'mg/dL' },
        { name: 'direct_bilirubin', label: 'Direct Bilirubin', type: 'number', required: true, min: 0.1, max: 19.7, step: 0.1, unit: 'mg/dL' },
        { name: 'alkaline_phosphotase', label: 'Alkaline Phosphotase', type: 'number', required: true, min: 63, max: 2110, unit: 'IU/L' },
        { name: 'alamine_aminotransferase', label: 'Alamine Aminotransferase', type: 'number', required: true, min: 10, max: 2000, unit: 'IU/L' },
        { name: 'aspartate_aminotransferase', label: 'Aspartate Aminotransferase', type: 'number', required: true, min: 10, max: 4929, unit: 'IU/L' },
        { name: 'total_proteins', label: 'Total Proteins', type: 'number', required: true, min: 2.7, max: 9.6, step: 0.1, unit: 'g/dL' },
        { name: 'albumin', label: 'Albumin', type: 'number', required: true, min: 0.9, max: 5.5, step: 0.1, unit: 'g/dL' },
        { name: 'albumin_and_globulin_ratio', label: 'Albumin and Globulin Ratio', type: 'number', required: true, min: 0.3, max: 2.8, step: 0.1 }
      ]
    },
    alzheimer: {
      id: 'alzheimer',
      name: 'Alzheimer\'s Predictor',
      description: 'Early detection of Alzheimer\'s and dementia using memory and behavioral assessment data.',
      category: 'Disease Risk & Diagnosis',
      icon: Brain,
      difficulty: 'Advanced',
      estimatedTime: '8-10 min',
      accuracy: '85%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 50, max: 120, unit: 'years' },
        { name: 'gender', label: 'Gender', type: 'select', required: true, options: ['Male', 'Female'] },
        { name: 'education_years', label: 'Years of Education', type: 'number', required: true, min: 0, max: 30, unit: 'years' },
        { name: 'cognitive_score', label: 'Cognitive Assessment Score (MMSE)', type: 'number', required: true, min: 0, max: 30 },
        { name: 'family_history', label: 'Family History of Dementia', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'apoe4_status', label: 'APOE4 Gene Status', type: 'select', required: true, options: ['Negative', 'Positive', 'Unknown'] },
        { name: 'memory_complaints', label: 'Memory Complaints', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'depression_score', label: 'Depression Score (0-15)', type: 'number', required: true, min: 0, max: 15 },
        { name: 'anxiety_score', label: 'Anxiety Score (0-21)', type: 'number', required: true, min: 0, max: 21 },
        { name: 'sleep_quality', label: 'Sleep Quality', type: 'select', required: true, options: ['Poor', 'Fair', 'Good', 'Excellent'] },
        { name: 'physical_activity', label: 'Physical Activity Level', type: 'select', required: true, options: ['Sedentary', 'Light', 'Moderate', 'Vigorous'] },
        { name: 'social_engagement', label: 'Social Engagement Level', type: 'select', required: true, options: ['Low', 'Moderate', 'High'] }
      ]
    },
    parkinson: {
      id: 'parkinson',
      name: 'Parkinson\'s Disease Predictor',
      description: 'Analyze voice patterns, tremor, and movement data for Parkinson\'s disease detection.',
      category: 'Disease Risk & Diagnosis',
      icon: Activity,
      difficulty: 'Advanced',
      estimatedTime: '7-9 min',
      accuracy: '87%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 30, max: 120, unit: 'years' },
        { name: 'gender', label: 'Gender', type: 'select', required: true, options: ['Male', 'Female'] },
        { name: 'mdvp_fo', label: 'Average vocal fundamental frequency', type: 'number', required: true, min: 88, max: 260, step: 0.1, unit: 'Hz' },
        { name: 'mdvp_fhi', label: 'Maximum vocal fundamental frequency', type: 'number', required: true, min: 102, max: 592, step: 0.1, unit: 'Hz' },
        { name: 'mdvp_flo', label: 'Minimum vocal fundamental frequency', type: 'number', required: true, min: 65, max: 239, step: 0.1, unit: 'Hz' },
        { name: 'mdvp_jitter_percent', label: 'Jitter (percentage)', type: 'number', required: true, min: 0.00168, max: 0.03316, step: 0.00001 },
        { name: 'mdvp_jitter_abs', label: 'Jitter (absolute)', type: 'number', required: true, min: 0.000007, max: 0.000260, step: 0.000001 },
        { name: 'mdvp_rap', label: 'Relative amplitude perturbation', type: 'number', required: true, min: 0.00068, max: 0.02144, step: 0.00001 },
        { name: 'mdvp_ppq', label: 'Five-point period perturbation quotient', type: 'number', required: true, min: 0.00092, max: 0.01958, step: 0.00001 },
        { name: 'jitter_ddp', label: 'Jitter DDP', type: 'number', required: true, min: 0.00204, max: 0.06433, step: 0.00001 },
        { name: 'mdvp_shimmer', label: 'Shimmer', type: 'number', required: true, min: 0.00954, max: 0.11908, step: 0.00001 },
        { name: 'mdvp_shimmer_db', label: 'Shimmer (dB)', type: 'number', required: true, min: 0.085, max: 1.302, step: 0.001, unit: 'dB' },
        { name: 'shimmer_apq3', label: 'Three-point amplitude perturbation quotient', type: 'number', required: true, min: 0.00455, max: 0.05647, step: 0.00001 },
        { name: 'shimmer_apq5', label: 'Five-point amplitude perturbation quotient', type: 'number', required: true, min: 0.00757, max: 0.07940, step: 0.00001 },
        { name: 'mdvp_apq', label: 'Amplitude perturbation quotient', type: 'number', required: true, min: 0.00719, max: 0.13778, step: 0.00001 },
        { name: 'shimmer_dda', label: 'Shimmer DDA', type: 'number', required: true, min: 0.01364, max: 0.16942, step: 0.00001 },
        { name: 'nhr', label: 'Noise-to-harmonics ratio', type: 'number', required: true, min: 0.00065, max: 0.31482, step: 0.00001 },
        { name: 'hnr', label: 'Harmonics-to-noise ratio', type: 'number', required: true, min: 8.441, max: 33.047, step: 0.001, unit: 'dB' },
        { name: 'rpde', label: 'Recurrence period density entropy', type: 'number', required: true, min: 0.256570, max: 0.685151, step: 0.000001 },
        { name: 'dfa', label: 'Detrended fluctuation analysis', type: 'number', required: true, min: 0.574282, max: 0.825288, step: 0.000001 },
        { name: 'spread1', label: 'Nonlinear measure of fundamental frequency variation', type: 'number', required: true, min: -7.964984, max: -2.434031, step: 0.000001 },
        { name: 'spread2', label: 'Nonlinear measure of fundamental frequency variation', type: 'number', required: true, min: 0.006274, max: 0.450493, step: 0.000001 },
        { name: 'd2', label: 'Nonlinear dynamical complexity measure', type: 'number', required: true, min: 1.423287, max: 3.671155, step: 0.000001 },
        { name: 'ppe', label: 'Pitch period entropy', type: 'number', required: true, min: 0.044539, max: 0.527367, step: 0.000001 }
      ]
    },
    covid_risk: {
      id: 'covid_risk',
      name: 'COVID-19 Risk Assessment',
      description: 'Assess COVID-19 infection risk and severity based on symptoms, exposure, and health factors.',
      category: 'Disease Risk & Diagnosis',
      icon: Shield,
      difficulty: 'Easy',
      estimatedTime: '3-5 min',
      accuracy: '86%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 0, max: 120, unit: 'years' },
        { name: 'gender', label: 'Gender', type: 'select', required: true, options: ['Male', 'Female', 'Other'] },
        { name: 'fever', label: 'Fever (>100.4°F)', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'cough', label: 'Cough', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'shortness_of_breath', label: 'Shortness of Breath', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'fatigue', label: 'Fatigue', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'loss_of_taste_smell', label: 'Loss of Taste or Smell', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'close_contact', label: 'Close Contact with COVID-19 Case', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'travel_history', label: 'Recent Travel to High-Risk Area', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'underlying_conditions', label: 'Underlying Health Conditions', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'vaccination_status', label: 'COVID-19 Vaccination Status', type: 'select', required: true, options: ['Unvaccinated', 'Partially Vaccinated', 'Fully Vaccinated', 'Boosted'] }
      ]
    },
    asthma_copd: {
      id: 'asthma_copd',
      name: 'Asthma & COPD Predictor',
      description: 'Respiratory health assessment for asthma and COPD using lung function and symptom data.',
      category: 'Disease Risk & Diagnosis',
      icon: Activity,
      difficulty: 'Medium',
      estimatedTime: '6-8 min',
      accuracy: '90%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 18, max: 120, unit: 'years' },
        { name: 'gender', label: 'Gender', type: 'select', required: true, options: ['Male', 'Female'] },
        { name: 'smoking_history', label: 'Smoking History', type: 'select', required: true, options: ['Never Smoked', 'Former Smoker', 'Current Smoker'] },
        { name: 'pack_years', label: 'Pack Years (if applicable)', type: 'number', required: false, min: 0, max: 100, unit: 'pack-years' },
        { name: 'shortness_of_breath', label: 'Shortness of Breath', type: 'select', required: true, options: ['None', 'Mild', 'Moderate', 'Severe'] },
        { name: 'wheezing', label: 'Wheezing', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'chronic_cough', label: 'Chronic Cough', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'sputum_production', label: 'Sputum Production', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'chest_tightness', label: 'Chest Tightness', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'family_history', label: 'Family History of Respiratory Disease', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'occupational_exposure', label: 'Occupational Exposure to Dust/Chemicals', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'allergies', label: 'Known Allergies', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'exercise_tolerance', label: 'Exercise Tolerance', type: 'select', required: true, options: ['Normal', 'Mildly Reduced', 'Moderately Reduced', 'Severely Reduced'] }
      ]
    },
    anemia: {
      id: 'anemia',
      name: 'Anemia Detection',
      description: 'Iron deficiency and anemia detection using blood test parameters and symptoms.',
      category: 'Disease Risk & Diagnosis',
      icon: Droplets,
      difficulty: 'Easy',
      estimatedTime: '4-6 min',
      accuracy: '93%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 0, max: 120, unit: 'years' },
        { name: 'gender', label: 'Gender', type: 'select', required: true, options: ['Male', 'Female'] },
        { name: 'hemoglobin', label: 'Hemoglobin Level', type: 'number', required: true, min: 3, max: 20, step: 0.1, unit: 'g/dL' },
        { name: 'hematocrit', label: 'Hematocrit', type: 'number', required: true, min: 10, max: 60, step: 0.1, unit: '%' },
        { name: 'mcv', label: 'Mean Corpuscular Volume (MCV)', type: 'number', required: true, min: 60, max: 120, unit: 'fL' },
        { name: 'mch', label: 'Mean Corpuscular Hemoglobin (MCH)', type: 'number', required: true, min: 20, max: 40, step: 0.1, unit: 'pg' },
        { name: 'mchc', label: 'Mean Corpuscular Hemoglobin Concentration (MCHC)', type: 'number', required: true, min: 28, max: 38, step: 0.1, unit: 'g/dL' },
        { name: 'fatigue', label: 'Fatigue', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'weakness', label: 'Weakness', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'pale_skin', label: 'Pale Skin', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'shortness_of_breath', label: 'Shortness of Breath', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'cold_hands_feet', label: 'Cold Hands or Feet', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'brittle_nails', label: 'Brittle or Spoon-shaped Nails', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'heavy_menstrual_periods', label: 'Heavy Menstrual Periods (if applicable)', type: 'radio', required: false, options: ['Yes', 'No'] },
        { name: 'dietary_iron_intake', label: 'Adequate Dietary Iron Intake', type: 'radio', required: true, options: ['Yes', 'No'] }
      ]
    },
    nutrition_analysis: {
      id: 'nutrition_analysis',
      name: 'Nutrition & Diet Analysis',
      description: 'Personalized nutrition recommendations and deficiency detection based on dietary habits.',
      category: 'Lifestyle & Prevention',
      icon: Apple,
      difficulty: 'Easy',
      estimatedTime: '5-7 min',
      accuracy: '82%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 18, max: 120, unit: 'years' },
        { name: 'gender', label: 'Gender', type: 'select', required: true, options: ['Male', 'Female'] },
        { name: 'weight', label: 'Weight', type: 'number', required: true, min: 30, max: 300, unit: 'kg' },
        { name: 'height', label: 'Height', type: 'number', required: true, min: 100, max: 250, unit: 'cm' },
        { name: 'activity_level', label: 'Physical Activity Level', type: 'select', required: true, options: ['Sedentary', 'Lightly Active', 'Moderately Active', 'Very Active', 'Extremely Active'] },
        { name: 'dietary_restrictions', label: 'Dietary Restrictions', type: 'select', required: true, options: ['None', 'Vegetarian', 'Vegan', 'Gluten-Free', 'Keto', 'Paleo', 'Other'] },
        { name: 'meals_per_day', label: 'Meals per Day', type: 'number', required: true, min: 1, max: 10 },
        { name: 'water_intake', label: 'Daily Water Intake', type: 'number', required: true, min: 0, max: 10, step: 0.1, unit: 'liters' },
        { name: 'fruit_vegetable_servings', label: 'Daily Fruit & Vegetable Servings', type: 'number', required: true, min: 0, max: 20 },
        { name: 'processed_food_frequency', label: 'Processed Food Frequency', type: 'select', required: true, options: ['Never', 'Rarely', 'Sometimes', 'Often', 'Daily'] },
        { name: 'supplement_use', label: 'Supplement Use', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'cooking_frequency', label: 'Home Cooking Frequency', type: 'select', required: true, options: ['Never', 'Rarely', 'Sometimes', 'Often', 'Daily'] }
      ]
    },
    fitness_assessment: {
      id: 'fitness_assessment',
      name: 'Fitness & Exercise Assessment',
      description: 'Comprehensive fitness evaluation and personalized workout recommendations.',
      category: 'Lifestyle & Prevention',
      icon: Dumbbell,
      difficulty: 'Medium',
      estimatedTime: '6-8 min',
      accuracy: '85%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 18, max: 120, unit: 'years' },
        { name: 'gender', label: 'Gender', type: 'select', required: true, options: ['Male', 'Female'] },
        { name: 'current_fitness_level', label: 'Current Fitness Level', type: 'select', required: true, options: ['Beginner', 'Intermediate', 'Advanced', 'Elite'] },
        { name: 'exercise_frequency', label: 'Exercise Frequency per Week', type: 'number', required: true, min: 0, max: 14, unit: 'times' },
        { name: 'exercise_duration', label: 'Average Exercise Duration', type: 'number', required: true, min: 0, max: 300, unit: 'minutes' },
        { name: 'preferred_activities', label: 'Preferred Exercise Activities', type: 'select', required: true, options: ['Cardio', 'Strength Training', 'Yoga/Pilates', 'Sports', 'Mixed'] },
        { name: 'fitness_goals', label: 'Primary Fitness Goals', type: 'select', required: true, options: ['Weight Loss', 'Muscle Gain', 'Endurance', 'Flexibility', 'General Health'] },
        { name: 'resting_heart_rate', label: 'Resting Heart Rate', type: 'number', required: true, min: 40, max: 120, unit: 'bpm' },
        { name: 'injuries_limitations', label: 'Current Injuries or Limitations', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'sleep_quality', label: 'Sleep Quality', type: 'select', required: true, options: ['Poor', 'Fair', 'Good', 'Excellent'] },
        { name: 'stress_level', label: 'Stress Level (1-10)', type: 'number', required: true, min: 1, max: 10 },
        { name: 'recovery_time', label: 'Recovery Time Between Workouts', type: 'select', required: true, options: ['<24 hours', '24-48 hours', '48-72 hours', '>72 hours'] }
      ]
    },
    sleep_analysis: {
      id: 'sleep_analysis',
      name: 'Sleep Quality Analysis',
      description: 'Sleep pattern analysis and insomnia detection using wearable data and sleep surveys.',
      category: 'Lifestyle & Prevention',
      icon: Moon,
      difficulty: 'Easy',
      estimatedTime: '4-6 min',
      accuracy: '87%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 18, max: 120, unit: 'years' },
        { name: 'gender', label: 'Gender', type: 'select', required: true, options: ['Male', 'Female', 'Other'] },
        { name: 'bedtime', label: 'Usual Bedtime', type: 'time', required: true },
        { name: 'wake_time', label: 'Usual Wake Time', type: 'time', required: true },
        { name: 'sleep_duration', label: 'Average Sleep Duration', type: 'number', required: true, min: 0, max: 24, step: 0.5, unit: 'hours' },
        { name: 'time_to_fall_asleep', label: 'Time to Fall Asleep', type: 'number', required: true, min: 0, max: 180, unit: 'minutes' },
        { name: 'night_awakenings', label: 'Night Awakenings per Night', type: 'number', required: true, min: 0, max: 20 },
        { name: 'sleep_quality_rating', label: 'Sleep Quality Rating (1-10)', type: 'number', required: true, min: 1, max: 10 },
        { name: 'morning_alertness', label: 'Morning Alertness', type: 'select', required: true, options: ['Very Groggy', 'Groggy', 'Neutral', 'Alert', 'Very Alert'] },
        { name: 'daytime_fatigue', label: 'Daytime Fatigue', type: 'select', required: true, options: ['Never', 'Rarely', 'Sometimes', 'Often', 'Always'] },
        { name: 'caffeine_intake', label: 'Daily Caffeine Intake', type: 'select', required: true, options: ['None', 'Low (1-2 cups)', 'Moderate (3-4 cups)', 'High (5+ cups)'] },
        { name: 'screen_time_before_bed', label: 'Screen Time Before Bed', type: 'select', required: true, options: ['None', '<30 min', '30-60 min', '1-2 hours', '>2 hours'] },
        { name: 'sleep_environment', label: 'Sleep Environment Quality', type: 'select', required: true, options: ['Poor', 'Fair', 'Good', 'Excellent'] },
        { name: 'snoring', label: 'Snoring', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'sleep_medications', label: 'Sleep Medications/Aids', type: 'radio', required: true, options: ['Yes', 'No'] }
      ]
    },
    stress_burnout: {
      id: 'stress_burnout',
      name: 'Stress & Burnout Assessment',
      description: 'Workplace stress and burnout detection with personalized coping strategies.',
      category: 'Lifestyle & Prevention',
      icon: AlertTriangle,
      difficulty: 'Medium',
      estimatedTime: '7-9 min',
      accuracy: '83%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 18, max: 120, unit: 'years' },
        { name: 'occupation', label: 'Occupation Type', type: 'select', required: true, options: ['Healthcare', 'Education', 'Technology', 'Finance', 'Retail', 'Manufacturing', 'Other'] },
        { name: 'work_hours_per_week', label: 'Work Hours per Week', type: 'number', required: true, min: 0, max: 100, unit: 'hours' },
        { name: 'work_stress_level', label: 'Work Stress Level (1-10)', type: 'number', required: true, min: 1, max: 10 },
        { name: 'job_satisfaction', label: 'Job Satisfaction', type: 'select', required: true, options: ['Very Dissatisfied', 'Dissatisfied', 'Neutral', 'Satisfied', 'Very Satisfied'] },
        { name: 'work_life_balance', label: 'Work-Life Balance', type: 'select', required: true, options: ['Very Poor', 'Poor', 'Fair', 'Good', 'Excellent'] },
        { name: 'emotional_exhaustion', label: 'Emotional Exhaustion', type: 'select', required: true, options: ['Never', 'Rarely', 'Sometimes', 'Often', 'Always'] },
        { name: 'cynicism', label: 'Cynicism/Detachment', type: 'select', required: true, options: ['Never', 'Rarely', 'Sometimes', 'Often', 'Always'] },
        { name: 'personal_accomplishment', label: 'Sense of Personal Accomplishment', type: 'select', required: true, options: ['Very Low', 'Low', 'Moderate', 'High', 'Very High'] },
        { name: 'physical_symptoms', label: 'Physical Stress Symptoms', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'sleep_problems', label: 'Sleep Problems Due to Stress', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'coping_strategies', label: 'Current Coping Strategies', type: 'select', required: true, options: ['None', 'Exercise', 'Meditation', 'Social Support', 'Professional Help', 'Multiple'] },
        { name: 'support_system', label: 'Support System Quality', type: 'select', required: true, options: ['Very Poor', 'Poor', 'Fair', 'Good', 'Excellent'] }
      ]
    },
    mental_health: {
      id: 'mental_health',
      name: 'Mental Health Predictor',
      description: 'Depression and anxiety detection using surveys, voice analysis, and wearable data.',
      category: 'Lifestyle & Prevention',
      icon: Brain,
      difficulty: 'Medium',
      estimatedTime: '8-10 min',
      accuracy: '84%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 18, max: 100, unit: 'years' },
        { name: 'gender', label: 'Gender', type: 'select', required: true, options: ['Male', 'Female', 'Other'] },
        { name: 'sleep_hours', label: 'Average Sleep Hours per Night', type: 'number', required: true, min: 0, max: 24, step: 0.5, unit: 'hours' },
        { name: 'stress_level', label: 'Stress Level (1-10)', type: 'number', required: true, min: 1, max: 10 },
        { name: 'social_support', label: 'Social Support Level', type: 'select', required: true, options: ['Very Low', 'Low', 'Moderate', 'High', 'Very High'] },
        { name: 'exercise_frequency', label: 'Exercise Frequency per Week', type: 'number', required: true, min: 0, max: 14, unit: 'times' },
        { name: 'work_satisfaction', label: 'Work/Life Satisfaction', type: 'select', required: true, options: ['Very Dissatisfied', 'Dissatisfied', 'Neutral', 'Satisfied', 'Very Satisfied'] },
        { name: 'family_history', label: 'Family History of Mental Health Issues', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'substance_use', label: 'Substance Use', type: 'select', required: true, options: ['None', 'Occasional', 'Regular', 'Heavy'] },
        { name: 'chronic_illness', label: 'Chronic Illness', type: 'radio', required: true, options: ['Yes', 'No'] }
      ]
    },
    thyroid_disorders: {
      id: 'thyroid_disorders',
      name: 'Thyroid Disorder Predictor',
      description: 'Detect hyperthyroidism and hypothyroidism using thyroid function tests.',
      category: 'Specialized Care',
      icon: Activity,
      difficulty: 'Medium',
      estimatedTime: '4-6 min',
      accuracy: '90%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 18, max: 120, unit: 'years' },
        { name: 'sex', label: 'Sex', type: 'select', required: true, options: ['Male', 'Female'] },
        { name: 'tsh', label: 'TSH Level', type: 'number', required: true, min: 0.1, max: 50, step: 0.1, unit: 'mIU/L' },
        { name: 't3', label: 'T3 Level', type: 'number', required: true, min: 0.5, max: 10, step: 0.1, unit: 'pg/mL' },
        { name: 't4', label: 'T4 Level', type: 'number', required: true, min: 0.5, max: 25, step: 0.1, unit: 'μg/dL' },
        { name: 'family_history_thyroid', label: 'Family History of Thyroid Disease', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'weight_changes', label: 'Recent Weight Changes', type: 'select', required: true, options: ['Significant Loss', 'Moderate Loss', 'No Change', 'Moderate Gain', 'Significant Gain'] },
        { name: 'heart_rate', label: 'Resting Heart Rate', type: 'number', required: true, min: 40, max: 150, unit: 'bpm' },
        { name: 'fatigue_level', label: 'Fatigue Level', type: 'select', required: true, options: ['None', 'Mild', 'Moderate', 'Severe'] },
        { name: 'heat_cold_intolerance', label: 'Temperature Intolerance', type: 'select', required: true, options: ['Heat Intolerance', 'Cold Intolerance', 'Neither', 'Both'] },
        { name: 'sleep_changes', label: 'Sleep Pattern Changes', type: 'select', required: true, options: ['Insomnia', 'Excessive Sleep', 'No Change'] },
        { name: 'mood_changes', label: 'Mood Changes', type: 'select', required: true, options: ['Anxiety/Irritability', 'Depression', 'Mood Swings', 'No Change'] }
      ]
    },
    cancer_recurrence: {
      id: 'cancer_recurrence',
      name: 'Cancer Recurrence Predictor',
      description: 'Predict likelihood of cancer recurrence after successful treatment.',
      category: 'Specialized Care',
      icon: Shield,
      difficulty: 'Advanced',
      estimatedTime: '8-10 min',
      accuracy: '85%',
      fields: [
        { name: 'age_at_diagnosis', label: 'Age at Initial Diagnosis', type: 'number', required: true, min: 18, max: 100, unit: 'years' },
        { name: 'cancer_type', label: 'Cancer Type', type: 'select', required: true, options: ['Breast', 'Lung', 'Colorectal', 'Prostate', 'Ovarian', 'Other'] },
        { name: 'cancer_stage', label: 'Initial Cancer Stage', type: 'select', required: true, options: ['Stage I', 'Stage II', 'Stage III', 'Stage IV'] },
        { name: 'tumor_size', label: 'Initial Tumor Size', type: 'number', required: true, min: 0.1, max: 20, step: 0.1, unit: 'cm' },
        { name: 'lymph_nodes_affected', label: 'Lymph Nodes Affected', type: 'number', required: true, min: 0, max: 50 },
        { name: 'treatment_type', label: 'Primary Treatment', type: 'select', required: true, options: ['Surgery Only', 'Surgery + Chemotherapy', 'Surgery + Radiation', 'Surgery + Chemo + Radiation', 'Chemotherapy Only', 'Radiation Only'] },
        { name: 'months_since_treatment', label: 'Months Since Treatment Completion', type: 'number', required: true, min: 1, max: 120, unit: 'months' },
        { name: 'hormone_receptor_status', label: 'Hormone Receptor Status', type: 'select', required: true, options: ['Positive', 'Negative', 'Unknown'] },
        { name: 'genetic_markers', label: 'High-Risk Genetic Markers', type: 'radio', required: true, options: ['Yes', 'No', 'Unknown'] },
        { name: 'family_history_cancer', label: 'Family History of Cancer', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'lifestyle_factors', label: 'High-Risk Lifestyle Factors', type: 'select', required: true, options: ['Smoking', 'Heavy Alcohol Use', 'Poor Diet', 'Sedentary Lifestyle', 'Multiple Factors', 'None'] },
        { name: 'follow_up_compliance', label: 'Follow-up Appointment Compliance', type: 'select', required: true, options: ['Excellent', 'Good', 'Fair', 'Poor'] },
        { name: 'current_symptoms', label: 'Current Concerning Symptoms', type: 'radio', required: true, options: ['Yes', 'No'] }
      ]
    },
    diabetes: {
      id: 'diabetes',
      name: 'Diabetes Risk Predictor',
      description: 'Assess diabetes risk using glucose levels, BMI, family history, and lifestyle factors.',
      category: 'Disease Risk & Diagnosis',
      icon: Activity,
      difficulty: 'Medium',
      estimatedTime: '5-7 min',
      accuracy: '87%',
      fields: [
        { name: 'age', label: 'Age', type: 'number', required: true, min: 18, max: 120, unit: 'years' },
        { name: 'gender', label: 'Gender', type: 'select', required: true, options: ['Male', 'Female'] },
        { name: 'bmi', label: 'Body Mass Index (BMI)', type: 'number', required: true, min: 15, max: 50, step: 0.1, unit: 'kg/m²' },
        { name: 'glucose_level', label: 'Fasting Glucose Level', type: 'number', required: true, min: 70, max: 300, unit: 'mg/dL' },
        { name: 'blood_pressure', label: 'Systolic Blood Pressure', type: 'number', required: true, min: 80, max: 200, unit: 'mmHg' },
        { name: 'family_history_diabetes', label: 'Family History of Diabetes', type: 'radio', required: true, options: ['Yes', 'No'] },
        { name: 'physical_activity', label: 'Physical Activity Level', type: 'select', required: true, options: ['Sedentary', 'Light', 'Moderate', 'High'] },
        { name: 'smoking_status', label: 'Smoking Status', type: 'select', required: true, options: ['Never', 'Former', 'Current'] },
        { name: 'alcohol_consumption', label: 'Alcohol Consumption', type: 'select', required: true, options: ['None', 'Light', 'Moderate', 'Heavy'] },
        { name: 'stress_level', label: 'Stress Level (1-10)', type: 'number', required: true, min: 1, max: 10 },
        { name: 'sleep_hours', label: 'Average Sleep Hours per Night', type: 'number', required: true, min: 3, max: 12, step: 0.5, unit: 'hours' },
        { name: 'waist_circumference', label: 'Waist Circumference', type: 'number', required: true, min: 50, max: 150, unit: 'cm' }
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
      const isStaticMode = process.env.REACT_APP_STATIC_MODE === 'true';
      
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
        
        setResult(mockResult);
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
      case 'High': return 'text-orange-600 dark:text-orange-400 bg-orange-100 dark:bg-orange-900/30';
      case 'Critical': return 'text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-900/30';
      default: return 'text-gray-600 dark:text-gray-400 bg-gray-100 dark:bg-gray-800';
    }
  };

  const getRiskIcon = (riskLevel: string) => {
    switch (riskLevel) {
      case 'Low': return CheckCircle;
      case 'Medium': return Info;
      case 'High': return AlertTriangle;
      case 'Critical': return AlertTriangle;
      default: return Info;
    }
  };

  const handleDownloadPDF = async () => {
    if (!result || !predictor) return;
    
    // Check if we're in static mode (no backend)
    const isStaticMode = process.env.REACT_APP_STATIC_MODE === 'true';
    
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
    const value = formData[field.name] || '';
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
                  value={value}
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
              {/* Form Header with Progress */}
              <div className="mb-8">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Health Assessment Form</h2>
                  <div className="text-sm text-gray-500 dark:text-gray-400">
                    {Math.round(formProgress)}% Complete
                  </div>
                </div>
                
                {/* Progress Bar */}
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-6">
                  <div 
                    className="bg-gradient-to-r from-blue-500 to-blue-600 h-2 rounded-full transition-all duration-500 ease-out"
                    style={{ width: `${formProgress}%` }}
                  ></div>
                </div>
                
                <p className="text-gray-600 dark:text-gray-300 mb-4">
                  Please fill out all required fields to get your personalized health assessment.
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
                {/* Form Fields organized by sections */}
                <div className="space-y-8">
                  {/* Basic Information Section */}
                  <div className="border-b border-gray-200 dark:border-gray-700 pb-6">
                    <div className="flex items-center gap-2 mb-4">
                      <User className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Basic Information</h3>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
                      {predictor?.fields?.filter(field => 
                        ['age', 'gender', 'sex', 'ever_married', 'work_type', 'residence_type'].includes(field.name)
                      ).map(renderField)}
                    </div>
                  </div>

                  {/* Health Metrics Section */}
                  <div className="border-b border-gray-200 dark:border-gray-700 pb-6">
                    <div className="flex items-center gap-2 mb-4">
                      <Heart className="h-5 w-5 text-red-600 dark:text-red-400" />
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Health Metrics</h3>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
                      {predictor?.fields?.filter(field => 
                        ['resting_bp', 'cholesterol', 'fasting_bs', 'avg_glucose_level', 'bmi', 'max_hr', 'oldpeak'].includes(field.name)
                      ).map(renderField)}
                    </div>
                  </div>

                  {/* Medical History Section */}
                  <div className="border-b border-gray-200 dark:border-gray-700 pb-6">
                    <div className="flex items-center gap-2 mb-4">
                      <FileText className="h-5 w-5 text-green-600 dark:text-green-400" />
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Medical History</h3>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
                      {predictor?.fields?.filter(field => 
                        ['hypertension', 'heart_disease', 'chest_pain_type', 'resting_ecg', 'exercise_angina', 'family_history', 'chronic_illness', 'family_history_diabetes', 'glucose_level', 'blood_pressure', 'insulin_level', 'pregnancies', 'skin_thickness', 'diabetes_pedigree_function'].includes(field.name)
                      ).map(renderField)}
                    </div>
                  </div>

                  {/* Lifestyle Factors Section */}
                  <div className="pb-6">
                    <div className="flex items-center gap-2 mb-4">
                      <Activity className="h-5 w-5 text-purple-600 dark:text-purple-400" />
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Lifestyle Factors</h3>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
                      {predictor?.fields?.filter(field => 
                        ['smoking_status', 'sleep_hours', 'stress_level', 'social_support', 'exercise_frequency', 'work_satisfaction', 'substance_use', 'physical_activity', 'alcohol_consumption', 'waist_circumference'].includes(field.name)
                      ).map(renderField)}
                    </div>
                  </div>

                  {/* Other Fields Section */}
                  {predictor?.fields?.filter(field => 
                    !['age', 'gender', 'sex', 'ever_married', 'work_type', 'residence_type', 
                      'resting_bp', 'cholesterol', 'fasting_bs', 'avg_glucose_level', 'bmi', 'max_hr', 'oldpeak',
                      'hypertension', 'heart_disease', 'chest_pain_type', 'resting_ecg', 'exercise_angina', 'family_history', 'chronic_illness', 'family_history_diabetes', 'glucose_level', 'blood_pressure', 'insulin_level', 'pregnancies', 'skin_thickness', 'diabetes_pedigree_function',
                      'smoking_status', 'sleep_hours', 'stress_level', 'social_support', 'exercise_frequency', 'work_satisfaction', 'substance_use', 'physical_activity', 'alcohol_consumption', 'waist_circumference'].includes(field.name)
                  ).length > 0 && (
                    <div className="pb-6">
                      <div className="flex items-center gap-2 mb-4">
                        <BarChart3 className="h-5 w-5 text-gray-600 dark:text-gray-400" />
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Additional Information</h3>
                      </div>
                      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        {predictor?.fields?.filter(field => 
                          !['age', 'gender', 'sex', 'ever_married', 'work_type', 'residence_type', 
                            'resting_bp', 'cholesterol', 'fasting_bs', 'avg_glucose_level', 'bmi', 'max_hr', 'oldpeak',
                            'hypertension', 'heart_disease', 'chest_pain_type', 'resting_ecg', 'exercise_angina', 'family_history', 'chronic_illness', 'family_history_diabetes', 'glucose_level', 'blood_pressure', 'insulin_level', 'pregnancies', 'skin_thickness', 'diabetes_pedigree_function',
                            'smoking_status', 'sleep_hours', 'stress_level', 'social_support', 'exercise_frequency', 'work_satisfaction', 'substance_use', 'physical_activity', 'alcohol_consumption', 'waist_circumference'].includes(field.name)
                        ).map(renderField)}
                      </div>
                    </div>
                  )}
                </div>
                
                {/* Form Actions */}
                <div className="flex flex-col sm:flex-row items-center justify-between pt-8 border-t border-gray-200 dark:border-gray-700">
                  <div className="flex items-center text-sm text-gray-500 dark:text-gray-400 mb-4 sm:mb-0">
                    <CheckCircle className="h-4 w-4 mr-2 text-green-500" />
                    <span>
                      {Object.values(formData).filter(val => val !== '' && val !== null && val !== undefined).length} of {predictor?.fields?.length || 0} fields completed
                    </span>
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
                            ? result.detailed_analysis.lifestyle_impact.slice(0, 4).map(item => item.description || item.factor)
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