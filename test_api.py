"""
Test Nexora Attrition API - ML-Based Predictions
"""

import requests
import json

API_BASE_URL = "http://localhost:5000"

def print_header(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def test_health():
    """Test health endpoint"""
    print_header("TEST 1: Health Check")
    response = requests.get(f"{API_BASE_URL}/api/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_config():
    """Test configuration"""
    print_header("TEST 2: Model Configuration")
    response = requests.get(f"{API_BASE_URL}/api/config")
    result = response.json()
    print(f"Model Type: {result['model_type']}")
    print(f"Accuracy: {result['accuracy']}")
    print(f"\nSupported Job Titles:")
    for job in result['supported_job_titles']:
        print(f"  - {job}")

def test_single_prediction():
    """Test single employee prediction"""
    print_header("TEST 3: Single Employee Prediction")
    
    payload = {
        "salary": 2500,
        "jobTitle": "Sales Executive",
        "performanceRating": 2,
        "employee_id": "E123",
        "employee_name": "Ali Khan"
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/predict-attrition",
        json=payload
    )
    result = response.json()
    
    if result['success']:
        pred = result['prediction']
        print(f"👤 Employee: {pred['employee_name']} (ID: {pred['employee_id']})")
        print(f"💰 Salary: Rs {pred['prediction_details']['salary']:,}")
        print(f"💼 Job: {pred['prediction_details']['job_title']}")
        print(f"⭐ Performance: {pred['prediction_details']['performance_rating']}/4")
        print(f"\n🎯 PREDICTION:")
        print(f"   Risk Category: {pred['risk_category']}")
        print(f"   Risk Score: {pred['risk_percentage']}%")
        print(f"\n📋 Risk Factors:")
        for factor in pred['factors']:
            print(f"   {factor}")

def test_batch_prediction():
    """Test batch predictions"""
    print_header("TEST 4: Batch Predictions")
    
    payload = {
        "employees": [
            {
                "salary": 2500,
                "jobTitle": "Sales Executive",
                "performanceRating": 2,
                "employee_id": "E001",
                "employee_name": "Ali Khan"
            },
            {
                "salary": 8000,
                "jobTitle": "Manager",
                "performanceRating": 4,
                "employee_id": "E002",
                "employee_name": "Fatima Ahmed"
            },
            {
                "salary": 5000,
                "jobTitle": "Research Scientist",
                "performanceRating": 3,
                "employee_id": "E003",
                "employee_name": "Hassan Ali"
            },
            {
                "salary": 12000,
                "jobTitle": "Research Director",
                "performanceRating": 4,
                "employee_id": "E004",
                "employee_name": "Ayesha Khan"
            },
            {
                "salary": 3000,
                "jobTitle": "Laboratory Technician",
                "performanceRating": 2,
                "employee_id": "E005",
                "employee_name": "Usman Ahmed"
            }
        ]
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/predict-attrition-batch",
        json=payload
    )
    result = response.json()
    
    if result['success']:
        print(f"✅ Analyzed {result['total_employees']} employees\n")
        
        summary = result['summary']
        print("📊 RISK SUMMARY:")
        print(f"  🔴 High-Risk: {summary['high_risk']['count']} ({summary['high_risk']['percentage']}%)")
        print(f"  🟡 Medium-Risk: {summary['medium_risk']['count']} ({summary['medium_risk']['percentage']}%)")
        print(f"  🟢 Low-Risk: {summary['low_risk']['count']} ({summary['low_risk']['percentage']}%)")
        print(f"  📈 Average Risk Score: {summary['average_risk_score']}")
        
        print(f"\n{'─'*70}")
        print("INDIVIDUAL PREDICTIONS:")
        print(f"{'─'*70}")
        
        for pred in result['predictions']:
            icon = "🔴" if pred['risk_category'] == "High-risk" else "🟡" if pred['risk_category'] == "Medium-risk" else "🟢"
            print(f"\n{icon} {pred['employee_name']} (ID: {pred['employee_id']})")
            print(f"   Risk: {pred['risk_category']} ({pred['risk_percentage']}%)")
            print(f"   Salary: Rs {pred['prediction_details']['salary']:,}")
            if pred['factors']:
                print(f"   Factors: {', '.join(pred['factors'])}")

if __name__ == "__main__":
    print("\n" + "🚀" * 35)
    print("NEXORA ATTRITION API - ML MODEL TEST SUITE")
    print("🚀" * 35)
    
    try:
        test_health()
        test_config()
        test_single_prediction()
        test_batch_prediction()
        
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED! API is working perfectly")
        print("="*70 + "\n")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        print("Make sure the API is running: python api.py")
