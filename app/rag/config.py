"""
Admin configuration for RAG layers and system settings.
Allows runtime enable/disable of RAG for each layer.
"""

from typing import Dict, Any, List
from dataclasses import dataclass, asdict
import json
import os


@dataclass
class RAGLayerConfig:
    """Configuration for a single RAG layer"""
    layer_name: str
    enabled: bool
    knowledge_sources: List[str]  # e.g., ["esi_handbook", "acs_protocols"]
    confidence_threshold: float = 0.7
    max_results: int = 3
    use_vector_db: bool = False
    description: str = ""


@dataclass
class RAGSystemConfig:
    """Full RAG system configuration"""
    layer_1_sanity_check: RAGLayerConfig
    layer_2_extraction: RAGLayerConfig
    layer_3_red_flag_detection: RAGLayerConfig
    layer_4_vital_signal_assessment: RAGLayerConfig
    layer_5_resource_inference: RAGLayerConfig
    layer_6_handbook_verification: RAGLayerConfig
    layer_7_final_decision: RAGLayerConfig
    
    global_settings: Dict[str, Any]  # Budget, timeouts, etc


class RAGConfigManager:
    """Manage RAG configuration with file persistence"""
    
    def __init__(self, config_path: str = "/app/config/rag_config.json"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> RAGSystemConfig:
        """Load configuration from file or create defaults"""
        if os.path.exists(self.config_path):
            with open(self.config_path) as f:
                data = json.load(f)
                return self._parse_config(data)
        else:
            return self._create_default_config()
    
    def _create_default_config(self) -> RAGSystemConfig:
        """Create default RAG configuration (all enabled)"""
        return RAGSystemConfig(
            layer_1_sanity_check=RAGLayerConfig(
                layer_name="Sanity Check",
                enabled=False,  # No RAG needed
                knowledge_sources=[],
                description="Input validation - no RAG needed"
            ),
            layer_2_extraction=RAGLayerConfig(
                layer_name="Extraction",
                enabled=True,
                knowledge_sources=["medical_ontology"],
                confidence_threshold=0.8,
                max_results=1,
                description="Normalize medical terminology and extract structured data"
            ),
            layer_3_red_flag_detection=RAGLayerConfig(
                layer_name="Red Flag Detection",
                enabled=True,
                knowledge_sources=["esi_handbook", "acs_protocols", "sepsis_criteria", "differential_diagnosis"],
                confidence_threshold=0.85,
                max_results=5,
                description="Detect ESI-2 criteria using handbook and clinical guidelines"
            ),
            layer_4_vital_signal_assessment=RAGLayerConfig(
                layer_name="Vital Signal Assessment",
                enabled=True,
                knowledge_sources=["vital_ranges"],
                confidence_threshold=0.9,
                max_results=1,
                description="Age-aware vital sign interpretation using clinical norms"
            ),
            layer_5_resource_inference=RAGLayerConfig(
                layer_name="Resource Inference",
                enabled=True,
                knowledge_sources=["esi_handbook", "acs_protocols", "lab_indications"],
                confidence_threshold=0.8,
                max_results=10,
                description="Infer required resources using clinical protocols"
            ),
            layer_6_handbook_verification=RAGLayerConfig(
                layer_name="Handbook Verification",
                enabled=True,
                knowledge_sources=["esi_handbook"],
                confidence_threshold=0.85,
                max_results=5,
                description="Verify ESI decision against official handbook"
            ),
            layer_7_final_decision=RAGLayerConfig(
                layer_name="Final Decision",
                enabled=True,
                knowledge_sources=["esi_handbook"],
                confidence_threshold=0.75,
                max_results=2,
                description="Format final ESI decision with handbook reasoning"
            ),
            global_settings={
                "enable_rag_globally": True,
                "log_rag_usage": True,
                "track_rag_accuracy": True,
                "rag_response_timeout_seconds": 5,
                "vector_db_enabled": False,
                "cost_tracking_enabled": True,
                "debug_mode": False
            }
        )
    
    def _parse_config(self, data: Dict) -> RAGSystemConfig:
        """Parse config from JSON"""
        def parse_layer(layer_data):
            return RAGLayerConfig(
                layer_name=layer_data.get("layer_name"),
                enabled=layer_data.get("enabled", True),
                knowledge_sources=layer_data.get("knowledge_sources", []),
                confidence_threshold=layer_data.get("confidence_threshold", 0.7),
                max_results=layer_data.get("max_results", 3),
                use_vector_db=layer_data.get("use_vector_db", False),
                description=layer_data.get("description", "")
            )
        
        return RAGSystemConfig(
            layer_1_sanity_check=parse_layer(data.get("layer_1_sanity_check", {})),
            layer_2_extraction=parse_layer(data.get("layer_2_extraction", {})),
            layer_3_red_flag_detection=parse_layer(data.get("layer_3_red_flag_detection", {})),
            layer_4_vital_signal_assessment=parse_layer(data.get("layer_4_vital_signal_assessment", {})),
            layer_5_resource_inference=parse_layer(data.get("layer_5_resource_inference", {})),
            layer_6_handbook_verification=parse_layer(data.get("layer_6_handbook_verification", {})),
            layer_7_final_decision=parse_layer(data.get("layer_7_final_decision", {})),
            global_settings=data.get("global_settings", {})
        )
    
    def save_config(self) -> bool:
        """Save current configuration to file"""
        try:
            config_dict = {
                "layer_1_sanity_check": asdict(self.config.layer_1_sanity_check),
                "layer_2_extraction": asdict(self.config.layer_2_extraction),
                "layer_3_red_flag_detection": asdict(self.config.layer_3_red_flag_detection),
                "layer_4_vital_signal_assessment": asdict(self.config.layer_4_vital_signal_assessment),
                "layer_5_resource_inference": asdict(self.config.layer_5_resource_inference),
                "layer_6_handbook_verification": asdict(self.config.layer_6_handbook_verification),
                "layer_7_final_decision": asdict(self.config.layer_7_final_decision),
                "global_settings": self.config.global_settings
            }
            
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(config_dict, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def enable_layer_rag(self, layer_number: int) -> bool:
        """Enable RAG for a specific layer"""
        if not self.config.global_settings.get("enable_rag_globally"):
            return False
        
        layer_attr = f"layer_{layer_number}_*"
        layers = {
            1: self.config.layer_1_sanity_check,
            2: self.config.layer_2_extraction,
            3: self.config.layer_3_red_flag_detection,
            4: self.config.layer_4_vital_signal_assessment,
            5: self.config.layer_5_resource_inference,
            6: self.config.layer_6_handbook_verification,
            7: self.config.layer_7_final_decision,
        }
        
        if layer_number in layers:
            layers[layer_number].enabled = True
            return self.save_config()
        return False
    
    def disable_layer_rag(self, layer_number: int) -> bool:
        """Disable RAG for a specific layer"""
        layers = {
            1: self.config.layer_1_sanity_check,
            2: self.config.layer_2_extraction,
            3: self.config.layer_3_red_flag_detection,
            4: self.config.layer_4_vital_signal_assessment,
            5: self.config.layer_5_resource_inference,
            6: self.config.layer_6_handbook_verification,
            7: self.config.layer_7_final_decision,
        }
        
        if layer_number in layers:
            layers[layer_number].enabled = False
            return self.save_config()
        return False
    
    def get_layer_config(self, layer_number: int) -> RAGLayerConfig:
        """Get configuration for a specific layer"""
        layers = {
            1: self.config.layer_1_sanity_check,
            2: self.config.layer_2_extraction,
            3: self.config.layer_3_red_flag_detection,
            4: self.config.layer_4_vital_signal_assessment,
            5: self.config.layer_5_resource_inference,
            6: self.config.layer_6_handbook_verification,
            7: self.config.layer_7_final_decision,
        }
        return layers.get(layer_number)
    
    def update_knowledge_sources(self, layer_number: int, sources: List[str]) -> bool:
        """Update knowledge sources for a layer"""
        layer = self.get_layer_config(layer_number)
        if layer:
            layer.knowledge_sources = sources
            return self.save_config()
        return False
    
    def set_confidence_threshold(self, layer_number: int, threshold: float) -> bool:
        """Update confidence threshold for a layer"""
        if 0.0 <= threshold <= 1.0:
            layer = self.get_layer_config(layer_number)
            if layer:
                layer.confidence_threshold = threshold
                return self.save_config()
        return False
    
    def toggle_global_rag(self, enabled: bool) -> bool:
        """Enable/disable RAG globally"""
        self.config.global_settings["enable_rag_globally"] = enabled
        return self.save_config()
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get summary of current configuration"""
        return {
            "global_rag_enabled": self.config.global_settings.get("enable_rag_globally"),
            "layers": {
                "layer_1": {"name": "Sanity Check", "rag_enabled": self.config.layer_1_sanity_check.enabled},
                "layer_2": {"name": "Extraction", "rag_enabled": self.config.layer_2_extraction.enabled},
                "layer_3": {"name": "Red Flag Detection", "rag_enabled": self.config.layer_3_red_flag_detection.enabled},
                "layer_4": {"name": "Vital Signal Assessment", "rag_enabled": self.config.layer_4_vital_signal_assessment.enabled},
                "layer_5": {"name": "Resource Inference", "rag_enabled": self.config.layer_5_resource_inference.enabled},
                "layer_6": {"name": "Handbook Verification", "rag_enabled": self.config.layer_6_handbook_verification.enabled},
                "layer_7": {"name": "Final Decision", "rag_enabled": self.config.layer_7_final_decision.enabled},
            }
        }
