import numpy as np

MAX_RUNTIME_MS = 1500.0

DIMENSIONS = {
    "correctness": {
        "pass_rate": 0.7,
        "execution_success": 0.3,
    },
    "performance": {
        "runtime": 1.0,
    }
}

def normalize(x):
    """
    TODO Will be updated to z-score when there is alot of data
    """
    return max(0.0, min(1.0, x))

def aggregrate_dimension_scoring(problem_scores):
    """
    Dimension scoring for one model for ALL questions.
    """

    if len(problem_scores) == 0:
        return {
            "final_score": 0.0,
            "stability": 0.0
        }
    
    problem_scores_only = [score["problem_score"] for score in problem_scores]
    runtimes = [score["runtime_ms"] for score in problem_scores]
    pass_rates = [score["pass_rate"] for score in problem_scores]
    exec_failures = [score["execution_success"] for score in problem_scores]

    mean_problem_score = float(np.mean(problem_scores_only))
    mean_runtime = float(np.mean(runtimes))

    runtime_std = np.std(runtimes)
    pass_rate_std = np.std(pass_rates)
    timeout_rate = np.mean(exec_failures)


    stability = normalize(
        1 - (
            0.4 * (runtime_std / MAX_RUNTIME_MS)
            + 0.4 * pass_rate_std
            + 0.2 * timeout_rate
        )
    )

    final_score = (
        0.6 * mean_problem_score
        + 0.2 * normalize(1 - mean_runtime / MAX_RUNTIME_MS)
        + 0.2 * stability
    )

    return {
        "final_score": final_score,
        "dimensions": {
            "mean_problem_score": mean_problem_score,
            "stability": stability,
        },
        "raw_metrics": {
            "runtime_std_ms": runtime_std,
            "pass_rate_std": pass_rate_std,
            "timeout_rate": timeout_rate
        }
    }

def calculate_delta(current, baseline):
    """
    Calculates the difference between the scores between the baseline and current dimension scores.
    """
    delta = current["final_score"] - baseline["final_score"]
    dimension_delta = {
        d: current["dimensions"][d] - baseline["dimensions"][d]
        for d in DIMENSIONS
    }
    return delta, dimension_delta