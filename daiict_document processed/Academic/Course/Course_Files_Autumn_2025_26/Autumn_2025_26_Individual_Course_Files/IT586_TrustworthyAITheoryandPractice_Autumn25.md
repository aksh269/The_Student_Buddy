# IT586_TrustworthyAITheoryandPractice_Autumn25

Source: `Z:/minor project/daiict_documents raw/Academic/Course/Course_Files_Autumn_2025_26/Autumn_2025_26_Individual_Course_Files/IT586_TrustworthyAITheoryandPractice_Autumn25.pdf`

## Page 1

Course Title

Trustworthy AI – Theory and Practice

Course Code
IT586
Credit Structure
3-0-2-4 (L-T-P-C)
Category
Elective
Semester
Autumn Semester (AY 25-26)
Program
B.Tech/ M.Tech /M.Sc
Prerequisites
Machine Learning and Deep Learning
Course
Objectives/
Brief Course
Description
Artificial-intelligence systems now power everything from boiler-plate document
generators to ICU monitors and trading engines. With that ubiquity has come
intense regulatory scrutiny: the EU AI Act, NIST AI RMF 1.0, India’s DPDP Act,
and a wave of sector-specific mandates all demand proof that models are robust,
reliable, private, fair, and value-aligned.
This course supplies the theory and hands-on techniques you need to meet those
demands. Through lectures, code labs students will learn to interrogate models for
failure modes, harden them against attacks and drift, quantify bias and privacy risk,
and translate legal text into concrete engineering controls.
Evaluation/
Grading Policy
(Tentative)
•
Mid-Sem – 20%
•
Assignments – 40%
•
Project Work – 30%
•
Participation – 10%
Course
Materials/
References
•
Course materials and other references will be provided throughout the
course duration.
Detailed Course
Content
Appendix

Course Outcome: Upon completion of this course, students will be able to:

•
Formulate risk models for end-to-end ML pipelines, mapping failure modes to security,
privacy, fairness, and alignment taxonomies.
•
Stress-test models with distribution shifts, adversarial/poisoning attacks, and jailbreak
prompts, then implement certified defenses.
•
Quantify and mitigate bias & privacy leakage using causal metrics and differential-privacy
guarantees.
•
Detect drift in production with conformal and OOD detectors tied to real-time incident
workflows.

## Page 2

APPENDIX

Detailed Course Contents

Foundations of AI Risk, NIST Risk Framework, EU AI Act snapshot

Adversarial Attacks and Defenses
Threat model taxonomy, Adversarial Examples, Fast Gradient Sign Method, Basic Iterative Method,
Projected Gradient Descent, Carlini& Wagner, One-pixel attack; Defenses: Adversarial Training,
Feature Squeezing, Adversarial Detection

Data Poisoning Attacks
Threat model taxonomy, label-flip based attacks, gradient-based attacks, backdoor attacks, data
sanitization filters, robust training

Distribution Shift and OOD detection
Problem Framing, Evaluation metrics, Density and Classical Detectors, SoftMax-based

Privacy
Intro to Privacy in ML, Membership Inference Attacks, Model Inversion Attacks, Pitfall of
Overfitting and Unintended Memorization in Neural Networks, Differential Privacy (DP), DP-SGD,
Privacy vs. Utility, Federated Learning, Attack vectors and corresponding defences in FL

Bias and Fairness
What is Bias, Bias sources, Evaluation Metrics, Re-weighting, adversarial debiasing, calibrated
equalized odds

Explainability and Interpretability
What is XAI, Taxonomy, Feature Importance (LIME, SHAP), Saliency Maps, Counterfactual and
contrastive explanations, Evaluation Metrics

Secure and Private LLMs
Security: Jailbreaks, Prompt Injection (direct, indirect, RAG), Red-teaming taxonomy, Filtering and
firewall models, prompt-hardening; Privacy: Threats, Differential Privacy for LLMs, Evaluation
Metrics

Robust Training Pipelines*
Pipeline anatomy & failure modes, data quality and shift proof curation, certified robustness,
randomized smoothing.
