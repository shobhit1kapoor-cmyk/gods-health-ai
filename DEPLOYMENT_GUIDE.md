# Gods Health AI - Netlify Deployment Guide

## 🚀 Quick Deployment Steps

### Prerequisites
- GitHub account
- Netlify account (free)
- Your project pushed to GitHub

### Step 1: Prepare Your Repository

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

### Step 2: Deploy Frontend to Netlify

1. **Go to [Netlify](https://netlify.com) and sign up/login**

2. **Click "New site from Git"**

3. **Connect to GitHub and select your repository**

4. **Configure build settings:**
   - **Base directory:** `frontend`
   - **Build command:** `npm run build`
   - **Publish directory:** `frontend/build`

5. **Set environment variables in Netlify dashboard:**
   - Go to Site settings → Environment variables
   - Add: `REACT_APP_API_BASE_URL` = `your-backend-url`

6. **Deploy!** Netlify will automatically build and deploy your site.

### Step 3: Backend Deployment Options

#### Option A: Railway (Recommended)
1. Go to [Railway](https://railway.app)
2. Connect GitHub repository
3. Select the `backend` folder
4. Railway will auto-detect Python and deploy

#### Option B: Render
1. Go to [Render](https://render.com)
2. Create new Web Service
3. Connect repository
4. Set:
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`

### Step 4: Update Frontend with Backend URL

1. **Get your backend URL** from Railway/Render
2. **Update Netlify environment variables:**
   - `REACT_APP_API_BASE_URL` = `https://your-backend-url.com`
3. **Redeploy** (Netlify will auto-redeploy on environment variable changes)

## 📁 Files Created for Deployment

- ✅ `.env.production` - Production environment variables
- ✅ `netlify.toml` - Netlify configuration
- ✅ `build/` folder - Production build (ready to deploy)

## 🔧 Configuration Details

### Netlify Configuration (`netlify.toml`)
- Handles React Router routing
- Sets security headers
- Configures build settings

### Environment Variables
- `REACT_APP_API_BASE_URL` - Your backend API URL
- `REACT_APP_ENVIRONMENT` - Set to 'production'

## 🚨 Important Notes

1. **CORS Configuration:** Make sure your backend allows requests from your Netlify domain
2. **HTTPS:** Both frontend and backend should use HTTPS in production
3. **Environment Variables:** Never commit sensitive data to Git

## 🎯 Expected Results

- **Frontend URL:** `https://your-site-name.netlify.app`
- **Custom Domain:** Available in Netlify settings
- **Automatic Deployments:** Every push to main branch
- **Build Time:** ~2-3 minutes

## 🔍 Troubleshooting

### Build Fails
- Check Node.js version (should be 18+)
- Verify all dependencies in package.json
- Check build logs in Netlify dashboard

### API Calls Fail
- Verify `REACT_APP_API_BASE_URL` is correct
- Check CORS settings in backend
- Ensure backend is deployed and accessible

### Routing Issues
- Verify `netlify.toml` redirects are configured
- Check React Router setup

## 📞 Support

If you encounter issues:
1. Check Netlify build logs
2. Verify environment variables
3. Test backend API endpoints directly
4. Check browser console for errors

---

**Your Gods Health AI website is now ready for the world! 🌍**