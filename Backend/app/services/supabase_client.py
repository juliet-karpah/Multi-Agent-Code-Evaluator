import os
from supabase import create_client
from Backend.app.models import Evaluation

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
client = create_client(url, key)

def insert_run(record: Evaluation.RunRecord):
    return client.table("runs").insert(record.model_dump()).execute()

def insert_raw_eval(record: Evaluation.RawEvaluationRecord):
    """
    Insert evaluation results into Supabase DB
    """
    return client.table("raw_evaluations").insert(record.model_dump()).execute()

def insert_problem_score(record: Evaluation.ProblemScoreRecord):
    """
    Insert Problem Score into Supabase DB
    """
    return client.table("problem_scores").insert(record.model_dump()).execute()

def get_all_evaluations(model_id):
    """
    Retrieve all for a model
    """
    return client.table("evaluations").select("*").eq("model_key", model_id).execute()
