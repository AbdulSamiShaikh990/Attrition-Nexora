"""
Train Attrition Model - 4 Fields (Nexora Compatible)
Fields: salary, performanceRating, department, jobTitle
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

print("="*70)
print("ATTRITION MODEL TRAINING - 4 FIELDS (NEXORA)")
print("="*70)

# Load data
print("\n[1/7] Loading dataset...")
df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')
print(f"✅ Loaded {len(df)} employee records")

# Select 4 fields + target
print("\n[2/7] Selecting fields: salary, performanceRating, department, jobTitle")
data = df[['MonthlyIncome', 'PerformanceRating', 'Department', 'JobRole', 'Attrition']].copy()

# Rename to match Nexora
data.columns = ['salary', 'performanceRating', 'department', 'jobTitle', 'attrition']
print(f"✅ Fields renamed for Nexora compatibility")
print(f"Missing values: {data.isnull().sum().sum()}")

# Encode categorical variables
print("\n[3/7] Encoding categorical data...")

# Encode department
le_dept = LabelEncoder()
data['department_encoded'] = le_dept.fit_transform(data['department'])
print(f"✅ Departments: {list(le_dept.classes_)}")

# Encode jobTitle
le_job = LabelEncoder()
data['jobTitle_encoded'] = le_job.fit_transform(data['jobTitle'])
print(f"✅ Job Titles: {list(le_job.classes_)}")

# Encode attrition (Yes/No to 1/0)
data['attrition_binary'] = (data['attrition'] == 'Yes').astype(int)

# Prepare features and target
X = data[['salary', 'performanceRating', 'department_encoded', 'jobTitle_encoded']]
y = data['attrition_binary']

print(f"\n✅ Feature matrix: {X.shape}")
print(f"✅ Target distribution:")
print(f"   Stayed (0): {(y==0).sum()} ({(y==0).sum()/len(y)*100:.1f}%)")
print(f"   Left (1): {(y==1).sum()} ({(y==1).sum()/len(y)*100:.1f}%)")

# Split data
print("\n[4/7] Splitting data (80% train, 20% test)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"✅ Training: {len(X_train)} | Testing: {len(X_test)}")

# Train model
print("\n[5/7] Training Random Forest...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=12,
    random_state=42,
    n_jobs=-1,
    class_weight='balanced'
)
model.fit(X_train, y_train)
print("✅ Training complete!")

# Evaluate
print("\n[6/7] Evaluating model...")
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n✅ Accuracy: {accuracy*100:.2f}%")
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Stayed', 'Left']))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print("\n📊 Confusion Matrix:")
print(f"   Predicted: Stayed | Left")
print(f"Actually Stayed: {cm[0][0]:4d}    | {cm[0][1]:4d}")
print(f"Actually Left:   {cm[1][0]:4d}    | {cm[1][1]:4d}")

# Feature importance
print("\n📈 Feature Importance:")
features = ['salary', 'performanceRating', 'department', 'jobTitle']
for name, imp in zip(features, model.feature_importances_):
    print(f"   {name}: {imp:.3f} ({imp*100:.1f}%)")

# Save model
print("\n[7/7] Saving model...")
joblib.dump(model, 'nexora_attrition_model.pkl')
joblib.dump(le_dept, 'department_encoder.pkl')
joblib.dump(le_job, 'job_encoder.pkl')

# Save config
import json
config = {
    'feature_names': features,
    'departments': list(le_dept.classes_),
    'job_titles': list(le_job.classes_),
    'accuracy': float(accuracy),
    'trained_on': str(pd.Timestamp.now()),
    'total_samples': len(df),
    'fields': 4
}

with open('model_config.json', 'w') as f:
    json.dump(config, f, indent=2)

print("✅ Model saved: nexora_attrition_model.pkl")
print("✅ Encoders saved: department_encoder.pkl, job_encoder.pkl")
print("✅ Config saved: model_config.json")

# Test with Nexora-like sample
print("\n" + "="*70)
print("TESTING WITH NEXORA SAMPLE DATA")
print("="*70)

nexora_samples = [
    {'salary': 50000, 'performanceRating': 4, 'department': 'Research & Development', 'jobTitle': 'Research Scientist'},
    {'salary': 35000, 'performanceRating': 2, 'department': 'Sales', 'jobTitle': 'Sales Executive'},
    {'salary': 60000, 'performanceRating': 5, 'department': 'Research & Development', 'jobTitle': 'Manager'},
    {'salary': 25000, 'performanceRating': 2, 'department': 'Sales', 'jobTitle': 'Sales Representative'},
]

for i, sample in enumerate(nexora_samples, 1):
    try:
        dept_enc = le_dept.transform([sample['department']])[0]
        job_enc = le_job.transform([sample['jobTitle']])[0]
        
        X_sample = np.array([[
            sample['salary'],
            sample['performanceRating'],
            dept_enc,
            job_enc
        ]])
        
        risk = model.predict_proba(X_sample)[0][1]
        category = 'High-risk' if risk > 0.5 else 'Low-risk'
        
        print(f"\nSample {i}:")
        print(f"  Salary: Rs {sample['salary']:,}")
        print(f"  Performance: {sample['performanceRating']}/4")
        print(f"  Department: {sample['department']}")
        print(f"  Job: {sample['jobTitle']}")
        print(f"  → Risk: {risk*100:.1f}% ({category})")
    except Exception as e:
        print(f"\nSample {i}: Error - {e}")

print("\n" + "="*70)
print("✅ TRAINING COMPLETE! Ready for Nexora Integration")
print("="*70)
