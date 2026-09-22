<p align="center">
  <img src="docs/img/background.gif" width="100%">
</p>

# DiscoRSE — Training Material Metadata Extraction

This project extracts **structured metadata from training-material repositories** (mainly GitHub today) and exports it as **[Bioschemas TrainingMaterial](https://bioschemas.org/profiles/TrainingMaterial/1.0-RELEASE)** JSON-LD.

It supports the [DiscoRSE](https://www.discorse.de/) goal of making Research Software Engineering (RSE) open educational resources easier to find, describe, and reuse.

The codebase is a fork of [CoMET-RS](https://github.com/zbmed-semtec/maSMP-metadata-extraction) (Code Metadata Extraction Toolkit for Research Software). The original **maSMP** and **CodeMeta** software pipelines are still available; the main focus of this fork is **training materials + Bioschemas**.

---

## What this tool does

1. You provide a **GitHub** (or GitLab) repository URL.
2. The backend reads platform metadata and common repo files (README, `CITATION.cff`, license, etc.).
3. For **Bioschemas**, it builds training-oriented fields such as `name`, `description`, `keywords`, `abstract`, `teaches`, `learningResourceType`, `educationalLevel`, `license`, and `author`.
4. You get JSON-LD plus optional enrichment (source, confidence, category: Minimum / Recommended / Optional).

### Main components

| Component | Stack | Role |
|-----------|--------|------|
| **Backend** (`backend-migration/`) | FastAPI, layered architecture | Extraction pipelines, schemas, API, CLI |
| **Frontend** (`frontend-migration/`) | Nuxt 3, Vue 3, TypeScript | DiscoRSE-branded UI to run extraction and view results |

Supported schemas:

- **Bioschemas** — TrainingMaterial (primary for this fork)
- **maSMP** — machine-actionable Software Management Plan (inherited)
- **CODEMETA** — software metadata (inherited)

---

## Quick start with Docker (recommended)

### 1. Install Docker

Download from [Docker’s website](https://www.docker.com/get-started).

### 2. Build and run

From the project root:

```sh
docker compose up --build
```

This starts:

- **Backend** (FastAPI) on port **8000**
- **Frontend** (Nuxt) on port **3000**

### 3. Open the app

| Service | URL |
|---------|-----|
| Frontend UI | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API docs (Swagger) | http://localhost:8000/docs |

Example Bioschemas call:

```text
GET /api/metadata/enriched?repo_url=https://github.com/owner/repo&schema=Bioschemas
```

### 4. Stop

```sh
docker compose down
```

### Authentication (recommended)

GitHub rate limits are low without a token. For regular use or private repos:

```bash
export GITHUB_TOKEN=ghp_...      # GitHub
export GITLAB_TOKEN=glpat_...    # GitLab
```

You can also paste a token in the web UI when extracting.

---

## Running without Docker

### Backend

See [backend-migration/README.md](./backend-migration/README.md):

```bash
cd backend-migration
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

See [frontend-migration/README.md](./frontend-migration/README.md):

```bash
cd frontend-migration
npm install
npm run dev
```

Frontend expects the API at `http://127.0.0.1:8000` by default.

---

## CLI and Python package

The backend is also available as **`comet-rs`** (package name inherited from CoMET-RS).

```bash
pip install comet-rs   # or install from this repo’s backend-migration/
```

Python **3.10+** required.

### Extract training-material metadata (Bioschemas)

```bash
comet-rs extract https://github.com/owner/repo Bioschemas --with-enrichment
```

### Extract software metadata (legacy schemas)

```bash
comet-rs extract https://github.com/owner/repo maSMP --with-enrichment
comet-rs extract https://github.com/owner/repo CODEMETA
```

### Single property

```bash
comet-rs extract_property https://github.com/owner/repo abstract --schema Bioschemas
```

### From Python

```python
import os
from app.layer_4.services.metadata_service import run_extraction

jsonld_document, enriched = run_extraction(
    repo_url="https://github.com/owner/repo",
    schema="Bioschemas",  # or "maSMP" / "CODEMETA"
    access_token=os.getenv("GITHUB_TOKEN"),
    with_enrichment=True,
)
```

More detail: [backend-migration/README_PYPI.md](./backend-migration/README_PYPI.md).

---

## Project status (this fork)

**Done / in progress**

- Bioschemas TrainingMaterial schema + GitHub training extraction pipeline
- README / CITATION-oriented training field parsing (`abstract`, `teaches`, `learningResourceType`, …)
- Web UI support for Bioschemas (Minimum / Recommended / Optional)
- DiscoRSE frontend branding (logo, About, footer)
- CLI support for Bioschemas

**Still planned**

- Broader testing on real RSE training repos (e.g. via [glittr.org](https://www.glittr.org/))
- First fully functional GitHub release
- Zenodo metadata extraction (draft)
- Further Bioschemas field coverage and quality improvements

---

## Contributing

Fork the repository, create a branch, and open a pull request with your changes.

## License

This project is licensed under the MIT License.
