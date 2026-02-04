# Quick Launch Checklist - Copy & Paste Ready

**Mission**: Red flag detector API + demo UI on Railway tomorrow  
**Duration**: <24 hours  
**Team**: 1 engineer  

---

## Phase 1: Setup (0-1 hours)

```bash
# Initialize project
cd /Users/luoz4/research/ai_triage
mkdir -p new_rag_system
cd new_rag_system

# Create core directories
mkdir -p app/{detectors,utils}
mkdir -p nextjs-app/{pages/api,components}
mkdir -p .github/workflows

# Backend setup
cd app
python3 -m venv venv
source venv/bin/activate
cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
openai==1.3.0
requests==2.31.0
EOF
pip install -r requirements.txt

# Frontend setup (from new_rag_system/)
cd ../nextjs-app
npm init -y
npm install next react react-dom
cat > package.json << 'EOF'
{
  "name": "triage-demo",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.3.6"
  }
}
EOF
npm install
```

---

## Phase 2: Backend Code (1-2 hours)

### app/main.py
```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from detectors.red_flag import RedFlagDetector
from auth import RateLimiter

load_dotenv()

app = FastAPI(title="ESI Triage - MVP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

detector = RedFlagDetector()
rate_limiter = RateLimiter()

@app.post("/classify")
async def classify(request: Request, case_text: str):
    client_ip = request.client.host
    allowed, msg = rate_limiter.check_limit(client_ip)
    
    if not allowed:
        return JSONResponse({"error": msg}, status_code=429)
    
    rate_limiter.increment(client_ip)
    result = await detector.classify(case_text)
    
    return {
        **result,
        "queries_remaining": rate_limiter.get_remaining(client_ip)
    }

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### app/detectors/red_flag.py
```python
import openai
import os
import json

class RedFlagDetector:
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=os.getenv("OPENROUTER_API_KEY"))
    
    async def classify(self, case_text: str):
        prompt = """Analyze this case for ESI-2 red flags (life-threatening).
Return JSON:
{
    "has_flags": true/false,
    "flags": ["flag1"],
    "esi": 1-5,
    "confidence": 0.0-1.0,
    "reason": "brief"
}"""
        
        try:
            resp = await self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": case_text}
                ],
                temperature=0.1,
                max_tokens=200,
                response_format={"type": "json_object"}
            )
            return json.loads(resp.choices[0].message.content)
        except:
            return {
                "esi": 3,
                "confidence": 0.5,
                "reason": "Error",
                "flags": []
            }
```

### app/auth.py
```python
from datetime import datetime

class RateLimiter:
    def __init__(self):
        self.limits = {}
        self.daily_limit = 20
    
    def check_limit(self, ip: str):
        key = f"{ip}:{datetime.now().strftime('%Y-%m-%d')}"
        count = self.limits.get(key, 0)
        return count < self.daily_limit, "Rate limit" if count >= self.daily_limit else "OK"
    
    def increment(self, ip: str):
        key = f"{ip}:{datetime.now().strftime('%Y-%m-%d')}"
        self.limits[key] = self.limits.get(key, 0) + 1
    
    def get_remaining(self, ip: str):
        key = f"{ip}:{datetime.now().strftime('%Y-%m-%d')}"
        return max(0, self.daily_limit - self.limits.get(key, 0))
```

---

## Phase 3: Frontend Code (2-3 hours)

### nextjs-app/pages/demo.tsx
```typescript
import { useState } from 'react';

export default function Demo() {
  const [input, setInput] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const classify = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await fetch('/api/classify', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({case_text: input})
      });
      const data = await res.json();
      if (!res.ok) setError(data.error);
      else setResult(data);
    } catch(e) {
      setError('API error: ' + e.message);
    }
    setLoading(false);
  };

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-4xl font-bold mb-6">ESI Triage Classifier</h1>
      
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Enter case..."
        className="w-full h-32 p-2 border rounded mb-4"
      />
      
      <button
        onClick={classify}
        disabled={loading}
        className="bg-blue-600 text-white px-6 py-2 rounded"
      >
        {loading ? 'Classifying...' : 'Classify'}
      </button>
      
      {error && <div className="text-red-600 mt-4">{error}</div>}
      
      {result && (
        <div className="mt-6 p-4 bg-gray-100 rounded">
          <h2 className="text-2xl font-bold mb-2">ESI-{result.esi}</h2>
          <p>Confidence: {(result.confidence * 100).toFixed(0)}%</p>
          <p>Reason: {result.reason}</p>
          <p className="text-sm mt-4">Remaining: {result.queries_remaining}/20</p>
        </div>
      )}
    </div>
  );
}
```

### nextjs-app/pages/api/classify.ts
```typescript
import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') return res.status(405).end();

  const api_url = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  
  try {
    const response = await fetch(`${api_url}/classify`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(req.body)
    });
    
    const data = await response.json();
    res.status(response.status).json(data);
  } catch (error) {
    res.status(500).json({error: 'Backend error'});
  }
}
```

### nextjs-app/.env.local
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### nextjs-app/next.config.js
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {}
module.exports = nextConfig
```

---

## Phase 4: Docker & Deployment (3-4 hours)

### app/Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY app/requirements.txt .
RUN pip install -r requirements.txt
COPY app/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### nextjs-app/Dockerfile
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY nextjs-app/package*.json ./
RUN npm ci
COPY nextjs-app/ .
RUN npm run build
CMD ["npm", "start"]
```

### docker-compose.yml
```yaml
version: '3.8'
services:
  backend:
    build:
      context: .
      dockerfile: app/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
  
  frontend:
    build:
      context: .
      dockerfile: nextjs-app/Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
```

### railway.yml
```yaml
services:
  backend:
    build: ./app
    port: 8000
  
  frontend:
    build: ./nextjs-app
    port: 3000
```

### .env
```
OPENROUTER_API_KEY=your_key_here
```

---

## Phase 5: Test Locally (4-5 hours)

```bash
# From new_rag_system/ directory

# Start services
docker-compose up

# In another terminal, test backend
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"case_text": "58yo chest pain"}'

# Open frontend
open http://localhost:3000/demo

# Test the UI with a few cases
```

---

## Phase 6: Deploy to Railway (5-6 hours)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create project
railway init

# Set environment variables
railway variable set OPENROUTER_API_KEY=your_key_here

# Deploy
railway up

# Get domain
railway domain

# Test deployed version
open https://your-app.up.railway.app/demo
```

---

## ✅ Success Criteria (MVP is Done When)

- [ ] POST /classify returns ESI-1 or ESI-2 for high-risk cases
- [ ] Demo UI at /demo is accessible
- [ ] Rate limiting enforces 20 requests/day
- [ ] Both services running on Railway
- [ ] No errors in logs
- [ ] Takes <2s per classification
- [ ] JSON responses valid

---

## 🚨 If Behind Schedule

**Drop these features:**
1. Nice UI styling → Keep it minimal
2. Error handling → Use try/except everywhere
3. Docker multi-stage builds → Use simple Dockerfile
4. Railway domain custom config → Use default Railway domain
5. Explainability → Return just ESI level + confidence

---

## 📞 Debugging Commands

```bash
# View logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild containers
docker-compose build --no-cache

# Clear everything
docker-compose down -v

# Test API health
curl http://localhost:8000/health

# View environment
docker-compose exec backend printenv | grep OPENSWITCH
```

---

**Target**: Everything done by tomorrow morning ⚡**

Good luck! You've got this! 🚀
