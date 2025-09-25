#!/usr/bin/env python3
"""
Test script for enhanced API endpoints with detailed analysis methods.
This script tests the updated /predict and new /analyze endpoints.
"""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:5000"

def test_enhanced_predict_endpoint():
    """Test the enhanced /predict endpoint with detailed analysis"""
    print("\n=== Testing Enhanced /predict Endpoint ===")
    
    # Test data for heart disease predictor (using correct integer format)
    test_data = {
        "predictor_type": "heart_disease",
        "data": {
            "age": 45,
            "sex": 1,  # 1 = male, 0 = female
            "chest_pain_type": 2,  # 0-3
            "resting_bp": 130.0,
            "cholesterol": 220.0,
            "fasting_blood_sugar": 0,  # 0 = false, 1 = true
            "resting_ecg": 0,  # 0-2
            "max_heart_rate": 150.0,
            "exercise_angina": 0,  # 0 = no, 1 = yes
            "st_depression": 1.2,
            "st_slope": 1,  # 0-2
            "smoking": 0,  # 0 = no, 1 = yes
            "family_history": 1  # 0 = no, 1 = yes
        },
        "include_analysis": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Enhanced prediction successful!")
            print(f"   Risk Score: {result.get('risk_score', 'N/A')}")
            print(f"   Risk Level: {result.get('risk_level', 'N/A')}")
            
            # Check for detailed analysis
            if "detailed_analysis" in result:
                analysis = result["detailed_analysis"]
                print("   📊 Detailed Analysis Available:")
                print(f"      - Contributing Factors: {len(analysis.get('contributing_factors', {}))} items")
                print(f"      - Health Metrics: {len(analysis.get('health_metrics', {}))} items")
                print(f"      - Lifestyle Impact: {len(analysis.get('lifestyle_impact', {}))} items")
            else:
                print("   ⚠️  No detailed analysis in response")
                if "analysis_error" in result:
                    print(f"   Error: {result['analysis_error']}")
        else:
            print(f"❌ Enhanced prediction failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")

def test_analyze_endpoint():
    """Test the new /analyze endpoint"""
    print("\n=== Testing /analyze Endpoint ===")
    
    # Test data for mental health predictor (using correct integer format)
    test_data = {
        "predictor_type": "mental_health",
        "data": {
            "age": 28,
            "gender": 0,  # 1 = male, 0 = female
            "phq9_score": 12,
            "gad7_score": 8,
            "stress_level": 7,  # 0-10 scale
            "sleep_hours": 5.0,
            "sleep_quality": 3,  # 0-10 scale
            "physical_activity_minutes": 60,  # per week
            "social_support_score": 5,  # 0-10 scale
            "work_stress_level": 8,  # 0-10 scale
            "financial_stress": 1,  # 1 = yes, 0 = no
            "relationship_stress": 0,
            "chronic_illness": 0,
            "substance_use": 0,  # 0-3 scale
            "trauma_history": 0,  # 1 = yes, 0 = no
            "family_history_mental_health": 1,  # 1 = yes, 0 = no
            "medication_antidepressants": 0,
            "therapy_sessions_monthly": 2,
            "meditation_frequency": 1,  # 0-7 times per week
            "caffeine_intake_mg": 200.0,
            "alcohol_drinks_per_week": 3,
            "social_isolation_score": 4  # 0-10 scale
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/analyze", json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Analysis successful!")
            print(f"   Predictor: {result.get('predictor_type', 'N/A')}")
            
            if "analysis" in result:
                analysis = result["analysis"]
                print("   📊 Analysis Results:")
                print(f"      - Contributing Factors: {len(analysis.get('contributing_factors', {}))} items")
                print(f"      - Health Metrics: {len(analysis.get('health_metrics', {}))} items")
                print(f"      - Lifestyle Impact: {len(analysis.get('lifestyle_impact', {}))} items")
            else:
                print("   ⚠️  No analysis data in response")
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")

def test_predictor_fields_endpoint():
    """Test the enhanced /predictor/<type>/fields endpoint"""
    print("\n=== Testing Enhanced /predictor/fields Endpoint ===")
    
    try:
        response = requests.get(f"{BASE_URL}/predictor/cancer_recurrence/fields")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Predictor fields retrieved successfully!")
            print(f"   Name: {result.get('name', 'N/A')}")
            print(f"   Required Fields: {len(result.get('required_fields', []))} fields")
            print(f"   Supports Enhanced Analysis: {result.get('supports_enhanced_analysis', False)}")
        else:
            print(f"❌ Fields retrieval failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")

def test_predictors_endpoint():
    """Test the /predictors endpoint to see enhanced analysis support"""
    print("\n=== Testing /predictors Endpoint ===")
    
    try:
        response = requests.get(f"{BASE_URL}/predictors")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Predictors list retrieved successfully!")
            print(f"   Total Predictors: {len(result)} predictors")
            
            # Count predictors with enhanced analysis
            enhanced_count = 0
            for name, info in result.items():
                # We'll check this by making a quick field request
                try:
                    field_response = requests.get(f"{BASE_URL}/predictor/{name}/fields")
                    if field_response.status_code == 200:
                        field_data = field_response.json()
                        if field_data.get('supports_enhanced_analysis', False):
                            enhanced_count += 1
                except:
                    pass
            
            print(f"   Enhanced Analysis Support: {enhanced_count} predictors")
        else:
            print(f"❌ Predictors retrieval failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")

def main():
    """Run all API tests"""
    print("🚀 Starting Enhanced API Tests")
    print(f"Testing API at: {BASE_URL}")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test all endpoints
    test_predictors_endpoint()
    test_predictor_fields_endpoint()
    test_enhanced_predict_endpoint()
    test_analyze_endpoint()
    
    print("\n🎉 Enhanced API testing completed!")

if __name__ == "__main__":
    main()