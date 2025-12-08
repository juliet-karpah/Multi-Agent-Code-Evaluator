from fastapi import APIRouter, HTTPException
import ast
import json

from models.EvaluationRequest import EvaluationRequestModel
from infra.sandbox.executor import run_code_in_sandbox
from util.questions import load_question

router = APIRouter()

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
        return {
            "error": "Invalid sandbox result",
            "sandbox_output": response
        }
    
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

        results.append({
            "input": test["input"],
            "actual": actual_result,
            "expected": expected_result,
            "error": error,
            "passed": passed
        })
    return results


@router.post("/evaluate")
async def evaluate_agent_response(payload: EvaluationRequestModel):
    question = load_question(payload.question_id)
    agent_response = payload.agent_code

    if not question:
        raise HTTPException(status_code=404, detail="Question does not exist")
    
    if not agent_response:
        raise HTTPException(status_code=404, detail="There is no agent response")
    
    function_name = extract_function_name(agent_response)

    if not function_name:
        raise HTTPException(status_code=404, detail="No function definition")

    stdout, stderr = run_code_in_sandbox(payload.agent_code, question["tests"], function_name)

    if stderr:
        print(f"error: {stderr}")
        raise HTTPException(status_code=500, detail="Error while executing model code in sandbox")
    
    try:
        results = process_sandbox_response(stdout, question["tests"])
    except Exception as e:
        print("Processing error", str(e))
        raise HTTPException(
            status_code=500,
            detail="Error parsing sandbox output"
        )
    
    test_summary = {
        "total_tests": len(results),
        "passed": sum([result["passed"] for result in results]),
        "failed": sum([not result["passed"] for result in results])
    }
    
    return {
        "question_id": payload.question_id,
        "function_name": function_name,
        "results": results,
        "test_summary": test_summary
        }