"""
Knowledge base and RAG system for medical triage.
Retrieves clinical evidence from vector DB to augment LLM reasoning.
"""

import json
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from openai import AsyncOpenAI

# For vector similarity (will integrate with Pinecone/Weaviate in production)
try:
    import pinecone
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False


@dataclass
class RetrievalResult:
    """Result from knowledge base retrieval"""
    query: str
    collection: str
    results: List[Dict[str, Any]]
    num_results: int
    confidence_scores: List[float]


class KnowledgeBase:
    """
    Central RAG system for medical triage.
    Retrieves clinical evidence to augment LLM decision-making.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.llm = AsyncOpenAI(
            api_key=config.get("openrouter_api_key"),
            base_url=config.get("openrouter_base_url", "https://openrouter.ai/api/v1")
        )
        
        # Initialize vector DB (Pinecone or mock)
        self.use_vector_db = config.get("use_vector_db", False)
        if self.use_vector_db and PINECONE_AVAILABLE:
            pinecone.init(
                api_key=config.get("pinecone_api_key"),
                environment=config.get("pinecone_env", "us-west1-gcp")
            )
            self.index = pinecone.Index(config.get("pinecone_index", "medical-triage"))
        else:
            self.index = None
        
        # Load knowledge documents
        self.knowledge_docs = self._load_knowledge_documents()
        
    def _load_knowledge_documents(self) -> Dict[str, List[Dict]]:
        """Load medical knowledge from embedded documents"""
        return {
            "esi_handbook": self._load_esi_handbook(),
            "acs_protocols": self._load_acs_protocols(),
            "sepsis_criteria": self._load_sepsis_criteria(),
            "vital_ranges": self._load_vital_ranges(),
            "lab_indications": self._load_lab_indications(),
            "differential_diagnosis": self._load_differentials()
        }
    
    def _load_esi_handbook(self) -> List[Dict]:
        """ESI Handbook v4 criteria and decision rules"""
        return [
            {
                "id": "esi_1_definition",
                "level": 1,
                "name": "Resuscitation",
                "definition": "Patient requires immediate life-saving intervention (intubation, defibrillation, emergency medications)",
                "examples": ["Unresponsive", "Severe respiratory distress", "Shock", "Severe trauma"]
            },
            {
                "id": "esi_2_definition",
                "level": 2,
                "name": "Emergency",
                "definition": "High-risk situations requiring immediate physician evaluation and room assignment",
                "red_flags": [
                    "Severe pain",
                    "Altered mental status",
                    "Hemodynamic instability",
                    "Severe respiratory distress",
                    "Acute vision loss",
                    "Chest or abdominal pain in high-risk patient",
                    "Acute hemorrhage"
                ]
            },
            {
                "id": "esi_2_chest_pain",
                "level": 2,
                "condition": "Chest Pain",
                "criteria": "Any patient with chest pain and high-risk features (age >40, known CAD, SOB, diaphoresis, risk factors)",
                "required_tests": ["ECG", "Troponin", "CXR"],
                "source": "ESI Handbook + ACC/AHA ACS Guidelines"
            },
            {
                "id": "esi_3_definition",
                "level": 3,
                "name": "Urgent",
                "definition": "Patient with multiple resources needed or semicritical condition",
                "criteria": "Requires 2+ resources; hemodynamically stable; non-severe presentations"
            },
            {
                "id": "esi_4_definition",
                "level": 4,
                "name": "Less Urgent",
                "definition": "Patient who may require 1 resource",
                "examples": ["Single lab test", "Single imaging study", "Wound care"]
            },
            {
                "id": "esi_5_definition",
                "level": 5,
                "name": "Minimal",
                "definition": "Patient with no resources needed",
                "criteria": "No workup, observation, or interventions required"
            },
            {
                "id": "esi_resource_discrimination",
                "title": "ESI Resource Discrimination Rules",
                "content": "0 resources → ESI-5, 1 resource → ESI-4, 2+ resources → ESI-3 (unless ESI-2 by other criteria)"
            }
        ]
    
    def _load_acs_protocols(self) -> List[Dict]:
        """ACS evaluation and risk stratification protocols"""
        return [
            {
                "id": "timi_score",
                "name": "TIMI Risk Score for UA/NSTEMI",
                "components": [
                    {"variable": "Age ≥65 years", "points": 1},
                    {"variable": "≥3 CAD risk factors", "points": 1},
                    {"variable": "Known CAD", "points": 1},
                    {"variable": "ASA use in past 7 days", "points": 1},
                    {"variable": "Severe angina (≥2 episodes in 24h)", "points": 1},
                    {"variable": "ST changes", "points": 1},
                    {"variable": "Elevated cardiac biomarkers", "points": 1}
                ],
                "risk_stratification": {
                    "0-1": "5% risk at 14 days (consider discharge)",
                    "2-4": "Intermediate risk (admission likely)",
                    "≥5": "High risk (admission + aggressive management)"
                }
            },
            {
                "id": "heart_score",
                "name": "HEART Score for Major Cardiac Events",
                "components": [
                    {"variable": "History (typical chest pain)", "points": "0-2"},
                    {"variable": "EKG changes", "points": "0-2"},
                    {"variable": "Age", "points": "0-2"},
                    {"variable": "Risk factors (smoking, HTN, HC, DM, family Hx)", "points": "0-2"},
                    {"variable": "Troponin elevation", "points": "0-3"}
                ],
                "risk_categories": {
                    "0-3": "0.9-1.7% MACE (discharge candidate)",
                    "4-6": "12-16.6% MACE (admission advised)",
                    "≥7": "50-65% MACE (early invasive measures)"
                }
            },
            {
                "id": "acs_workup",
                "title": "ACS Workup Protocol",
                "stat_tests": ["12-lead ECG (within 10 min)", "Troponin (STAT)"],
                "concurrent_tests": ["CBC", "CMP", "Coagulation studies"],
                "imaging": ["CXR (rule out other causes)"],
                "monitoring": "Continuous cardiac monitoring for ischemic changes"
            }
        ]
    
    def _load_sepsis_criteria(self) -> List[Dict]:
        """Sepsis recognition and risk stratification"""
        return [
            {
                "id": "sepsis_3_definition",
                "title": "Sepsis-3 Definition (JAMA 2016)",
                "definition": "Life-threatening organ dysfunction due to dysregulated host response to infection",
                "key_change": "Moved away from SIRS criteria to organ dysfunction focus"
            },
            {
                "id": "qsofa_score",
                "name": "Quick Sequential Organ Failure Assessment (qSOFA)",
                "components": [
                    {"variable": "Altered mentation", "points": 1},
                    {"variable": "Systolic BP ≤100 mmHg", "points": 1},
                    {"variable": "Respiratory rate ≥22", "points": 1}
                ],
                "interpretation": {
                    "≥2": "Higher mortality risk in ED setting",
                    "note": "Low qSOFA does NOT exclude sepsis (poor sensitivity)"
                }
            },
            {
                "id": "phoenix_criteria_pediatric",
                "title": "Phoenix Sepsis Criteria for Children (2024 Update)",
                "replaces": "2005 SIRS criteria",
                "components": [
                    "Temperature",
                    "Respiratory rate",
                    "Oxygen requirement",
                    "Systolic BP",
                    "Lactate",
                    "Behavior"
                ],
                "interpretation": "Phoenix score ≥2 = sepsis, with shock if cardiovascular dysfunction present"
            },
            {
                "id": "sepsis_workup",
                "title": "Sepsis Workup Protocol",
                "stat_actions": [
                    "Blood cultures (before antibiotics)",
                    "Lactate level",
                    "CBC, CMP, coagulation",
                    "Source imaging (CXR, imaging of suspected source)",
                    "Early broad-spectrum antibiotics"
                ],
                "goal": "Lactate clearance <10% or normalization within 6 hours"
            }
        ]
    
    def _load_vital_ranges(self) -> List[Dict]:
        """Age-specific vital sign normal ranges"""
        return [
            {
                "age_group": "Infant 0-3 months",
                "hr_normal": "100-160 bpm",
                "sbp_normal": "50-70 mmHg",
                "rr_normal": "30-40",
                "temp_normal": "97-99°F"
            },
            {
                "age_group": "Infant 3-6 months",
                "hr_normal": "100-160 bpm",
                "sbp_normal": "60-80 mmHg",
                "rr_normal": "25-40",
                "temp_normal": "97-99°F"
            },
            {
                "age_group": "Infant 6-12 months",
                "hr_normal": "80-120 bpm",
                "sbp_normal": "70-100 mmHg",
                "rr_normal": "25-35",
                "temp_normal": "98-99°F"
            },
            {
                "age_group": "Toddler 1-2 years",
                "hr_normal": "80-130 bpm",
                "sbp_normal": "80-110 mmHg",
                "rr_normal": "20-30",
                "temp_normal": "98-99°F"
            },
            {
                "age_group": "Child 3-6 years",
                "hr_normal": "70-110 bpm",
                "sbp_normal": "80-110 mmHg",
                "rr_normal": "20-25",
                "temp_normal": "98-99°F"
            },
            {
                "age_group": "Child 7-11 years",
                "hr_normal": "70-110 bpm",
                "sbp_normal": "90-130 mmHg",
                "rr_normal": "18-22",
                "temp_normal": "98.6°F"
            },
            {
                "age_group": "Adolescent 12+ years",
                "hr_normal": "60-100 bpm",
                "sbp_normal": "110-140 mmHg",
                "rr_normal": "12-20",
                "temp_normal": "98.6°F"
            },
            {
                "age_group": "Adult 18-65 years",
                "hr_normal": "60-100 bpm",
                "sbp_normal": "<120 mmHg",
                "rr_normal": "12-20",
                "temp_normal": "98.6°F",
                "note": "SBP 120-140 considered elevated; 140+ is hypertension Stage 1"
            },
            {
                "age_group": "Geriatric 65+ years",
                "hr_normal": "60-100 bpm (may be blunted)",
                "sbp_normal": "Up to 150/90 mmHg often acceptable",
                "rr_normal": "12-20",
                "temp_normal": "97-98°F (lower baseline common)",
                "note": "Assess for ACUTE change from baseline, not absolute values"
            }
        ]
    
    def _load_lab_indications(self) -> List[Dict]:
        """Laboratory test indications and interpretation"""
        return [
            {
                "test": "Troponin (high-sensitivity)",
                "indications": ["Chest pain", "Dyspnea", "Syncope", "Hemodynamic instability"],
                "interpretation": ">99th percentile = concerning for MI",
                "esi_relevance": "Normal troponin helps rule out ACS; ESI-3 if negative in low-risk"
            },
            {
                "test": "CBC",
                "indications": ["Infection suspected", "Anemia", "Bleeding", "Shock"],
                "red_flags": ["WBC >11K or <4K", "Hemoglobin <10", "Platelets <100K"],
                "esi_relevance": "Abnormalities often require admission (ESI-3)"
            },
            {
                "test": "Lactate",
                "indications": ["Sepsis", "Shock", "Multi-trauma", "Altered mental status"],
                "interpretation": ">2 mmol/L abnormal; >4 mmol/L severe",
                "esi_relevance": "Elevated lactate = potential ESI-2 (shock concern)"
            },
            {
                "test": "D-dimer",
                "indications": ["PE/DVT rule-out", "Wells score <2"],
                "caveat": "Highly sensitive but low specificity; don't order for low-risk presentations",
                "esi_relevance": "Normal D-dimer may allow lower ESI if PE risk low"
            },
            {
                "test": "Procalcitonin",
                "indications": ["Sepsis risk stratification", "Bacterial infection suspected"],
                "interpretation": "Emerging marker; >0.5 ng/mL suggests bacterial infection",
                "esi_relevance": "May help stratify sepsis risk (ESI-2 vs ESI-3)"
            }
        ]
    
    def _load_differentials(self) -> List[Dict]:
        """Differential diagnosis lists for common presentations"""
        return [
            {
                "chief_complaint": "Chest Pain",
                "differentials": [
                    {"diagnosis": "Acute Coronary Syndrome", "probability": 0.35, "severity": "HIGH"},
                    {"diagnosis": "Pulmonary Embolism", "probability": 0.15, "severity": "HIGH"},
                    {"diagnosis": "Aortic Dissection", "probability": 0.05, "severity": "HIGH"},
                    {"diagnosis": "Pneumothorax", "probability": 0.10, "severity": "MODERATE"},
                    {"diagnosis": "Pneumonia", "probability": 0.15, "severity": "MODERATE"},
                    {"diagnosis": "Musculoskeletal", "probability": 0.15, "severity": "LOW"},
                    {"diagnosis": "GERD/Reflux", "probability": 0.05, "severity": "LOW"}
                ]
            },
            {
                "chief_complaint": "Dyspnea",
                "differentials": [
                    {"diagnosis": "CHF exacerbation", "probability": 0.25, "severity": "HIGH"},
                    {"diagnosis": "COPD exacerbation", "probability": 0.20, "severity": "HIGH"},
                    {"diagnosis": "Pneumonia", "probability": 0.20, "severity": "MODERATE"},
                    {"diagnosis": "Pulmonary Embolism", "probability": 0.15, "severity": "HIGH"},
                    {"diagnosis": "Asthma exacerbation", "probability": 0.10, "severity": "MODERATE"},
                    {"diagnosis": "Anaphylaxis", "probability": 0.05, "severity": "HIGH"},
                    {"diagnosis": "Pneumothorax", "probability": 0.05, "severity": "MODERATE"}
                ]
            },
            {
                "chief_complaint": "Altered Mental Status",
                "differentials": [
                    {"diagnosis": "Sepsis/Infection", "probability": 0.20, "severity": "HIGH"},
                    {"diagnosis": "Intoxication", "probability": 0.25, "severity": "MODERATE"},
                    {"diagnosis": "Hypoglycemia", "probability": 0.10, "severity": "HIGH"},
                    {"diagnosis": "Stroke/CVA", "probability": 0.15, "severity": "HIGH"},
                    {"diagnosis": "Encephalopathy", "probability": 0.15, "severity": "HIGH"},
                    {"diagnosis": "Medication effect", "probability": 0.10, "severity": "MODERATE"},
                    {"diagnosis": "Psychiatric", "probability": 0.05, "severity": "LOW"}
                ]
            }
        ]
    
    async def retrieve_esi_criteria(self, esi_level: int, condition: Optional[str] = None) -> RetrievalResult:
        """Retrieve ESI criteria for a specific level and optional condition"""
        query = f"ESI-{esi_level} criteria{f' for {condition}' if condition else ''}"
        
        results = [doc for doc in self.knowledge_docs["esi_handbook"]
                  if doc.get("level") == esi_level or (condition and condition.lower() in str(doc).lower())]
        
        return RetrievalResult(
            query=query,
            collection="esi_handbook",
            results=results[:3],
            num_results=len(results),
            confidence_scores=[0.95] * len(results[:3])
        )
    
    async def retrieve_vital_norms(self, age: int, population: str = "general") -> RetrievalResult:
        """Retrieve age-specific vital sign normal ranges"""
        age_group = self._get_age_group(age, population)
        
        results = [doc for doc in self.knowledge_docs["vital_ranges"]
                  if age_group.lower() in doc.get("age_group", "").lower()]
        
        query = f"Normal vital signs for {age_group}"
        
        return RetrievalResult(
            query=query,
            collection="vital_ranges",
            results=results,
            num_results=len(results),
            confidence_scores=[0.98] * len(results)
        )
    
    async def retrieve_lab_indications(self, test_name: str) -> RetrievalResult:
        """Retrieve lab test indications and interpretation"""
        results = [doc for doc in self.knowledge_docs["lab_indications"]
                  if test_name.lower() in doc.get("test", "").lower()]
        
        return RetrievalResult(
            query=f"Indications and interpretation for {test_name}",
            collection="lab_indications",
            results=results,
            num_results=len(results),
            confidence_scores=[0.92] * len(results)
        )
    
    async def retrieve_differential_diagnoses(self, chief_complaint: str) -> RetrievalResult:
        """Retrieve differential diagnosis list for chief complaint"""
        results = [doc for doc in self.knowledge_docs["differential_diagnosis"]
                  if chief_complaint.lower() in doc.get("chief_complaint", "").lower()]
        
        return RetrievalResult(
            query=f"Differential diagnosis for {chief_complaint}",
            collection="differential_diagnosis",
            results=results,
            num_results=len(results),
            confidence_scores=[0.88] * len(results)
        )

    async def retrieve_acs_protocols(self, condition: Optional[str] = None) -> RetrievalResult:
        """Retrieve ACS protocols and risk scores"""
        results = self.knowledge_docs["acs_protocols"]
        query = f"ACS protocols{f' for {condition}' if condition else ''}"

        return RetrievalResult(
            query=query,
            collection="acs_protocols",
            results=results[:3],
            num_results=len(results),
            confidence_scores=[0.9] * len(results[:3])
        )

    async def retrieve_sepsis_criteria(self, condition: Optional[str] = None) -> RetrievalResult:
        """Retrieve sepsis criteria and workup guidelines"""
        results = self.knowledge_docs["sepsis_criteria"]
        query = f"Sepsis criteria{f' for {condition}' if condition else ''}"

        return RetrievalResult(
            query=query,
            collection="sepsis_criteria",
            results=results[:3],
            num_results=len(results),
            confidence_scores=[0.9] * len(results[:3])
        )
    
    def _get_age_group(self, age: int, population: str) -> str:
        """Determine age group classification"""
        if age < 1:
            if age < 0.25:
                return "Infant 0-3 months"
            elif age < 0.5:
                return "Infant 3-6 months"
            else:
                return "Infant 6-12 months"
        elif age < 3:
            return "Toddler 1-2 years"
        elif age < 7:
            return "Child 3-6 years"
        elif age < 12:
            return "Child 7-11 years"
        elif age < 18:
            return "Adolescent 12+ years"
        elif age < 65:
            return "Adult 18-65 years"
        else:
            return "Geriatric 65+ years"
    
    async def format_for_llm(self, retrieval_result: RetrievalResult) -> str:
        """Format retrieval results for LLM context"""
        formatted = f"\n# Clinical Evidence: {retrieval_result.collection.upper()}\n"
        formatted += f"**Query**: {retrieval_result.query}\n"
        formatted += f"**Results**: {retrieval_result.num_results} documents found\n\n"
        
        for i, result in enumerate(retrieval_result.results, 1):
            formatted += f"## Result {i} (Confidence: {retrieval_result.confidence_scores[i-1]:.1%})\n"
            formatted += json.dumps(result, indent=2) + "\n\n"
        
        return formatted
