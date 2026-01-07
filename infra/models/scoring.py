from infra.models.normalize import normalize_runtime
from aggregation import model_stability
from Backend.app.services import supabase_client

MAX_RUNTIME_MS = 1500.0


def score_problem(evaluation):
    """
    Returns the score based on passed tests and execution error of a model with one question.

    :param results: The results from the sandbox evaluation of the model's code.
    """
    test_summary = evaluation["test_summary"]
    total_tests = test_summary["total_tests"]
    passed_tests = test_summary["passed"]

    runtime_ms = evaluation.get("runtime_ms", MAX_RUNTIME_MS)

    if total_tests == 0:
        return {
            "runtime_ms": runtime_ms,
            "pass_rate": 0.0,
            "execution_success": 0.0,
            "problem_score": 0.0,
        }

    pass_rate = passed_tests / total_tests

    execution_success = (
        1.0 if all(test["error"] is None for test in evaluation["results"]) else 0.0
    )

    correctness = 0.7 * pass_rate + 0.3 * execution_success

    performance = normalize_runtime(runtime_ms)

    problem_score = 0.7 * correctness + 0.3 * performance

    return {
        "pass_rate": round(pass_rate, 4),
        "runtime_ms": runtime_ms,
        "execution_success": execution_success,
        "problem_score": problem_score,
    }


def rank_models_per_run(problem_scores: dict):
    ranked = []
    for model, score in problem_scores.items():
        ranked.append({"model": model, **score})

    return sorted(ranked, key=lambda x: x["problem_score"], reverse=True)
