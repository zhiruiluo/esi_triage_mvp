# RAG Admin Control Panel - Complete Reference

## 🎮 Admin Dashboard Commands

### 1. View Full Configuration

```bash
curl https://backend.railway.app/admin/rag/config
```

**Response Structure**:
```json
{
  "global_rag_enabled": true,
  "cost_tracking_enabled": true,
  "debug_mode": false,
  "total_layers": 7,
  "layers": {
    "layer_1": {
      "name": "Sanity Check",
      "rag_enabled": false,
      "knowledge_sources": [],
      "confidence_threshold": 0.0,
      "description": "Input validation only"
    },
    "layer_2": {
      "name": "Extraction",
      "rag_enabled": true,
      "knowledge_sources": ["medical_ontology"],
      "confidence_threshold": 0.8,
      "description": "Parse and normalize case text"
    },
    "layer_3": {
      "name": "Red Flag Detection",
      "rag_enabled": true,
      "knowledge_sources": ["esi_handbook", "acs_protocols", "sepsis_criteria", "differential_diagnosis"],
      "confidence_threshold": 0.85,
      "description": "Detect ESI-2 red flag criteria"
    },
    // ... layers 4-7
  }
}
```

---

### 2. View Specific Layer Config

```bash
curl https://backend.railway.app/admin/rag/layer/3/config
```

**Response**:
```json
{
  "layer_number": 3,
  "name": "Red Flag Detection",
  "rag_enabled": true,
  "knowledge_sources": ["esi_handbook", "acs_protocols", "sepsis_criteria", "differential_diagnosis"],
  "confidence_threshold": 0.85,
  "max_results": 5,
  "description": "Detect ESI-2 criteria using handbook and clinical guidelines",
  "last_modified": "2026-02-05T10:15:00Z"
}
```

---

### 3. Enable RAG for Layer

```bash
# Enable layer 3
curl -X POST https://backend.railway.app/admin/rag/layer/3/enable

# Enable layer 4
curl -X POST https://backend.railway.app/admin/rag/layer/4/enable
```

**Response**:
```json
{
  "status": "success",
  "layer_number": 3,
  "rag_enabled": true,
  "message": "RAG enabled for layer 3 (Red Flag Detection)"
}
```

---

### 4. Disable RAG for Layer

```bash
# Disable layer 2 (Extraction) to reduce latency
curl -X POST https://backend.railway.app/admin/rag/layer/2/disable

# Disable layer 7 (Final Decision) to reduce cost
curl -X POST https://backend.railway.app/admin/rag/layer/7/disable
```

**Response**:
```json
{
  "status": "success",
  "layer_number": 2,
  "rag_enabled": false,
  "message": "RAG disabled for layer 2 (Extraction)"
}
```

---

### 5. Update Knowledge Sources

```bash
# Use only ESI handbook for layer 6
curl -X POST "https://backend.railway.app/admin/rag/layer/6/knowledge-sources?sources=esi_handbook"

# Add multiple sources for layer 3
curl -X POST "https://backend.railway.app/admin/rag/layer/3/knowledge-sources?sources=esi_handbook&sources=acs_protocols&sources=sepsis_criteria&sources=differential_diagnosis"

# Use all available sources
curl -X POST "https://backend.railway.app/admin/rag/layer/3/knowledge-sources?sources=esi_handbook&sources=acs_protocols&sources=sepsis_criteria&sources=differential_diagnosis&sources=vital_ranges&sources=lab_indications&sources=medical_ontology"
```

**Valid Sources**:
- `esi_handbook` - ESI Handbook v4 (all levels)
- `acs_protocols` - ACS, TIMI, HEART scores
- `sepsis_criteria` - qSOFA, Phoenix, Surviving Sepsis
- `vital_ranges` - Age-specific vital standards
- `lab_indications` - Lab test guidelines and urgency
- `differential_diagnosis` - Condition lists by chief complaint
- `medical_ontology` - Terminology normalization

**Response**:
```json
{
  "status": "success",
  "layer_number": 3,
  "knowledge_sources": ["esi_handbook", "acs_protocols", "sepsis_criteria", "differential_diagnosis"],
  "message": "Knowledge sources updated for layer 3"
}
```

---

### 6. Set Confidence Threshold

```bash
# High threshold: Use only high-confidence knowledge
curl -X POST "https://backend.railway.app/admin/rag/layer/3/threshold?threshold=0.95"

# Medium threshold: Balance coverage and confidence
curl -X POST "https://backend.railway.app/admin/rag/layer/3/threshold?threshold=0.75"

# Low threshold: Use more knowledge
curl -X POST "https://backend.railway.app/admin/rag/layer/3/threshold?threshold=0.50"
```

**Threshold Guidelines**:
- **0.95+** - Strict: Only use highest confidence knowledge (few results)
- **0.85-0.90** - Balanced (Recommended): Good coverage with high confidence
- **0.70-0.80** - Permissive: More results, slightly lower confidence
- **0.50-0.70** - Aggressive: Maximum coverage (may include borderline results)

**Response**:
```json
{
  "status": "success",
  "layer_number": 3,
  "confidence_threshold": 0.95,
  "message": "Confidence threshold updated to 0.95 for layer 3"
}
```

---

### 7. Toggle Global RAG

```bash
# Disable all RAG globally (emergency)
curl -X POST "https://backend.railway.app/admin/rag/toggle-global?enabled=false"

# Re-enable all RAG
curl -X POST "https://backend.railway.app/admin/rag/toggle-global?enabled=true"
```

**Response**:
```json
{
  "status": "success",
  "global_rag_enabled": false,
  "message": "Global RAG disabled. All layers will use LLM only."
}
```

---

### 8. Reset to Defaults

```bash
curl -X POST https://backend.railway.app/admin/rag/reset-defaults
```

**Response**:
```json
{
  "status": "success",
  "message": "Configuration reset to defaults",
  "configuration": {
    "layer_1": {"rag_enabled": false},
    "layer_2": {"rag_enabled": true, "knowledge_sources": ["medical_ontology"]},
    // ... all layers reset to defaults
  }
}
```

---

### 9. Get Statistics

```bash
curl https://backend.railway.app/admin/rag/stats
```

**Response**:
```json
{
  "global_rag_enabled": true,
  "total_layers": 7,
  "layers_with_rag_enabled": 6,
  "layers_with_rag_disabled": 1,
  "total_requests_processed": 1250,
  "total_knowledge_retrievals": 8750,
  "average_retrieval_latency_ms": 145,
  "knowledge_base_size": "~400 facts",
  "layer_details": {
    "layer_1": {"rag_enabled": false, "requests": 1250},
    "layer_2": {"rag_enabled": true, "requests": 1250, "knowledge_retrievals": 1250},
    "layer_3": {"rag_enabled": true, "requests": 1250, "knowledge_retrievals": 1250},
    // ... etc
  }
}
```

---

## 📊 Admin Dashboard Workflows

### Workflow 1: Maximizing Accuracy

**Goal**: Get the best possible classification accuracy

```bash
# Step 1: Enable all RAG globally
curl -X POST "https://backend.railway.app/admin/rag/toggle-global?enabled=true"

# Step 2: Lower confidence thresholds to use more knowledge
curl -X POST "https://backend.railway.app/admin/rag/layer/3/threshold?threshold=0.75"
curl -X POST "https://backend.railway.app/admin/rag/layer/4/threshold?threshold=0.80"
curl -X POST "https://backend.railway.app/admin/rag/layer/5/threshold?threshold=0.75"
curl -X POST "https://backend.railway.app/admin/rag/layer/6/threshold?threshold=0.80"

# Step 3: Add all knowledge sources to critical layers
curl -X POST "https://backend.railway.app/admin/rag/layer/3/knowledge-sources?sources=esi_handbook&sources=acs_protocols&sources=sepsis_criteria&sources=differential_diagnosis&sources=vital_ranges&sources=lab_indications"

# Step 4: Verify configuration
curl https://backend.railway.app/admin/rag/config | jq '.layers'

# Step 5: Test with sample cases
curl -X POST https://backend.railway.app/classify \
  -H "Content-Type: application/json" \
  -d '{"case_text": "58yo male with chest pain"}'
```

---

### Workflow 2: Reducing Latency

**Goal**: Minimize response time

```bash
# Step 1: Disable non-critical layers
curl -X POST "https://backend.railway.app/admin/rag/layer/2/disable"
curl -X POST "https://backend.railway.app/admin/rag/layer/7/disable"

# Step 2: Increase confidence thresholds (fewer results to process)
curl -X POST "https://backend.railway.app/admin/rag/layer/3/threshold?threshold=0.92"
curl -X POST "https://backend.railway.app/admin/rag/layer/4/threshold?threshold=0.95"
curl -X POST "https://backend.railway.app/admin/rag/layer/5/threshold?threshold=0.90"

# Step 3: Use minimal knowledge sources
curl -X POST "https://backend.railway.app/admin/rag/layer/3/knowledge-sources?sources=esi_handbook"
curl -X POST "https://backend.railway.app/admin/rag/layer/5/knowledge-sources?sources=lab_indications"

# Step 4: Verify latency improvement
# Monitor response times for several requests
```

---

### Workflow 3: Cost Optimization

**Goal**: Minimize API costs

```bash
# Step 1: Disable RAG for lowest-impact layers
curl -X POST "https://backend.railway.app/admin/rag/layer/1/disable"
curl -X POST "https://backend.railway.app/admin/rag/layer/2/disable"

# Step 2: Use single knowledge source per layer
curl -X POST "https://backend.railway.app/admin/rag/layer/3/knowledge-sources?sources=esi_handbook"
curl -X POST "https://backend.railway.app/admin/rag/layer/4/knowledge-sources?sources=vital_ranges"
curl -X POST "https://backend.railway.app/admin/rag/layer/5/knowledge-sources?sources=lab_indications"

# Step 3: Increase confidence threshold (fewer results = shorter prompts)
for layer in 3 4 5 6; do
  curl -X POST "https://backend.railway.app/admin/rag/layer/$layer/threshold?threshold=0.92"
done

# Step 4: Monitor cost per request
# Expected reduction: 20-30% cost savings
```

---

### Workflow 4: Testing New Protocol

**Goal**: Test a new clinical protocol (e.g., new ACS guidelines)

```bash
# Step 1: Create test and control groups by disabling for test
curl -X POST "https://backend.railway.app/admin/rag/layer/3/disable"

# Step 2: Run some test cases with RAG disabled
# Test cases here...

# Step 3: Re-enable and test same cases with RAG
curl -X POST "https://backend.railway.app/admin/rag/layer/3/enable"

# Step 4: Compare accuracy
# Protocol A (RAG disabled) vs Protocol B (RAG enabled)

# Step 5: Deploy better protocol
# If RAG better: keep enabled
# If RAG worse: disable and investigate
```

---

### Workflow 5: Debugging Low Accuracy

**Goal**: Identify and fix accuracy problems

```bash
# Step 1: Check if RAG is enabled
curl https://backend.railway.app/admin/rag/stats

# Step 2: If disabled, enable globally
curl -X POST "https://backend.railway.app/admin/rag/toggle-global?enabled=true"

# Step 3: Check specific layer thresholds
curl https://backend.railway.app/admin/rag/layer/3/config

# Step 4: Lower threshold to use more knowledge
curl -X POST "https://backend.railway.app/admin/rag/layer/3/threshold?threshold=0.70"

# Step 5: Verify knowledge sources
curl https://backend.railway.app/admin/rag/layer/3/config | jq '.knowledge_sources'

# Step 6: Add more sources if needed
curl -X POST "https://backend.railway.app/admin/rag/layer/3/knowledge-sources?sources=esi_handbook&sources=acs_protocols&sources=differential_diagnosis"

# Step 7: Re-test problematic cases
# Monitor accuracy improvement
```

---

## 🔍 Troubleshooting Commands

### Check Backend Health
```bash
curl https://backend.railway.app/health
# Expected: {"status": "healthy"}
```

### Verify Admin Routes Loaded
```bash
curl https://backend.railway.app/admin/rag/config
# If 404, check app/main.py includes admin router
```

### Test Classification with RAG
```bash
curl -X POST https://backend.railway.app/classify \
  -H "Content-Type: application/json" \
  -d '{
    "case_text": "58 year old male presents with chest pain, shortness of breath, heart rate 110"
  }'
```

### Check Current Configuration
```bash
curl https://backend.railway.app/admin/rag/config | jq '.' | less
```

### View Layer Statistics
```bash
curl https://backend.railway.app/admin/rag/stats | jq '.layer_details'
```

### Test Layer Toggle
```bash
# Before
curl https://backend.railway.app/admin/rag/layer/3/config | jq '.rag_enabled'

# Disable
curl -X POST https://backend.railway.app/admin/rag/layer/3/disable

# After (should be false)
curl https://backend.railway.app/admin/rag/layer/3/config | jq '.rag_enabled'

# Re-enable
curl -X POST https://backend.railway.app/admin/rag/layer/3/enable
```

---

## 📈 Performance Monitoring Commands

### Monitor Response Latency
```bash
time curl -X POST https://backend.railway.app/classify \
  -H "Content-Type: application/json" \
  -d '{"case_text": "test"}'
# Real: Check "real" time
```

### Batch Test for Latency
```bash
for i in {1..10}; do
  echo "Request $i:"
  time curl -X POST https://backend.railway.app/classify \
    -H "Content-Type: application/json" \
    -d '{"case_text": "58yo chest pain"}'
  echo ""
done
```

### Monitor Cost Impact
```bash
# Get stats before and after toggling RAG
curl https://backend.railway.app/admin/rag/stats > stats_before.json

# Disable expensive layers
curl -X POST https://backend.railway.app/admin/rag/layer/3/disable
curl -X POST https://backend.railway.app/admin/rag/layer/4/disable

# Run some requests
for i in {1..100}; do
  curl -X POST https://backend.railway.app/classify \
    -H "Content-Type: application/json" \
    -d '{"case_text": "test"}'
done

# Get stats after
curl https://backend.railway.app/admin/rag/stats > stats_after.json

# Compare cost difference
```

---

## 🎯 Pre-Built Configuration Presets

### Preset 1: Production (Balanced)
```bash
#!/bin/bash
echo "Setting production configuration..."

# Enable all layers
curl -X POST https://backend.railway.app/admin/rag/toggle-global?enabled=true

# Medium thresholds
for layer in 2 3 4 5 6 7; do
  curl -X POST "https://backend.railway.app/admin/rag/layer/$layer/threshold?threshold=0.82"
done

# Standard sources
curl -X POST "https://backend.railway.app/admin/rag/layer/3/knowledge-sources?sources=esi_handbook&sources=acs_protocols&sources=sepsis_criteria&sources=differential_diagnosis"

echo "Production configuration applied"
```

### Preset 2: Maximum Accuracy
```bash
#!/bin/bash
echo "Setting maximum accuracy configuration..."

curl -X POST https://backend.railway.app/admin/rag/toggle-global?enabled=true

# Low thresholds
for layer in 2 3 4 5 6 7; do
  curl -X POST "https://backend.railway.app/admin/rag/layer/$layer/threshold?threshold=0.65"
done

# All sources
for layer in 3 5; do
  curl -X POST "https://backend.railway.app/admin/rag/layer/$layer/knowledge-sources?sources=esi_handbook&sources=acs_protocols&sources=sepsis_criteria&sources=differential_diagnosis&sources=vital_ranges&sources=lab_indications"
done

echo "Maximum accuracy configuration applied"
```

### Preset 3: Low Latency
```bash
#!/bin/bash
echo "Setting low latency configuration..."

# Disable non-critical layers
curl -X POST https://backend.railway.app/admin/rag/layer/2/disable
curl -X POST https://backend.railway.app/admin/rag/layer/7/disable

# High thresholds
for layer in 3 4 5 6; do
  curl -X POST "https://backend.railway.app/admin/rag/layer/$layer/threshold?threshold=0.92"
done

# Minimal sources
curl -X POST "https://backend.railway.app/admin/rag/layer/3/knowledge-sources?sources=esi_handbook"

echo "Low latency configuration applied"
```

### Preset 4: Cost Optimized
```bash
#!/bin/bash
echo "Setting cost-optimized configuration..."

# Disable expensive layers
curl -X POST https://backend.railway.app/admin/rag/layer/1/disable
curl -X POST https://backend.railway.app/admin/rag/layer/2/disable
curl -X POST https://backend.railway.app/admin/rag/layer/7/disable

# Single source per layer
curl -X POST "https://backend.railway.app/admin/rag/layer/3/knowledge-sources?sources=esi_handbook"
curl -X POST "https://backend.railway.app/admin/rag/layer/4/knowledge-sources?sources=vital_ranges"
curl -X POST "https://backend.railway.app/admin/rag/layer/5/knowledge-sources?sources=lab_indications"

# High thresholds
for layer in 3 4 5 6; do
  curl -X POST "https://backend.railway.app/admin/rag/layer/$layer/threshold?threshold=0.90"
done

echo "Cost-optimized configuration applied"
```

---

## 📋 Configuration Checklist

Before deploying to production:

- [ ] All admin endpoints responding (test with curl)
- [ ] Configuration file loads correctly
- [ ] Can enable/disable individual layers
- [ ] Can update knowledge sources
- [ ] Can set confidence thresholds
- [ ] Can toggle global RAG
- [ ] Can reset to defaults
- [ ] Statistics endpoint working
- [ ] Changes persist after restart
- [ ] No errors in logs
- [ ] Response time acceptable
- [ ] Cost tracking accurate

---

## Summary

The RAG Admin Control Panel provides complete runtime control over the 7-layer triage pipeline. All 9 admin endpoints enable:

✅ **Enable/Disable** RAG per layer without redeployment
✅ **Configure** knowledge sources for each layer
✅ **Optimize** confidence thresholds for accuracy/latency tradeoff
✅ **Monitor** usage statistics in real-time
✅ **Test** different configurations easily
✅ **Rollback** to defaults if needed
✅ **Scale** from MVP to production-ready system

**Recommended Approach**: Start with Production (Balanced) preset, monitor accuracy, adjust thresholds as needed.
