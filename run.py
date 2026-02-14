import argparse
import yaml
from infra.models.huggingface import HuggingClient
from Backend.util.questions import load_questions
from Backend.evaluation import run_evaluation


def main():
    cli_command_parser = argparse.ArgumentParser(description="LLM-Eval Runner")
    cli_command_parser.add_argument("--config", type=str, required=True, help="find path to config")
    args = cli_command_parser.parse_args()

    # get the information in the config
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

    hf_client = HuggingClient()

    models = config["models"]
    questions_config = config["questions"]

    questions = load_questions(
        questions_config["file"],
        filters=questions_config.get("filter")
    )

    

    for question_id in questions:
        print(f"Running Evaluation for Problem={question_id}")
        result = run_evaluation(
            question_id=question_id,
            models=models,
            hf_client=hf_client
        )

        print(f"Completed {question_id} and stored={result['run_id']}")

    if config.get("judge", {}).get("enabled", False):
        # Todo: need to add judge
        print("Running LLM judge [judge]")

    print("Evaluation complete")

if __name__ == "__main__":
    main()
        

           