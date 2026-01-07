🚀 DEPLOY YOUR AI RESUME ANALYZER - GET LIVE LINK!

📋 DEPLOYMENT OPTIONS:

1️⃣ RENDER (FREE) - RECOMMENDED:
   • Go to: https://render.com
   • Sign up with GitHub
   • Click "New +" → "Web Service"
   • Connect GitHub: RANAPRINCE06/ai-resume-analyzer
   • Settings:
     - Name: ai-resume-analyzer
     - Environment: Python 3
     - Build Command: pip install -r requirements.txt && python -m spacy download en_core_web_sm && python database/init_db.py
     - Start Command: gunicorn app:app
   • Click "Create Web Service"
   • Your live link: https://ai-resume-analyzer-xxxx.onrender.com

2️⃣ RAILWAY (FREE):
   • Go to: https://railway.app
   • Sign up with GitHub
   • Click "Deploy from GitHub repo"
   • Select: RANAPRINCE06/ai-resume-analyzer
   • Auto-deploys with Procfile
   • Your live link: https://ai-resume-analyzer-production.up.railway.app

3️⃣ HEROKU (PAID):
   • Go to: https://heroku.com
   • Create new app
   • Connect GitHub repo
   • Enable automatic deploys
   • Your live link: https://your-app-name.herokuapp.com

🎯 FASTEST DEPLOYMENT (5 MINUTES):

1. Go to https://render.com
2. Sign up with GitHub account
3. Click "New +" → "Web Service"
4. Connect your repo: RANAPRINCE06/ai-resume-analyzer
5. Use these settings:
   - Build Command: pip install -r requirements.txt && python -m spacy download en_core_web_sm && python database/init_db.py
   - Start Command: gunicorn app:app
6. Click "Create Web Service"
7. Wait 5-10 minutes for deployment
8. Get your live link!

✅ FILES READY FOR DEPLOYMENT:
- Procfile ✅
- render.yaml ✅
- requirements.txt (updated with gunicorn) ✅
- All source code ✅

Your app will be live at: https://ai-resume-analyzer-xxxx.onrender.com