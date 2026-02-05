"""
Admin API endpoints for RAG layer management.
Allow runtime configuration of RAG without redeploying.
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Dict, Any

from rag.config import RAGConfigManager
from auth_admin import verify_admin_key


router = APIRouter(prefix="/admin/rag", tags=["admin"])

# Initialize config manager
config_manager = RAGConfigManager()


@router.get("/config")
async def get_rag_config(authenticated: bool = Depends(verify_admin_key)) -> Dict[str, Any]:
    """
    GET /admin/rag/config
    Get current RAG configuration for all layers
    """
    return config_manager.get_config_summary()


@router.get("/layer/{layer_number}/config")
async def get_layer_config(layer_number: int, authenticated: bool = Depends(verify_admin_key)) -> Dict[str, Any]:
    """
    GET /admin/rag/layer/{layer_number}/config
    Get configuration for a specific layer
    """
    if layer_number < 1 or layer_number > 7:
        raise HTTPException(status_code=400, detail="Layer number must be 1-7")
    
    layer = config_manager.get_layer_config(layer_number)
    if not layer:
        raise HTTPException(status_code=404, detail=f"Layer {layer_number} not found")
    
    return {
        "layer_number": layer_number,
        "name": layer.layer_name,
        "rag_enabled": layer.enabled,
        "knowledge_sources": layer.knowledge_sources,
        "confidence_threshold": layer.confidence_threshold,
        "max_results": layer.max_results,
        "description": layer.description
    }


@router.post("/layer/{layer_number}/enable")
async def enable_layer_rag(layer_number: int, authenticated: bool = Depends(verify_admin_key)) -> Dict[str, Any]:
    """
    POST /admin/rag/layer/{layer_number}/enable
    Enable RAG for a specific layer
    """
    if layer_number < 1 or layer_number > 7:
        raise HTTPException(status_code=400, detail="Layer number must be 1-7")
    
    if not config_manager.config.global_settings.get("enable_rag_globally"):
        raise HTTPException(status_code=400, detail="Global RAG is disabled")
    
    success = config_manager.enable_layer_rag(layer_number)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to enable layer RAG")
    
    return {
        "status": "success",
        "layer": layer_number,
        "rag_enabled": True,
        "message": f"RAG enabled for layer {layer_number}"
    }


@router.post("/layer/{layer_number}/disable")
async def disable_layer_rag(layer_number: int, authenticated: bool = Depends(verify_admin_key)) -> Dict[str, Any]:
    """
    POST /admin/rag/layer/{layer_number}/disable
    Disable RAG for a specific layer
    """
    if layer_number < 1 or layer_number > 7:
        raise HTTPException(status_code=400, detail="Layer number must be 1-7")
    
    success = config_manager.disable_layer_rag(layer_number)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to disable layer RAG")
    
    return {
        "status": "success",
        "layer": layer_number,
        "rag_enabled": False,
        "message": f"RAG disabled for layer {layer_number}"
    }


@router.post("/layer/{layer_number}/knowledge-sources")
async def update_knowledge_sources(
    layer_number: int,
    sources: List[str] = Query(...),
    authenticated: bool = Depends(verify_admin_key)
) -> Dict[str, Any]:
    """
    POST /admin/rag/layer/{layer_number}/knowledge-sources
    Update knowledge sources for a layer
    
    Valid sources:
    - esi_handbook
    - acs_protocols
    - sepsis_criteria
    - vital_ranges
    - lab_indications
    - differential_diagnosis
    - medical_ontology
    """
    if layer_number < 1 or layer_number > 7:
        raise HTTPException(status_code=400, detail="Layer number must be 1-7")
    
    valid_sources = {
        "esi_handbook",
        "acs_protocols",
        "sepsis_criteria",
        "vital_ranges",
        "lab_indications",
        "differential_diagnosis",
        "medical_ontology"
    }
    
    # Validate sources
    invalid = set(sources) - valid_sources
    if invalid:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sources: {invalid}. Valid: {valid_sources}"
        )
    
    success = config_manager.update_knowledge_sources(layer_number, sources)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update knowledge sources")
    
    return {
        "status": "success",
        "layer": layer_number,
        "knowledge_sources": sources,
        "message": f"Knowledge sources updated for layer {layer_number}"
    }


@router.post("/layer/{layer_number}/threshold")
async def set_confidence_threshold(
    layer_number: int,
    threshold: float = Query(..., ge=0.0, le=1.0),
    authenticated: bool = Depends(verify_admin_key)
) -> Dict[str, Any]:
    """
    POST /admin/rag/layer/{layer_number}/threshold
    Set confidence threshold for a layer (0.0 - 1.0)
    """
    if layer_number < 1 or layer_number > 7:
        raise HTTPException(status_code=400, detail="Layer number must be 1-7")
    
    success = config_manager.set_confidence_threshold(layer_number, threshold)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to set threshold")
    
    return {
        "status": "success",
        "layer": layer_number,
        "confidence_threshold": threshold,
        "message": f"Confidence threshold set to {threshold} for layer {layer_number}"
    }


@router.post("/toggle-global")
async def toggle_global_rag(enabled: bool, authenticated: bool = Depends(verify_admin_key)) -> Dict[str, Any]:
    """
    POST /admin/rag/toggle-global?enabled=true
    Enable/disable RAG globally (affects all layers)
    """
    success = config_manager.toggle_global_rag(enabled)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to toggle global RAG")
    
    return {
        "status": "success",
        "global_rag_enabled": enabled,
        "message": f"Global RAG {'enabled' if enabled else 'disabled'}"
    }


@router.post("/reset-defaults")
async def reset_to_defaults(authenticated: bool = Depends(verify_admin_key)) -> Dict[str, Any]:
    """
    POST /admin/rag/reset-defaults
    Reset all RAG configuration to defaults (all layers enabled)
    """
    config_manager.config = config_manager._create_default_config()
    success = config_manager.save_config()
    if not success:
        raise HTTPException(status_code=500, detail="Failed to reset configuration")
    
    return {
        "status": "success",
        "message": "RAG configuration reset to defaults",
        "config": config_manager.get_config_summary()
    }


@router.get("/stats")
async def get_rag_stats(authenticated: bool = Depends(verify_admin_key)) -> Dict[str, Any]:
    """
    GET /admin/rag/stats
    Get RAG usage statistics (for monitoring)
    """
    summary = config_manager.get_config_summary()
    
    enabled_layers = sum(
        1 for layer in summary["layers"].values()
        if layer["rag_enabled"]
    )
    
    return {
        "global_rag_enabled": summary["global_rag_enabled"],
        "total_layers": 7,
        "layers_with_rag_enabled": enabled_layers,
        "layers_with_rag_disabled": 7 - enabled_layers,
        "layer_details": summary["layers"]
    }
