from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class RequirementBase(BaseModel):
    id: str
    nom: str
    contenu: str
    doublon_probable: bool = False
    complexity_score: int = 1


class Requirement(RequirementBase):
    pass


class ReformulationResult(BaseModel):
    id: str
    conforme: Optional[bool] = None
    reformulations: List[str] = []


class ExtractionResponse(BaseModel):
    session_id: str
    requirements: List[Requirement]
    total_requirements: int
    extraction_cost: Dict[str, Any]
    timestamp: datetime


class ReformulationResponse(BaseModel):
    session_id: str
    reformulations: Dict[str, ReformulationResult]
    completed_count: int
    cost: Dict[str, Any]
    timestamp: datetime


class SessionData(BaseModel):
    session_id: str
    filename: str
    requirements: List[Requirement]
    reformulations: Optional[Dict[str, ReformulationResult]] = None
    created_at: datetime
    updated_at: datetime


class ExportRequest(BaseModel):
    format: str  # "word" or "excel"
    selected_requirements: Dict[str, str] = {}


class CostEstimate(BaseModel):
    remaining_requirements: int
    estimated_tokens: int
    estimated_usd: float
