from pydantic import BaseModel
from typing import List, Any, Dict
from infra.models.registry import Models
from uuid import UUID


class EvaluationRequestModel(BaseModel):
    question_id: int
    models: List[Models]


class RunRecord(BaseModel):
    id: UUID
    models: List[int]
    question_id: int
    scoring_version: str
    config: Dict[str, Any] | None = None


class RawEvaluationRecord(BaseModel):
    model_id: int
    question_id: int
    run_id: UUID
    agent_code: str
    results: Dict[str, Any]
    test_summary: Dict[str, Any]
    runtime_ms: float


class ProblemScoreRecord(BaseModel):
    model_id: int
    question_id: int
    run_id: UUID
    problem_score: float
    pass_rate: float
    execution_success: bool
    runtime_ms: float
