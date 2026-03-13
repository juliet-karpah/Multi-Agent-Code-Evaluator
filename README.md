# LLM-Eval(My notes)

Testing code snippets from LLM with objective verifiers, LLM-judge, and Human Labels. 

Verifier-> define objective metrics -> implement measurable checks -> generate verifiable signals 

Human ranking(by domain expert, someone who is an expert on childhood education)

## combined review:
Objective verifiers:
- accuracy = code_reward(response, correct_answer)
- format = format_check(response)

Qualitative verifiers/signals:
- quality = llm_judge(response) AI feedback data AI feedback with a frontier AI model, such as GPT-4o costs less than $0.01
- human = if human(response) judge_confidence < 0.7 else None

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

If the judge is unable to determine which model's response is better with a confidence of 80%, then the evaluation will be put into the human review queue. The human review queue is rendered in a ReactJS frontend.

Human labeler chooses the winner. 

<code>
Winner: Model B

Why did Model A lose?

[ ] incorrect complexity
[x] fails edge case
[ ] hallucinated
</code>


## Architectural Design

![design](https://github.com/juliet-karpah/Multi-Agent-Code-Evaluator/blob/main/architecture.png)

Key Components:
- CLI Runner: orchestrates evaluation experiments
- Docker Sandbox: safely executes generated code
- LLM Judge: compares model outputs
- Supabase: stores evaluation results and human feedback
- Review UI: enables human preference annotation

# Scaling 
The app has two components:
- the CLI component for running code snippets and storing in Supabase.
- the frontend component for human labeling.


## The CLI component:

### Phase 1: Run 25 questions with 2 models(50 code snippets)
- single developer
- local execution
- synchronous evaluations

```CLI -> Prompt Models -> Docker Sandbox -> Persist Results```

### Phase 2: 100 questions with 2 models(200 code snippets)
- 8 workers with 25 questions each
- CLI Runner -> Job Queue -> Worker Pool -> Docker Sandboxes -> Persist Results
