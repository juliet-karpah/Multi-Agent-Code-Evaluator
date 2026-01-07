# Multi-Agent-Code-Evaluator
In this project, I use a "research-grade" scoring system to grade different agent's response to different coding algorithms. Research-grade eval systems do the following:

- Have independent dimensions
- normalize metrics for comparability
- preserve variance
- are reproducible
- enable regression testing

## Metrics 
Each model's response to a coding problem is graded on hard signals and soft signals(stretch goal). The hard signals are the correctness and execution metrics that are measured based on pass_rate, execution_success, and runtime_ms. The soft signals also known as behavioral tell us about the format_adherence, verbosity, tool_usage, and hallucination. The final metric is the stability metrics which measures the consistency of the model's reponse on the same question over N runs using runtime variance, pass rate variance, timeout rate, and crash rate. 
The raw metrics(pass_rate, runtime, execution success, variance) is normalized to be between [0, 1] to make it easier to compare. 
The metrics are grouped into dimensions such as correctness, performance, and stability. The dimensions are scored using a function that multiples the weights of the dimension to the normalized value of the metric in that dimension.
The dimension score for each dimension is then multiplied with its corresponding dimension weight to derive final dimension core. Then each final dimension score is added to create a final structured score. So that the results from each run would provide:
{
    "final_score": 0.9126,
    "dimensions": {
        "correctness": 0.94,
        "performance": 0.88,
        "stability": 0.90,
    },
    "raw_metrics": {
        "pass_rate": 0.95,
        "runtime_ms": 412,
        "variance": 0.03,
    }
}
This above result will be sent to MLFlow for tracking, frontend for the dashboards, and to calculate regression difference. The results above will also be passed into a ranking function that ranks the models based on this result. 
The final score will also be used in Baselines. This is where the best final score to this point is stored as a baseline and then each run or current final score is used to calculate the delta. Then the dimension deltas are also calculated for each dimension
If the delta and the dimension delta for correctness fails to meet some threshold, the continuous integration fails. 

| Model | Pass Rate | Runtime Variance | Timeout Rate | Crash Rate |
| ----- | --------- | ---------------- | ------------ | ---------- |
| A     | 95%       | Low              | **0%**       | **0%**     |
| B     | 95%       | Low              | **30%**      | **10%**    |


Steps to take to complete the backend:
Layer 1: Measurement (sandbox → raw metrics)
Layer 2: Scoring (normalize → dimension scores → final score)
Layer 3: Persistence (store results, MLflow logging)
Layer 4: Comparison (baseline & regression)
Layer 5: Enforcement (CI gate)


1. Sandbox execution (per run)
2. Problem-level scoring (per model × problem)
3. Model-level aggregation (across problems)

| Layer             | Scope                      | Purpose                 |
| ----------------- | -------------------------- | ----------------------- |
| `score_problem`   | model × question           | correctness + runtime   |
| `aggregate_model` | model across all questions | stability + final score |
| `rank_models`     | all models                 | sorting only            |

evaluate route
│
├─ run sandbox
├─ persist RAW results  ← HERE
│
├─ score_problem (pure function)
├─ persist SCORES       ← HERE
│
├─ rank_models
└─ return response

evaluate route
│
├─ run sandbox
├─ persist RAW results  ← HERE
│
├─ score_problem (pure function)
├─ persist SCORES       ← HERE
│
├─ rank_models
└─ return response
