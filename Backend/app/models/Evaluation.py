from pydantic import BaseModel
from typing import Any, Dict
from infra.models.registry import Models
from uuid import UUID

class Model(BaseModel):
    display_name: str
    provider: str
    model_key: str

class RunRecord(BaseModel):
    id: UUID
    config_version: str
    dataset_version: str
    scoring_version: str

class RawEvaluationRecord(BaseModel):
    model_id: int
    question_id: int
    run_id: UUID
    solver_prompt_version: str
    agent_code: str
    results: Dict[str, Any]
    test_summary: Dict[str, Any]
    runtime_ms: float


class ProblemScoreRecord(BaseModel):
    evaluation_id: int
    problem_score: float
    pass_rate: float
    execution_success: bool
    runtime_ms: float


class JudgeEvalRecord(BaseModel):
    run_id: UUID 
    question_id: int
    response_a_id: int
    response_b_id: int
    winner_response_id: int
    reason: str
    judge_model_id: int
    prompt_version: str
    judge_confidence: float #to do: change to pedagogy