# 11 Requirements - Quick Reference Card

**Print this or bookmark it. All 11 requirements on one page.**

---

## 📋 All 11 Requirements at a Glance

### 1️⃣ New Folder Structure ✅ READY

**Requirement**: Replace root direction to `ai_triage/new_rag_system`

**MVP**: ✅ 100% Complete
```
/Users/luoz4/research/ai_triage/new_rag_system/
  ├── app/                (Python backend)
  ├── nextjs-app/         (React frontend)
  ├── .github/workflows/  (CI/CD)
  └── config/             (Configuration)
```

**Status**: Create folder structure, copy base files  
**File**: COMPREHENSIVE_PLAN.md (section "Folder Structure")

---

### 2️⃣ Judge 90% Accuracy Potential ✅ READY

**Requirement**: Is 90% achievable?

**Answer**: YES, but requires iterations

**MVP**: ✅ Current: 69.5%
**Phase 1**: ✅ Target: 75-78% (+5-8% from decomposed pipeline)
**Phase 2**: ✅ Target: 80-82% (+2-4% from ensemble + tuning)
**Phase 3**: ✅ Target: 85-88% (+3-6% from advanced optimization)
**Future**: ✅ Target: 90%+ (+2-5% from continuous learning)

**Strategy**: 
- Monolithic model (69.5%) → Decomposed pipeline (+5-8%)
- Single model per step (+2-4%) → Model ensemble (+3-6%)
- Manual optimization (+2-5%) → Continuous learning

**File**: COMPREHENSIVE_PLAN.md (section "90% Accuracy Roadmap")

---

### 3️⃣ Better Explainability ✅ PHASE 1

**Requirement**: Intermediate responses + confidence levels

**MVP**: ⏳ Not included
```json
{
  "esi_level": 2,
  "confidence": 0.94,
  "reason": "RED FLAGS DETECTED",
  "queries_remaining": 19
}
```

**Phase 1**: ✅ Full explainability
```json
{
  "esi_level": 2,
  "confidence": 0.94,
  "reason": "RED FLAGS DETECTED",
  "intermediate_outputs": {
    "step_1_extraction": {
      "symptoms": ["chest pain", "shortness of breath"],
      "confidence": 0.92
    },
    "step_2_red_flags": {
      "detected_flags": ["chest pain + SOB", "tachycardia"],
      "is_esi_2": true,
      "confidence": 0.96
    }
  },
  "confidence_breakdown": {
    "extraction_confidence": 0.92,
    "red_flag_confidence": 0.96,
    "overall_confidence": 0.94
  }
}
```

**What**: Show reasoning chain for every decision  
**Why**: Users understand why system classified case that way  
**How**: Each detector outputs intermediate step data

**File**: COMPREHENSIVE_PLAN.md (section "Explainability Design")  
**Implementation**: app/core/explainability.py (Phase 1)

---

### 4️⃣ API Designed with Explainability ✅ PHASE 1

**Requirement**: Make sure API spec includes explainability

**MVP Endpoint**:
```
POST /classify
{
  case_text: string
}
Response:
{
  esi_level: 1-5,
  confidence: 0.0-1.0,
  reason: string,
  queries_remaining: number
}
```

**Phase 1 Endpoint** (New):
```
POST /explain
{
  case_text: string
}
Response:
{
  classification: number,
  confidence: number,
  reasoning_chain: [
    {
      step: number,
      name: string,
      output: object,
      passed: boolean
    }
  ],
  summary: string,
  confidence_breakdown: object
}
```

**Files**:
- MVP: app/api/routes/classify.py
- Phase 1: app/api/routes/explain.py

**Design**: COMPREHENSIVE_PLAN.md (section "Explainability Design")

---

### 5️⃣ Cost Breakdown & Tracking ✅ PHASE 1

**Requirement**: Track LLM costs, provide breakdown

**MVP**: ⏳ Manual tracking only (doc cost spreadsheet)

**Phase 1**: ✅ Automatic tracking
```python
# Per request tracking
monthly_cost = 12.45
daily_cost = 0.67
cost_per_query = 0.0015

# Breakdown by model
red_flag_cost = 6.21
stability_cost = 2.01
resources_cost = 2.54
urgency_cost = 1.69
```

**Admin Dashboard** (Phase 1):
```
Monthly Budget: $20.00
Spent So Far:   $12.45 (62%)
Daily Average:  $0.67
Days Remaining: 13 days
Cost Per Query: $0.0015

Breakdown by Detector:
  Red Flag:      $6.21 (50%)
  Stability:     $2.01 (16%)
  Resources:     $2.54 (20%)
  Urgency:       $1.69 (14%)
```

**File**: app/core/cost_tracker.py (Phase 1)  
**Dashboard**: nextjs-app/pages/admin/analytics.tsx (Phase 1)

---

### 6️⃣ Configurable LLM Models Per Detector ✅ PHASE 1

**Requirement**: Can select different LLM models for each component

**Config File** (YAML):
```yaml
detectors:
  red_flag:
    model: gpt-4-turbo
    temperature: 0.1
    cost_per_1k: 0.03
  
  stability:
    model: gpt-3.5-turbo
    temperature: 0.2
    cost_per_1k: 0.001
  
  resources:
    model: gpt-3.5-turbo
    temperature: 0.3
    cost_per_1k: 0.001
  
  urgency:
    model: gpt-4-turbo
    temperature: 0.2
    cost_per_1k: 0.03
```

**Why**: 
- Critical detectors (red flag) → use expensive, accurate models
- Simple detectors (stability) → use cheap, fast models
- Optimize cost-accuracy tradeoff

**Admin Can Change**:
- Via dashboard (Phase 1)
- Changes take effect immediately
- Can A/B test different models

**File**: config/llm_models.yaml  
**Selector**: app/models/selector.py (Phase 1)  
**UI**: nextjs-app/pages/admin/settings.tsx (Phase 1)

---

### 7️⃣ CI/CD at Beginning ✅ READY

**Requirement**: Set up GitHub Actions from day 1

**MVP Workflows**:
```
.github/workflows/
  ├── deploy.yml      (Deploy on merge to main)
  └── test.yml        (Run tests on PR)
```

**Deploy Workflow** (MVP):
```yaml
on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - checkout
      - build Docker images
      - deploy to Railway
```

**Phase 1 Adds**:
```
  ├── test.yml        (Unit + integration tests)
  ├── lint.yml        (Code quality checks)
  └── build.yml       (Build and push images)
```

**File**: .github/workflows/deploy.yml (MVP)  
**Reference**: COMPREHENSIVE_PLAN.md (section "CI/CD Pipeline")

---

### 8️⃣ Web UI (Next.js) + Python Backend (LangChain) ✅ PHASE 1

**Requirement**: Modern web interface + Python backend

**MVP**:
```
Frontend:  ✅ Next.js (demo page only)
           /demo route
           Simple form interface
           
Backend:   ✅ FastAPI (red flag detector)
           POST /classify endpoint
           Rate limiting
```

**Phase 1 Adds**:
```
Frontend:  ✅ Next.js enhanced
           + Admin dashboard (/admin/*)
           + Better styling
           + State management
           
Backend:   ✅ LangChain integration
           + Full 5-step pipeline
           + Explainability module
           + Cost tracking
           + Database persistence
```

**Files**:
- Backend: app/main.py + app/detectors/*.py
- Frontend: nextjs-app/pages/{demo,admin}/*.tsx
- LangChain: app/core/pipeline.py (Phase 1)

---

### 9️⃣ Demo Mode + Admin Mode ✅ PHASE 1

**Requirement**: Separate UIs for external users and admins

**Demo Mode (External Users)** ✅ MVP:
```
URL: /demo
Access: Public (no auth)
Features:
  - Text input for case description
  - Shows ESI classification
  - Shows confidence score
  - Shows reason
  - Displays queries remaining
UI: Simple, friendly, responsive
```

**Admin Mode (Dashboard)** ⏳ Phase 1:
```
URL: /admin/*
Access: Protected (API key)
Features:
  - /admin/dashboard       System status
  - /admin/settings        Model selection per detector
  - /admin/limits          Rate limit configuration
  - /admin/analytics       Usage statistics
  - /admin/logs            Query history
UI: Functional, data-rich
```

**Files**:
- Demo: nextjs-app/pages/demo.tsx (MVP)
- Admin: nextjs-app/pages/admin/*.tsx (Phase 1)

---

### 🔟 Production-Ready Design ✅ PHASE 2

**Requirement**: Prepare architecture for production

**What "Production-Ready" Means**:
```
Security:       ✅ MVP 60%, Phase 1 100%
  - Rate limiting
  - Input validation
  - API key protection
  - HTTPS/TLS

Monitoring:     ✅ MVP 0%, Phase 1 80%, Phase 2 100%
  - Structured logging
  - Metrics collection
  - Alerting rules
  - Dashboard

Reliability:    ✅ MVP 70%, Phase 1 95%, Phase 2 100%
  - Error handling
  - Graceful degradation
  - Retry logic
  - Health checks

Scalability:    ✅ MVP 30%, Phase 1 50%, Phase 2 90%
  - Load balancing
  - Auto-scaling
  - Database optimization
  - Caching layer

Disaster Recovery: ✅ MVP 10%, Phase 1 40%, Phase 2 80%
  - Backups
  - Recovery procedures
  - Failover strategy
  - Audit logs
```

**File**: PRODUCTION_READINESS.md (comprehensive checklist)

---

### 1️⃣1️⃣ Rate Limiting ✅ PHASE 1

**Requirement**: Free tier 20/day, +20 with Google auth

**MVP** (IP-based):
```
Free users:  20 queries/day per IP
Rate Limit:  In-memory tracking
Implementation: app/auth.py
UI Feedback: Show "5/20 remaining"
```

**Phase 1** (User-based + IP):
```
Free (no auth):     20 queries/day per IP
Authenticated:      40 queries/day per user (20 + 20 bonus)
Admin:              Unlimited
Budget Limit:       Admin can pause if over $20/month
```

**How It Works**:
```python
# Layer 1: IP-based (always active)
if ip_count >= 20:
    return 429 "Rate limit exceeded"

# Layer 2: User-based (if authenticated)
if user_authenticated:
    if user_count >= 40:
        return 429 "User limit exceeded"

# Layer 3: System-wide (if budget exceeded)
if monthly_cost > 20:
    return 503 "Budget exceeded, system paused"
```

**Admin Controls** (Phase 1):
```yaml
free_tier_ip_limit: 20          # Can change
auth_user_limit: 40             # Can change
monthly_budget: 20              # Can change
action_on_limit: "pause"        # pause or alert
```

**Files**:
- MVP: app/auth.py
- Phase 1: app/api/routes/admin/limits.py + UI

---

## 📊 Requirements Matrix

| # | Requirement | MVP | Phase 1 | Phase 2 | Implementation |
|---|---|---|---|---|---|
| 1 | New folder | ✅ 100% | ✅ | ✅ | Create structure |
| 2 | 90% potential | ✅ Doc | ✅ 75% | ✅ 80%+ | COMPREHENSIVE_PLAN.md |
| 3 | Explainability | ⏳ 0% | ✅ 100% | ✅ | app/core/explainability.py |
| 4 | API explainability | ⏳ 0% | ✅ 100% | ✅ | POST /explain endpoint |
| 5 | Cost tracking | ⏳ 0% | ✅ 100% | ✅ | app/core/cost_tracker.py |
| 6 | LLM config | ⏳ 0% | ✅ 100% | ✅ | config/llm_models.yaml |
| 7 | CI/CD | ✅ 80% | ✅ 100% | ✅ | .github/workflows/ |
| 8 | Web UI + Backend | ✅ 60% | ✅ 100% | ✅ | app/ + nextjs-app/ |
| 9 | Demo + Admin | ✅ Demo | ✅ Both | ✅ | /demo + /admin/* |
| 10 | Production design | ✅ 60% | ✅ 80% | ✅ 100% | PRODUCTION_READINESS.md |
| 11 | Rate limiting | ✅ IP | ✅ Both | ✅ | app/auth.py |
| **TOTAL** | | **54%** | **100%** | **100%** | **SEE BREAKDOWN BELOW** |

---

## 🎯 Implementation Priority

### Must Have (MVP Tomorrow)
1. ✅ New folder structure
2. ✅ Red flag detector (Req #2)
3. ✅ Demo UI (Req #9)
4. ✅ Rate limiting by IP (Req #11)
5. ✅ API endpoint (Req #8)
6. ✅ Deploy to Railway (Req #10)
7. ✅ GitHub Actions test (Req #7)

### Should Have (Phase 1 Week 1)
1. ✅ Full pipeline (Req #2)
2. ✅ Explainability (Req #3, #4)
3. ✅ Cost tracking (Req #5)
4. ✅ LLM config (Req #6)
5. ✅ Admin mode (Req #9)
6. ✅ Google OAuth rate limit (Req #11)
7. ✅ LangChain integration (Req #8)

### Nice to Have (Phase 2+)
1. ✅ Advanced monitoring (Req #10)
2. ✅ Auto-scaling (Req #10)
3. ✅ Advanced security (Req #10)
4. ✅ A/B testing (Req #6)

---

## 📝 Summary

**MVP (Tomorrow)**: 6 requirements (54%)
- Folder, Red Flag, Demo, Rate Limiting, API, CI/CD partial

**Phase 1 (Week 1)**: All 11 requirements (100%)
- Add: Explainability, Cost Tracking, LLM Config, Admin, OAuth

**Phase 2+ (Weeks 2-4)**: Full Production (100%)
- Enhanced: Monitoring, Security, Scaling, Disaster Recovery

---

**See detailed docs for each requirement:**
- COMPREHENSIVE_PLAN.md (master plan)
- REQUIREMENTS_MAPPING.md (requirement-by-requirement)
- PRODUCTION_READINESS.md (production checklist)

**All files in**: `/Users/luoz4/research/ai_triage/new_rag_system/`
