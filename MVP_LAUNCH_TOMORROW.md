# MVP Implementation Guide - Tomorrow's Launch

**Timeline**: <24 hours  
**Goal**: Red flag detector API + simple demo UI on Railway  
**Team**: 1 person  

---

## 🚀 What Ships Tomorrow

```
CRITICAL PATH (4-6 hours):
1. Red flag detector API endpoint working locally
2. Demo UI interface (HTML form)
3. Rate limiting by IP (20 requests/day)
4. Deploy backend & frontend to Railway
5. Verify both services talking

OPTIONAL (if time permits):
- Explainability endpoint
- Admin status page
- Basic error handling
```

---

## ⏱️ Hour-by-Hour Plan

### Hour 1-2: Set Up Project Structure

```bash
# Create directory structure
cd /Users/luoz4/research/ai_triage
mkdir -p new_rag_system/{app,nextjs-app,.github/workflows}

# Backend initialization
cd new_rag_system/app
python -m venv venv
source venv/bin/activate

# Create basic structure
mkdir -p {routes,detectors,models,utils}
touch main.py requirements.txt auth.py config.py
```

### Hour 2-3: Implement Red Flag Detector API

**Key files to create:**
1. `app/main.py` - FastAPI app
2. `app/detectors/red_flag.py` - Red flag logic
3. `app/auth.py` - Rate limiting
4. `app/requirements.txt` - Dependencies

### Hour 3-4: Create Demo UI (Next.js)

**Key files to create:**
1. `nextjs-app/pages/demo.tsx` - Main interface
2. `nextjs-app/pages/api/classify.ts` - API proxy
3. `nextjs-app/pages/_app.tsx` - App wrapper
4. `nextjs-app/package.json` - Dependencies

### Hour 4-5: Docker & Deployment Setup

**Key files to create:**
1. `Dockerfile` (backend)
2. `nextjs-app/Dockerfile`
3. `docker-compose.yml`
4. `.github/workflows/deploy.yml` - Auto-deploy
5. `railway.yml` - Railway config

### Hour 5-6: Test, Debug, Deploy

- Test locally with docker-compose
- Fix any issues
- Deploy to Railway
- Verify both services running

---

## 📝 Implementation Step-by-Step

### Step 1: Backend Requirements

```txt
# app/requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
redis==5.0.1
openai==1.3.0
requests==2.31.0
```

### Step 2: FastAPI Main App

```python
# app/main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from detectors.red_flag import RedFlagDetector
from auth import RateLimiter

load_dotenv()

app = FastAPI(
    title="ESI Triage Classifier - MVP",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Demo only, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize detector and rate limiter
detector = RedFlagDetector()
rate_limiter = RateLimiter()

@app.post("/classify")
async def classify(request: Request, case_text: str):
    """
    Classify case as ESI level
    
    Returns:
        {
            "esi_level": 1-5,
            "confidence": 0.0-1.0,
            "reason": "explanation",
            "intermediate": {
                "red_flags": ["flag1", "flag2"],
                "severity": 0.95
            }
        }
    """
    # Rate limit by IP
    client_ip = request.client.host
    allowed, message = rate_limiter.check_limit(client_ip)
    
    if not allowed:
        return JSONResponse(
            {"error": message},
            status_code=429
        )
    
    # Increment counter
    rate_limiter.increment(client_ip)
    
    try:
        # Classify
        result = await detector.classify(case_text)
        
        return {
            "esi_level": result["esi"],
            "confidence": result["confidence"],
            "reason": result["reason"],
            "intermediate": {
                "red_flags": result.get("flags", []),
                "severity": result.get("severity_score", 0)
            },
            "queries_remaining": rate_limiter.get_remaining(client_ip)
        }
    except Exception as e:
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "triage-classifier"}

@app.get("/info")
async def info():
    return {
        "name": "ESI Triage Classifier",
        "version": "1.0.0-mvp",
        "deployed_at": os.getenv("DEPLOYED_AT", "development")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Step 3: Red Flag Detector

```python
# app/detectors/red_flag.py
import openai
import os
from typing import Dict, Any

class RedFlagDetector:
    def __init__(self):
        self.client = openai.AsyncOpenAI(
          api_key=os.getenv("OPENROUTER_API_KEY")
        )
        self.model = "gpt-4-turbo"
    
    async def classify(self, case_text: str) -> Dict[str, Any]:
        """
        Detect red flags in case text
        Returns ESI level (prioritizes ESI-2)
        """
        
        # System prompt for red flag detection
        system_prompt = """You are an ESI (Emergency Severity Index) triage expert.
Your task: Identify if this case has RED FLAGS that would classify as ESI-2.

ESI-2 (Potentially Life-Threatening): Cases with:
- Chest pain / shortness of breath
- Severe hemorrhage / shock
- Altered mental status
- Severe allergic reaction
- Severe hypotension / hypertension
- Uncontrolled seizure
- Severe respiratory distress
- Life-threatening trauma

Return JSON:
{
    "has_red_flags": true/false,
    "flags_detected": ["flag1", "flag2"],
    "severity_score": 0.0-1.0,
    "esi_level": 1-5,
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation"
}"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Case: {case_text}"}
                ],
                temperature=0.1,  # Low for consistency
                max_tokens=300,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            return {
                "esi": result.get("esi_level", 3),
                "confidence": result.get("confidence", 0.0),
                "reason": result.get("reasoning", ""),
                "flags": result.get("flags_detected", []),
                "severity_score": result.get("severity_score", 0.0)
            }
        except Exception as e:
            # Fallback for errors
            return {
                "esi": 3,
                "confidence": 0.5,
                "reason": f"Error in classification: {str(e)}",
                "flags": [],
                "severity_score": 0.0
            }
```

### Step 4: Rate Limiting

```python
# app/auth.py
from datetime import datetime, timedelta
import os

class RateLimiter:
    def __init__(self):
        self.limit_per_day = 20
        self.limits = {}  # In-memory (fine for MVP)
    
    def check_limit(self, client_ip: str) -> tuple:
        """Check if IP has requests remaining today"""
        
        today = datetime.now().strftime("%Y-%m-%d")
        key = f"{client_ip}:{today}"
        
        count = self.limits.get(key, 0)
        
        if count >= self.limit_per_day:
            return False, f"Rate limit exceeded ({self.limit_per_day} per day)"
        
        return True, "OK"
    
    def increment(self, client_ip: str):
        """Increment request count"""
        today = datetime.now().strftime("%Y-%m-%d")
        key = f"{client_ip}:{today}"
        
        self.limits[key] = self.limits.get(key, 0) + 1
    
    def get_remaining(self, client_ip: str) -> int:
        """Get remaining requests for IP today"""
        today = datetime.now().strftime("%Y-%m-%d")
        key = f"{client_ip}:{today}"
        
        count = self.limits.get(key, 0)
        return max(0, self.limit_per_day - count)
```

### Step 5: Config Management

```python
# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Settings
    API_TITLE = "ESI Triage Classifier"
    API_VERSION = "1.0.0-mvp"
    
    # LLM Settings
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
    LLM_MODEL = "gpt-4-turbo"
    LLM_TEMPERATURE = 0.1
    LLM_MAX_TOKENS = 300
    
    # Rate Limiting
    RATE_LIMIT_PER_DAY = 20
    
    # Feature Flags
    ENABLE_EXPLAINABILITY = True
    ENABLE_COST_TRACKING = False  # Enable in Phase 1
    
    # Database (Optional for MVP)
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    
    # Deployment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
```

### Step 6: Next.js Demo UI

```typescript
// nextjs-app/pages/demo.tsx
import { useState } from 'react';
import Head from 'next/head';

export default function DemoPage() {
  const [caseText, setCaseText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [remaining, setRemaining] = useState(20);

  const handleClassify = async () => {
    if (!caseText.trim()) {
      setError('Please enter a case description');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('/api/classify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ case_text: caseText })
      });

      if (!response.ok) {
        const data = await response.json();
        setError(data.error || 'Classification failed');
        return;
      }

      const data = await response.json();
      setResult(data);
      setRemaining(data.queries_remaining || 0);
    } catch (err) {
      setError('Failed to connect to API: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const getESIColor = (esi: number) => {
    const colors = {
      1: 'bg-red-600',
      2: 'bg-red-500',
      3: 'bg-yellow-500',
      4: 'bg-blue-500',
      5: 'bg-green-500'
    };
    return colors[esi] || 'bg-gray-500';
  };

  const getESIDescription = (esi: number) => {
    const descriptions = {
      1: 'Requires Immediate Evaluation',
      2: 'Potentially Life-Threatening',
      3: 'Urgent',
      4: 'Less Urgent',
      5: 'Non-Urgent'
    };
    return descriptions[esi] || 'Unknown';
  };

  return (
    <>
      <Head>
        <title>ESI Triage Classifier - Demo</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="max-w-2xl mx-auto px-4 py-8">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              ESI Triage Classifier
            </h1>
            <p className="text-gray-600">
              AI-powered Emergency Severity Index classification
            </p>
          </div>

          {/* Main Card */}
          <div className="bg-white rounded-lg shadow-xl p-8 mb-8">
            {/* Input Section */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Patient Case Description
              </label>
              <textarea
                value={caseText}
                onChange={(e) => setCaseText(e.target.value)}
                placeholder="Enter patient symptoms, vitals, and chief complaint (e.g., '58-year-old with chest pain, SOB, HR 110, BP 140/90')..."
                className="w-full h-32 p-4 border-2 border-gray-200 rounded-lg focus:border-indigo-500 focus:outline-none resize-none"
                disabled={loading}
              />
            </div>

            {/* Error Message */}
            {error && (
              <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
                {error}
              </div>
            )}

            {/* Buttons */}
            <div className="flex gap-4 mb-6">
              <button
                onClick={handleClassify}
                disabled={loading || !caseText.trim()}
                className="flex-1 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-300 text-white font-bold py-3 px-4 rounded-lg transition"
              >
                {loading ? 'Classifying...' : 'Classify'}
              </button>
              <button
                onClick={() => {
                  setCaseText('');
                  setResult(null);
                }}
                disabled={loading}
                className="flex-1 bg-gray-200 hover:bg-gray-300 disabled:bg-gray-100 text-gray-800 font-bold py-3 px-4 rounded-lg transition"
              >
                Clear
              </button>
            </div>

            {/* Rate Limit Info */}
            <div className="text-sm text-gray-600 text-center">
              Queries remaining today: <span className="font-bold text-indigo-600">{remaining}</span>/20
            </div>
          </div>

          {/* Results Section */}
          {result && (
            <div className="bg-white rounded-lg shadow-xl p-8">
              {/* ESI Level Badge */}
              <div className={`${getESIColor(result.esi_level)} text-white p-6 rounded-lg mb-6 text-center`}>
                <div className="text-6xl font-bold mb-2">ESI-{result.esi_level}</div>
                <div className="text-xl font-semibold">{getESIDescription(result.esi_level)}</div>
                <div className="text-sm mt-2">Confidence: {(result.confidence * 100).toFixed(1)}%</div>
              </div>

              {/* Reasoning */}
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Reasoning</h3>
                <p className="text-gray-700">{result.reason}</p>
              </div>

              {/* Intermediate Outputs */}
              {result.intermediate && (
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-gray-900 mb-2">Analysis Details</h4>
                  <ul className="space-y-1 text-sm text-gray-700">
                    {result.intermediate.red_flags && result.intermediate.red_flags.length > 0 && (
                      <>
                        <li className="font-semibold text-red-600">Red Flags Detected:</li>
                        {result.intermediate.red_flags.map((flag, i) => (
                          <li key={i} className="ml-4">• {flag}</li>
                        ))}
                      </>
                    )}
                    <li className="mt-2">Severity Score: {(result.intermediate.severity * 100).toFixed(1)}%</li>
                  </ul>
                </div>
              )}

              {/* Feedback */}
              <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg text-center">
                <p className="text-sm text-gray-600">
                  Is this classification correct? <a href="mailto:feedback@example.com" className="text-blue-600 hover:underline">Send feedback</a>
                </p>
              </div>
            </div>
          )}

          {/* Footer */}
          <div className="mt-12 text-center text-gray-600 text-sm">
            <p>🔒 Demo Mode | No data is stored | For demonstration purposes only</p>
          </div>
        </div>
      </div>
    </>
  );
}
```

### Step 7: Next.js API Route

```typescript
// nextjs-app/pages/api/classify.ts
import type { NextApiRequest, NextApiResponse } from 'next';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { case_text } = req.body;

  if (!case_text) {
    return res.status(400).json({ error: 'case_text is required' });
  }

  try {
    const response = await fetch(`${API_URL}/classify`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ case_text })
    });

    if (!response.ok) {
      const errorData = await response.json();
      return res.status(response.status).json(errorData);
    }

    const data = await response.json();
    return res.status(200).json(data);
  } catch (error) {
    console.error('API Error:', error);
    return res.status(500).json({ 
      error: 'Failed to classify case',
      details: error.message 
    });
  }
}
```

### Step 8: Docker Setup

```dockerfile
# app/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# nextjs-app/Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

RUN npm run build

CMD ["npm", "start"]
```

```yaml
# docker-compose.yml
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
      - ENVIRONMENT=development
    volumes:
      - ./app:/app

  frontend:
    build:
      context: .
      dockerfile: nextjs-app/Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - backend
```

### Step 9: GitHub Actions CI/CD

```yaml
# .github/workflows/deploy.yml
name: Deploy to Railway

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Test Backend
        run: |
          cd app
          python -m pip install -r requirements.txt
          python -m pytest tests/ || echo "No tests configured"

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Railway
        run: |
          npm install -g @railway/cli
          railway up
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

### Step 10: Environment Variables

```bash
# .env
OPENROUTER_API_KEY=sk_test_your_key_here
ENVIRONMENT=development
```

---

## 🧪 Quick Testing

```bash
# Local testing
docker-compose up

# Test backend
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"case_text": "58yo with chest pain and shortness of breath"}'

# Expected response:
# {
#   "esi_level": 2,
#   "confidence": 0.95,
#   "reason": "RED FLAGS DETECTED",
#   "intermediate": {
#     "red_flags": ["chest pain", "shortness of breath"],
#     "severity": 0.95
#   },
#   "queries_remaining": 19
# }

# Test frontend
open http://localhost:3000/demo
```

---

## 🚀 Deployment Checklist

- [ ] Backend works locally
- [ ] Frontend works locally  
- [ ] Rate limiting working
- [ ] Docker images build
- [ ] Set OPENROUTER_API_KEY secret in Railway
- [ ] Deploy backend to Railway
- [ ] Deploy frontend to Railway
- [ ] Test end-to-end on Railway
- [ ] Monitor logs for errors

---

## 🔧 Common Issues & Fixes

### Issue: API not responding
```bash
# Check backend logs
docker logs new_rag_system-backend-1

# Verify API key
echo $OPENROUTER_API_KEY
```

### Issue: Frontend can't reach backend
```bash
# Verify NEXT_PUBLIC_API_URL points to Railway domain
# Update docker-compose:
# NEXT_PUBLIC_API_URL=http://backend:8000
```

### Issue: Rate limiting not working
```bash
# Check request count in memory
# For MVP, state is lost on restart (fine)
# Will use Redis in Phase 1
```

---

## 🎯 MVP Success = Tomorrow

When you can:
1. ✅ POST to /classify and get ESI-2 classification
2. ✅ See demo UI at /demo route
3. ✅ Get rate limited after 20 requests
4. ✅ Both running on Railway publicly accessible

**That's MVP! Everything else is Phase 1+ ⚡**
