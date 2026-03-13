import argparse
import yaml
from infra.models.huggingface import HuggingClient
from Backend.util.questions import load_questions
from Backend.evaluation import run_evaluation
from Backend.llm_judge import LLMJudge
from infra.models.registry import resolve_models, Models, MODEL_REGISTRY
from Backend.app.models.Evaluation import JudgeEvalRecord
from Backend.app.services.supabase_client import insert_judge_eval


def validate_config(config: dict):
    required_top = ["models", "questions", "solver"]
    for key in required_top:
        if key not in config:
            raise ValueError(f"Missing required config section: {key}")

    if "selected" not in config["models"]:
        raise ValueError("models.selected is required")

    if "prompt_version" not in config["solver"]:
        raise ValueError("solver.prompt_version is required")

    if config.get("judge", {}).get("enabled", False):
        judge = config["judge"]
        for k in ["model", "prompt_version"]:
            if k not in judge:
                raise ValueError(f"judge.{k} is required when judge.enabled=true")

async def main():
    cli_command_parser = argparse.ArgumentParser(description="LLM-Eval Runner")
    cli_command_parser.add_argument("--config", type=str, required=True, help="find path to config")

    args = cli_command_parser.parse_args()

    # get the information in the config
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)
    
    validate_config(config)

    hf_client = HuggingClient()

    models = [Models[m] for m in config["models"]["selected"]]
    resolved_models = resolve_models(models)

    questions_config = config["questions"]
    questions = load_questions(
        questions_config["file"],
        filters=questions_config.get("filter")
    )

    judge = None

    if config.get("judge", {}).get("enabled", False):
        # Todo: need to add judge
        judge_cfg = config['judge']
        judge_model = MODEL_REGISTRY[Models[judge_cfg["model"]]]
        print("Running LLM judge [judge]")
        judge = LLMJudge(
            client=hf_client,
            model=judge_model,
            config="config_v1",
            prompt_version=judge_cfg["prompt_version"])

    solver_prompt_version = config["solver"]["prompt_version"]
    for question_id in questions:
        print(f"Running Evaluation for Problem={question_id}")
        
        result = await run_evaluation(
            question_id=question_id,
            models=resolved_models,
            hf_client=hf_client,
            prompt_version=solver_prompt_version,
            config_version="config_v1"
        )

        print(f"Completed {question_id} and stored={result['run_id']}")

        if judge:
            judge_evaluation = await judge.compare(
                prompt=result["prompt"],
                responses={result["responses"]["model_a"].agent_code,
                           result["responses"["model_b"].agent_code]}
            )
            response_a = result["responses"]["model_a"]
            response_b = result["responses"]["model_b"]

            winner_response_id = (
                response_a.id
                if judge_evaluation["winner"] == "A"
                else response_b.id
            )

            print(f"Judge winner={judge_evaluation["winner"]}"
                  f"(confidence={judge_evaluation["confidence"]})"
                  )

            judge_record = {
                "run_id": result["run_id"],
                "question_id": question_id,
                "response_a_id": response_a.id,
                "response_b_id": response_b.id,
                "winner_response_id": winner_response_id,
                "judge_model": judge.model,
                "judge_prompt_version": judge.prompt_version,
                "confidence": judge_evaluation["confidence"],
                "reason": judge_evaluation["reason"]
            }

            insert_judge_eval(judge_record)

    print("Evaluation complete")

if __name__ == "__main__":
    main()
        

           