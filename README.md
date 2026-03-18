# LLM-Eval(My notes)

## Architectural Design

![design](https://github.com/juliet-karpah/Multi-Agent-Code-Evaluator/blob/main/architecture.png)

Key Components:
- CLI Runner: orchestrates evaluation experiments
- Docker Sandbox: safely executes generated code
- LLM Judge: compares model outputs
- Supabase: stores evaluation results and human feedback
- MLFlow: for experiment tracking
- Review UI: enables human preference annotation

## AI Usage Disclosure
This project was not vibe-decoded but AI was used in the same way you would ask a senior engineering colleague over Slack design decisions. 
Example questions I asked AI during this project: Will my sandbox setup break with recursive coding algorithms? 

## Evaluation Strategy

Testing code snippets from LLM with objective verifiers, LLM-judge, and Human Labels. 

CLI Runner -> Prompt Dataset -> Model A + Model B -> Sandbox Execution -> Judge LLM -> Human Review -> Analytics

## Combined review:

### Quantitative Signals:
- Runtime in milliseconds

Verifier-> define objective metrics -> implement measurable checks -> generate verifiable signals

sandbox results 
-> score_problem() (model x question) 
-> rank_models_per_run() (per question) 
-> aggregate_dimension_scoring() (per model x run)


### Quality Signals
- quality = llm_judge(response) AI feedback data AI feedback with a frontier AI model, such as GPT-4o costs less than $0.01
- human = if human(response) judge_confidence < 0.7 else None

## Sandboxed Code execution
Run LLM generated code safely in a containerized docker sandbox. The sandbox is setup with layers of protection such as restricted permissions, runtime resource limits, and container isoloation in the event of malicious LLM output. 

The features of this safe docker sandbox:
- create a non-root user
- fixed memory
- fixed CPU
- no network
- fixed processes
- readonly

Docker process:
- create a container from image
- start python
- run executor script
- destroy container

The program flow is as follows:
run.py -> run_evaluation() -> run_code_in_sandbox() -> docker run python-sandbox -> python /sandbox/code.py


## Running the evaluations
- First build a container from the home directory

```docker build -t python-sandbox infra/sandbox```

- run evaluations

```python run.py --config [latestConfig].yaml```


## v1 
one config represents one experimental execution

1 CLI run = 1 experiment run

- run CLI with config name

eg ```python run.py --config config_v1.yaml```

for every run
    - raw_eval rows
        - model A × question 1
        - model B × question 1
        - model A × question 2

example of a run:

Run #1
Config: config_v1
Models: QWEN vs MISTRAL
Questions: 10
Win rate: 57%

win rate is determined by the llm judge unless it has a confidence score of <80 and the human reviewer decides. 

why 80? I am not sure. I just picked this. 

run details 

slice:
- dataset slice
    - topic(dp, array, graph)
    - category(easy, medium, hard)
- error slice:
    - timeout, crash, execution error from sandbox
    - pedagogy, explanation clarity from judge
    - hallucination, syntax from human eval(if available)

## Human labeling Required If Low Confidence Score From LLM-Judge:


```if judge_confidence < 0.8: show in review queue```

If the judge is unable to determine which model's response is better with a confidence of 80%, then the evaluation will be put into the human review queue. The human review queue is a list rendered in a ReactJS frontend.

Human labeler chooses the winner. 

<code>
Winner: Model B

Why did Model A lose?

[ ] incorrect complexity
[x] fails edge case
[ ] hallucinated
</code>


# Scaling and Cost
The app has two components:
- the CLI component for running code snippets and storing in Supabase.
- the frontend component for human labeling.

## The CLI component:

### Phase 1: Run 25 questions with 2 models(50 code snippets)
- single developer
- local execution
- synchronous evaluations

50 sandbox runs

docker startup 200-500msto startup docker




```CLI -> Prompt Models -> Docker Sandbox -> Persist Results```

### Phase 2: 100 questions with 2 models(200 code snippets)
- 8 workers with 25 questions each
```CLI Runner -> Job Queue -> Worker Pool -> Docker Sandboxes -> Persist Results```

## Resources
[Anthropic Evals For AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
[Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/)
[Preference Data](https://rlhfbook.com/c/11-preference-data)