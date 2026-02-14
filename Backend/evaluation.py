import uuid
import json
import ast

from infra.sandbox.executor import run_code_in_sandbox
from infra.models.registry import resolve_models
from util.questions import load_question
from infra.models.huggingface import HuggingClient
from infra.models.scoring import score_problem, rank_models_per_run
from app.services.supabase_client import insert_run, insert_raw_eval, insert_problem_score
from infra.observability.mlflow_logger import log_run

MAX_RUNTIME_MS = 1500.0

def extract_function_name(agent_code):
    """
    Extract function name from agent response
    """
    try:
        tree = ast.parse(agent_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                return node.name
    except Exception as e:
        print(f"error: {str(e)}")
        pass
    return None

def process_sandbox_response(response, tests):
    """
    Process the results from running the code in the sandbox
    """
    results = []
    try:
        test_results = json.loads(response.strip())
    except json.JSONDecodeError:
        return {"error": "Invalid sandbox result", "sandbox_output": response}

    for test_result in test_results:
        i = test_result["index"]
        test = tests[i]

        raw_result = test_result["output"]
        error = test_result["error"]
        expected_result = test["expected"]

        try:
            actual_result = ast.literal_eval(raw_result)
        except Exception:
            actual_result = raw_result

        passed = (actual_result == expected_result) and error is None

        results.append(
            {
                "input": test["input"],
                "actual": actual_result,
                "expected": expected_result,
                "error": error,
                "passed": passed,
            }
        )
    return results


def run_evaluation(
    *,
    question_id: str,
    models: list[str],
    hf_client: HuggingClient,
):
    question = load_question(question_id)
    models = resolve_models(models)

    if not question:
        raise ValueError(f"Question does not exist: {question_id}")

    run_id = uuid.uuid4()

    insert_run(
        {
            "id": str(run_id),
            "question_id": question_id,
            "models": models,
            "scoring_version": "v1.0",
            "config": {"MAX_RUNTIME_MS": MAX_RUNTIME_MS},
        }
    )

    prompt = f"""
Write a python solution for this algorithm:
Title: {question["title"]}
Description: {question["description"]}

Return ONLY valid Python code.
"""

    
    agent_responses = hf_client.generate_from_many(
        models=models,
        prompt=prompt,
    )

    model_results = {}

    for model, agent_response in agent_responses.items():

        if not agent_response:
            raise RuntimeError(f"No response from model: {model}")

        function_name = extract_function_name(agent_response)
        if not function_name:
            raise RuntimeError(f"No function definition from model: {model}")

        sandbox_result = run_code_in_sandbox(
            agent_response,
            question["tests"],
            function_name,
        )

        if sandbox_result.stderr:
            raise RuntimeError(
                f"Sandbox execution failed for {model}: {sandbox_result.stderr}"
            )

        results = process_sandbox_response(
            sandbox_result.stdout,
            question["tests"],
        )

        test_summary = {
            "total_tests": len(results),
            "passed": sum(r["passed"] for r in results),
            "failed": sum(not r["passed"] for r in results),
        }

        model_results[model] = {
            "results": results,
            "test_summary": test_summary,
            "agent_code": agent_response,
            "runtime_ms": sandbox_result.runtime_ms,
        }

        insert_raw_eval(
            {
                "run_id": str(run_id),
                "model_id": model,
                "question_id": question_id,
                "agent_code": agent_response,
                "results": json.dumps(results),
                "test_summary": json.dumps(test_summary),
                "runtime_ms": sandbox_result.runtime_ms,
            }
        )

  
    scored_models = {}

    for model, data in model_results.items():
        score = score_problem(data, model)
        scored_models[model] = score

        insert_problem_score(
            {
                "run_id": str(run_id),
                "model_id": model,
                "question_id": question_id,
                **score,
            }
        )

        log_run(
            model_id=model,
            question_id=question_id,
            scoring_version="v1.0",
            config={"MAX_RUNTIME_MS": MAX_RUNTIME_MS},
            score=score,
            agent_code=data["agent_code"],
            raw_results={
                "results": data["results"],
                "test_summary": data["test_summary"],
            },
        )

    ranked = rank_models_per_run(scored_models)

    return {
        "run_id": str(run_id),
        "question_id": question_id,
        "results": model_results,
        "scores": scored_models,
        "ranking": ranked,
    }
