# DOC.md — Remote Ophthalmology AgentOps Platform

## 1. Project intent

This project is designed as a realistic production-style AI platform for remote ophthalmology support.
The system is intentionally built around a clinically safer workflow:
- models assist
- rules constrain
- clinicians decide
The main idea is to separate:
- perception
- retrieval
- reasoning
- explanation
- approval
- feedback-driven improvement
## 2. End-to-end architecture

### Application layer
The FastAPI layer receives requests and validates, creates cases, and exposes review and feedback endpoints.
Main responsibilities:
- request validation
- case creation
- persistence
- orchestration entrypoint
- clinician feedback capture
Key modules:
- `app/main.py`
- `app/schemas.py`
- `app/db.py`
- `app/orchestrator.py`

### Model layer
The platform uses multiple specialized models instead of one monolithic system.

#### Image quality model
Purpose:
- reject unusable images
- prevent low-quality input from contaminating downstream decisions

#### Disease model
Purpose:
- classify disease label
- estimate disease name
- assign severity and confidence

#### Reasoning layer
Purpose:
- combine disease output with background context and policy constraints
- generate workflow recommendation

Key modules:
- `models/quality/`
- `models/vision/`
- `models/reasoning/`

### Retrieval layer
Retrieves patient background and later feedback-memory examples.

Purpose:
- add contextual reasoning
- support grounded recommendations
- enable memory-aware prompt improvement

Key modules:
- `app/retrieval_clients.py`
- `memory/patient_memory.py`
- `memory/retrieve_feedback.py`

### Summary and explanation layer
Turns structured outputs into readable clinician-facing summaries.
Purpose:
- improve usability
- preserve groundedness
- keep explanations aligned with policy and retrieval context
Key modules:
- `app/agents.py`
- `app/llm_client.py`
- `prompts/summary/`
- `prompts/explanation/`

### Review layer
Ensures clinician approval before final recommendation or prescription.
Purpose:
- human-in-the-loop safety
- auditability
- correction capture

Key modules:
- `app/review_queue.py`
- `app/clinician_feedback.py`

## 3. Policy design

The policy engine is deliberately separate from the models.
Why:
- predictions are not actions
- the workflow must be explainable
- rules should be updatable without retraining
Typical policy outputs:
- request retake
- routine review
- standard clinician review
- urgent clinician review
Key module:
- `app/policy_engine.py`

## 4. Memory design

### Workflow memory
Short-lived memory for the active case.

Stores:
- current stage
- intermediate model outputs
- pending action

### Patient memory
Persistent clinical history from storage.

Stores:
- conditions
- medications
- allergies
- previous diagnoses

### Agent memory
Operational memory for agent behavior and reusable examples.

### Feedback memory
Stores structured clinician corrections.

Examples:
- disease corrected
- route corrected
- summary issue noted
- medication conflict identified

Feedback memory is later reused for:
- gold-label generation
- retraining datasets
- prompt optimization
- few-shot examples for summaries
- few-shot examples for judges

## 5. Prompting and prompt versioning

Prompts are versioned because they affect production behavior.

Use prompt versioning for:
- summary prompts
- explanation prompts
- judge prompts

Prompt improvement should be driven by:
- recurring clinician corrections
- evaluation failures
- feedback-memory retrieval

Principles:
- keep prompts grounded
- never let prompts invent new facts
- make uncertainty explicit
- log prompt version alongside outputs

## 6. Evaluation framework

### Offline model evaluation
Use for:
- quality model accuracy
- disease classification performance
- calibration
- subgroup performance

### Retrieval evaluation
Use for:
- patient background completeness
- feedback-memory retrieval quality

### Workflow evaluation
Use for:
- routing correctness
- retake correctness
- doctor override rate
- summary quality

### AgentOps evaluation
Use for:
- deterministic validation
- LLM judge checks
- safety checks
- function-call evaluation if tools are used

### Online evaluation
Use for:
- drift
- disagreement
- feedback reuse effectiveness
- anomaly detection

## 7. Monitoring design

Monitoring is separate from evaluation.

Evaluation asks:
- was the output correct?

Monitoring asks:
- what is happening in production?

Track:
- API latency
- model latency
- action distribution
- retake rate
- override rate
- feedback-memory hit rate
- workflow failures

Key modules:
- `monitoring/tracing/`
- `monitoring/metrics/`
- `monitoring/alerts/`
- `monitoring/exporters/`

## 8. Feedback loop and promotion

The system should improve safely.

Flow:
1. clinician feedback captured
2. feedback memory updated
3. gold labels built
4. retraining dataset prepared
5. retraining triggered when thresholds are met
6. challenger compared to champion
7. safe promotion or rollback decision made

Key modules:
- `feedback_loop/collect_feedback.py`
- `feedback_loop/build_gold_labels.py`
- `feedback_loop/prepare_retraining_dataset.py`
- `feedback_loop/retraining_trigger.py`
- `feedback_loop/champion_challenger.py`
- `feedback_loop/rollback_promotion.py`

## 9. Suggested GitHub presentation

Top repo description:
> Production-grade multi-agent clinical decision-support platform on AWS with memory-aware AgentOps, evaluation, monitoring, and feedback-driven improvement.

Suggested topics:
- agentops
- mlops
- aws
- fastapi
- sagemaker
- kubernetes
- healthcare-ai
- observability
- llm
- multi-agent

## 10. Push flow

### Initialize repo if needed

```bash
git init
git branch -M main
```

### Add remote

```bash
git remote add origin https://github.com/<your-username>/<your-repo>.git
```

### Add and commit

```bash
git add .
git commit -m "Initial production scaffold for remote ophthalmology AgentOps platform"
```

### Push

```bash
git push -u origin main
```

### Recommended follow-up commits

```bash
git add .
git commit -m "Integrate memory and prompt versioning layer"
git commit -m "Add evaluation and online monitoring scaffolds"
git commit -m "Add feedback loop and promotion logic"
git push
```

## 11. Final note

This scaffold reflects how real production AI systems:
- modular
- observable
- evaluable
- feedback-aware
- safe by design
