# 🚀 NEXORA ATTRITION PREDICTION API

**Status:** ✅ Running on `http://localhost:5000`

---

## 📋 API Endpoints

### 1. **Health Check**
```
GET /api/health
```
**Response:**
```json
{
  "status": "ok",
  "message": "Attrition API is running"
}
```

---

### 2. **Single Employee Prediction** 
```
POST /api/predict-attrition
```

**Request Body:**
```json
{
  "salary": 5000,
  "performanceRating": 3,
  "jobTitle": "Sales Executive",
  "employee_id": "E123",
  "employee_name": "Ali Khan"
}
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
    ],
    "salary": 5000,
    "performance_rating": 3,
    "job_title": "Sales Executive",
    "employee_id": "E123",
    "employee_name": "Ali Khan"
  }
}
```

---

### 3. **Batch Prediction** ⚡
```
POST /api/predict-attrition-batch
```

**Request Body:**
```json
{
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
    },
    {
      "salary": 5000,
      "performanceRating": 3,
      "jobTitle": "Analyst",
      "employee_id": "E125",
      "employee_name": "Hassan Ali"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "total_employees": 3,
  "predictions": [
    {
      "risk_score": 1.0,
      "risk_percentage": 100.0,
      "risk_category": "High-risk",
      "factors": [
        "⚠️ Low salary (< 3000)",
        "⚠️ Low performance rating",
        "⚠️ High-attrition role: Sales Executive"
      ],
      "employee_id": "E123",
      "employee_name": "Ali Khan"
    },
    {
      "risk_score": 0.857,
      "risk_percentage": 85.7,
      "risk_category": "High-risk",
      "factors": [
        "✅ High performance rating",
        "✅ Stable role: Manager"
      ],
      "employee_id": "E124",
      "employee_name": "Fatima Ahmed"
    },
    {
      "risk_score": 1.0,
      "risk_percentage": 100.0,
      "risk_category": "High-risk",
      "factors": [],
      "employee_id": "E125",
      "employee_name": "Hassan Ali"
    }
  ],
  "summary": {
    "high_risk": {
      "count": 3,
      "percentage": 100.0,
      "employees": [
        {"id": "E123", "name": "Ali Khan", "risk_score": 1.0},
        {"id": "E124", "name": "Fatima Ahmed", "risk_score": 0.857},
        {"id": "E125", "name": "Hassan Ali", "risk_score": 1.0}
      ]
    },
    "medium_risk": {
      "count": 0,
      "percentage": 0.0,
      "employees": []
    },
    "low_risk": {
      "count": 0,
      "percentage": 0.0,
      "employees": []
    },
    "average_risk_score": 0.952
  }
}
```

---

### 4. **Get Model Configuration**
```
GET /api/config
```

**Response:**
```json
{
  "model_version": "1.0",
  "required_fields": ["salary", "performanceRating", "jobTitle"],
  "supported_job_titles": [
    "Sales Executive",
    "Research Scientist",
    "Laboratory Technician",
    "Manufacturing Director",
    "Healthcare Representative",
    "Manager",
    "Technical Lead",
    "Analyst",
    "Developer",
    "Designer"
  ],
  "performance_rating_scale": "1-5 (1=low, 5=high)",
  "risk_categories": ["Low-risk", "Medium-risk", "High-risk"]
}
```

---

## 🔧 **How to Use with Nexora**

### **Step 1: API is Running**
```
✅ http://localhost:5000
```

### **Step 2: In Nexora, Create API Connector**
- **Name:** Attrition Prediction
- **Base URL:** `http://localhost:5000`
- **Type:** HTTP/REST

### **Step 3: Add API Action in Nexora**
- **Method:** POST
- **Endpoint:** `/api/predict-attrition-batch`
- **Payload Template:**
```
{
  "employees": [
    {
      "employee_id": {{employeeId}},
      "employee_name": {{employeeName}},
      "salary": {{salary}},
      "performanceRating": {{performanceRating}},
      "jobTitle": {{jobTitle}}
    }
  ]
}
```

### **Step 4: Use in Workflows/Rules**
- Trigger on employee data changes
- Get attrition risk prediction
- Create alerts for High-risk employees
- Auto-send retention offers

---

## 📊 **Risk Scoring Logic**

| Score | Category | Action |
|-------|----------|--------|
| 0 - 0.33 | 🟢 **Low-risk** | Monitor |
| 0.33 - 0.66 | 🟡 **Medium-risk** | Review & Plan |
| 0.66 - 1.0 | 🔴 **High-risk** | Immediate Action |

**Factors Considered:**
1. **Salary (40%)** - Lower salary = Higher attrition risk
2. **Performance Rating (30%)** - Lower rating = Higher risk
3. **Job Title (30%)** - Some roles have naturally higher attrition

---

## 🧪 **Test with cURL**

### **Health Check**
```bash
curl http://localhost:5000/api/health
```

### **Single Prediction**
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

### **Batch Prediction**
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

---

## 🔐 **Security Notes**
- Currently running in **DEBUG mode** (for development only)
- For production, use **WSGI server** (Gunicorn, uWSGI)
- Add **API authentication** (API Keys, OAuth)
- Enable **HTTPS/SSL**

---

## ⚡ **Next Steps**

1. ✅ Copy this API URL to Nexora
2. ✅ Create API connector in Nexora
3. ✅ Test with sample data
4. ✅ Create workflows/automations
5. ✅ Deploy to production server

---

**API Created:** February 16, 2026  
**Version:** 1.0 (Beta)
