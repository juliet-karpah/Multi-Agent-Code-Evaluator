# LLM-Eval

## Architectural Design

![design](https://github.com/juliet-karpah/Multi-Agent-Code-Evaluator/blob/main/architecture.png)

Key Components:
- CLI Runner: orchestrates evaluation experiments
- Docker Sandbox: safely executes generated code
- LLM Judge: compares model outputs
- Supabase: stores evaluation results and human feedback
- Review UI: enables human preference annotation