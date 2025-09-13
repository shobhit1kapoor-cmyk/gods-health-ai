#!/usr/bin/env python3
"""
Script to check what fields each predictor requires
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

def check_predictor_fields(predictor_class, predictor_name):
    """Check what fields a predictor requires"""
    print(f"\n=== {predictor_name} Required Fields ===")
    
    try:
        predictor = predictor_class()
        required_fields = predictor.get_required_fields()
        
        print(f"Total fields: {len(required_fields)}")
        for i, field in enumerate(required_fields, 1):
            print(f"{i:2d}. {field}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    """Check required fields for all predictors"""
    print("🔍 Checking Required Fields for All Predictors")
    print("=" * 60)
    
    predictors_to_check = [
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
    
    all_fields = set()
    
    for predictor_class, predictor_name in predictors_to_check:
        check_predictor_fields(predictor_class, predictor_name)
        
        # Collect all unique fields
        try:
            predictor = predictor_class()
            required_fields = predictor.get_required_fields()
            all_fields.update(required_fields)
        except:
            pass
    
    print(f"\n=== All Unique Fields ({len(all_fields)}) ===")
    for i, field in enumerate(sorted(all_fields), 1):
        print(f"{i:2d}. {field}")

if __name__ == "__main__":
    main()