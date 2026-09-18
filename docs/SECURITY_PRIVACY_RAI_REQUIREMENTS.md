# Security, Privacy, and Responsible AI Requirements

## Purpose

This document defines mandatory boundaries for the controlled StyLens hackathon
prototype. These requirements must be satisfied before a demonstration. Moving
beyond these boundaries requires formal Privacy, Security, Responsible AI, and
Legal review.

## Data boundary

| ID | Requirement | Acceptance criterion |
|---|---|---|
| SPR-01 | The prototype shall process only synthetic people and fictional profiles. | 100% of upload requests require an affirmative synthetic-data attestation; requests without it or with a negative value return HTTP 403. |
| SPR-02 | The prototype shall exclude minors. | The consent workflow requires adult confirmation for 100% of sessions before image upload. |
| SPR-03 | The system shall minimize collected data. | No legal name, address, email, phone number, exact birth date, or government identifier is required by an MVP API schema. |
| SPR-04 | The system shall remove embedded source metadata. | Every accepted image is decoded and re-encoded; automated tests verify that processing does not preserve source EXIF metadata. |
| SPR-05 | The system shall not extract background or bystander information. | Analysis schemas and prompts contain no fields for bystanders, location, objects unrelated to styling, or background profiling. |
| SPR-06 | The system shall keep personal content out of logs. | Automated log-capture tests find zero image bytes, prompts, measurements, profile content, or report content. |
| SPR-07 | The system shall not use submitted data for training. | Every candidate provider must document that inputs are not used for training before it can pass provider evaluation. |
| SPR-08 | The MVP shall delete uploaded artifacts by default. | Authorized deletion removes session metadata and artifact bytes immediately; the measured API completion target is at most 15 seconds for the in-memory MVP. |

## Responsible AI boundary

| ID | Requirement | Acceptance criterion |
|---|---|---|
| RAI-01 | StyLens shall provide subjective styling recommendations, not objective judgments about a person. | 100% of report templates label recommendations as advisory and require consultant approval. |
| RAI-02 | StyLens shall not rank attractiveness or use body-shaming language. | A prohibited-output test set produces zero attractiveness scores, rankings, insults, or weight-loss recommendations. |
| RAI-03 | StyLens shall not infer sensitive or unrelated attributes. | Output schemas contain no fields for ethnicity, health, religion, gender identity, emotion, disability, or sexual orientation. |
| RAI-04 | StyLens shall not perform facial identification or create biometric identity templates. | No face-recognition, identity-matching, face-embedding, or biometric-template component is present in the dependency inventory. |
| RAI-05 | A professional consultant shall control final recommendations. | 100% of observations and visualizations require approve, edit, reject, or regenerate disposition before PDF inclusion. |
| RAI-06 | Confidence values shall correspond to validated measurements. | No confidence percentage is displayed without a documented evaluation dataset, metric, sample size, and threshold. |
| RAI-07 | Evaluation shall cover representative visual diversity. | The synthetic evaluation set documents multiple skin tones and body types and reports results by subgroup before a model is selected. |
| RAI-08 | StyLens shall disclose limitations. | Every generated report includes the model/provider version, advisory-use statement, known limitations, and AI-generated-image label when applicable. |

## Security and provider boundary

| ID | Requirement | Acceptance criterion |
|---|---|---|
| SEC-01 | Credentials shall remain outside source control and logs. | Secret scanning reports zero committed credentials; configuration uses environment variables or an approved secret store. |
| SEC-02 | Access shall follow least privilege. | Each component and provider credential has a documented minimum permission set; no shared administrator credential is used. |
| SEC-03 | Images shall remain isolated by pseudonymous session identifier. | Cross-session access tests return no artifact or metadata from another session. |
| SEC-04 | Candidate providers shall be assessed before integration. | Evaluation records retention, training use, processing location, storage location, subprocessors, deletion behavior, license, latency, and cost for every provider. |
| SEC-05 | Components and content shall have compatible licenses and usage rights. | 100% of models, datasets, libraries, images, and knowledge sources have a recorded license and permitted-use decision. |
| SEC-06 | Real-person processing shall remain disabled until governance reviews approve it. | Version 1 contains no configuration switch that enables real-person data; changing this boundary requires a documented review decision and a reviewed code change. |

## Geographic and governance constraint

The intended user locations and all processing and storage regions must be
documented before deployment. Applicable requirements may differ across the
European Union, United Kingdom, California, other U.S. states, and additional
jurisdictions.

The current prototype is not approved for production or for real participant data.
