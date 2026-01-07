import uuid
from fastapi import APIRouter, HTTPException, Depends
import ast
import json

MAX_RUNTIME_MS = 1500.0

from Backend.app.models.Evaluation import EvaluationRequestModel
from infra.sandbox.executor import run_code_in_sandbox
from infra.models.registry import resolve_models
from util.questions import load_question
from infra.models.huggingface import HuggingClient
from infra.models.scoring import score_problem, rank_models_per_run
from services.supabase_client import insert_run, insert_raw_eval, insert_problem_score
from infra.observability.mlflow_logger import log_run

router = APIRouter()


def get_hf_client():
    return HuggingClient()


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


@router.post("/evaluate")
async def evaluate_agent_response(
    payload: EvaluationRequestModel, hf_client: HuggingClient = Depends(get_hf_client)
):
    question = load_question(payload.question_id)
    models = resolve_models(payload.models)

    if not question:
        raise HTTPException(status_code=404, detail="Question does not exist")

    run_id = uuid.uuid4()

    insert_run(
        {
            "id": str(run_id),
            "question_id": payload.question_id,
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

    agent_responses = await hf_client.generate_from_many(models=models, prompt=prompt)

    model_results = {}
    for model, agent_response in agent_responses.items():

        if not agent_response:
            raise HTTPException(status_code=404, detail="There is no response LLM")

        function_name = extract_function_name(agent_response)

        if not function_name:
            raise HTTPException(status_code=404, detail="No function definition")

        sandbox_result = run_code_in_sandbox(
            agent_response, question["tests"], function_name
        )

        if sandbox_result.stderr:
            print(f"error: {sandbox_result.stderr}")
            raise HTTPException(
                status_code=500, detail="Error while executing model code in sandbox"
            )

        try:
            results = process_sandbox_response(sandbox_result.stdout, question["tests"])
        except Exception as e:
            print("Processing error", str(e))
            raise HTTPException(status_code=500, detail="Error parsing sandbox output")

        test_summary = {
            "total_tests": len(results),
            "passed": sum([result["passed"] for result in results]),
            "failed": sum([not result["passed"] for result in results]),
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
                "question_id": payload.question_id,
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
                "question_id": payload.question_id,
                **score,
            }
        )
        
        log_run(
            model_id=model,
            question_id=payload.question_id,
            scoring_version="v1.0",
            config={
                "MAX_RUNTIME_MS": MAX_RUNTIME_MS,
            },
            score=score,
            agent_code=data["agent_code"],
            raw_results={
                "results": data["results"],
                "test_summary": data["test_summary"],
            },
        )

    ranked = rank_models_per_run(scored_models)

    return {
        "question_id": payload.question_id,
        "function_name": function_name,
        "results": model_results,
        "scores": scored_models,
        "ranking": ranked,
    }
