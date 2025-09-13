#!/usr/bin/env python3
"""
Simplified test script to verify enhanced predictors have the new analysis methods
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from predictors.lifestyle_predictors import (
    ObesityRiskPredictor, HypertensionPredictor, CholesterolRiskPredictor,
    MentalHealthPredictor, SleepApneaPredictor
)
from predictors.specialized_predictors import (
    CovidRiskPredictor, AsthmaCopdPredictor, AnemiaPredictor,
    ThyroidDisorderPredictor, CancerRecurrencePredictor
)

def test_predictor_methods(predictor_class, predictor_name):
    """Test that a predictor has all required methods"""
    print(f"\n=== Testing {predictor_name} ===")
    
    try:
        # Initialize predictor
        predictor = predictor_class()
        print(f"✓ {predictor_name} initialized successfully")
        
        # Test basic methods exist
        assert hasattr(predictor, 'get_required_fields'), "Missing get_required_fields method"
        assert hasattr(predictor, 'get_field_descriptions'), "Missing get_field_descriptions method"
        assert hasattr(predictor, 'preprocess_data'), "Missing preprocess_data method"
        print(f"✓ Basic methods exist")
        
        # Test new analysis methods exist
        assert hasattr(predictor, 'identify_contributing_factors'), "Missing identify_contributing_factors method"
        assert hasattr(predictor, 'analyze_health_metrics'), "Missing analyze_health_metrics method"
        assert hasattr(predictor, 'assess_lifestyle_impact'), "Missing assess_lifestyle_impact method"
        print(f"✓ Enhanced analysis methods exist")
        
        # Test methods are callable
        assert callable(predictor.identify_contributing_factors), "identify_contributing_factors not callable"
        assert callable(predictor.analyze_health_metrics), "analyze_health_metrics not callable"
        assert callable(predictor.assess_lifestyle_impact), "assess_lifestyle_impact not callable"
        print(f"✓ All methods are callable")
        
        # Test basic method calls work
        required_fields = predictor.get_required_fields()
        descriptions = predictor.get_field_descriptions()
        print(f"✓ get_required_fields() returned {len(required_fields)} fields")
        print(f"✓ get_field_descriptions() returned {len(descriptions)} descriptions")
        
        print(f"✅ {predictor_name} - All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ {predictor_name} - Error: {str(e)}")
        return False

def main():
    """Run tests on all enhanced predictors"""
    print("🧪 Testing Enhanced Predictors - Method Existence")
    print("=" * 60)
    
    # Define predictors to test
    predictors_to_test = [
        (ObesityRiskPredictor, "ObesityRiskPredictor"),
        (HypertensionPredictor, "HypertensionPredictor"),
        (CholesterolRiskPredictor, "CholesterolRiskPredictor"),
        (MentalHealthPredictor, "MentalHealthPredictor"),
        (SleepApneaPredictor, "SleepApneaPredictor"),
        (CovidRiskPredictor, "CovidRiskPredictor"),
        (AsthmaCopdPredictor, "AsthmaCopdPredictor"),
        (AnemiaPredictor, "AnemiaPredictor"),
        (ThyroidDisorderPredictor, "ThyroidDisorderPredictor"),
        (CancerRecurrencePredictor, "CancerRecurrencePredictor")
    ]
    
    results = []
    
    for predictor_class, predictor_name in predictors_to_test:
        success = test_predictor_methods(predictor_class, predictor_name)
        results.append((predictor_name, success))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for predictor_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {predictor_name}")
    
    print(f"\n🎯 Results: {passed}/{total} predictors passed all tests")
    
    if passed == total:
        print("🎉 All enhanced predictors have the required analysis methods!")
        return True
    else:
        print("⚠️  Some predictors are missing required methods.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)