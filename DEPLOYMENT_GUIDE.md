# Railway Deployment Guide

## Prerequisites
- Railway account (create at https://railway.app)
- Git repository pushed to GitHub/GitLab
- All model files (`.pkl` files) committed to git

## Quick Deploy (Streamlit App)

### Option 1: Deploy via Railway CLI

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login to Railway
railway login

# 3. Create new project
railway init

# 4. Deploy
railway up
```

### Option 2: Deploy via GitHub (Recommended)

1. Push code to GitHub:
```bash
git add .
git commit -m "Setup Railway deployment"
git push origin main
```

2. Go to https://railway.app/dashboard
3. Click "New Project" → "Deploy from GitHub"
4. Select your repository
5. Railway will auto-detect and deploy your Streamlit app

## Environment Variables (if needed)

Add in Railway Dashboard → Project → Variables:
```
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

## Alternative: Deploy Flask API

If you want to deploy the Flask API instead, change Procfile to:

```
web: gunicorn api:app
```

And add to requirements.txt:
```
gunicorn
```

## Model Files

Make sure all `.pkl` files are committed:
- `nexora_attrition_model.pkl`
- `department_encoder.pkl`
- `job_encoder.pkl`
- `model_config.json`

## Troubleshooting

**Error: Model file not found**
- Ensure all `.pkl` files are committed to git
- Check `.gitignore` isn't blocking them

**Error: Port already in use**
- Railway automatically assigns ports via `$PORT` variable
- Procfile already handles this

**Slow first startup**
- Streamlit installations can be slow
- First build may take 2-3 minutes

## Status Check

After deployment, Railway provides a URL like:
```
https://your-app-xxx.railway.app
```

Visit the health endpoint (Flask API):
```
https://your-api-xxx.railway.app/api/health
```

## Cost

Railway offers:
- Free tier with $5 monthly credit
- Pay-as-you-go after that
- Streamlit app typically uses ~$2-5/month
