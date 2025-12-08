from pydantic import BaseModel

class EvaluationRequestModel(BaseModel):
    question_id: int
    agent_code: str