# Deploy Flask Backend to Render.com (Free)

## Why Render?
- **750 free hours per month** (enough for continuous hosting)
- **No credit card required** to start
- **Easy GitHub integration**
- **Custom domains supported** on free tier
- **Automatic HTTPS** certificates

## Quick Deployment Steps

### 1. Sign Up and Connect Repository
1. Go to [render.com](https://render.com) and sign up
2. Click **"New"** → **"Web Service"**
3. Connect your GitHub account and select this repository: `gods-health-ai`

### 2. Configure Deployment Settings
```
Name: gods-health-ai-backend
Branch: main
Root Directory: (leave empty)
Runtime: Python 3
Build Command: cd backend && pip install -r requirements.txt
Start Command: cd backend && gunicorn app:app --host 0.0.0.0 --port $PORT
Instance Type: Free
```

### 3. Environment Variables (Optional)
Add any environment variables your app needs in the Render dashboard.

### 4. Deploy
Click **"Create Web Service"** and wait for deployment to complete.

## After Deployment

1. **Copy your Render URL** (e.g., `https://gods-health-ai-backend.onrender.com`)

2. **Update frontend/.env.production**:
   ```bash
   REACT_APP_API_BASE_URL=https://your-app-name.onrender.com
   ```

3. **Commit and push changes**:
   ```bash
   git add frontend/.env.production
   git commit -m "Update production API URL to Render deployment"
   git push origin main
   ```

4. **GitHub Pages will automatically rebuild** with the new backend URL

## Free Tier Limitations
- Apps sleep after 15 minutes of inactivity (30-60 second wake-up time)
- 750 hours/month limit
- 1GB bandwidth included

## Alternative Free Platforms
- **Fly.io**: $5 signup credit, supports 3 free services
- **Koyeb**: One free service + PostgreSQL database
- **Google Cloud Run**: Pay-as-you-go, often $0 for small projects

## Troubleshooting
- If build fails, check that `requirements.txt` is in the `backend/` folder
- Ensure your Flask app runs on `0.0.0.0` and uses the `$PORT` environment variable
- Check logs in Render dashboard for any runtime errors