import argparse
import yaml
from infra.models.huggingface import HuggingClient
from Backend.util.questions import load_questions
from Backend.evaluation import run_evaluation
from Backend.llm_judge import LLMJudge
from infra.models.registry import resolve_models, Models, MODEL_REGISTRY


async def main():
    cli_command_parser = argparse.ArgumentParser(description="LLM-Eval Runner")
    cli_command_parser.add_argument("--config", type=str, required=True, help="find path to config")
    # cli_command_parser.add_argument(
    # "--judge-prompt-version",
    # type=str,
    # default="v1",
    # help="Judge prompt version (e.g. v1, v2)")

    # cli_command_parser.add_argument(
    # "--solver-prompt-version",
    # type=str,
    # default="v1",
    # help="Solver prompt version (e.g. v1, v2)")

    args = cli_command_parser.parse_args()

    # get the information in the config
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

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
        judge_model = MODEL_REGISTRY[Models[judge_cfg["model"]]]
        print("Running LLM judge [judge]")
        judge_cfg = config['judge']
        judge = LLMJudge(
            client=hf_client,
            model=judge_model,
            config="config_v1",
            prompt_version=judge_cfg["prompt_version"])


    for question_id in questions:
        print(f"Running Evaluation for Problem={question_id}")
        solver_prompt_version = config["solver"]["prompt_version"]
        result = await run_evaluation(
            question_id=question_id,
            models=resolved_models,
            hf_client=hf_client,
            prompt_version=solver_prompt_version
        )

        print(f"Completed {question_id} and stored={result['run_id']}")

        if judge:
            judge_evaluation = await judge.compare(
                run_id=result["run_id"],
                question_id=question_id,
                prompt=result["prompt"],
                outputs=result["outputs"]
            )

            print(f"Judge winner={judge_evaluation.winner}"
                  f"(confidence={judge_evaluation.confidence})"
                  )
            # if judge_evaluation["winner"] == "A":
            #     winner_response_id = response_a.id
            # else:
            #     winner_response_id = response_b.id
            

    print("Evaluation complete")

if __name__ == "__main__":
    main()
        

           