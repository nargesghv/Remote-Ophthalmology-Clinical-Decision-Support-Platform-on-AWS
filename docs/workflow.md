# Workflow

1. patient submits eye image and metadata
2. quality model checks if image is usable
3. disease model predicts disease class and severity
4. patient background is retrieved from database
5. reasoning layer combines findings and context
6. summary layer prepares clinician-facing explanation
7. doctor approves or overrides
8. correction enters feedback memory
9. evaluation and retraining pipeline consume new feedback
