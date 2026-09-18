# StyLens Installation Manual

## 1. Purpose

This manual defines the installation profiles and environment baseline for the StyLens MVP.

## 2. Choose a deployment profile

### Profile A: mobile or tablet client

No local application installation is required.

Requirements:

- a current Android or iOS device;
- a supported modern browser;
- a camera or access to stored photographs; and
- an HTTPS connection to an authorized StyLens server.

The mobile device captures photographs and uses the responsive interface. It does not need to execute heavy AI inference.

### Profile B: Raspberry Pi client or gateway

Recommended baseline:

- Raspberry Pi 5;
- 8 GB RAM recommended, 4 GB minimum;
- 64-bit Raspberry Pi OS;
- 16 GB or larger storage;
- Chromium or another current browser; and
- wired Ethernet or trusted Wi-Fi.

The Raspberry Pi may provide a kiosk, camera station, lightweight validation, or gateway. Multimodal and generative inference should run on an approved remote or local GPU host unless an edge model passes the same acceptance tests.

### Profile C: developer workstation

Minimum baseline:

- Linux, macOS, Windows, or WSL2;
- 4 CPU cores;
- 16 GB RAM;
- 10 GB free storage;
- Git 2.40 or later;
- Python 3.12; and
- network access to the selected model provider when managed inference is enabled.

### Profile D: optional local AI host

Recommended baseline:

- Linux;
- 8 CPU cores;
- 32 GB RAM;
- NVIDIA GPU with at least 16 GB VRAM;
- compatible NVIDIA driver and CUDA runtime; and
- sufficient encrypted storage for model weights and temporary artifacts.

Exact GPU, CUDA, PyTorch, and model versions will be pinned after the technical spike.

## 3. Repository setup

```bash
git clone https://github.com/eng-djc/stylens-image-consultant.git
cd stylens-image-consultant

python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Windows PowerShell activation:

```powershell
.venv\Scripts\Activate.ps1
```

Copy the environment template before starting the service:

```bash
cp .env.example .env
```

## 4. Configuration

Runtime configuration will use environment variables loaded from a local file excluded from Git.

Expected configuration groups:

- application environment;
- session lifetime;
- artifact-retention period;
- allowed file types and maximum size;
- analysis-provider selection;
- image-editing-provider selection;
- provider endpoints and credentials;
- encrypted storage location;
- logging level; and
- PDF output settings.

Rules:

- never commit API keys, tokens, client photographs, generated reports, or `.env` files;
- use a secret store for shared or production deployments;
- use different credentials for development and deployment;
- grant the minimum required permissions; and
- verify provider retention and training settings before processing real images.

## 5. Application start

Start the development service with:

```bash
uvicorn stylens.main:app --host 127.0.0.1 --port 8000 --reload
```

Remote devices must not use the development server directly. A shared deployment requires HTTPS, an approved reverse proxy or managed ingress, authentication, and network restrictions.

## 6. Verification checklist

Before processing any photograph, verify:

1. the health endpoint returns success;
2. HTTPS is active for remote access;
3. authentication and session isolation tests pass;
4. the consent notice version is configured;
5. storage encryption is active;
6. provider training and retention behavior is approved;
7. test images pass upload validation;
8. unapproved content cannot enter a report;
9. deletion completes within the configured threshold; and
10. logs contain no photographs, PII, prompts, secrets, or report content.

## 7. Raspberry Pi notes

Use the Raspberry Pi as a thin client or gateway by default.

- Prefer browser kiosk mode for a fixed consultation station.
- Store no photographs permanently on removable media.
- Disable browser password and form-data retention.
- Clear downloads after a report is transferred.
- Apply Raspberry Pi OS security updates.
- Use a dedicated non-administrator account.
- Restrict inbound network access.

## 8. Troubleshooting

### Python version is incorrect

Confirm:

```bash
python --version
```

The planned baseline is Python 3.12.

### A mobile or Raspberry Pi client cannot connect

Check server availability, DNS or IP address, firewall rules, HTTPS certificate validity, and whether the client is on an authorized network.

### Local model fails to load

Check model license acceptance, available RAM and VRAM, PyTorch and CUDA compatibility, storage capacity, and the pinned model revision.

### An image is rejected

Confirm that it is JPEG, PNG, or WebP; is no larger than 15 MB; has at least 1024 x 1024 resolution; contains one clearly visible consenting adult; and satisfies lighting and framing guidance.

## 9. Current limitation

The current MVP stores sessions and image bytes only in process memory. Restarting
the service deletes them. Use synthetic test images only until authentication,
encrypted persistent storage, automatic expiration, and deployment controls are
implemented and security-reviewed.
