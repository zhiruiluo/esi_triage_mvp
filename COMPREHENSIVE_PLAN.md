# New RAG System - Comprehensive Plan v2.0

**Status**: Revised for MVP Tomorrow + Production-Ready Architecture  
**Project Path**: `/Users/luoz4/research/ai_triage/new_rag_system/`  
**Team**: 1 Person  
**Timeline**: MVP Tomorrow → Phase 1 Week 1 → Full Features TBD  
**Deployment**: Railway ($20/month budget)  

---

## 🎯 Executive Summary

### The Pivot
**From**: Decomposed pipeline (nice-to-have research project)  
**To**: Production system with demo + admin UI, explainability, cost tracking, rate limiting  
**MVP Tomorrow**: Red flag detector API + simple demo UI  
**Feasibility**: YES, with aggressive scope prioritization  

### 90% Accuracy Roadmap
```
Current RAG:         69.5%
Phase 1 (Week 1):    75-78% ← MVP + full pipeline
Phase 2 (Week 2-3):  80-82% ← Explainability + tuning
Phase 3 (Week 4-6):  85-88% ← Multi-model ensemble + reinforcement
Future Iterations:   90%+ ← Continuous improvement loop
```

**Note**: 90% reachable but requires iterations. Each phase is a separate deployment.

---

## 📁 Folder Structure (new_rag_system/)

```
/Users/luoz4/research/ai_triage/new_rag_system/
│
├── 📋 DOCUMENTATION
│   ├── README.md                          Project overview
│   ├── MVP_PLAN.md                        What ships tomorrow
│   ├── ARCHITECTURE.md                    Full system design
│   ├── API_SPEC.md                        API endpoints + schemas
│   ├── EXPLAINABILITY_DESIGN.md          Intermediate outputs
│   ├── COST_BREAKDOWN.md                 Budget tracking
│   ├── RATE_LIMITING_DESIGN.md           Free tier + rate limits
│   ├── CI_CD_PIPELINE.md                 GitHub Actions setup
│   ├── PRODUCTION_READINESS.md           Security, monitoring, scaling
│   └── 90_PERCENT_ROADMAP.md             Path to 90% accuracy
│
├── 🎨 FRONTEND (Next.js)
│   ├── nextjs-app/
│   │   ├── pages/
│   │   │   ├── index.tsx                 Landing page
│   │   │   ├── demo.tsx                  Demo mode (public)
│   │   │   ├── admin/
│   │   │   │   ├── dashboard.tsx         Admin dashboard
│   │   │   │   ├── settings.tsx          LLM model selection
│   │   │   │   ├── limits.tsx            Budget/rate limit config
│   │   │   │   ├── analytics.tsx         Usage analytics
│   │   │   │   └── logs.tsx              Audit logs
│   │   │   └── api/
│   │   │       ├── classify.ts           Proxy to backend
│   │   │       ├── explain.ts            Explainability endpoint
│   │   │       └── admin/*.ts            Admin APIs
│   │   ├── components/
│   │   │   ├── DemoInterface.tsx         User-friendly demo UI
│   │   │   ├── AdminDashboard.tsx        Admin panel
│   │   │   ├── ResponseDisplay.tsx       Show intermediate outputs
│   │   │   └── ConfidenceVisualization.tsx  Confidence scores
│   │   ├── hooks/
│   │   │   ├── useRateLimit.ts           Client-side rate limit check
│   │   │   └── useAuth.ts                Google auth integration
│   │   ├── lib/
│   │   │   ├── api.ts                    Backend API calls
│   │   │   └── storage.ts                Local storage for IP tracking
│   │   ├── styles/                       Tailwind CSS
│   │   └── package.json
│   │
│   └── Dockerfile                        Next.js container
│
├── 🐍 BACKEND (Python + LangChain)
│   ├── app/
│   │   ├── main.py                       FastAPI app entry
│   │   ├── config.py                     Settings, LLM model selection
│   │   ├── auth.py                       API key, rate limiting, Google OAuth
│   │   │
│   │   ├── core/
│   │   │   ├── pipeline.py               Main 5-step pipeline
│   │   │   ├── explainability.py         Intermediate response builder
│   │   │   └── cost_tracker.py           LLM API cost tracking
│   │   │
│   │   ├── detectors/
│   │   │   ├── extractor.py              Step 1: Extract data
│   │   │   ├── red_flag.py               Step 2: Red flags
│   │   │   ├── stability.py              Step 3: Stability
│   │   │   ├── resources.py              Step 4: Resources
│   │   │   └── urgency.py                Step 5: Urgency
│   │   │
│   │   ├── models/
│   │   │   ├── selector.py               Choose LLM per detector
│   │   │   ├── openswitch_client.py      OpenSwitch integration
│   │   │   └── cache.py                  Response caching
│   │   │
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── classify.py           POST /classify (main endpoint)
│   │   │   │   ├── explain.py            POST /explain (explainability)
│   │   │   │   ├── health.py             GET /health
│   │   │   │   └── admin/
│   │   │   │       ├── config.py         GET/POST /admin/config
│   │   │   │       ├── budget.py         GET/POST /admin/budget
│   │   │   │       ├── limits.py         GET/POST /admin/limits
│   │   │   │       ├── analytics.py      GET /admin/analytics
│   │   │   │       └── logs.py           GET /admin/logs
│   │   │   └── schemas.py                Pydantic models
│   │   │
│   │   ├── database/
│   │   │   ├── models.py                 SQLAlchemy ORM
│   │   │   ├── crud.py                   DB operations
│   │   │   └── migrations/               Alembic migrations
│   │   │
│   │   ├── utils/
│   │   │   ├── logging.py                Structured logging
│   │   │   ├── metrics.py                Prometheus metrics
│   │   │   └── errors.py                 Error handling
│   │   │
│   │   └── tests/
│   │       ├── unit/
│   │       ├── integration/
│   │       └── fixtures/
│   │
│   ├── .env.example                      Environment variables template
│   ├── requirements.txt                  Python dependencies
│   ├── Dockerfile                        Python container
│   └── docker-compose.yml                Local development
│
├── ⚙️ INFRASTRUCTURE & CI/CD
│   ├── .github/
│   │   └── workflows/
│   │       ├── test.yml                  Run tests on PR
│   │       ├── lint.yml                  Code quality checks
│   │       ├── build.yml                 Build containers
│   │       └── deploy.yml                Deploy to Railway
│   │
│   ├── docker/
│   │   ├── Dockerfile.backend            Python service
│   │   ├── Dockerfile.frontend           Next.js service
│   │   └── docker-compose.prod.yml       Production compose
│   │
│   ├── railway/
│   │   ├── railway.yml                   Railway config
│   │   └── railway.json                  Service definitions
│   │
│   └── monitoring/
│       ├── prometheus.yml                Metrics collection
│       ├── grafana.json                  Dashboard
│       └── alerts.yml                    Alert rules
│
├── 📦 CONFIGURATION
│   ├── config/
│   │   ├── llm_models.yaml              Model selection per detector
│   │   ├── api_keys.yaml                 API keys (OpenSwitch, etc)
│   │   ├── rate_limits.yaml              Rate limit thresholds
│   │   ├── costs.yaml                    Cost tracking per model
│   │   └── feature_flags.yaml            Feature toggles
│   │
│   └── secrets/
│       ├── .env.railway                  Railway environment
│       ├── .env.local                    Local development
│       └── .env.example                  Template
│
└── 📄 ROOT FILES
    ├── README.md                         Project overview
    ├── LICENSE                           MIT or your choice
    ├── docker-compose.yml                Dev setup
    ├── Makefile                          Common commands
    └── .gitignore                        Git ignore rules
```

---

## 🚀 MVP Plan - Tomorrow (Aggressive)

### What Ships Tomorrow
```
MUST HAVE (4-6 hours):
  ✅ Red flag detector working (highest safety priority)
  ✅ API endpoint: POST /classify (basic)
  ✅ Simple demo UI (HTML form + response display)
  ✅ Deployed to Railway
  ✅ Basic rate limiting by IP (20 requests/day hardcoded)

NICE TO HAVE (if time):
  ⏳ Full 5-step pipeline (or stub other steps)
  ⏳ Explainability layer (or basic explanation text)
  ⏳ Cost tracking (or hardcoded limit)
```

### MVP Architecture (Simplified)

```python
# app/main.py - MVP VERSION
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from detectors.red_flag import RedFlagDetector

app = FastAPI(title="New RAG System - MVP")
detector = RedFlagDetector()

# Rate limiting - super simple for MVP
request_counts = {}  # In-memory (fine for MVP)

@app.post("/classify")
async def classify(request: Request, case_text: str):
    # Rate limit by IP
    client_ip = request.client.host
    if request_counts.get(client_ip, 0) >= 20:
        return JSONResponse(
            {"error": "Rate limit exceeded"},
            status_code=429
        )
    request_counts[client_ip] += 1
    
    # Classify
    result = detector.classify(case_text)
    
    return {
        "esi_level": result.esi,
        "confidence": result.confidence,
        "reason": result.reason,  # Simple explanation
        "intermediate": {
            "red_flags_detected": result.flags,
            "severity_score": result.severity
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

### MVP Frontend (Next.js)

```tsx
// pages/demo.tsx - MVP VERSION
import { useState } from 'react';

export default function DemoPage() {
  const [input, setInput] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleClassify = async () => {
    setLoading(true);
    const res = await fetch('/api/classify', {
      method: 'POST',
      body: JSON.stringify({ case_text: input }),
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div className="p-8">
      <h1>ESI Triage Classifier</h1>
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Enter case description..."
        className="w-full h-32 p-2 border"
      />
      <button onClick={handleClassify} disabled={loading}>
        {loading ? 'Classifying...' : 'Classify'}
      </button>

      {result && (
        <div className="mt-8 p-4 bg-gray-100">
          <h2>Result: ESI-{result.esi_level}</h2>
          <p>Confidence: {(result.confidence * 100).toFixed(1)}%</p>
          <p>Reason: {result.reason}</p>
          <details>
            <summary>Reasoning Details</summary>
            <pre>{JSON.stringify(result.intermediate, null, 2)}</pre>
          </details>
        </div>
      )}
    </div>
  );
}
```

### MVP Deployment (Railway)

```yaml
# railway.yml
services:
  backend:
    build: ./app
    env:
      RAILWAY_DOMAIN: your-domain.up.railway.app
      DATABASE_URL: postgresql://...
    expose: 8000

  frontend:
    build: ./nextjs-app
    env:
      NEXT_PUBLIC_API_URL: https://your-domain.up.railway.app
    expose: 3000
```

### MVP Checklist (Tomorrow)
- [ ] Red flag detector API working locally
- [ ] Next.js demo page at `/demo`
- [ ] Rate limiting by IP (in-memory)
- [ ] Deployed to Railway
- [ ] Both services talking
- [ ] Test with 5 sample cases
- [ ] Document MVP limitations

---

## 📈 Phase 1 (Week 1) - Full Pipeline

### What Gets Added
```
+ Full 5-step pipeline (extractor → red flag → stability → resources → urgency)
+ Better UI (styled, responsive)
+ Admin dashboard basics (view queries, see config)
+ Cost tracking (real tracking, not hardcoded)
+ Explainability layer (confidence scores, intermediate outputs)
+ Structured logging
```

### Phase 1 Architecture Addition

```python
# app/core/pipeline.py - Full version
class TriagePipeline:
    def __init__(self, config: PipelineConfig):
        self.extractor = DataExtractor()
        self.red_flag = RedFlagDetector()
        self.stability = StabilityChecker()
        self.resources = ResourceCounter()
        self.urgency = UrgencyClassifier()
        self.explainability = ExplainabilityBuilder()
        self.cost_tracker = CostTracker()
    
    def classify(self, case_text: str) -> ClassificationResult:
        # Step 1: Extract
        extracted = self.extractor.extract(case_text)
        
        # Step 2: Red flag check
        if self.red_flag.is_esi_2(extracted):
            return self._build_result(
                esi=2,
                reason="RED FLAGS DETECTED",
                intermediate={"step_completed": 2}
            )
        
        # Step 3: Stability
        if not self.stability.check_stable(extracted):
            return self._build_result(esi=3, reason="UNSTABLE")
        
        # Step 4: Resources
        resources = self.resources.count(extracted)
        if not resources.has_any:
            return self._build_result(esi=5, reason="NO RESOURCES")
        
        # Step 5: Urgency
        esi = self.urgency.classify(resources)
        
        return self._build_result(esi=esi, reason="RESOURCE-BASED")
    
    def _build_result(self, esi, reason, intermediate=None):
        # Track cost
        self.cost_tracker.log_request(esi, reason)
        
        # Build explainability
        explain = self.explainability.build(esi, reason, intermediate)
        
        return ClassificationResult(
            esi_level=esi,
            confidence=self._calculate_confidence(esi),
            reason=reason,
            intermediate_outputs=explain
        )
```

---

## 💰 Cost Breakdown & Tracking

### Monthly Budget: $20

```
OpenSwitch Models Pricing (estimated):
  Red flag detector:      $2-3/10K requests
  Stability checker:      $1-2/10K requests  
  Resource counter:       $1-2/10K requests
  Urgency classifier:     $2-3/10K requests
  ─────────────────────────────────────────
  Total per 10K requests: ~$6-10

Query Distribution (estimated):
  Free tier (50 demo users × 20/day): ~30K/month
  Admin testing:                       ~5K/month
  ─────────────────────────────────────
  Total:                              ~35K/month

Annual Cost at 35K/month: $210-350/year ✅ Within budget

### Cost Tracking Implementation

```python
# app/core/cost_tracker.py
class CostTracker:
    def __init__(self):
        self.monthly_budget = 20  # dollars
        self.monthly_spent = 0
        self.daily_spent = {}
    
    def log_request(self, model_used: str, tokens_used: int):
        cost = self.calculate_cost(model_used, tokens_used)
        self.monthly_spent += cost
        
        if self.monthly_spent > self.monthly_budget:
            self.trigger_alert("Budget exceeded!")
            # Admin can pause system
    
    def get_analytics(self):
        return {
            "monthly_budget": self.monthly_budget,
            "monthly_spent": self.monthly_spent,
            "remaining": self.monthly_budget - self.monthly_spent,
            "percentage_used": (self.monthly_spent / self.monthly_budget) * 100
        }
```

### Admin Can Set Hard Limit

```yaml
# config/costs.yaml
budget:
  monthly_limit_usd: 20
  daily_limit_usd: 0.67
  
  # When limit hit
  action_on_limit: "pause"  # or "alert_only"
  
  # Auto-scaling (disable features if budget low)
  disable_expensive_features_at: 80%  # disable explainability layer if 80% spent
  
models:
  red_flag:
    provider: "openswitch"
    model: "fast-model"  # cheaper/faster
    cost_per_1k_tokens: 0.0001
  
  stability:
    provider: "openswitch"
    model: "fast-model"
    cost_per_1k_tokens: 0.0001
  
  # ... etc
```

---

## 🔐 Rate Limiting & Free Tier

### Three-Layer Rate Limiting

```python
# Layer 1: IP-based (no account)
# 20 requests/day per IP

# Layer 2: Account-based (with Google auth)
# 40 requests/day per account (20 + 20 bonus)

# Layer 3: Admin-set hard limit
# Can pause entire system if needed

class RateLimiter:
    def check_limit(self, client_ip: str, user_id: Optional[str]):
        # Get IP-based count
        ip_count = self.redis.get(f"ip:{client_ip}:daily") or 0
        
        # Get user-based count (if authenticated)
        user_count = 0
        if user_id:
            user_count = self.redis.get(f"user:{user_id}:daily") or 0
        
        # Check limits
        if ip_count >= 20 and not user_id:
            return False, "IP limit reached"
        
        if user_count >= 40:
            return False, "User limit reached"
        
        # Check system-wide budget
        if self.cost_tracker.is_budget_exceeded():
            return False, "System budget exceeded"
        
        return True, "OK"
```

### Google OAuth Integration

```python
# app/auth.py
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

class GoogleAuth:
    async def verify_token(self, token: str):
        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                CLIENT_ID
            )
            user_id = idinfo['sub']
            email = idinfo['email']
            
            # Give +20 free queries
            return {"user_id": user_id, "email": email, "bonus": 20}
        except ValueError:
            return None
```

---

## 🤖 LLM Model Selection (Per Detector)

### OpenRouter Integration

```yaml
# config/llm_models.yaml
providers:
  openrouter:
    api_key: "${OPENROUTER_API_KEY}"
    base_url: "https://openrouter.ai/api/v1"

detectors:
  extractor:
    provider: "openrouter"
    model: "gpt-4-turbo"      # Fast extraction
    temperature: 0.3
    max_tokens: 500
    cost_per_1k: 0.03
  
  red_flag:
    provider: "openrouter"
    model: "gpt-4-turbo"      # Best accuracy for safety
    temperature: 0.1          # Low temperature for consistency
    max_tokens: 200
    cost_per_1k: 0.03
  
  stability:
    provider: "openrouter"
    model: "gpt-3.5-turbo"    # Cheaper for binary classification
    temperature: 0.2
    max_tokens: 100
    cost_per_1k: 0.001
  
  resources:
    provider: "openswitch"
    model: "gpt-3.5-turbo"    # Extraction task, cheaper
    temperature: 0.3
    max_tokens: 300
    cost_per_1k: 0.001
  
  urgency:
    provider: "openswitch"
    model: "gpt-4-turbo"      # Complex logic, use better model
    temperature: 0.2
    max_tokens: 150
    cost_per_1k: 0.03

# Runtime selection (admin can change via dashboard)
admin_overrides:
  enabled: true
  allowed_models:
    - gpt-4-turbo
    - gpt-3.5-turbo
    - claude-2
    - etc...
```

### Model Selector Implementation

```python
# app/models/selector.py
class LLMSelector:
    def __init__(self, config_path: str):
        self.config = load_yaml(config_path)
        self.clients = {}
    
    def get_model_for_detector(self, detector_name: str):
        """Get LLM client configured for this detector"""
        config = self.config['detectors'][detector_name]
        
        # Check admin override
        if admin_override := self.get_admin_override(detector_name):
            config['model'] = admin_override
        
        # Initialize if needed
        key = f"{detector_name}_{config['model']}"
        if key not in self.clients:
            self.clients[key] = self._init_client(config)
        
        return self.clients[key]
    
    def _init_client(self, config):
        provider = config['provider']
        
        if provider == 'openrouter':
          return OpenRouterClient(
            api_key=os.getenv('OPENROUTER_API_KEY'),
                model=config['model'],
                temperature=config['temperature']
            )
        # Add other providers
```

---

## 🔍 Explainability Design

### Return Structure (Intermediate Outputs)

```python
# Response includes all intermediate steps
response = {
    "esi_level": 2,
    "confidence": 0.94,
    "reasoning": "RED FLAGS DETECTED",
    
    # Intermediate outputs for transparency
    "intermediate_outputs": {
        "step_1_extraction": {
            "symptoms": ["chest pain", "shortness of breath"],
            "vitals": {"heart_rate": 110, "bp": "140/90"},
            "confidence": 0.92
        },
        "step_2_red_flags": {
            "detected_flags": ["chest pain + SOB", "tachycardia"],
            "severity_score": 0.95,
            "is_esi_2": True,
            "confidence": 0.96
        },
        "step_3_stability": {
            "hemodynamically_stable": False,
            "reason": "HR 110, tachycardia present",
            "confidence": 0.88,
            # Would normally continue but ESI-2 gates early
        }
    },
    
    # Confidence breakdown
    "confidence_breakdown": {
        "extraction_confidence": 0.92,
        "red_flag_confidence": 0.96,
        "stability_confidence": 0.88,
        "overall_confidence": 0.94
    },
    
    # For demo UI
    "user_friendly_explanation": "This case shows critical red flags (chest pain + shortness of breath + elevated heart rate). Needs immediate evaluation as potential ESI-2 (life-threatening).",
    
    # For debugging
    "debug_info": {
        "models_used": ["gpt-4-turbo", "gpt-3.5-turbo"],
        "tokens_used": 523,
        "cost_usd": 0.0156,
        "processing_time_ms": 1240
    }
}
```

### Explainability API Endpoint

```python
# app/api/routes/explain.py
@router.post("/explain")
async def explain_decision(request: ClassifyRequest):
    """
    Return detailed explanation of classification decision
    (includes intermediate outputs, confidence scores, reasoning chain)
    """
    result = pipeline.classify(request.case_text)
    
    return {
        "classification": result.esi_level,
        "confidence": result.confidence,
        "reasoning_chain": [
            {
                "step": 1,
                "name": "Data Extraction",
                "output": result.intermediate_outputs['step_1_extraction'],
                "passed": True
            },
            {
                "step": 2,
                "name": "Red Flag Detection",
                "output": result.intermediate_outputs['step_2_red_flags'],
                "passed": True,
                "gated_early": True
            },
            # ... remaining steps
        ],
        "summary": result.user_friendly_explanation,
        "confidence_breakdown": result.confidence_breakdown
    }
```

---

## 🎨 UI/UX Design

### Demo Mode (External Users)

```
┌─────────────────────────────────────────────────┐
│         ESI Triage Classifier - Demo            │
├─────────────────────────────────────────────────┤
│                                                 │
│  Enter Patient Case Description:                │
│  ┌─────────────────────────────────────────┐   │
│  │ 58-year-old presents with chest pain... │   │
│  │                                         │   │
│  │                                         │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  [Classify]  [Clear]  [Sign In with Google]    │
│                                                 │
│  ───────────────────────────────────────────   │
│  Result: ESI-2 (Potentially Life-Threatening)  │
│  Confidence: 94%                                │
│                                                 │
│  Reasoning:                                     │
│  ✓ RED FLAGS DETECTED                          │
│    • Chest pain + shortness of breath          │
│    • Heart rate 110 (tachycardia)              │
│    • Blood pressure 140/90                      │
│                                                 │
│  [View Detailed Reasoning] [Provide Feedback]  │
│                                                 │
│  Queries remaining today: 15/20                │
│  [Sign In to Get 20 More]                      │
└─────────────────────────────────────────────────┘
```

### Admin Dashboard

```
┌─────────────────────────────────────────────────┐
│  Admin Dashboard                     [Settings] │
├─────────────────────────────────────────────────┤
│                                                 │
│  SYSTEM STATUS                                  │
│  ├─ Budget: $12.45 / $20.00 (62%)  ▓▓▓░       │
│  ├─ Daily Queries: 1,234 / unlimited          │
│  ├─ Error Rate: 0.2%                          │
│  └─ Uptime: 99.9%                             │
│                                                 │
│  MODELS CONFIGURATION                          │
│  ├─ Red Flag Detector:      gpt-4-turbo       │
│  ├─ Stability Checker:      gpt-3.5-turbo    │
│  ├─ Resource Counter:       gpt-3.5-turbo    │
│  └─ [Change Models]                           │
│                                                 │
│  RATE LIMITS                                   │
│  ├─ Free IP Limit:          20/day      [Edit]│
│  ├─ Auth User Limit:        40/day      [Edit]│
│  ├─ Monthly Budget Limit:   $20         [Edit]│
│  └─ Action on Limit:        Pause       [Edit]│
│                                                 │
│  ANALYTICS                                     │
│  ├─ Total Queries (Month):  45,123            │
│  ├─ Accuracy (vs benchmark): 75.3%            │
│  ├─ Avg Response Time:      1.2s              │
│  └─ [View Detailed Logs]                      │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions (Minimal for MVP)

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          cd app && pytest tests/
          cd ../nextjs-app && npm test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Railway
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: |
          npm install -g @railway/cli
          railway up
```

### Local Development

```bash
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./app
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/triage
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
    depends_on:
      - db

  frontend:
    build: ./nextjs-app
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000

  db:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## 🎯 90% Accuracy Roadmap

### Why 90% is Achievable (Over Time)

```
Baseline (Current):        69.5%
├─ Problem: Monolithic model
└─ Solution: Decomposed pipeline ✓

Phase 1 (Week 1):          75-78%
├─ Problem: Basic detectors, simple models
├─ Solution: 5-step pipeline working
└─ Gain: +5-8%

Phase 2 (Week 2-3):        80-82%
├─ Problem: Single model per step, no optimization
├─ Solution: Explainability enables analysis of errors
├─ Techniques:
│   • Error analysis from logs
│   • Threshold tuning per step
│   • Better prompts for red flag detector
└─ Gain: +2-4%

Phase 3 (Week 4-6):        85-88%
├─ Problem: Single model per step limits accuracy
├─ Solution: Model ensembling + specialized tuning
├─ Techniques:
│   • Use multiple OpenSwitch models, vote
│   • Fine-tune prompts based on error patterns
│   • Add rule-based fallback for edge cases
│   • Confidence thresholds per step
└─ Gain: +3-6%

Phase 4 (Ongoing):         90%+
├─ Problem: Diminishing returns, rare cases
├─ Solution: Iterative learning + human feedback
├─ Techniques:
│   • Collect user corrections via admin UI
│   • Periodic retraining on corrections
│   • A/B test new model versions
│   • Multi-agent collaboration for ambiguous cases
│   • Custom fine-tuned models (if budget allows)
└─ Gain: +2-5%
```

### Implementation Details

```python
# Phase 2: Error Analysis & Threshold Tuning
class AccuracyOptimizer:
    def analyze_errors(self, evaluation_set):
        """
        Analyze misclassifications from logs
        Identify patterns in failures
        """
        errors_by_step = defaultdict(list)
        
        for case in evaluation_set:
            predicted = self.classify(case.text)
            if predicted.esi != case.actual_esi:
                errors_by_step[case.failure_at_step].append(case)
        
        return {
            "red_flag_errors": errors_by_step['step_2'],
            "stability_errors": errors_by_step['step_3'],
            # etc...
        }
    
    def optimize_thresholds(self, error_analysis):
        """Adjust confidence thresholds based on errors"""
        for detector, errors in error_analysis.items():
            # Analyze false positives vs false negatives
            # Adjust decision thresholds
            # Retest
        pass

# Phase 3: Ensemble Methods
class EnsembleClassifier:
    def classify(self, case_text):
        """Use multiple models, take majority vote"""
        models = [
            ("gpt-4-turbo", self.gpt4_client),
            ("gpt-3.5-turbo", self.gpt35_client),
            ("claude", self.claude_client),  # If added
        ]
        
        predictions = []
        for model_name, client in models:
            pred = self.classify_with_model(case_text, client)
            predictions.append(pred)
        
        # Majority vote
        esi_votes = [p.esi for p in predictions]
        final_esi = max(set(esi_votes), key=esi_votes.count)
        
        return ClassificationResult(
            esi=final_esi,
            confidence=esi_votes.count(final_esi) / len(esi_votes),
            models_used=model_names
        )
```

---

## 🛡️ Production Readiness

### Security

```python
# API Security
- ✅ Rate limiting (IP + user-based)
- ✅ CORS configured
- ✅ API key validation (for admin endpoints)
- ✅ HTTPS/TLS enforced
- ✅ Google OAuth for authentication
- ✅ No PII in logs
- ✅ Input sanitization (prevent injection)
- ✅ SQL injection prevention (ORM usage)
```

### Monitoring & Observability

```python
# Structured Logging
import structlog

logger = structlog.get_logger()

logger.info("classification_request", case_id=123, model="gpt-4")
logger.warning("budget_threshold_warning", spent=18.50, limit=20)
logger.error("api_error", detector="red_flag", error=str(e))

# Prometheus Metrics
- classification_requests_total
- classification_errors_total
- classification_latency_seconds
- llm_api_cost_dollars
- rate_limit_violations
- budget_usage_percentage
```

### Scaling Strategy

```
MVP Scale (Current):
  - 50 demo users × 20 queries/day = 1,000 queries/day
  - 1 Railway pod, $20/month

Phase 1 Scale:
  - 500 users = 10,000 queries/day
  - Add caching layer (Redis)
  - Add database for persistence
  - Cost: $40-60/month

Future Scale:
  - 10K+ users = 200K+ queries/day
  - Load balancing
  - Auto-scaling
  - CDN for frontend
  - Cost: $200+/month
```

---

## 📋 Implementation Checklist

### MVP (Tomorrow)
- [ ] Red flag detector API working
- [ ] Demo UI (demo.tsx)
- [ ] Rate limiting by IP (20/day)
- [ ] Deploy to Railway
- [ ] Test all endpoints

### Phase 1 (Week 1)
- [ ] Full 5-step pipeline
- [ ] Admin dashboard basics
- [ ] Cost tracking
- [ ] Explainability layer
- [ ] Google OAuth
- [ ] Structured logging

### Phase 2+ (Ongoing)
- [ ] Accuracy optimization
- [ ] Model ensemble
- [ ] Fine-tuning pipeline
- [ ] User feedback collection
- [ ] A/B testing framework

---

## 📚 Configuration Files

### .env.example

```env
# OpenRouter
OPENROUTER_API_KEY=your_key_here

# Railway
RAILWAY_DOMAIN=your-app.up.railway.app
DATABASE_URL=postgresql://...

# Google OAuth
GOOGLE_CLIENT_ID=your_id_here
GOOGLE_CLIENT_SECRET=your_secret_here

# Admin Settings
MONTHLY_BUDGET_USD=20
FREE_TIER_QUERIES_PER_DAY=20
ADMIN_API_KEY=secure_key

# Feature Flags
ENABLE_EXPLAINABILITY=true
ENABLE_COST_TRACKING=true
ENABLE_GOOGLE_AUTH=true
```

---

## 🎯 Success Metrics

```
MVP Success:
  ✅ Red flag detector working
  ✅ API responding < 2 seconds
  ✅ Demo UI accessible
  ✅ Rate limiting working
  ✅ Deployed on Railway

Phase 1 Success:
  ✅ Accuracy 75-78%
  ✅ Full pipeline working
  ✅ Admin dashboard functional
  ✅ Cost tracking accurate
  ✅ Explainability showing intermediate outputs

Phase 2+ Success:
  ✅ Accuracy 80%+
  ✅ System handling 10K+ daily queries
  ✅ Error rate < 1%
  ✅ < 5% budget utilization
```

---

**Project Version**: 2.0 (Production-Ready Plan)  
**Created**: February 4, 2026  
**Status**: Ready for MVP Implementation  
**Next**: Start with MVP red flag detector + simple UI tomorrow
