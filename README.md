# ESI Triage Classifier - New RAG System

**Status**: MVP Ready for Implementation  
**Version**: 2.0 (Production-Ready Architecture)  
**Deployment**: Railway  
**Timeline**: MVP Tomorrow → Full Features Week 1 → Production Week 2+  

---

## 📖 Quick Navigation

**Start here:**
1. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Overview & key stats
2. [QUICK_LAUNCH.md](QUICK_LAUNCH.md) - Copy-paste code & commands
3. [MVP_LAUNCH_TOMORROW.md](MVP_LAUNCH_TOMORROW.md) - Hour-by-hour plan

**Deep dives:**
- [COMPREHENSIVE_PLAN.md](COMPREHENSIVE_PLAN.md) - Full architecture (30 KB)
- [REQUIREMENTS_MAPPING.md](REQUIREMENTS_MAPPING.md) - All 11 requirements tracked
- [PRODUCTION_READINESS.md](PRODUCTION_READINESS.md) - What's needed for prod

---

## 🎯 Mission

Build a production ESI (Emergency Severity Index) triage classifier that:
- **Tomorrow**: Red flag detector API + demo UI on Railway
- **Week 1**: Full 5-step pipeline + admin dashboard + cost tracking
- **Week 2+**: High accuracy (80%+) + production monitoring

---

## 🚀 MVP (Tomorrow)

### What Ships
```
✅ Red flag detector API
✅ Simple demo UI (/demo)
✅ Rate limiting (20 queries/day per IP)
✅ Deployed on Railway
✅ Health check endpoint
```

### API Example
```bash
POST /classify
Content-Type: application/json

{
  "case_text": "58-year-old with chest pain and shortness of breath"
}

Response:
{
  "esi_level": 2,
  "confidence": 0.94,
  "reason": "RED FLAGS DETECTED",
  "intermediate": {
    "red_flags": ["chest pain", "shortness of breath"],
    "severity": 0.95
  },
  "queries_remaining": 19
}
```

### Quick Start (< 1 hour)
```bash
# 1. Copy QUICK_LAUNCH.md code snippets
# 2. Create folder structure
mkdir -p app/detectors nextjs-app/pages/api .github/workflows

# 3. Create files with provided code
# app/main.py, app/detectors/red_flag.py, app/auth.py
# nextjs-app/pages/demo.tsx, nextjs-app/pages/api/classify.ts

# 4. Docker setup
docker-compose up

# 5. Test locally
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"case_text": "chest pain"}'

# 6. Deploy
railway up
```

---

## 📈 Phase 1 (Week 1)

### New Features
- ✅ Full 5-step decomposed pipeline
- ✅ Explainability layer (confidence + reasoning)
- ✅ Cost tracking (per-request, monthly budget)
- ✅ LLM model configuration (per-detector)
- ✅ Admin dashboard (settings, analytics)
- ✅ Google OAuth (+20 queries for authenticated users)

### Accuracy Target
```
MVP:     69.5% (red flag only)
Week 1:  75-78% (full pipeline)
         ↑ +5-8% gain
```

---

## 🎨 Phase 2+ (Weeks 2-4)

### Advanced Features
- ✅ Model ensemble (multiple models voting)
- ✅ Error analysis & automatic tuning
- ✅ Production monitoring & alerting
- ✅ Automated scaling
- ✅ A/B testing framework
- ✅ User feedback loop

### Accuracy Target
```
Week 1:  75-78%
Week 2:  80-82% (+2-4% ensemble + tuning)
Week 3:  85-88% (+3-6% advanced optimization)
Week 4:  90%+ (continuous learning)
```

---

## 💰 Budget

### Monthly: $20

```
OpenSwitch APIs:  ~$15 (20K demo queries)
Railway Hosting:  ~$5
────────────────────
Total:           $20 ✅

Per Query:       ~$0.0015
Daily Budget:    ~$0.67
Sustainable Load: ~1,300 queries/day
```

### Cost Control
- Uses cheaper models for non-critical steps (GPT-3.5)
- Expensive models only for critical steps (GPT-4)
- Real-time cost tracking in admin dashboard
- Auto-pause if budget exceeded

---

## 🏗️ Architecture

### 5-Step Pipeline
```
Input Case Text
    ↓
[Step 1] Extract Data
  └─ Symptoms, vitals, chief complaint
    ↓
[Step 2] Red Flag Check
  └─ ESI-2? → Return immediately if YES
    ↓
[Step 3] Stability Check
  └─ Hemodynamically stable? → ESI-3 if NO
    ↓
[Step 4] Resource Count
  └─ Any resources needed?
    ↓
[Step 5] Urgency Classification
  └─ ESI-1 or ESI-5
    ↓
Output ESI Level + Confidence + Reasoning
```

### Technology Stack
```
Frontend:       Next.js 14+ (React)
Backend:        FastAPI + Python 3.11+
LLM:            OpenSwitch (gpt-4-turbo, gpt-3.5-turbo)
Database:       PostgreSQL (Phase 1)
Deployment:     Railway
CI/CD:          GitHub Actions
Cache:          Redis (Phase 1+)
Monitoring:     Prometheus + Grafana (Phase 2+)
```

---

## 📁 Folder Structure

```
/Users/luoz4/research/ai_triage/new_rag_system/
│
├── 📋 Documentation
│   ├── README.md (this file)
│   ├── PROJECT_SUMMARY.md
│   ├── QUICK_LAUNCH.md
│   ├── MVP_LAUNCH_TOMORROW.md
│   ├── COMPREHENSIVE_PLAN.md
│   ├── REQUIREMENTS_MAPPING.md
│   └── PRODUCTION_READINESS.md
│
├── 🎨 Frontend (Next.js)
│   └── nextjs-app/
│       ├── pages/
│       │   ├── index.tsx
│       │   ├── demo.tsx           (MVP)
│       │   ├── admin/
│       │   │   ├── dashboard.tsx (Phase 1)
│       │   │   ├── settings.tsx  (Phase 1)
│       │   │   └── ...
│       │   └── api/
│       │       ├── classify.ts   (MVP)
│       │       └── ...
│       ├── components/
│       ├── Dockerfile
│       └── package.json
│
├── 🐍 Backend (Python)
│   └── app/
│       ├── main.py              (MVP)
│       ├── requirements.txt
│       ├── auth.py              (MVP)
│       ├── config.py
│       ├── detectors/
│       │   ├── red_flag.py       (MVP)
│       │   ├── stability.py      (Phase 1)
│       │   ├── resources.py      (Phase 1)
│       │   └── urgency.py        (Phase 1)
│       ├── core/
│       │   ├── pipeline.py
│       │   ├── explainability.py (Phase 1)
│       │   └── cost_tracker.py   (Phase 1)
│       ├── api/
│       │   ├── routes/
│       │   └── schemas.py
│       ├── models/
│       ├── database/
│       ├── tests/
│       ├── Dockerfile
│       └── utils/
│
├── ⚙️ Infrastructure
│   ├── docker-compose.yml
│   ├── .github/
│   │   └── workflows/
│   │       ├── deploy.yml        (MVP)
│   │       ├── test.yml          (Phase 1)
│   │       └── lint.yml          (Phase 1)
│   └── railway.yml
│
└── 📦 Configuration
    ├── config/
    │   ├── llm_models.yaml       (Phase 1)
    │   ├── rate_limits.yaml      (MVP)
    │   └── costs.yaml            (Phase 1)
    ├── .env
    └── .env.example
```

---

## 🔧 Key Concepts

### 1. Early Exit Pattern
```
Red flags detected? → ESI-2 (stop here, highest priority)
Not stable? → ESI-3 (stop here)
No resources? → ESI-5 (stop here)
→ Continue through full pipeline only if needed
```

### 2. Confidence Scores
```
Each step outputs confidence (0.0-1.0)
Final confidence = average of all steps
Shown to user for transparency
Used for error analysis
```

### 3. Cost Per Query
```
Extract: 0.01 tokens → $0.00002
Red flag: 50 tokens → $0.0005
Stability: 30 tokens → $0.0001
Resources: 40 tokens → $0.0001
Urgency: 35 tokens → $0.0001
─────────────────────────────
Total: ~155 tokens → $0.0015 per query
```

### 4. Rate Limiting Tiers
```
Free (IP-based):     20 queries/day
Authenticated (OAuth): 40 queries/day (20 + 20 bonus)
Admin:               Unlimited
System:              Can pause if budget exceeded
```

---

## 📊 Success Metrics

### MVP (Tomorrow)
- ✅ Red flag detector working
- ✅ API response < 2 seconds
- ✅ Demo UI accessible
- ✅ Rate limiting enforced
- ✅ Deployed on Railway
- ✅ No critical errors

### Phase 1 (Week 1)
- ✅ Accuracy 75-78% (↑ from 69.5%)
- ✅ All 5 pipeline steps working
- ✅ Explainability visible to users
- ✅ Admin dashboard functional
- ✅ Cost tracking accurate
- ✅ Handles 500+ concurrent users

### Phase 2+ (Weeks 2-4)
- ✅ Accuracy 80%+ (↑ from 75%)
- ✅ Handles 5000+ concurrent users
- ✅ Cost stable < $20/month
- ✅ Error rate < 1%
- ✅ Monitoring & alerting active
- ✅ Production-ready infrastructure

---

## 🚀 Implementation Roadmap

### Today (MVP Prep)
```
1. Read documentation (30 min)
2. Setup environment (30 min)
3. Create base project (1 hour)
```

### Tomorrow (MVP Deployment)
```
1. Implement backend (2 hours)
2. Implement frontend (1 hour)
3. Docker setup (30 min)
4. Deploy to Railway (30 min)
5. Test & verify (1 hour)
```

### Week 1 (Phase 1 Full)
```
Monday:   Add pipeline steps 3-5
Tuesday:  Add explainability
Wednesday: Cost tracking + LLM config
Thursday:  Admin dashboard
Friday:    Test & deploy
```

### Week 2+ (Advanced Features)
```
Week 2: Ensemble models + error analysis
Week 3: Auto-optimization + monitoring
Week 4+: Production hardening + ops
```

---

## 💡 Pro Tips

1. **Don't overthink the MVP**
   - Red flag detector only
   - In-memory rate limiting (no database)
   - Simple HTML/CSS (no fancy UI)

2. **Deploy early and often**
   - MVP to Railway ASAP
   - Test with real users immediately
   - Gather feedback for Phase 1

3. **Use the decomposition**
   - Each step is independent
   - Can optimize each separately
   - Easy to test & debug

4. **Track accuracy obsessively**
   - Every phase: measure accuracy
   - Compare to baseline
   - Root cause analysis on failures

5. **Monitor costs in real-time**
   - Know price per query
   - Can adjust models immediately
   - Budget is hard limit

---

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Railway Documentation](https://railway.app/docs)
- [OpenRouter API](https://openrouter.ai/docs)
- [LangChain Documentation](https://python.langchain.com/)

---

## 🆘 Getting Help

### If Something Breaks
1. Check logs: `docker-compose logs backend`
2. Verify env variables: `echo $OPENROUTER_API_KEY`
3. Test API directly: `curl http://localhost:8000/health`
4. Restart: `docker-compose restart`

### Common Issues
- **API not responding**: Check OPENROUTER_API_KEY
- **Frontend can't reach backend**: Check NEXT_PUBLIC_API_URL
- **Rate limiting not working**: In-memory state lost on restart (ok for MVP)
- **Cost calculation wrong**: Check token counting logic

---

## 📞 Deployment & Operations

### Deploy to Railway
```bash
npm install -g @railway/cli
railway login
railway init
railway variable set OPENROUTER_API_KEY=your_key
railway up
```

### Monitor in Production
```bash
# View logs
railway logs

# Check metrics
railway metrics

# Scale services
railway scale backend=2
```

### Rollback if Needed
```bash
# Just deploy previous commit
git revert HEAD
git push  # Triggers CI/CD
```

---

## 📅 Timeline Summary

| Phase | Timeline | Accuracy | Features | Status |
|-------|----------|----------|----------|--------|
| MVP | Tomorrow | 69.5% | Red flag API + demo UI | Ready to code |
| Phase 1 | Week 1 | 75-78% | Full pipeline + admin | Designed |
| Phase 2 | Week 2-3 | 80-82% | Ensemble + optimization | Planned |
| Phase 3 | Week 4+ | 85-88% | Advanced features | Planned |
| Future | Ongoing | 90%+ | Continuous learning | Aspirational |

---

## ✅ Launch Checklist

Before pushing to Railway:
- [ ] Backend API tests pass
- [ ] Frontend demo page works
- [ ] Rate limiting enforced
- [ ] Docker builds without errors
- [ ] Environment variables set
- [ ] GitHub Actions configured
- [ ] OPENROUTER_API_KEY ready
- [ ] Tested locally end-to-end

---

## 🎉 You're Ready!

Everything you need is documented:
- ✅ QUICK_LAUNCH.md - Copy-paste code
- ✅ MVP_LAUNCH_TOMORROW.md - Hour-by-hour plan
- ✅ COMPREHENSIVE_PLAN.md - Full architecture
- ✅ REQUIREMENTS_MAPPING.md - All 11 requirements tracked
- ✅ PRODUCTION_READINESS.md - Production checklist

**Start with QUICK_LAUNCH.md and follow the hour-by-hour plan.**

**MVP deployed tomorrow 🚀 → Full features Week 1 → Production-ready Week 2+**

Let's build this! 💪
