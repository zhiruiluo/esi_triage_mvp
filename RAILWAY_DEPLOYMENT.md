# Railway Deployment Guide

## Option 1: Deploy Backend Only (Recommended for MVP)

Railway works best with single-service deployments. Deploy backend first:

### Step 1: Create New Project
1. Go to [Railway](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select `zhiruiluo/esi_triage_mvp`

### Step 2: Configure Backend Service
Railway will auto-detect the build. If not, configure manually:

**Build Settings:**
- Root Directory: `/` (leave empty or set to root)
- Build Command: `pip install -r app/requirements.txt` (auto-detected)
- Start Command: `cd app && uvicorn main:app --host 0.0.0.0 --port $PORT`

**Environment Variables:**
```
OPENROUTER_API_KEY=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
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=gpt-4-turbo
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=300
RATE_LIMIT_PER_DAY=20
PORT=8000
```

### Step 3: Deploy
1. Click "Deploy"
2. Wait for build to complete
3. Copy the public URL (e.g., `https://your-app.railway.app`)

### Step 4: Test Backend
```bash
curl https://your-app.railway.app/health
curl -X POST https://your-app.railway.app/classify \
  -H "Content-Type: application/json" \
  -d '{"case_text": "58-year-old with chest pain"}'
```

---

## Option 2: Deploy Frontend (After Backend)

### Create Second Service for Frontend:
1. In same Railway project, click "New Service"
2. Select same GitHub repo
3. Configure:

**Build Settings:**
- Root Directory: `nextjs-app`
- Build Command: `npm install && npm run build`
- Start Command: `npm start`

**Environment Variables:**
```
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
PORT=3000
```

---

## Option 3: Use Dockerfile Deployment

Railway can detect and use your Dockerfiles:

### Backend (Preferred):
1. Railway will auto-detect `app/Dockerfile`
2. Or manually set Dockerfile path: `app/Dockerfile`

### Frontend:
1. Set Dockerfile path: `nextjs-app/Dockerfile`
2. Set environment variables as above

---

## Troubleshooting

### "Error creating build plan with Railpack"
This happens when Railway can't auto-detect the project type.

**Solution 1: Use railway.toml (already created)**
- Railway will use the `railway.toml` in the repo root
- It specifies Dockerfile build and start command

**Solution 2: Use nixpacks.toml (already created)**
- Alternative to railway.toml for Nixpacks builder

**Solution 3: Manual Configuration**
In Railway dashboard:
- Settings → Build → Custom Start Command
- Enter: `cd app && uvicorn main:app --host 0.0.0.0 --port $PORT`

### Port Issues
- Railway provides `$PORT` env variable dynamically
- Make sure start command uses `--port $PORT`

### Build Failures
- Check logs in Railway dashboard
- Verify all environment variables are set
- Ensure Python 3.11+ is used

---

## Quick Deploy Commands

If using Railway CLI:
```bash
# Install CLI
npm i -g @railway/cli

# Login
railway login

# Link to project (or create new)
railway link

# Add environment variables
railway variables set OPENROUTER_API_KEY=sk-or-v1-...
railway variables set OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
railway variables set LLM_MODEL=gpt-4-turbo

# Deploy
railway up
```

---

## Cost Considerations

**Railway Free Tier:**
- $5 free credit per month
- ~500 hours of usage
- Sufficient for MVP testing

**Estimated Usage:**
- Backend: ~1GB RAM, minimal CPU
- LLM API costs via OpenRouter (separate)
- Rate limit (20/day) helps control costs

---

## Next Steps After Deployment

1. Test all endpoints
2. Update frontend `NEXT_PUBLIC_API_URL` if deploying frontend
3. Monitor logs in Railway dashboard
4. Set up custom domain (optional)
5. Configure production-ready rate limits and monitoring
