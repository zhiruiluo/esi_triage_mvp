# New RAG System - Project Summary

**Status**: Ready for MVP Implementation  
**Created**: February 4, 2026  
**Version**: 2.0 (Production-Ready Plan)  

---

## 🎯 What's Happening

You're building a production ESI (Emergency Severity Index) triage classifier with:
- **MVP tomorrow**: Red flag detector API + simple demo UI
- **Phase 1 (Week 1)**: Full 5-step pipeline + admin dashboard + cost tracking
- **Phase 2+ (Weeks 2-4)**: Explainability, ensemble models, monitoring

---

## 📊 Quick Stats

| Metric | Value |
|--------|-------|
| Team Size | 1 engineer |
| MVP Timeline | < 24 hours |
| Full Feature Timeline | 2-4 weeks |
| Budget/Month | $20 |
| Target Accuracy | 90% (achievable in iterations) |
| Current Accuracy | 69.5% |
| Phase 1 Target | 75-78% |
| Deployment | Railway |
| Frontend | Next.js |
| Backend | FastAPI + LangChain |
| LLM Provider | OpenSwitch (multi-model) |

---

## 📁 Key Documents

**Location**: `/Users/luoz4/research/ai_triage/new_rag_system/`

```
COMPREHENSIVE_PLAN.md         ← Master plan (everything)
MVP_LAUNCH_TOMORROW.md        ← Hour-by-hour implementation
QUICK_LAUNCH.md               ← Copy-paste code snippets
REQUIREMENTS_MAPPING.md       ← All 11 requirements tracked
PRODUCTION_READINESS.md       ← What needs to be done for production
```

---

## 🚀 Quick Start (Tomorrow)

### What Ships Tomorrow
```
API Endpoint:  POST /classify
Response:      { esi_level, confidence, reason, queries_remaining }
Demo UI:       /demo (simple form)
Rate Limit:    20 queries/day per IP
Status:        Red flag detector only
Deployment:    Railway
```

### Hour-by-Hour Plan
```
Hour 1-2: Setup (folder structure, venv, npm init)
Hour 2-3: Backend code (FastAPI + red flag detector)
Hour 3-4: Frontend code (Next.js demo page)
Hour 4-5: Docker setup (containers + docker-compose)
Hour 5-6: Deploy (test locally, push to Railway)
```

### Critical Files to Create
```
Backend:
  app/main.py                 (FastAPI app)
  app/detectors/red_flag.py   (Red flag logic)
  app/auth.py                 (Rate limiting)
  app/requirements.txt
  Dockerfile

Frontend:
  nextjs-app/pages/demo.tsx   (Demo UI)
  nextjs-app/pages/api/classify.ts
  nextjs-app/package.json
  nextjs-app/Dockerfile

Infrastructure:
  docker-compose.yml
  .github/workflows/deploy.yml
  railway.yml
  .env
```

---

## 📈 Accuracy Roadmap

```
Current:     69.5% (monolithic model)
MVP:         69.5% (same model, just API)

Week 1:      75-78% (+5-8%)
  - Decomposed 5-step pipeline
  - Explainability layer
  
Week 2-3:    80-82% (+2-4%)
  - Error analysis & threshold tuning
  - Better prompts
  
Week 4-6:    85-88% (+3-6%)
  - Model ensemble
  - Rule-based fallbacks
  
Future:      90%+ (+2-5%)
  - Continuous learning
  - Fine-tuned models
```

---

## 💰 Cost Tracking

### Monthly Budget: $20

```
OpenSwitch Models:  ~$15/month (20K demo queries)
Railway Hosting:    ~$5/month
────────────────────────────
Total:             $20/month ✅

Per Query Cost:     ~$0.015 (decreases with scale)
Daily Budget:       ~$0.67
Daily Queries:      ~1,300 queries (sustainable)
```

### How to Stay Within Budget

1. Use cheap models for non-critical steps (gpt-3.5-turbo)
2. Use expensive models only for critical steps (gpt-4-turbo)
3. Cache responses when possible
4. Monitor cost in real-time (admin dashboard)
5. Can pause if budget hits 80%

---

## 🎯 11 Requirements Status

| # | Requirement | MVP | Phase 1 | Status |
|---|---|---|---|---|
| 1 | New folder `/new_rag_system` | ✅ | ✅ | Ready |
| 2 | 90% accuracy potential | ✅ Doc | ✅ 75% | Roadmap clear |
| 3 | Explainability (intermediate + confidence) | ⏳ | ✅ | Week 1 |
| 4 | API with explainability | ⏳ | ✅ | Week 1 |
| 5 | Cost breakdown & tracking | ⏳ | ✅ | Week 1 |
| 6 | Configurable LLM models per detector | ⏳ | ✅ | Week 1 |
| 7 | CI/CD (GitHub Actions) | ✅ | ✅ | Ready |
| 8 | Web UI (Next.js) + Backend (Python) | ✅ | ✅ | Ready |
| 9 | Demo mode + Admin mode | ✅ Demo | ✅ Both | Demo today, Admin week 1 |
| 10 | Production-ready design | ✅ Basic | ✅ 80% | Documented |
| 11 | Rate limiting (20/day free, +20 with OAuth) | ✅ IP | ✅ Both | IP today, OAuth week 1 |

**MVP Score: 6/11 (54%)**  
**Phase 1 Score: 11/11 (100%)**

---

## 🔧 Architecture Overview

### Data Flow
```
User Input
    ↓
[API] /classify
    ↓
[5-Step Pipeline]
  1. Extract data
  2. Red flag check → ESI-2 (early exit if positive)
  3. Stability check → ESI-3 (early exit if negative)
  4. Resource count → ESI-4 (depends on resources)
  5. Urgency classification → ESI-1 or ESI-5
    ↓
[Explainability Layer]
  - Confidence scores per step
  - Intermediate outputs
  - Reasoning chain
    ↓
[Cost Tracker]
  - Track tokens used
  - Calculate cost
  - Check budget
    ↓
Response to User
  {
    esi_level: 2,
    confidence: 0.94,
    reason: "RED FLAGS DETECTED",
    intermediate: {...},
    queries_remaining: 15
  }
```

### Infrastructure
```
Frontend (Next.js)
  ├─ /demo (public)
  └─ /admin (protected)
        ↓
Backend (FastAPI)
  ├─ POST /classify
  ├─ POST /explain
  ├─ GET /health
  └─ POST/GET /admin/...
        ↓
LLM API (OpenSwitch)
  └─ (gpt-4-turbo, gpt-3.5-turbo, etc)
        ↓
Database (PostgreSQL)
  └─ Audit logs, user feedback
        ↓
Railway (Deployment)
  └─ Backend + Frontend on same platform
```

---

## 🛡️ Safety Features

### MVP
- ✅ Rate limiting by IP (20/day)
- ✅ Input validation (Pydantic)
- ✅ Basic error handling
- ✅ Health check endpoint

### Phase 1
- ✅ Google OAuth (40/day for authenticated users)
- ✅ Admin API key validation
- ✅ Structured logging
- ✅ Cost tracking & budget limits
- ✅ Request timeouts

### Phase 2+
- ✅ Encryption at rest
- ✅ Advanced monitoring
- ✅ Automated backups
- ✅ Incident response runbooks

---

## 📊 Success Metrics

### MVP Success (Tomorrow)
```
✅ Red flag detector API working
✅ < 2 seconds per classification
✅ Demo UI accessible
✅ Rate limiting enforced
✅ Deployed on Railway
✅ No critical errors
```

### Phase 1 Success (Week 1)
```
✅ Accuracy 75-78% (up from 69.5%)
✅ All 5 pipeline steps working
✅ Explainability visible
✅ Admin dashboard functional
✅ Cost tracking accurate
✅ Handles 500 concurrent users
```

### Phase 2+ Success (Weeks 2-4)
```
✅ Accuracy 80%+ (up from 75%)
✅ Handles 5000+ concurrent users
✅ Cost stable at < $20/month
✅ < 1% error rate
✅ Monitoring & alerting active
```

---

## ⚠️ What to Watch

### Common Pitfalls
1. **Don't** build admin features in MVP (Week 1 only)
2. **Don't** add database in MVP (in-memory OK)
3. **Don't** worry about perfect accuracy (iterate)
4. **Don't** over-engineer (simple is better)

### What Matters Most
1. **Red flag detector working** (safety critical)
2. **API responding quickly** (< 2 sec)
3. **Rate limiting working** (cost control)
4. **Easy to deploy** (CI/CD working)

---

## 🔄 Phase Timeline

### Tomorrow (MVP)
```
Goal: Red flag detector + demo UI on Railway
Files: 6 Python files + 2 React files
Code: ~500 lines total
Effort: 4-6 hours
```

### Week 1 (Phase 1)
```
Goal: Full pipeline + admin + cost tracking
New Files: 10+ Python files + 5+ React files
Code: ~2000 lines
Effort: 40 hours
Features:
  + Explainability layer
  + Cost tracking
  + Admin dashboard (basic)
  + Google OAuth
  + LangChain integration
```

### Week 2+ (Phase 2)
```
Goal: High accuracy + production ready
New Files: Monitoring, advanced features
Code: ~1000 lines
Effort: 40+ hours
Features:
  + Ensemble models
  + A/B testing
  + User feedback loop
  + Advanced monitoring
  + Automated optimization
```

---

## 📚 Documentation Provided

```
1. COMPREHENSIVE_PLAN.md (30 KB)
   - Full architecture
   - 90% accuracy roadmap
   - Cost breakdown
   - Explainability design
   - 5-step pipeline details

2. MVP_LAUNCH_TOMORROW.md (15 KB)
   - Hour-by-hour implementation
   - Complete code snippets
   - Docker setup
   - Testing commands
   - Deployment checklist

3. QUICK_LAUNCH.md (20 KB)
   - Copy-paste ready code
   - Phase 1 snippets
   - Docker files
   - GitHub Actions
   - Environment setup

4. REQUIREMENTS_MAPPING.md (18 KB)
   - All 11 requirements mapped
   - MVP → Phase 1 → Phase 2 progression
   - Success criteria per phase
   - Cost allocation

5. PRODUCTION_READINESS.md (25 KB)
   - Security checklist
   - Monitoring setup
   - Scaling strategy
   - Disaster recovery
   - Compliance framework
```

---

## 🎬 Next Steps (Right Now!)

1. **Read QUICK_LAUNCH.md** - Get exact code to copy
2. **Create folder structure** - `mkdir -p new_rag_system/{app,nextjs-app}`
3. **Set OPENROUTER_API_KEY** - Get your API key ready
4. **Start coding** - Follow MVP_LAUNCH_TOMORROW.md hour by hour
5. **Deploy by tomorrow** - Push to Railway

---

## 💡 Key Insights

### Why 90% is Achievable
- Current monolithic model = 69.5% accuracy
- Problem: Single model tries to do everything
- Solution: 5-step specialized pipeline
- Each step: Optimized for one task
- Result: Compound improvements over 4 weeks

### Why $20/Month is Feasible
- MVP: 50 demo users × 20 queries/day = 30K queries/month
- Cost per query: ~$0.0005-0.001 with OpenSwitch
- Total: $15-30 (using cheaper models where possible)
- Optimization: Cache responses, batch processing

### Why Railway Works
- $5-20/month for both frontend & backend
- Auto-scaling built-in
- Easy deployment with git push
- HTTPS/TLS auto-managed
- Perfect for MVP + Phase 1

---

## 🚀 Final Checklist

Before you start:
- [ ] OPENROUTER_API_KEY ready
- [ ] Docker installed
- [ ] Node.js 18+ installed
- [ ] Python 3.11+ installed
- [ ] Railway account created
- [ ] GitHub Actions enabled
- [ ] Read QUICK_LAUNCH.md
- [ ] 4-6 hours uninterrupted time

---

**You've got complete docs, code snippets, and a clear roadmap.**

**Mission: MVP deployed tomorrow 🚀**
**Then iterate to 90% accuracy over 4 weeks.**

**Let's ship it!**
