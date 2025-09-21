# Gods Health AI - Backend Deployment

## 🚀 Quick Deploy to Railway

1. **Go to [Railway](https://railway.app)**
2. **Sign up/Login with GitHub**
3. **Click "New Project" → "Deploy from GitHub repo"**
4. **Select this repository**
5. **Set Root Directory to `backend`**
6. **Railway will auto-detect Python and deploy!**

## 🔧 Environment Variables (Optional)

Set these in Railway dashboard if needed:
- `FLASK_ENV=production`
- `PORT=5000` (Railway sets this automatically)

## 📋 What Railway Does Automatically

1. **Detects Python app** from `requirements.txt`
2. **Installs dependencies** with `pip install -r requirements.txt`
3. **Starts the app** with `python app.py`
4. **Provides HTTPS URL** (e.g., `https://your-app.railway.app`)

## 🔗 After Deployment

1. **Copy your Railway URL**
2. **Update `frontend/.env.production`:**
   ```
   REACT_APP_API_BASE_URL=https://your-app.railway.app
   ```
3. **Commit and push** - GitHub Pages will auto-redeploy!

## 🧪 Test Your Deployment

Visit: `https://your-railway-url.railway.app/`

You should see:
```json
{
  "message": "Welcome to Gods Health AI API",
  "predictors": [...],
  "total_predictors": 22,
  "version": "1.0.0"
}
```

## 🆘 Troubleshooting

- **Build fails?** Check Railway logs for Python/dependency errors
- **CORS errors?** The app is configured for GitHub Pages and Netlify
- **Port issues?** Railway automatically sets the PORT environment variable

---

**Your backend will be live in ~2-3 minutes! 🎉**