# Remote Ophthalmology Clinical Decision Support Platform on AWS

Production-grade, cloud-native, multi-agent clinical decision-support platform that combines image quality assessment, specialist disease classification, patient background retrieval, multimodal clinical reasoning, and human-in-the-loop prescription approval.

## Overview

This project demonstrates how to design a real production workflow for remote ophthalmology support.

Patients can upload eye images from home, and the platform processes them through multiple controlled stages:

1. image quality assessment  
2. specialist disease classification  
3. retrieval of patient background from the database  
4. multimodal reasoning combining image findings and patient context  
5. clinician review and approval  
6. prescription generation after doctor confirmation  

This is not a simple image-classification demo. It is a full clinical decision-support system designed around safety, observability, evaluation, and continuous improvement.

## Why this project matters

Most AI healthcare demos stop at model accuracy. This project focuses on the real production questions:

- how to combine vision outputs with patient context
- how to keep doctor oversight in the loop
- how to trace and evaluate multi-agent decisions
- how to use feedback memory for continuous improvement
- how to separate model prediction from clinical action

## High-Level Workflow

Patient Upload  
→ Image Quality Model  
→ Specialist Vision Model  
→ Background Retrieval  
→ Clinical Reasoning Layer  
→ Clinician Summary  
→ Doctor Review / Approval  
→ Prescription or Final Recommendation

## Core Components

### Image Quality Assessment
The first model checks whether the uploaded image is usable for downstream interpretation.

### Specialist Vision Inference
A specialist vision model predicts disease class, disease name, severity, and confidence.

### Patient Background Retrieval
The system retrieves structured clinical background such as previous diagnoses, medications, allergies, prescriptions, and relevant history.

### Clinical Reasoning Layer
A grounded reasoning layer combines image findings, patient background, symptoms, and policy constraints to generate the final AI recommendation.

### Clinician Review
Doctors review, edit, approve, or override the recommendation.

### Prescription Generation
Final prescriptions or recommendations are generated only after clinician approval.

## Memory Design

This platform uses multiple kinds of memory:

### Workflow Memory
Short-term memory for the active case, including intermediate results and workflow state.

### Patient Memory
Persistent patient medical background retrieved from the clinical database.

### Agent Memory
Operational memory for agent decisions, reasoning traces, and workflow patterns.

### Feedback Memory
Stores clinician corrections such as:
- AI said disease = X, doctor corrected to Y
- AI suggested routine review, doctor escalated urgently
- AI summary omitted important background
- AI draft prescription conflicted with medication history

Feedback memory is later used for:
- gold-label generation
- retraining datasets
- prompt improvement
- few-shot examples for summary agents
- few-shot examples for LLM judges

## Prompt Engineering Strategy

LLM usage is constrained and grounded.

The LLM is used primarily for:
- clinician-facing summaries
- explanation generation
- optional LLM-as-a-judge evaluation

The LLM is not treated as the diagnostic engine.

Prompts are:
- versioned
- grounded on structured inputs
- constrained to avoid hallucination
- improved using retrieved feedback-memory examples

## Versioning Strategy

This project versions:
- quality model versions
- disease classification model versions
- reasoning logic versions
- prompt versions
- dataset versions
- policy versions
- feedback-memory index versions

This makes it possible to trace changes in performance back to specific system components.

## Evaluation Strategy

### Offline Evaluation
- quality model accuracy
- disease model accuracy and calibration
- slice-based evaluation by clinic / age / device

### Retrieval Evaluation
- patient background retrieval correctness
- feedback memory retrieval quality

### Workflow Evaluation
- retake correctness
- routing correctness
- doctor override rate
- summary grounding
- clinician summary usefulness

### AgentOps Evaluation
- deterministic validation
- LLM-as-a-judge
- safety evaluation
- function-calling checks when applicable
- trace completeness

### Online Evaluation
- live trace evaluation
- drift monitoring
- clinician disagreement
- anomaly detection
- feedback reuse effectiveness

## Monitoring

The platform monitors:

### Infrastructure
- request count
- latency
- service health
- queue size

### Models
- quality rejection rate
- disease class distribution
- confidence drift
- inference latency

### Workflow
- retake rate
- urgent escalation rate
- review latency
- completion rate

### Human Review
- clinician approval rate
- override rate
- review turnaround time

### AgentOps
- route patterns
- reasoning step latency
- summary generation issues
- feedback-memory hit rate
- policy violations

## AWS Stack

- Amazon S3 for image and artifact storage
- Amazon RDS PostgreSQL for metadata and patient context
- Amazon SageMaker for training and serving
- Amazon EKS for orchestration and API runtime
- AWS IAM / IRSA for service authentication
- AWS KMS for encryption
- CloudWatch, OpenTelemetry, Prometheus, and Grafana for observability

## Continuous Improvement Loop

The system improves through clinician feedback.

When clinicians override AI outputs, those corrections are stored in feedback memory and later reused for:
- generating gold labels
- retraining candidate models
- improving prompts
- improving evaluation prompts and judges
- improving summaries through few-shot retrieval

The platform uses a Champion–Challenger lifecycle for safe promotion.

## Disclaimer

This repository is a technical demonstration of architecture, AgentOps, MLOps, and cloud engineering. It is not a validated medical product and must not be used for real diagnosis or prescribing without appropriate clinical validation, regulatory approval, and clinician oversight.
