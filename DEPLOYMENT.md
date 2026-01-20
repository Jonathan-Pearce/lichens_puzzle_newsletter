# Deployment Guide

This application consists of two parts that need to be deployed separately:

## 1. Frontend (GitHub Pages)

The frontend is automatically deployed to GitHub Pages when you push to the main branch.

### Setup Steps:

1. Go to your GitHub repository settings
2. Navigate to **Pages** (under "Code and automation")
3. Under "Build and deployment":
   - Source: **GitHub Actions**
4. Push your code to the main branch

The frontend will be available at: `https://jonathan-pearce.github.io/lichens_puzzle_newsletter/`

### Configure Backend URL:

After deploying the backend, update the API URL in `/frontend/config.js`:

```javascript
const CONFIG = {
    API_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? `${window.location.protocol}//${window.location.host}/api`
        : 'https://YOUR-BACKEND-URL.com/api'  // Replace with actual backend URL
};
```

## 2. Backend (Python Flask)

The backend needs to be deployed to a Python-supporting platform. Here are recommended options:

### Option A: Render.com (Recommended - Free Tier Available)

1. Create account at https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: lichens-puzzle-newsletter
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Add environment variables:
   - `FLASK_DEBUG=0`
   - `PORT=10000`
   - `LICHESS_API_TOKEN=your_token`
   - `SMTP_SERVER=smtp.gmail.com`
   - `SMTP_PORT=587`
   - `SMTP_USERNAME=your_email@gmail.com`
   - `SMTP_PASSWORD=your_app_password`
   - `FROM_EMAIL=your_email@gmail.com`

**Note**: Add `gunicorn` to your `requirements.txt`:
```bash
echo "gunicorn" >> backend/requirements.txt
```

### Option B: Railway.app

1. Create account at https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Python
5. Set root directory to `backend`
6. Add the same environment variables as above

### Option C: Replit

1. Import repository to Replit
2. Set run command: `cd backend && python app.py`
3. Configure secrets (environment variables)
4. Deploy and get your URL

### Option D: Heroku

1. Install Heroku CLI
2. Create `backend/Procfile`:
   ```
   web: gunicorn app:app
   ```
3. Deploy:
   ```bash
   cd backend
   heroku create your-app-name
   heroku config:set LICHESS_API_TOKEN=your_token
   # ... set other env vars
   git push heroku main
   ```

## 3. Update CORS Settings

After deploying, update `backend/app.py` to allow requests from your GitHub Pages URL:

```python
from flask_cors import CORS

# Replace with your GitHub Pages URL
CORS(app, origins=["https://jonathan-pearce.github.io"])
```

## 4. Testing

1. Visit your GitHub Pages URL
2. Enter email and Lichess username
3. Submit the form
4. Check if the backend receives the request

## Local Development

To run locally:

```bash
# Backend
cd backend
python app.py

# Frontend - open in browser
# Visit: http://localhost:5000
```

## Environment Variables Required

- `LICHESS_API_TOKEN` - Your Lichess API token
- `SMTP_SERVER` - Email server (e.g., smtp.gmail.com)
- `SMTP_PORT` - Email port (e.g., 587)
- `SMTP_USERNAME` - Email username
- `SMTP_PASSWORD` - Email password/app password
- `FROM_EMAIL` - Sender email address
- `FLASK_DEBUG` - Set to 0 in production
- `PORT` - Port number (usually set by hosting platform)
