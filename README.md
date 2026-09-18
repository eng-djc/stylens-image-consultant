# StyLens

**StyLens** is a human-centered multimodal AI assistant that helps professional image consultants create structured, explainable, and personalized recommendations.

## Scope

StyLens combines client photographs, consultant-provided context, and a versioned image-consulting knowledge base covering:

- face shape;
- body shape and proportions;
- 12-season color theory;
- seven universal styles and personal style combinations;
- garment fit, color, contrast, patterns, silhouettes, and accessories; and
- outfit ideas, wardrobe planning, capsule wardrobes, and shopping guidance.

The system produces structured observations, confidence indicators, recommendations, controlled visualizations, and an approved PDF report. StyLens is decision support: it does not replace the consultant or make the final professional recommendation.

### MVP boundary

The first vertical slice will support one consenting adult, one consultation session, validated photographs, structured consultant input, one complete analysis path, one controlled garment visualization, consultant approval, PDF generation, and secure deletion.

Training or fine-tuning, minors, multiple people, body transformation, unrestricted person regeneration, video, and long-term client storage are outside the MVP.

## Human-in-the-Loop Design

1. The client provides informed consent.
2. The consultant uploads validated photographs and enters structured context.
3. Multimodal AI produces observations, not final decisions.
4. The knowledge layer applies traceable professional rules.
5. StyLens returns structured recommendations with confidence and limitations.
6. Controlled image editing modifies only consultant-authorized regions.
7. Automated checks measure face, body, and protected-region fidelity.
8. The consultant corrects, approves, rejects, or regenerates every result.
9. Only approved content is included in the PDF.
10. Source and derived artifacts are deleted under the configured retention policy.

Professional judgment, empathy, client goals, emotional context, and final accountability always remain with the consultant.

## Design to Be Implemented

StyLens uses a hybrid, modular architecture selected through the Case Method:

```text
Responsive Client
      |
Application API and Session Orchestrator
      |
      +-- Consent and Security
      +-- Multimodal Analysis Adapter
      +-- Versioned Knowledge and Rules
      +-- Controlled Image-Editing Adapter
      +-- Segmentation and Protected Masks
      +-- SSIM and IoU Validation
      +-- Consultant Approval
      +-- PDF Generation
      +-- Secure Deletion
```

The AI providers are replaceable. Microsoft Foundry, Hugging Face, Microsoft open-weight models, local inference, and other services remain candidates until they pass the same functional, privacy, licensing, latency, and fidelity criteria.

## Hardware Components

StyLens separates the client device from the inference host.

| Profile | Purpose | Baseline |
|---|---|---|
| Mobile phone or tablet | Capture images and use the responsive web interface | Current Android or iOS device, modern browser, camera, HTTPS connection |
| Raspberry Pi client or gateway | Kiosk, local capture, lightweight validation, or secure gateway | Raspberry Pi 5, 4 GB minimum, 8 GB recommended, 64-bit Raspberry Pi OS |
| Developer workstation | Development, tests, PDF generation, and provider integration | 4 CPU cores, 16 GB RAM, 10 GB free storage |
| Optional local AI host | Open-weight multimodal, segmentation, or image-editing inference | Linux, NVIDIA GPU, CUDA support, 16 GB VRAM recommended |
| Cloud or managed inference | Heavy inference without local GPU requirements | Selected only after privacy, licensing, cost, and acceptance testing |

A phone or Raspberry Pi can run the client and lightweight services. Heavy multimodal and generative inference is delegated to a local GPU host or approved managed provider unless a tested edge model satisfies the same acceptance criteria.

## Proposed Software Stack

Versions below are the implementation baseline and will be pinned in dependency files when development begins.

| Layer | Component | Baseline | Responsibility |
|---|---|---:|---|
| Runtime | [Python](https://www.python.org/) | 3.12 | Application and AI orchestration |
| API | [FastAPI](https://fastapi.tiangolo.com/) | 0.116+ | HTTP API, validation flow, and OpenAPI |
| Server | [Uvicorn](https://www.uvicorn.org/) | 0.35+ | ASGI development server |
| Schemas | [Pydantic](https://docs.pydantic.dev/) | 2.13+ | Structured inputs, outputs, and configuration |
| Client | HTML5, CSS3, JavaScript | ES2023 | Responsive mobile, desktop, and Raspberry Pi interface |
| Imaging | [OpenCV](https://opencv.org/) | 4.12+ | Image validation, alignment, masks, and geometry |
| Imaging | [Pillow](https://python-pillow.org/) | 11+ | Image loading, conversion, and safe export |
| Metrics | [scikit-image](https://scikit-image.org/) | 0.25+ | SSIM and image-quality measurements |
| Reports | [ReportLab](https://www.reportlab.com/opensource/) | 4.4+ | Local PDF generation |
| ML runtime | [PyTorch](https://pytorch.org/) | 2.6+ | Optional local model inference |
| Model SDK | [Transformers](https://huggingface.co/docs/transformers/) | 4.48.2+ | Open-weight multimodal adapters |
| Segmentation | [SAM 2](https://github.com/facebookresearch/sam2) | 2.1 checkpoints | Protected-region and garment masks |
| Candidate analysis | [Phi-4 Multimodal](https://huggingface.co/microsoft/Phi-4-multimodal-instruct) | Model-card revision under evaluation | Structured multimodal observations |
| Candidate vision | [Florence-2](https://huggingface.co/microsoft/Florence-2-large) | Model-card revision under evaluation | Grounding, detection, and region analysis |
| Testing | [pytest](https://docs.pytest.org/) | 8+ | Unit, integration, security, and acceptance tests |

### Main components and subcomponents

- **Client:** consent, capture/upload, consultant questionnaire, review, approval, report access.
- **Application:** sessions, orchestration, authorization, retries, retention, deletion.
- **Knowledge:** professional taxonomy, versioned rules, recommendation traceability.
- **AI adapters:** multimodal analysis and controlled image editing.
- **Image control:** segmentation, protected masks, recomposition, SSIM, IoU.
- **Reporting:** approved-content assembly, AI labels, PDF export.
- **Security:** encryption, least privilege, session isolation, minimal logs, secrets management.

## Documentation

- [Installation Manual](docs/INSTALLATION.md)
- [User Guide](docs/USER_GUIDE.md)

## Status

StyLens now includes an executable FastAPI MVP foundation with consultation sessions,
explicit adult consent, validated JPEG/PNG/WebP uploads, ephemeral in-memory storage,
and secure session deletion. Models and deployment providers still require quantitative
acceptance testing before integration.

## License

See [LICENSE](LICENSE).
