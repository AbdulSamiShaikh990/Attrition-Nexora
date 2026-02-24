import pandas as pd
import numpy as np
import pickle
import streamlit as st
import plotly.express as px
import pydeck as pdk
from faker import Faker
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report, precision_recall_curve, recall_score, accuracy_score, average_precision_score
import time
import os
import joblib

# Define paths relative to the script location
MODEL_PATH = os.path.join(os.path.dirname(__file__), "nexora_attrition_model.pkl")
DEPT_ENCODER_PATH = os.path.join(os.path.dirname(__file__), "department_encoder.pkl")
JOB_ENCODER_PATH = os.path.join(os.path.dirname(__file__), "job_encoder.pkl")
st.set_page_config(
    page_title="StratifyHR | Employee Analytics",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Professional Design Tokens ---
COLOR_THEME = {
    "primary": "#1E3A8A",      # Deep Navy
    "secondary": "#3B82F6",    # Blue
    "accent": "#F59E0B",       # Amber
    "success": "#10B981",      # Emerald
    "danger": "#EF4444",       # Rose
    "neutral": "#64748B",      # Slate
}

APP_VERSION = "v1.0 Professional"

# --- Session State Initialization ---
if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None
if "predictions" not in st.session_state:
    st.session_state.predictions = None
if "true_labels" not in st.session_state:
    st.session_state.true_labels = None
if "processed" not in st.session_state:
    st.session_state.processed = False


# --- Model Loading ---
@st.cache_resource
def load_model():
    try:
        # Try using joblib first (more reliable for scikit-learn models)
        return joblib.load(MODEL_PATH)
    except:
        # Fallback to pickle if joblib fails
        with open(MODEL_PATH, "rb") as model_file:
            return pickle.load(model_file)

@st.cache_resource
def load_dept_encoder():
    try:
        return joblib.load(DEPT_ENCODER_PATH)
    except:
        with open(DEPT_ENCODER_PATH, "rb") as f:
            return pickle.load(f)

@st.cache_resource
def load_job_encoder():
    try:
        return joblib.load(JOB_ENCODER_PATH)
    except:
        with open(JOB_ENCODER_PATH, "rb") as f:
            return pickle.load(f)

try:
    model = load_model()
except FileNotFoundError:
    st.error(f"❌ Model file not found: {MODEL_PATH}")
    st.stop()

try:
    dept_encoder = load_dept_encoder()
except FileNotFoundError:
    st.error(f"❌ Department encoder not found: {DEPT_ENCODER_PATH}")
    st.stop()

try:
    job_encoder = load_job_encoder()
except FileNotFoundError:
    st.error(f"❌ Job encoder not found: {JOB_ENCODER_PATH}")
    st.stop()
fake = Faker()

# --- Advanced UI Configuration ---
def apply_custom_theme():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    :root {{
        --primary: {COLOR_THEME['primary']};
        --secondary: {COLOR_THEME['secondary']};
        --accent: {COLOR_THEME['accent']};
        --success: {COLOR_THEME['success']};
        --danger: {COLOR_THEME['danger']};
        --neutral: {COLOR_THEME['neutral']};
        --glass-bg: rgba(255, 255, 255, 0.12);
        --glass-border: rgba(255, 255, 255, 0.35);
        --glass-shadow: 0 10px 30px rgba(2, 6, 23, 0.25);
        --bg-gradient: radial-gradient(1200px 700px at 10% 10%, rgba(59,130,246,0.25), transparent 60%),
                       radial-gradient(900px 600px at 90% 10%, rgba(245,158,11,0.22), transparent 65%),
                       linear-gradient(135deg, #0f172a 0%, #0b1223 50%, #0b1020 100%);
        --card-gradient: linear-gradient(135deg, rgba(255,255,255,0.18) 0%, rgba(255,255,255,0.08) 100%);
        --accent-gradient: linear-gradient(90deg, var(--secondary), var(--accent));
    }}

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    /* App background */
    .stApp {{
        background: var(--bg-gradient) fixed;
    }}

    /* Main content container glass effect */
    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }}

    /* Headings with subtle gradient text */
    h1, h2, h3 {{
        font-weight: 800;
        background: linear-gradient(90deg, #ffffff 0%, #e2e8f0 60%, #cbd5e1 100%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        letter-spacing: -0.5px;
    }}

    /* Sidebar: frosted glass */
    [data-testid="stSidebar"] > div:first-child {{
        background: var(--card-gradient);
        border: 1px solid var(--glass-border);
        backdrop-filter: blur(14px) saturate(140%);
        -webkit-backdrop-filter: blur(14px) saturate(140%);
        box-shadow: var(--glass-shadow);
        border-radius: 16px;
        margin: 12px;
    }}

    /* Tabs: glass pills with accent for active */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 10px;
        border-radius: 14px;
        box-shadow: var(--glass-shadow);
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 45px;
        white-space: pre-wrap;
        background: var(--card-gradient);
        border: 1px solid var(--glass-border);
        border-radius: 10px;
        color: #e2e8f0;
        padding: 0 20px;
        font-weight: 600;
        transition: all 160ms ease;
    }}

    .stTabs [aria-selected="true"] {{
        background: var(--accent-gradient) !important;
        color: #0b1020 !important;
        border-color: transparent !important;
        box-shadow: 0 8px 24px rgba(16,185,129,0.35);
    }}

    /* Metric cards: glass + subtle float on hover */
    .metric-card {{
        padding: 24px;
        background: var(--card-gradient);
        border: 1px solid var(--glass-border);
        box-shadow: var(--glass-shadow);
        border-radius: 18px;
        margin-bottom: 20px;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        backdrop-filter: blur(12px) saturate(130%);
        -webkit-backdrop-filter: blur(12px) saturate(130%);
    }}
    .metric-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 16px 40px rgba(2, 6, 23, 0.45);
    }}

    /* Streamlit metric base block */
    .stMetric {{
        background: var(--card-gradient);
        padding: 18px;
        border-radius: 14px;
        border: 1px solid var(--glass-border);
        box-shadow: var(--glass-shadow);
    }}

    /* Buttons: premium gradient */
    .stButton > button, .stDownloadButton > button {{
        background: var(--accent-gradient);
        color: #0b1020;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1rem;
        font-weight: 700;
        letter-spacing: 0.2px;
        box-shadow: 0 8px 24px rgba(59,130,246,0.35);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    .stButton > button:hover, .stDownloadButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(245,158,11,0.45);
    }}

    /* Inputs: glass */
    .stTextInput > div > div > input,
    .stNumberInput input,
    .stSelectbox > div > div {{
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid var(--glass-border) !important;
        color: #e2e8f0 !important;
        border-radius: 10px !important;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.05);
    }}

    /* Tables/Dataframes */
    .stDataFrame, .stTable {{
        background: var(--card-gradient);
        border: 1px solid var(--glass-border);
        border-radius: 14px;
        box-shadow: var(--glass-shadow);
        overflow: hidden;
    }}

    /* Status badges */
    .status-badge {{
        padding: 6px 12px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 700;
        background: rgba(16,185,129,0.18);
        color: #a7f3d0;
        border: 1px solid rgba(16,185,129,0.35);
    }}

    /* Small animation helper */
    @keyframes subtle-float {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-2px); }}
        100% {{ transform: translateY(0px); }}
    }}
    .animate-float {{
        animation: subtle-float 3s ease-in-out infinite;
    }}
    </style>
    """, unsafe_allow_html=True)

apply_custom_theme()

# --- Navigation & Progress Tracking ---
# --- Sidebar Branding ---
with st.sidebar:
    st.markdown("### 🏢 StratifyHR")
    st.caption("Intelligence-Driven Retention")
    st.markdown("---")
    st.write("**Empowering data-driven retention strategies.**")
    st.write(f"🏷️ version: {APP_VERSION}")
    st.write("---")
    st.caption("Developed for Academic Presentation 🎓")
    
# Functions
def display_overview():
    st.title("Employee Attrition Prediction App")
    st.markdown("## 🏠 Overview")
    st.write("""
    This application helps predict employee attrition risk and provides actionable insights. Employee turnover (also known as "employee churn") is a costly problem for companies. The true cost of replacing an employee
    can often be quite large. This is due to the amount of time spent to interview and find a replacement, sign-on bonuses, and the loss of productivity for several months while the new employee gets accustomed to the new role.
    """)
    
    # Step-by-step guide
    with st.expander("📖 Getting Started Guide", expanded=True):
        steps = """
        1. **Upload Data**: Provide your employee dataset in CSV format
        2. **Model Evaluation**: Review model performance metrics
        3. **Feature Analysis**: Understand key attrition drivers
        4. **Recommendations**: Get personalized action plans
        """
        st.markdown(steps)
    
    # Quick stats if data exists and is processed
    if st.session_state.uploaded_data is not None and 'Risk Category' in st.session_state.uploaded_data.columns:
        st.markdown("### 🚨 Current Dataset Snapshot")
        data = st.session_state.uploaded_data
        risk_counts = data['Risk Category'].value_counts()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h4>Employees Analyzed</h4>
                <h2>{len(data)}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h4>High-Risk Employees</h4>
                <h2>{risk_counts.get('High-risk', 0)}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h4>Attrition Risk Score</h4>
                <h2>{st.session_state.predictions.mean() * 100:.1f}%</h2>
            </div>
            """, unsafe_allow_html=True)

# --- Upload Data Section ---
def display_upload_data():
    st.markdown("## 📤 Data Upload & Setup")
    
    # Display required features and data types
    with st.expander("📋 Data Requirements", expanded=True):
        required_features = get_required_features_from_model(model)
        feature_data_types = {
                            'Age': 'int64',
                            'DailyRate': 'int64',
                            'DistanceFromHome': 'int64',
                            'Education': 'int64',
                            'EmployeeNumber': 'int64',
                            'EnvironmentSatisfaction': 'int64',
                            'JobInvolvement': 'int64',
                            'JobLevel': 'int64',
                            'JobSatisfaction': 'int64',
                            'MonthlyIncome': 'int64',
                            'OverTime': 'bool',
                            'StockOptionLevel': 'int64',
                            'TotalWorkingYears': 'int64',
                            'TrainingTimesLastYear': 'int64',
                            'WorkLifeBalance': 'int64',
                            'YearsAtCompany': 'int64',
                            'YearsInCurrentRole': 'int64',
                            'YearsWithCurrManager': 'int64',
                            'BusinessTravel_Travel_Frequently': 'bool',
                            'BusinessTravel_Travel_Rarely': 'bool',
                            'MaritalStatus_Married': 'bool',
                            'MaritalStatus_Single': 'bool'
        }

        st.table(pd.DataFrame({
            "Feature": required_features,
            "Data Type": [feature_data_types[feature] for feature in required_features]
        }))

        # Download template
        if st.button("✨ Generate Custom Template"):
            custom_template = pd.DataFrame(columns=required_features)
            csv_template = custom_template.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Template",
                data=csv_template,
                file_name="data_template.csv",
                mime="text/csv"
            )

    # Enhanced upload zone
    with st.container():
        uploaded_file = st.file_uploader(
            "Drag CSV here or click to browse",
            type="csv",
            help="Ensure file matches required features below"
        )
        
        # Ensure file is uploaded before proceeding
        if uploaded_file is not None:
            try:
                # Read and store uploaded file in session state
                data = pd.read_csv(uploaded_file)
                
                if data.empty:
                    st.error("Uploaded CSV file is empty. Please upload a valid file.")
                    return
                
                # Store the file in session state (persists across pages)
                st.session_state.uploaded_data = data
                st.success("File successfully uploaded and stored!")

                # Display preview in an expander
                with st.expander("🔍 Data Preview", expanded=True):
                    st.dataframe(data.head(5), use_container_width=True)

            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
                return

        # Form to process the uploaded data
        if "uploaded_data" in st.session_state:
            with st.form("data_processing_form"):
                st.markdown("### ⚙️ Data Processing Options")
                
                have_true_labels = st.checkbox("File contains True labels", value=False)
                
                if st.form_submit_button("Process Data"):
                    with st.spinner("Analyzing data..."):
                        process_and_store_data(st.session_state.uploaded_data, have_true_labels)
                    st.success("Data processed successfully!")

def process_and_store_data(data, have_true_labels):
    """
    Processes uploaded data, checks required features, and stores predictions & risk categories in session state.
    """
    try:
        required_features = get_required_features_from_model(model)  # Ensure this function returns a list of features

        # Ensure data is a DataFrame
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Uploaded file could not be read as a DataFrame.")

        # Check for missing features
        missing_features = [f for f in required_features if f not in list(data.columns)]
        if missing_features:
            raise ValueError(f"Missing features: {', '.join(missing_features)}")

        # Extract true labels if present
        true_labels = data["Attrition"] if have_true_labels and "Attrition" in data.columns else None
        if have_true_labels and "Attrition" in data.columns:
            data = data.drop(columns=["Attrition"])

        # Prepare data for prediction
        data_for_prediction = data[required_features]

        # Make predictions
        predictions = model.predict_proba(data_for_prediction)[:, 1]

        # Categorize risk levels
        data['Risk Category'] = np.select(
            [predictions < 0.5, (predictions >= 0.5) & (predictions <= 0.75), predictions > 0.75],
            ["Low-risk", "Medium-risk", "High-risk"],
            default="Unknown"
        )

        # Store results in session state
        st.session_state.uploaded_data = data
        st.session_state.predictions = predictions
        st.session_state.true_labels = true_labels
        st.session_state.processed = True  # Mark data as processed

        st.success("✅ Data processed and stored successfully!")

    except Exception as e:
        st.error(f"❌ Error processing data: {str(e)}")


# --- Helper Function ---
def get_required_features_from_model(model):
    """Dynamically extract required features from the trained model."""
    if hasattr(model, 'feature_names_in_'):
        return list(model.feature_names_in_)
    else:
        # Fallback to a predefined list if the model doesn't expose feature names
        return ['Age', 'DailyRate', 'DistanceFromHome', 'Education', 'EmployeeNumber',
       'EnvironmentSatisfaction', 'JobInvolvement', 'JobLevel',
       'JobSatisfaction', 'MonthlyIncome', 'OverTime', 'StockOptionLevel',
       'TotalWorkingYears', 'TrainingTimesLastYear', 'WorkLifeBalance',
       'YearsAtCompany', 'YearsInCurrentRole', 'YearsWithCurrManager',
       'BusinessTravel_Travel_Frequently', 'BusinessTravel_Travel_Rarely',
       'MaritalStatus_Married', 'MaritalStatus_Single'
        ]

# Display model evaluation section
def display_model_evaluation():
    st.markdown("## 📊 Model Performance Analysis")
    
    if st.session_state.uploaded_data is not None:
        col1, col2 = st.columns([2, 3])
        
        with col1:
            st.markdown("### Key Metrics")
            if st.session_state.true_labels is not None:
                y_true = st.session_state.true_labels
                y_pred = (st.session_state.predictions > 0.5).astype(int)
                st.write("Accuracy:", round(accuracy_score(y_true, y_pred), 2))
                st.write("Precision:", round(average_precision_score(y_true, y_pred), 2))
                st.write("Recall:", round(recall_score(y_true, y_pred), 2))
            else:
                st.warning("No true labels available for metrics calculation")

        with col2:
            if st.session_state.true_labels is not None:
                st.markdown("### Confusion Matrix")
                cm = confusion_matrix(y_true, y_pred)
                fig, ax = plt.subplots()
                sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                            xticklabels=["Stay", "Leave"],
                            yticklabels=["Stay", "Leave"])
                ax.set_xlabel("Predicted")
                ax.set_ylabel("Actual")
                st.pyplot(fig)

def display_risk_summary():
    st.markdown("## 🎯 Retention Risk Intelligence")
    
    data = st.session_state.uploaded_data
    if data is not None:
        if 'Risk Category' not in data.columns:
            st.warning("⚠️ Data has been uploaded but not yet processed. Please go to 'Predictive Dashboard' tab and click 'Process Data'.")
            return
        risk_counts = data['Risk Category'].value_counts()
        retired_employees = data[data['Age'] >= 60].shape[0]

        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown("### Organizational Risk Distribution")
            fig = px.sunburst(
                data,
                path=['Risk Category'],
                color='Risk Category',
                color_discrete_map={
                    'High-risk': '#EF4444',
                    'Medium-risk': '#F59E0B',
                    'Low-risk': '#10B981',
                    'Unknown': '#64748B'
                },
                hover_data=['MonthlyIncome'],
            )
            fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### Executive Summary")
            st.markdown(f"""
            <div class="metric-card">
                <p style='margin:0; font-size:14px; color:#64748B;'>High-Risk Exposure</p>
                <h2 style='margin:0; color:#EF4444;'>{risk_counts.get('High-risk', 0)}</h2>
            </div>
            <div class="metric-card">
                <p style='margin:0; font-size:14px; color:#64748B;'>Medium-Risk Exposure</p>
                <h2 style='margin:0; color:#F59E0B;'>{risk_counts.get('Medium-risk', 0)}</h2>
            </div>
            <div class="metric-card">
                <p style='margin:0; font-size:14px; color:#64748B;'>Stable Force (Low-Risk)</p>
                <h2 style='margin:0; color:#10B981;'>{risk_counts.get('Low-risk', 0)}</h2>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Please upload and process data to see risk intelligence.")
    
# Display feature importance section
def display_feature_importance():
    st.markdown("## 📈 Feature Impact Analysis")
    
    if st.session_state.uploaded_data is not None:
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]
        # Use features from the model to avoid mismatch with 'Risk Category' or other added columns
        features = np.array(get_required_features_from_model(model))[indices]

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Top 10 Drivers")
            for i, (feat, imp) in enumerate(zip(features[:10], importances[indices][:10])):
                st.markdown(f"{i+1}. **{feat}** ({imp:.3f})")

        with col2:
            st.markdown("### Feature Importance Distribution")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=importances[indices][:10], y=features[:10], ax=ax)
            ax.set_title("Top 10 Most Important Features")
            st.pyplot(fig)

def display_work_model_analysis():
    st.markdown("## 🏢 Work Model - Remote VS Office")
    
    if st.session_state.uploaded_data is not None:
        data = st.session_state.uploaded_data
        
        # Calculate commute time in minutes (assuming distance in kilometers and average speed in km/h)
        if 'CommuteTime' not in data.columns:
            data['CommuteTime'] = (data['DistanceFromHome'] * 60) / 30  # Commute time in minutes assuming 30 km/h speed
        
        # Transportation mode selection
        transportation_options = ['Bus', 'Metro', 'Car', 'Bike']
        transport_mode = st.selectbox("Select Mode of Transportation", transportation_options)

        # Average commute times based on mode of transportation (in minutes per 1 km)
        transport_commute_times = {
            'Bus': 5,    # 5 minutes per km
            'Metro': 4,  # 4 minutes per km
            'Car': 3,    # 3 minutes per km
            'Bike': 2    # 2 minutes per km
        }

        # Apply the selected mode of transportation to calculate commute times
        data['CommuteTime'] = data['DistanceFromHome'] * transport_commute_times[transport_mode]

        # Distance vs Commute Time Analysis
        with st.expander("Distance From Home vs Commute Time", expanded=True):
            st.markdown("### Distance vs Commute Time for Selected Transportation Mode")
            fig = px.scatter(
                data, 
                x='DistanceFromHome', 
                y='CommuteTime', 
                title=f"Distance From Home vs Commute Time ({transport_mode})",
                labels={"": "Distance From Home (KM)", "CommuteTime": "Commute Time (minutes)"},
                color='CommuteTime',  # Assuming 'Work Model' column exists or can be derived
                color_discrete_map={"Remote": "#FFC107", "Office": "#4CAF50", "Hybrid": "#2196F3"}
            )
            st.plotly_chart(fig, use_container_width=True)

        # Commute Time Distribution
        with st.expander("Commute Time Distribution", expanded=True):
            st.markdown("### Distribution of Employees by Commute Time (in minutes)")
            fig_dist = px.histogram(
                data, 
                x='CommuteTime', 
                nbins=20, 
                title="Distribution of Employees by Commute Time",
                labels={"CommuteTime": "Commute Time (minutes)"}
            )
            st.plotly_chart(fig_dist, use_container_width=True)

        # Employee Work Schedule Recommendations
        with st.expander("Employee Work Schedule Recommendations", expanded=True):
            st.markdown("### Recommended Work Schedule Based on Commute Time")
            
            # Define work model recommendation based on commute time
            data['Recommended Work Model'] = data['CommuteTime'].apply(
                lambda x: 'Remote' if x >= 30 else ('Office' if x < 15 else 'Hybrid')
            )

            # Display schedule data
            schedule_data = data[['EmployeeNumber', 'DistanceFromHome', 'CommuteTime', 'Recommended Work Model']]
            st.dataframe(schedule_data)

            # Insights and Recommendations
            st.markdown("### Key Insights 🔎")
            remote_count = len(data[data['Recommended Work Model'] == "Remote"])
            office_count = len(data[data['Recommended Work Model'] == "Office"])
            hybrid_count = len(data[data['Recommended Work Model'] == "Hybrid"])

            st.write(f"- **{remote_count} employees** are recommended for remote work (Commute Time ≥ 30 minutes).")
            st.write(f"- **{office_count} employees** are recommended for office work (Commute Time < 15 minutes).")
            st.write(f"- **{hybrid_count} employees** have a hybrid work model.")

            st.markdown("### Recommendations 🎯")
            st.write("- Consider remote work for employees with long commutes (over 30 minutes).")
            st.write("- Provide transportation support for employees commuting to the office.")
            st.write("- Implement a hybrid model for employees with moderate commutes (15-30 minutes).")

    else:
        st.warning("Please upload data to analyze work models.")



# --- New Streamlined Layout ---
st.title("💼 StratifyHR: Executive Attrition Terminal")
st.markdown("---")

# Use a clean 2-Tab Executive view
tabs = st.tabs([
    "📊 Predictive Intelligence", 
    "🚨 Strategic Risk Radar"
])

with tabs[0]:
    st.header("Operations & Model Diagnostics")
    display_upload_data()
    
    if st.session_state.uploaded_data is not None and st.session_state.get('processed', False):
        st.divider()
        col_acc, col_feat = st.columns(2)
        with col_acc:
            display_model_evaluation()
        with col_feat:
            display_feature_importance()
    else:
        st.info("System awaiting data ingestion for diagnostic analysis.")

with tabs[1]:
    display_risk_summary()
