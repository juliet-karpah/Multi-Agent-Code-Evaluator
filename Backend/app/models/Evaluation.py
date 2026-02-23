from pydantic import BaseModel
from typing import List, Any, Dict
from infra.models.registry import Models
from uuid import UUID

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


class JudgeEvalRecord(BaseModel):
    run_id: UUID 
    question_id: int
    model_a: str
    model_b: str
    winner: str
    reason: str
    judge_model: str
    prompt_version: str
    judge_config: UUID