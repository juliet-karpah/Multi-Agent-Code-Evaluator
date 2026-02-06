A full-stack system for evaluating, comparing, and reviewing large language model outputs on coding problems using **objective execution-based metrics** and a **constrained LLM-as-a-judge** for qualitative assessment.
---

## Motivation

Evaluating LLMs—especially for code—is not just about pass/fail benchmarks.

Modern evaluation workflows rely on **multiple orthogonal signals**, including:

* execution-based verification
* qualitative assessment of solution quality
* comparison across models, prompts, and versions
* longitudinal tracking over time

The project explores how these signals can be combined in a practical, structured system to measure and compare model behavior on coding tasks.
---

## Core Features

### 🔹 Multi-Model Evaluation

* Run multiple LLMs on the same coding problem
* Execute generated Python code in a sandboxed environment
* Collect objective signals:

  * correctness
  * pass rate
  * runtime
  * execution errors

---

### 🔹 Objective, Deterministic Scoring

* Python execution is the **source of truth** for correctness
* Failures are categorized (runtime error, missing function, parsing error)
* Ensures reproducible, non-subjective evaluation

---

### 🔹 LLM-as-a-Judge (Quality-Only)

* Invoke a stronger external model (e.g. Claude) as a **quality judge**
* Judge compares **only solutions that already pass execution**
* Evaluation focuses on:

  * algorithmic soundness
  * code quality and clarity

The judge is explicitly constrained to **not re-evaluate correctness**.
---

### 🔹 Side-by-Side Model Comparison

* View outputs from multiple models for the same problem
* Inspect:

  * generated code
  * execution results
  * judge verdicts and scores
* Compare behavior across models and prompt versions

---

### 🔹 Experiment Tracking

* All runs logged to MLflow
* Metrics, artifacts, and configurations persisted per run
* Enables comparison across:

  * time
  * models
  * prompts
  * evaluation versions

---

## System Architecture

### Backend

* FastAPI (Python)
* Model orchestration and sandboxed execution
* Judge evaluation pipeline
* Structured storage of runs and results

### Frontend (Read-Only)

* React
* Problem list and run detail views
* Side-by-side model outputs
* Judge verdict visualization

### Evaluation

* Deterministic Python execution sandbox
* Structured failure categorization
* LLM-based qualitative comparison (no human input)

### Tracking

* MLflow for metrics and artifacts
* Database for runs, evaluations, and judge results

---

## Evaluation Flow

1. Select a coding problem
2. Run multiple models on the same input
3. Execute and score generated code
4. Display results side-by-side
5. Invoke LLM judge for quality comparison
6. Log all artifacts and metrics for analysis

---

EvalForge is an **evaluation and experimentation tool**, intentionally designed for inspection, iteration, and research workflows.

---

### Planned next steps include:

- Aggregating model performance across multiple problems and runs
- Comparing current results against historical baselines to detect regressions
- Integrating evaluation results into CI workflows once sufficient data exists

---

## Future Work

### 🔹 Expanded Evaluation Tasks

* Debugging-oriented coding problems
* Additional qualitative evaluation criteria

---

