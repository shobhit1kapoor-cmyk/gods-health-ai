from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import numpy as np
import os
from datetime import datetime
from pdf_generator import HealthReportGenerator

from predictors import (
    # Disease Risk & Diagnosis Predictors
    HeartDiseasePredictor,
    StrokeRiskPredictor,
    CancerDetectionPredictor,
    KidneyDiseasePredictor,
    LiverDiseasePredictor,
    AlzheimerPredictor,
    ParkinsonPredictor,
    # Condition & Complication Predictors
    SepsisPredictor,
    HospitalReadmissionPredictor,
    ICUMortalityPredictor,
    PostSurgeryComplicationPredictor,
    PregnancyComplicationPredictor,
    # Lifestyle & Preventive Health Predictors
    ObesityRiskPredictor,
    HypertensionPredictor,
    CholesterolRiskPredictor,
    MentalHealthPredictor,
    SleepApneaPredictor,
    # Specialized Predictors
    CovidRiskPredictor,
    AsthmaCopdPredictor,
    AnemiaPredictor,
    ThyroidDisorderPredictor,
    CancerRecurrencePredictor
)

app = Flask(__name__)
# Configure CORS for both development and production
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://shobhit1kapoor-cmyk.github.io",
    "https://gods-health-ai.netlify.app"
]
CORS(app, origins=allowed_origins)

# Initialize predictors
predictors = {
    # Disease Risk & Diagnosis Predictors
    "heart_disease": HeartDiseasePredictor(),
    "stroke_risk": StrokeRiskPredictor(),
    "cancer_detection": CancerDetectionPredictor(),
    "kidney_disease": KidneyDiseasePredictor(),
    "liver_disease": LiverDiseasePredictor(),
    "alzheimer": AlzheimerPredictor(),
    "parkinson": ParkinsonPredictor(),
    
    # Condition & Complication Predictors
    "sepsis": SepsisPredictor(),
    "hospital_readmission": HospitalReadmissionPredictor(),
    "icu_mortality": ICUMortalityPredictor(),
    "post_surgery_complication": PostSurgeryComplicationPredictor(),
    "pregnancy_complication": PregnancyComplicationPredictor(),
    
    # Lifestyle & Preventive Health Predictors
    "obesity_risk": ObesityRiskPredictor(),
    "hypertension": HypertensionPredictor(),
    "cholesterol_risk": CholesterolRiskPredictor(),
    "mental_health": MentalHealthPredictor(),
    "sleep_apnea": SleepApneaPredictor(),
    
    # Specialized Predictors
    "covid_risk": CovidRiskPredictor(),
    "asthma_copd": AsthmaCopdPredictor(),
    "anemia": AnemiaPredictor(),
    "thyroid_disorder": ThyroidDisorderPredictor(),
    "cancer_recurrence": CancerRecurrencePredictor()
}

@app.route("/")
def root():
    return jsonify({
        "message": "Welcome to Gods Health AI - Comprehensive Health Prediction Platform",
        "version": "1.0.0",
        "available_predictors": list(predictors.keys()),
        "total_predictors": len(predictors)
    })

@app.route("/predictors")
def get_available_predictors():
    """Get list of all available predictors with their descriptions"""
    predictor_info = {}
    for name, predictor in predictors.items():
        predictor_info[name] = {
            "name": predictor.name,
            "description": predictor.description,
            "required_fields": predictor.get_required_fields()
        }
    return jsonify(predictor_info)

@app.route("/predict", methods=["POST"])
def make_prediction():
    """Make a health prediction using the specified predictor with enhanced analysis"""
    try:
        data = request.get_json()
        predictor_type = data.get("predictor_type")
        input_data = data.get("data")
        include_analysis = data.get("include_analysis", True)  # Default to True for enhanced analysis
        
        if predictor_type not in predictors:
            return jsonify({
                "error": f"Predictor '{predictor_type}' not found. Available predictors: {list(predictors.keys())}"
            }), 400
        
        predictor = predictors[predictor_type]
        result = predictor.predict(input_data)
        
        # Base response
        response = {
            "predictor_type": predictor_type,
            "risk_score": result["risk_score"],
            "risk_level": result["risk_level"],
            "recommendations": result["recommendations"],
            "confidence": result["confidence"],
            "timestamp": datetime.now().isoformat()
        }
        
        # Add enhanced analysis if requested and predictor supports it
        if include_analysis and hasattr(predictor, 'identify_contributing_factors'):
            try:
                response["detailed_analysis"] = {
                    "contributing_factors": predictor.identify_contributing_factors(input_data),
                    "health_metrics": predictor.analyze_health_metrics(input_data),
                    "lifestyle_impact": predictor.assess_lifestyle_impact(input_data)
                }
            except Exception as analysis_error:
                # If analysis fails, still return basic prediction but log the error
                response["analysis_error"] = f"Enhanced analysis failed: {str(analysis_error)}"
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": f"Prediction error: {str(e)}"}), 500

@app.route("/predictor/<predictor_type>/fields")
def get_predictor_fields(predictor_type):
    """Get required input fields for a specific predictor"""
    if predictor_type not in predictors:
        return jsonify({
            "error": f"Predictor '{predictor_type}' not found"
        }), 404
    
    predictor = predictors[predictor_type]
    return jsonify({
        "predictor_type": predictor_type,
        "name": predictor.name,
        "description": predictor.description,
        "required_fields": predictor.get_required_fields(),
        "field_descriptions": predictor.get_field_descriptions(),
        "supports_enhanced_analysis": hasattr(predictor, 'identify_contributing_factors')
    })

@app.route("/analyze", methods=["POST"])
def analyze_health_data():
    """Perform detailed health analysis without prediction"""
    try:
        data = request.get_json()
        predictor_type = data.get("predictor_type")
        input_data = data.get("data")
        
        if predictor_type not in predictors:
            return jsonify({
                "error": f"Predictor '{predictor_type}' not found. Available predictors: {list(predictors.keys())}"
            }), 400
        
        predictor = predictors[predictor_type]
        
        # Check if predictor supports enhanced analysis
        if not hasattr(predictor, 'identify_contributing_factors'):
            return jsonify({
                "error": f"Predictor '{predictor_type}' does not support enhanced analysis"
            }), 400
        
        # Perform detailed analysis
        analysis_result = {
            "predictor_type": predictor_type,
            "analysis": {
                "contributing_factors": predictor.identify_contributing_factors(input_data),
                "health_metrics": predictor.analyze_health_metrics(input_data),
                "lifestyle_impact": predictor.assess_lifestyle_impact(input_data)
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(analysis_result)
    
    except Exception as e:
        return jsonify({"error": f"Analysis error: {str(e)}"}), 500

@app.route("/health")
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "predictors_loaded": len(predictors)
    })

@app.route("/download-report", methods=["POST"])
def download_report():
    """Generate and download PDF health assessment report"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        prediction_data = data.get('prediction_data')
        user_data = data.get('user_data', {})
        
        if not prediction_data:
            return jsonify({"error": "Prediction data is required"}), 400
        
        # Generate PDF report
        pdf_generator = HealthReportGenerator()
        pdf_buffer = pdf_generator.generate_report(prediction_data, user_data)
        
        # Generate filename
        predictor_type = prediction_data.get('predictor_type', 'health')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{predictor_type}_report_{timestamp}.pdf"
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
    
    except Exception as e:
        return jsonify({"error": f"PDF generation error: {str(e)}"}), 500

if __name__ == '__main__':
    # Use environment variables for production deployment
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host="0.0.0.0", port=port, debug=debug)