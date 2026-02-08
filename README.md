# LLM-Eval

LLM-Eval is an **evaluator-first, human-in-the-loop evaluation system** for large language models, focused on **measuring, reviewing, and comparing model behavior on coding tasks**.

It combines:

* a **CLI evaluation harness** for reproducible, automated runs
* **sandboxed execution** for objective correctness
* **LLM-assisted review** to accelerate qualitative assessment
* a **React human review interface** for preference data creation
* **MLflow + database persistence** for traceability and analysis

The system is designed to mirror **real internal evaluation infrastructure** used by applied AI and research teams.

---

## Core Principles

* Models are treated as **black boxes**
* Evaluation is **reproducible and inspectable**
* Humans remain **in the loop**, with LLMs as assistants
* Evaluation artifacts are **first-class data**, not logs

---

# ✅ MVP 

## 1. CLI Evaluation Harness

Primary interface:

```bash
make eval CONFIG=configs/eval_v1.yaml
```

End-to-end pipeline:

```
load config
→ run multiple models
→ sandbox execution
→ score outputs
→ LLM judge + pre-review
→ persist results
→ log to MLflow
```

Features:

* config-driven runs (YAML)
* explicit model/version selection
* deterministic execution
* single-command reproducibility

---

## 2. Objective Execution-Based Evaluation

* Generated Python code executed in a sandbox
* Deterministic parsing and scoring
* Metrics:

  * correctness / pass rate
  * runtime
  * execution failures
* Objective correctness is the **source of truth**

---

## 3. LLM-Assisted Review (Judge + Pre-Review)

A stronger LLM is used to **assist review**, not replace humans.

Capabilities:

* suggest preferred response
* highlight problematic spans
* provide critique and confidence score

Used to:

* accelerate human review
* reduce reviewer disagreement
* surface ambiguous cases early

---

## 4. Human-in-the-Loop Review Interface (React)

A **reviewer-focused UI**, inspired by real internal tooling.

### Reviewer Workflow

* side-by-side model responses
* selectable text spans
* structured issue categories
* one-click accept / override of LLM suggestion
* optional human rationale

Outputs:

* structured human preference data
* linked to runs, models, configs, and prompts

---

## 5. Preference Data System (RLHF-Compatible)

Human and LLM judgments are stored as **first-class artifacts**:

* winner / loser
* rationale
* source (`human` or `llm`)
* linked run + dataset + config hash

This produces **clean preference datasets** suitable for downstream RLHF-style workflows
(no training performed in this project).

---

## 6. Persistence & Experiment Tracking

* PostgreSQL schema
* MLflow tracking:

  * metrics
  * artifacts
  * configs
* Full traceability from judgment → model → run → config

---

## 7. Dockerized Deployment

Required for MVP.

* Backend (FastAPI)
* Frontend (React)
* MLflow server
* Database

Single command startup:

```bash
docker-compose up --build
```
---

## 8. Documentation (README)

The MVP includes:

* architecture diagram
* design decisions
* example CLI output
* how to run locally
* explanation of human-in-the-loop workflow

---

# 🚀 Stretch Goals (Post-MVP)

## 1. Aggregation & Model Stability Analysis

* aggregate scores across problems
* variance-based stability metrics
* model-level summaries
* baseline comparison

---

## 2. Regression Detection & CI Gates

* detect regressions vs baselines
* threshold-based alerts
* CI-compatible exit codes
* later: statistical significance tests

---

## 3. Consensus Reduction & Escalation Logic

* automatically route only hard cases to consensus
* disagreement clustering
* reviewer calibration metrics

---

## 4. Dataset Versioning & Export

* versioned preference datasets
* export to JSON / CSV
* compatibility with RLHF pipelines

---

## 5. Additional Language Support

* extend sandbox adapters to:

  * JavaScript / TypeScript
* same evaluation + review abstractions

---

## 6. Time-Series & Drift Visualization

* model behavior over time
* emerging failure modes
* longitudinal analysis dashboards

---

# What LLM-Eval Is *Not*

* Not a model training system
* Not a benchmark leaderboard
* Not a demo-first app
* Not a fine-tuning pipeline

LLM-Eval is **evaluation infrastructure**.

---