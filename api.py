"""
Flask API for Nexora Integration - 4 Fields
salary, performanceRating, department, jobTitle
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import json
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load model and encoders
try:
    model = joblib.load('nexora_attrition_model.pkl')
    dept_encoder = joblib.load('department_encoder.pkl')
    job_encoder = joblib.load('job_encoder.pkl')
    
    with open('model_config.json', 'r') as f:
        config = json.load(f)
    
    logger.info("✅ Model loaded successfully")
    logger.info(f"✅ Accuracy: {config['accuracy']*100:.2f}%")
except Exception as e:
    logger.error(f"❌ Error loading model: {str(e)}")
    model = None


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'message': 'Attrition API - 4 Fields (Nexora)',
        'model_loaded': model is not None,
        'accuracy': f"{config.get('accuracy', 0)*100:.2f}%" if config else 'N/A',
        'fields': ['salary', 'performanceRating', 'department', 'jobTitle']
    }), 200


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get configuration"""
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500
    
    return jsonify({
        'model_type': 'Random Forest (4 Fields)',
        'accuracy': f"{config.get('accuracy', 0)*100:.2f}%",
        'required_fields': ['salary', 'performanceRating', 'department', 'jobTitle'],
        'supported_departments': list(dept_encoder.classes_),
        'supported_job_titles': list(job_encoder.classes_),
        'performance_scale': '1-4'
    }), 200


def predict_single(salary, performance_rating, department, job_title):
    """Predict attrition for single employee"""
    try:
        # Department mapping for Nexora
        dept_mapping = {
            'developer': 'Research & Development',
            'development': 'Research & Development',
            'it': 'Research & Development',
            'tech': 'Research & Development',
            'engineering': 'Research & Development',
            'sales': 'Sales',
            'marketing': 'Sales',
            'hr': 'Human Resources',
            'human resources': 'Human Resources',
            'admin': 'Human Resources'
        }
        
        # Job title mapping
        job_mapping = {
            'developer': 'Research Scientist',
            'senior developer': 'Research Scientist',
            'junior developer': 'Research Scientist',
            'tech lead': 'Manager',
            'team lead': 'Manager',
            'software engineer': 'Research Scientist',
            'engineer': 'Research Scientist',
            'hr manager': 'Manager',
            'hr executive': 'Human Resources',
            'sales manager': 'Manager',
            'sales rep': 'Sales Representative'
        }
        
        # Map department
        dept_lower = department.lower()
        if department not in dept_encoder.classes_:
            department = dept_mapping.get(dept_lower, 'Research & Development')
            logger.warning(f'Mapped department to: {department}')
        
        # Map job title
        job_lower = job_title.lower()
        if job_title not in job_encoder.classes_:
            job_title = job_mapping.get(job_lower, 'Research Scientist')
            logger.warning(f'Mapped job title to: {job_title}')
        
        # Encode
        dept_enc = dept_encoder.transform([department])[0]
        job_enc = job_encoder.transform([job_title])[0]
        
        # Create feature vector (4 fields)
        X = pd.DataFrame([[salary, performance_rating, dept_enc, job_enc]],
                        columns=['salary', 'performanceRating', 'department_encoded', 'jobTitle_encoded'])
        
        # Predict
        risk_proba = model.predict_proba(X)[0][1]
        
        # Categorize
        if risk_proba < 0.33:
            risk_category = "Low-risk"
        elif risk_proba < 0.66:
            risk_category = "Medium-risk"
        else:
            risk_category = "High-risk"
        
        # Generate factors
        factors = []
        if salary < 30000:
            factors.append("⚠️ Low salary (< Rs 30,000)")
        elif salary > 60000:
            factors.append("✅ Good salary (> Rs 60,000)")
        
        if performance_rating <= 2:
            factors.append("⚠️ Low performance rating")
        elif performance_rating >= 4:
            factors.append("✅ High performance rating")
        
        if department == 'Sales':
            factors.append("⚠️ High-attrition department: Sales")
        
        return {
            'risk_score': round(risk_proba, 3),
            'risk_percentage': round(risk_proba * 100, 1),
            'risk_category': risk_category,
            'factors': factors,
            'prediction_details': {
                'salary': salary,
                'performance_rating': performance_rating,
                'department': department,
                'job_title': job_title
            }
        }
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return {'error': str(e)}


@app.route('/api/predict-attrition', methods=['POST'])
def predict_attrition():
    """Single employee prediction"""
    try:
        if not model:
            return jsonify({'error': 'Model not loaded'}), 500
        
        data = request.get_json()
        
        # Validate
        required = ['salary', 'performanceRating', 'department', 'jobTitle']
        missing = [f for f in required if f not in data]
        if missing:
            return jsonify({
                'success': False,
                'error': f'Missing fields: {", ".join(missing)}'
            }), 400
        
        # Predict
        result = predict_single(
            data['salary'],
            data['performanceRating'],
            data['department'],
            data['jobTitle']
        )
        
        if 'error' in result:
            return jsonify({'success': False, **result}), 400
        
        result['employee_id'] = data.get('employee_id', 'N/A')
        result['employee_name'] = data.get('employee_name', 'N/A')
        
        return jsonify({'success': True, 'prediction': result}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/predict-attrition-batch', methods=['POST'])
def predict_attrition_batch():
    """Batch prediction"""
    try:
        if not model:
            return jsonify({'error': 'Model not loaded'}), 500
        
        data = request.get_json()
        
        if 'employees' not in data:
            return jsonify({'success': False, 'error': 'Expected employees array'}), 400
        
        predictions = []
        errors = []
        
        for emp in data['employees']:
            required = ['salary', 'performanceRating', 'department', 'jobTitle']
            if not all(k in emp for k in required):
                errors.append({'employee_id': emp.get('employee_id', 'Unknown'), 'error': 'Missing fields'})
                continue
            
            result = predict_single(
                emp['salary'],
                emp['performanceRating'],
                emp['department'],
                emp['jobTitle']
            )
            
            if 'error' in result:
                errors.append({'employee_id': emp.get('employee_id', 'Unknown'), 'error': result['error']})
                continue
            
            result['employee_id'] = emp.get('employee_id', 'N/A')
            result['employee_name'] = emp.get('employee_name', 'N/A')
            predictions.append(result)
        
        # Summary
        high = [p for p in predictions if p['risk_category'] == 'High-risk']
        medium = [p for p in predictions if p['risk_category'] == 'Medium-risk']
        low = [p for p in predictions if p['risk_category'] == 'Low-risk']
        
        total = len(predictions)
        
        return jsonify({
            'success': True,
            'total_employees': total,
            'predictions': predictions,
            'summary': {
                'high_risk': {
                    'count': len(high),
                    'percentage': round((len(high) / total * 100) if total > 0 else 0, 1),
                    'employees': [{'id': p['employee_id'], 'name': p['employee_name'], 'risk': p['risk_percentage']} for p in high[:10]]
                },
                'medium_risk': {
                    'count': len(medium),
                    'percentage': round((len(medium) / total * 100) if total > 0 else 0, 1)
                },
                'low_risk': {
                    'count': len(low),
                    'percentage': round((len(low) / total * 100) if total > 0 else 0, 1)
                },
                'average_risk_score': round(sum([p['risk_score'] for p in predictions]) / total if total > 0 else 0, 3)
            },
            'errors': errors if errors else None
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║  🤖 NEXORA ATTRITION API (4 Fields)                        ║
    ║  Server: http://localhost:5000                             ║
    ║  Fields: salary, performanceRating, department, jobTitle   ║
    ║  Health: http://localhost:5000/api/health                  ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    app.run(debug=True, host='0.0.0.0', port=5000)
