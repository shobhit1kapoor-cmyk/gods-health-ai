# Gods Health AI - Comprehensive Health Prediction Platform

🏥 **Advanced AI-Powered Health Risk Assessment & Disease Prediction System**

A comprehensive health AI platform that provides predictive analytics for various diseases, conditions, and health risks using machine learning models.

## ✨ **NEW: Enhanced Prediction System**

🔬 **Advanced Analysis Features**:
- **Contributing Factors Analysis** - Identify key factors influencing health predictions
- **Health Metrics Assessment** - Detailed analysis of health indicators with status and recommendations
- **Lifestyle Impact Evaluation** - Comprehensive lifestyle factor analysis with improvement suggestions
- **Enhanced API Endpoints** - New `/analyze` endpoint and enhanced `/predict` with detailed analysis
- **Rich UI Components** - Beautiful, responsive analysis displays with actionable insights

📖 **[View Enhanced System Documentation](./ENHANCED_PREDICTION_SYSTEM.md)** for detailed technical information.

## 🔹 Disease Risk & Diagnosis Predictors
- **Heart Disease Predictor** - Predict risk of heart attack, arrhythmia, or heart failure
- **Stroke Risk Predictor** - Analyze blood pressure, cholesterol, lifestyle, family history
- **Cancer Detection & Risk Predictor** - Breast, lung, prostate, skin, cervical cancers
- **Kidney Disease Predictor** - Chronic kidney disease detection from blood/urine data
- **Liver Disease Predictor** - Hepatitis, cirrhosis, fatty liver detection from lab tests
- **Alzheimer's / Dementia Predictor** - Early detection using memory & behavioral data
- **Parkinson's Disease Predictor** - Voice patterns, tremor, movement analysis

## 🔹 Condition & Complication Predictors
- **Sepsis Predictor** - Early detection in hospitals (life-saving use case)
- **Hospital Readmission Predictor** - Predict if a patient will need to come back soon
- **ICU Mortality Predictor** - Survival prediction based on vitals & lab results
- **Post-Surgery Complication Predictor** - Predict risks after major surgeries
- **Pregnancy Complication Predictor** - Gestational diabetes, preeclampsia

## 🔹 Lifestyle & Preventive Health Predictors
- **Obesity & BMI Risk Predictor** - Long-term obesity complications
- **Hypertension Predictor** - Lifestyle & genetic risk factors
- **Cholesterol & Atherosclerosis Risk Predictor** - Plaque buildup leading to stroke/heart attack
- **Mental Health Predictor** - Depression, anxiety detection from surveys/voice/wearables
- **Sleep Apnea & Sleep Disorder Predictor** - Using wearable or questionnaire data

## 🔹 Specialized Predictors
- **COVID-19 / Infectious Disease Predictor** - Severity, hospitalization risk
- **Asthma & COPD Predictor** - Respiratory disease progression
- **Anemia Predictor** - Using blood test values
- **Thyroid Disorder Predictor** - Hyper/hypothyroidism detection
- **Cancer Recurrence Predictor** - Predict if cancer might return after treatment

## 🚀 Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Test Enhanced Features
```bash
# Test enhanced API endpoints
cd backend
python test_enhanced_api.py
```

Access the application at `http://localhost:3000` and experience the enhanced prediction analysis!

## 🏗️ Project Structure
```
Gods Health AI/
├── backend/
│   ├── app.py
│   ├── models/
│   ├── predictors/
│   ├── data/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
└── README.md
```

## 🌐 Live Demo & Deployment

### 🚀 GitHub Pages (Static Demo)
Experience the frontend interface with mock data:
**[https://shobhit1kapoor-cmyk.github.io/gods-health-ai/](https://shobhit1kapoor-cmyk.github.io/gods-health-ai/)**

*Note: This is a static demo using mock prediction data. For full functionality with real AI predictions, a backend deployment is required.*

### 📱 Static Mode Features
- ✅ Complete UI/UX experience
- ✅ Form validation and interactions
- ✅ Mock health predictions with realistic data
- ✅ Responsive design showcase
- ❌ PDF report generation (requires backend)
- ❌ Real AI model predictions (requires backend)

## 🔬 Technology Stack
- **Backend**: Python, Flask, Scikit-learn, TensorFlow, Pandas, NumPy
- **Frontend**: React, TypeScript, Tailwind CSS, Framer Motion, Axios
- **Enhanced Features**: Advanced ML analysis methods, detailed health insights
- **Database**: SQLite/PostgreSQL
- **Deployment**: GitHub Pages (Static), Docker, AWS/Heroku (Full Stack)

## 📊 Enhanced Features

### Detailed Analysis Components
- **22 Enhanced Predictors** - All predictors now include advanced analysis methods
- **Contributing Factors** - Visual identification of key risk factors
- **Health Metrics Dashboard** - Color-coded status indicators and recommendations
- **Lifestyle Impact Assessment** - Personalized improvement suggestions
- **Responsive Design** - Mobile-friendly analysis displays

### API Enhancements
- **Enhanced `/predict`** - Optional detailed analysis with `include_analysis` parameter
- **New `/analyze`** - Analysis-only endpoint for health insights without prediction
- **Enhanced Fields** - `supports_enhanced_analysis` indicator for predictor capabilities

## ⚠️ Disclaimer
This application is for educational and research purposes only. Always consult with healthcare professionals for medical advice and diagnosis.