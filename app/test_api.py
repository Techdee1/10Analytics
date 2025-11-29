"""
Test script for DebtSage API
Tests all endpoints to ensure they work correctly
"""

import requests
import json
from time import time

API_BASE_URL = "http://localhost:8000"

def test_endpoint(name, method, endpoint, data=None, params=None):
    """Test a single endpoint and report results"""
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        start = time()
        
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=data)
        
        elapsed = time() - start
        
        if response.status_code == 200:
            print(f"✅ {name:40s} ({response.status_code}) - {elapsed*1000:.0f}ms")
            return True, response.json()
        else:
            print(f"❌ {name:40s} ({response.status_code}) - {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ {name:40s} - ERROR: {str(e)}")
        return False, None

def main():
    print("="*80)
    print("🧪 DEBTSAGE API TEST SUITE")
    print("="*80)
    print(f"\nTesting API at: {API_BASE_URL}\n")
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Root endpoint
    success, data = test_endpoint("Root Endpoint", "GET", "/")
    if success:
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 2: Health check
    success, data = test_endpoint("Health Check", "GET", "/health")
    if success:
        tests_passed += 1
        print(f"   Models loaded: {data.get('models_loaded')}, Data files: {data.get('data_files_loaded')}")
    else:
        tests_failed += 1
    
    # Test 3: Get countries
    success, data = test_endpoint("Get Countries List", "GET", "/countries")
    if success:
        tests_passed += 1
        print(f"   Found {data.get('count')} countries")
    else:
        tests_failed += 1
    
    # Test 4: Single prediction
    prediction_data = {
        "debt_to_gdp": 65.0,
        "deficit_to_gdp": -3.5,
        "revenue_to_gdp": 18.5,
        "inflation_rate": 5.2,
        "gdp_growth": 3.8,
        "external_debt_ratio": 45.0,
        "debt_service_to_revenue": 25.0,
        "reserves_months": 4.5,
        "primary_balance": -1.2,
        "exchange_rate_change": 2.1,
        "model": "xgboost"
    }
    
    success, data = test_endpoint("Single Prediction", "POST", "/predict", data=prediction_data)
    if success:
        tests_passed += 1
        print(f"   Risk Score: {data.get('risk_score')}%, Level: {data.get('risk_level')}")
    else:
        tests_failed += 1
    
    # Test 5: Get country data
    success, data = test_endpoint("Get Country Data (Togo)", "GET", "/country/Togo", 
                                  params={"start_year": 2020})
    if success:
        tests_passed += 1
        print(f"   Records: {data.get('count')}, Years: {data.get('year_range')}")
    else:
        tests_failed += 1
    
    # Test 6: Get risk scores
    success, data = test_endpoint("Get Risk Scores", "GET", "/risk-scores", 
                                  params={"min_risk": 50})
    if success:
        tests_passed += 1
        print(f"   High-risk countries: {data.get('count')}")
    else:
        tests_failed += 1
    
    # Test 7: Get model performance
    success, data = test_endpoint("Get Model Performance", "GET", "/model/performance")
    if success:
        tests_passed += 1
        print(f"   Models evaluated: {data.get('count')}")
    else:
        tests_failed += 1
    
    # Test 8: Get feature importance
    success, data = test_endpoint("Get Feature Importance", "GET", "/model/feature-importance",
                                  params={"top_n": 5})
    if success:
        tests_passed += 1
        print(f"   Top features: {data.get('count')}")
    else:
        tests_failed += 1
    
    # Test 9: Get fiscal metrics
    success, data = test_endpoint("Get Fiscal Metrics", "GET", "/fiscal/metrics",
                                  params={"country": "Togo"})
    if success:
        tests_passed += 1
        print(f"   Fiscal records: {data.get('count')}")
    else:
        tests_failed += 1
    
    # Test 10: Get fiscal scorecard
    success, data = test_endpoint("Get Fiscal Scorecard", "GET", "/fiscal/scorecard")
    if success:
        tests_passed += 1
        print(f"   Countries in scorecard: {data.get('count')}")
    else:
        tests_failed += 1
    
    # Test 11: Get projections
    success, data = test_endpoint("Get Debt Projections (Togo)", "GET", "/projections/Togo")
    if success:
        tests_passed += 1
        print(f"   Scenarios: {list(data.get('scenarios', {}).keys())}")
    else:
        tests_failed += 1
    
    # Test 12: Get summary statistics
    success, data = test_endpoint("Get Summary Statistics", "GET", "/stats/summary")
    if success:
        tests_passed += 1
        print(f"   Total observations: {data.get('dataset', {}).get('total_observations')}")
    else:
        tests_failed += 1
    
    # Test 13: Batch prediction
    batch_data = {
        "predictions": [
            prediction_data,
            {**prediction_data, "debt_to_gdp": 85.0, "deficit_to_gdp": -5.5}
        ]
    }
    
    success, data = test_endpoint("Batch Prediction", "POST", "/predict/batch", data=batch_data)
    if success:
        tests_passed += 1
        print(f"   Predictions: {data.get('count')}")
    else:
        tests_failed += 1
    
    # Summary
    print("\n" + "="*80)
    print("📊 TEST RESULTS")
    print("="*80)
    print(f"✅ Passed: {tests_passed}")
    print(f"❌ Failed: {tests_failed}")
    print(f"📈 Success Rate: {tests_passed/(tests_passed+tests_failed)*100:.1f}%")
    print("="*80)
    
    if tests_failed == 0:
        print("\n🎉 ALL TESTS PASSED! API is ready for integration.\n")
    else:
        print(f"\n⚠️  {tests_failed} test(s) failed. Check API server status.\n")

if __name__ == "__main__":
    print("\n⚠️  Make sure API server is running:")
    print("   python app/api.py\n")
    
    # Check if server is running
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            print("✅ API server is running!\n")
            main()
        else:
            print("❌ API server returned error. Please restart the server.\n")
    except:
        print("❌ API server is not running. Please start it first:")
        print("   python app/api.py\n")
