import joblib
import os
import streamlit as st

MODEL_PATH = "rf_best.pkl"
SCALER_PATH = "scaler.pkl"

try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully")
    scaler = joblib.load(SCALER_PATH)
    print("Scaler loaded successfully")
except Exception as e:
    print(f"Error: {e}")
