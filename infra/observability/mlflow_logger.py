import mlflow
import tempfile
from pathlib import Path
import json

def log_run(
    model_id,
    question_id,
    scoring_version,
    config,
    score,
    agent_code,
    raw_results,
):
   with mlflow.start_run():
      mlflow.log_param("model_id", model_id)
      mlflow.log_param("question_id", question_id)
      mlflow.log_param("scoring_version", scoring_version)

      for key, value in config.items():
         mlflow.log_param(key, value)
         
      mlflow.log_metric("pass_rate", score["pass_rate"])
      mlflow.log_metric("runtime_ms", score["runtime_ms"])
      mlflow.log_metric("execution_success", score["execution_success"])
      mlflow.log_metric("problem_score", score["problem_score"])


      with tempfile.TemporaryDirectory() as tmpdir:
         tmpdir = Path(tmpdir)

         code_path = tmpdir / "agent_code.py"
         code_path.write_text(agent_code)

         result_path = tmpdir / "raw_results.json"
         result_path.write_text(json.dumps(raw_results, indent=2))

         mlflow.log_artifact(str(code_path))
         mlflow.log_artifact(str(result_path))


   

    
