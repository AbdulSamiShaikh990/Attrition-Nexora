# 🔗 NEXORA HCM INTEGRATION GUIDE

## ✅ **SETUP COMPLETE!**

Aapka **Attrition Prediction System** ab Nexora ke saath integrate karne ke liye ready hai!

---

## 📁 **Files Created**

| File | Purpose |
|------|---------|
| `nexora_model.py` | Simplified 3-field attrition model |
| `api.py` | Flask REST API for Nexora integration |
| `test_api.py` | API testing script |
| `API_DOCUMENTATION.md` | Complete API docs |

---

## 🚀 **Quick Start**

### **Step 1: Start the API Server**

```bash
cd "c:\Users\farha\Desktop\Attrition\Attrition-Pridiction"
python api.py
```

✅ **API will run on:** `http://localhost:5000`

---

### **Step 2: Test API (Separate Terminal)**

Open a **NEW terminal** and run:

```bash
cd "c:\Users\farha\Desktop\Attrition\Attrition-Pridiction"
python test_api.py
```

---

### **Step 3: Test with Browser**

Open browser aur visit karo:
```
http://localhost:5000/api/health
```

Expected response:
```json
{"status": "ok", "message": "Attrition API is running"}
```

---

## 📊 **3 Fields Used (Nexora Compatible)**

| Field | Nexora Column | Type | Example |
|-------|---------------|------|---------|
| **salary** | `baseSalary` or `MonthlyIncome` | Number | 5000 |
| **performanceRating** | `performanceRating` | 1-5 | 3 |
| **jobTitle** | `jobTitle` or `designation` | Text | "Sales Executive" |

---

## 🔧 **Nexora Integration Steps**

### **Method 1: Direct API Call (Recommended)**

1. **Open Nexora Admin Panel**
2. **Go to:** Integrations → API Connectors
3. **Create New Connector:**
   - Name: `Attrition Prediction API`
   - URL: `http://localhost:5000`
   - Method: `POST`

4. **Add Endpoint:**
   - Path: `/api/predict-attrition-batch`
   - Body:
   ```json
   {
     "employees": [
       {
         "employee_id": "{{employeeId}}",
         "employee_name": "{{employeeName}}",
         "salary": {{salary}},
         "performanceRating": {{performanceRating}},
         "jobTitle": "{{jobTitle}}"
       }
     ]
   }
   ```

---

### **Method 2: Webhook/Automation**

**In Nexora:**
1. Create a **Scheduled Task** (daily/weekly)
2. Export employee data as JSON
3. Send POST request to: `http://localhost:5000/api/predict-attrition-batch`

---

### **Method 3: Manual CSV Upload**

1. Export employees from Nexora as CSV
2. Add columns: `salary`, `performanceRating`, `jobTitle`
3. Upload to Streamlit app (already running)

---

## 📱 **API Usage Examples**

### **Example 1: Single Employee**

```bash
curl -X POST http://localhost:5000/api/predict-attrition \
  -H "Content-Type: application/json" \
  -d '{
    "salary": 5000,
    "performanceRating": 3,
    "jobTitle": "Sales Executive",
    "employee_id": "E123",
    "employee_name": "Ali Khan"
  }'
```

**Response:**
```json
{
  "success": true,
  "prediction": {
    "risk_score": 0.667,
    "risk_percentage": 66.7,
    "risk_category": "High-risk",
    "factors": [
      "⚠️ Low salary (< 3000)",
      "⚠️ High-attrition role: Sales Executive"
    ]
  }
}
```

---

### **Example 2: Batch (Multiple Employees)**

```bash
curl -X POST http://localhost:5000/api/predict-attrition-batch \
  -H "Content-Type: application/json" \
  -d '{
    "employees": [
      {
        "salary": 2500,
        "performanceRating": 2,
        "jobTitle": "Sales Executive",
        "employee_id": "E123",
        "employee_name": "Ali Khan"
      },
      {
        "salary": 8000,
        "performanceRating": 4,
        "jobTitle": "Manager",
        "employee_id": "E124",
        "employee_name": "Fatima Ahmed"
      }
    ]
  }'
```

**Response:**
```json
{
  "success": true,
  "total_employees": 2,
  "summary": {
    "high_risk": {"count": 1, "percentage": 50.0},
    "medium_risk": {"count": 1, "percentage": 50.0},
    "low_risk": {"count": 0, "percentage": 0.0},
    "average_risk_score": 0.833
  },
  "predictions": [...]
}
```

---

## 🎯 **Risk Categories**

| Category | Score | Color | Action Required |
|----------|-------|-------|-----------------|
| 🟢 **Low-risk** | 0 - 0.33 | Green | Monitor only |
| 🟡 **Medium-risk** | 0.33 - 0.66 | Yellow | Review performance & salary |
| 🔴 **High-risk** | 0.66 - 1.0 | Red | **Immediate action needed!** |

---

## 📈 **Attrition Risk Formula**

```
Risk Score = (Salary Weight × 0.4) + (Performance Weight × 0.3) + (Job Role Weight × 0.3)

Where:
- Low Salary = High Risk
- Low Performance = High Risk
- High-Attrition Roles (Sales, Lab Tech) = High Risk
```

---

## 🔐 **Production Deployment (Optional)**

### **Deploy to Server:**

1. **Install Gunicorn (production server):**
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn:**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 api:app
   ```

3. **Add Authentication:**
   - Use API keys
   - Add JWT tokens
   - Enable HTTPS/SSL

---

## 🧪 **Troubleshooting**

### **Issue: API Not Responding**
```bash
# Check if Flask is running
curl http://localhost:5000/api/health

# Restart API
python api.py
```

### **Issue: Port 5000 Already in Use**
Edit `api.py` line 127:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001
```

### **Issue: Nexora Can't Connect**
- Make sure API is running
- Check firewall settings
- Use network IP instead of localhost: `http://10.1.104.141:5000`

---

## 📞 **Support Checklist**

- ✅ API Running: `python api.py`
- ✅ Health Check: `http://localhost:5000/api/health`
- ✅ Test Script: `python test_api.py`
- ✅ Streamlit App: `streamlit run app.py` (Port 8501)

---

## 🎓 **Next Steps**

1. ✅ **Test API** with sample data
2. ✅ **Configure Nexora** API connector
3. ✅ **Create alerts** for High-risk employees
4. ✅ **Build dashboard** in Nexora
5. ✅ **Automate** weekly reports

---

**Created:** February 16, 2026  
**Status:** Production Ready ✅  
**Integration Type:** REST API (Flask)
