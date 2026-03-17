import mlflow
import tempfile
from pathlib import Path
import json


def log_run(
    run_id,
    config_version,
    dataset_name,
    dataset_version,
    models,
    scoring_version,
    metrics,
    config_snapshot,
):
    with mlflow.start_run(run_name=str(run_id)):

      mlflow.log_param("config_version", config_version)
      mlflow.log_param("dataset_name", dataset_name)
      mlflow.log_param("data_version", dataset_version)
      mlflow.log_param("models", ",".join(models))
      mlflow.log_param("scoring_version", scoring_version)

      for key, value in config_snapshot.items():
         mlflow.log_param(key, value)

      for metric_name, metric_value in metrics.items():
         mlflow.log_metric(metric_name, metric_value)

      with tempfile.TemporaryDirectory() as tmpdir:
         tmpdir = Path(tmpdir)

         config_path = tmpdir / "config.json"
         config_path.write_text(json.dumps(config_snapshot, indent=2))

         mlflow.log_artifact(str(config_path))

   

    
