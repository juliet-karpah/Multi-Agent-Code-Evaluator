# LLM-Eval

LLM-Eval is an **evaluator-first, human-in-the-loop evaluation system** for large language models, focused on **measuring, reviewing, and comparing model responses on python coding tasks**.

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

# Features

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

A stronger LLM is used to review the code responses.

Capabilities:

* suggest preferred response
* highlight problematic spans
* provide critique and confidence score

---

## 4. Human-in-the-Loop Review Interface (React)

### Reviewer Workflow

* side-by-side model responses
* selectable text spans
* structured issue categories
* one-click accept / override of LLM suggestion
* optional critique explanation

---

## 5. Preference Data System

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

## 7. Dockerized Deployment with Docker-compose

* Backend (FastAPI)
* Frontend (React)
* MLflow server
* PostgreSQL Database

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