# StyLens User Guide

## 1. Purpose

StyLens helps a professional image consultant analyze authorized client photographs, apply a professional knowledge base, prepare personalized recommendations, create controlled visualizations, and produce an approved PDF report.

StyLens supports professional judgment. It does not replace the consultant.

The hackathon prototype accepts only synthetic people and fictional profiles.
Do not upload photographs, measurements, preferences, or assessments belonging
to a real person.

## 2. User roles

### Client

- reviews the privacy and consent notice;
- authorizes the use of photographs;
- provides goals, preferences, and relevant context; and
- receives the approved report.

### Image consultant

- creates the consultation;
- validates consent and photographs;
- enters professional observations;
- reviews AI-assisted observations and recommendations;
- approves, corrects, rejects, or regenerates outputs; and
- authorizes the final report.

### Administrator or security reviewer

- configures approved providers and retention;
- controls access;
- verifies privacy and security settings; and
- reviews non-sensitive audit events.

## 3. Supported MVP workflow

### Step 1: obtain consent

Read the complete notice with the client. Confirm that:

- the photographed person is the consenting client;
- the client is an adult;
- the stated processing purpose is understood;
- the retention and deletion terms are understood; and
- the client affirmatively accepts the current notice.

The system must not accept or process photographs before consent.

### Step 2: create a consultation

Create a new session. Use the generated pseudonymous session identifier. Do not use the client's name in filenames or technical identifiers.

### Step 3: capture or upload photographs

For the MVP, use a front-facing or half-body photograph with:

- one consenting adult;
- neutral, even lighting;
- a sharp and unobstructed face;
- a natural pose;
- clearly visible clothing and silhouette;
- a simple background when possible;
- at least 1024 x 1024 resolution; and
- JPEG, PNG, or WebP format no larger than 15 MB.

Retake the photograph if the system reports poor lighting, blur, occlusion, framing, or insufficient resolution.

### Step 4: enter consultation information

Complete the required fields for:

- client goals;
- professional or social context;
- style preferences;
- color preferences;
- garment preferences;
- consultant observations; and
- selected analysis categories.

Collect only information required for the consultation.

### Step 5: request multimodal analysis

StyLens produces structured observations related to the selected categories. Review:

- the observation;
- supporting image evidence;
- applied knowledge rules;
- confidence or uncertainty;
- limitations; and
- proposed recommendations.

Do not treat model output as an established fact.

### Step 6: correct and approve observations

For every item, select one action:

- **Approve:** the item is professionally acceptable.
- **Edit:** correct the wording or professional interpretation.
- **Reject:** exclude the item.
- **Regenerate:** request another AI-assisted draft.

No item can enter the final PDF without explicit approval.

### Step 7: generate a controlled visualization

Select the garment or attribute that may change. StyLens must protect all other regions.

The MVP visualization should be limited to a garment-color change or supported upper-garment replacement. It must not intentionally change:

- facial identity;
- body type or proportions;
- apparent age;
- skin tone;
- ethnicity;
- disability-related characteristics; or
- any unselected attribute.

### Step 8: review fidelity results

Check the automated validation:

- facial protected-region SSIM must be at least 0.99;
- body-silhouette IoU must be at least 0.95; and
- SSIM outside the authorized mask and boundary must be at least 0.98.

These measurements support quality control; they do not prove identity. Reject the visualization if it does not accurately represent the client, even when automated thresholds pass.

### Step 9: approve the PDF

Review the complete report and confirm:

- all observations and recommendations were approved;
- rejected content is absent;
- visualizations accurately represent the client;
- AI-assisted images are labeled;
- limitations are visible; and
- no unnecessary personal information is included.

Generate and deliver the PDF only after this review.

### Step 10: close and delete the session

After delivery:

- confirm the client received the correct report;
- close the consultation;
- request immediate deletion when appropriate; and
- confirm deletion completion.

For the MVP, active artifacts must be removed within 15 minutes of an authorized deletion request and within 60 minutes after report delivery or session termination.

## 4. Expected report sections

The approved PDF may include:

1. consultation goals;
2. validated observations;
3. face-shape guidance;
4. body-shape and proportion guidance;
5. 12-season color findings;
6. universal-style profile and combinations;
7. garment, fit, contrast, pattern, silhouette, and accessory guidance;
8. outfit and wardrobe ideas;
9. shopping guidance;
10. approved visualizations; and
11. limitations and AI-assistance disclosure.

Only sections implemented and professionally validated for the MVP should be included.

## 5. Safe-use rules

- Process only authorized photographs.
- Use only synthetic people and fictional profiles in the hackathon prototype.
- Do not process minors in the MVP.
- Do not upload customer or confidential data during development tests.
- Do not use StyLens for identity verification.
- Do not infer health, personality, attractiveness, ethnicity, or unrelated sensitive characteristics.
- Do not use client data for model training.
- Do not copy images into tickets, logs, source control, or chat messages.
- Do not override failed fidelity or security checks.

## 6. Error handling

### Upload rejected

Follow the displayed correction, then retake or re-export the image.

### Analysis fails

Retry only after confirming that the session remains active and the provider is approved. Do not create duplicate sessions unless recovery fails.

### Visualization fails fidelity checks

Reject it. Adjust the authorized mask, simplify the requested transformation, or use the original photograph without a generated visualization.

### PDF contains incorrect content

Do not deliver it. Return to review, correct the affected items, and generate a new report.

### Deletion cannot be confirmed

Stop using the session and escalate to the administrator or security reviewer. Do not claim that the data was deleted without evidence.

## 7. Current status

This guide describes the approved target workflow. Interface labels and screenshots will be added after the first functional user interface is implemented.
