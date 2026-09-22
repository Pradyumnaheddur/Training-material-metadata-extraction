# DiscoRSE Backend — Training Material Metadata Extraction

FastAPI backend that extracts metadata from code repositories and exports **JSON-LD**.

This directory is the backend of a **DiscoRSE** fork of [CoMET-RS](https://github.com/zbmed-semtec/maSMP-metadata-extraction). The main focus here is **training materials** described with **[Bioschemas TrainingMaterial 1.0-RELEASE](https://bioschemas.org/profiles/TrainingMaterial/1.0-RELEASE)**. The original **maSMP** and **CodeMeta** software pipelines remain available.

<p align="center">
  <img src="../docs/img/backend_architecture.png" width="75%">
</p>

---

## What this backend does

Given a repository URL:

1. Detects the platform (**GitHub** or **GitLab**)
2. Runs a pipeline of extraction steps (API + files such as README / `CITATION.cff`)
3. Merges signals into an internal metadata model
4. Exports schema-specific JSON-LD (`Bioschemas`, `maSMP`, or `CODEMETA`)
5. Optionally returns enrichment (source, confidence, category)

### Supported schemas

| Schema | Domain | Platforms today | Notes |
|--------|--------|-----------------|--------|
| **Bioschemas** | `training` | **GitHub** | Primary for this fork — TrainingMaterial profile |
| **maSMP** | `software` | GitHub, GitLab | Inherited CoMET-RS path |
| **CODEMETA** | `software` | GitHub, GitLab | Inherited CoMET-RS path |

`schema=Bioschemas` is resolved to `domain=training` in `app/layer_2/use_cases/domain_schema.py`.

---

## Training-material path (important)

When you request **Bioschemas**, the composer selects:

`app/layer_3/composers/profiles/training_github_bioschemas.py`

That pipeline:

- Reuses GitHub steps (name, description, dates, contributors, keywords, license, …)
- Adds **training file steps** (`training_file_steps`): CITATION/README signals plus training-specific README parsing
- Builds a single root JSON-LD document (`@type: LearningResource`) with `dct:conformsTo` pointing at the TrainingMaterial profile

### Key training files

| Area | Path |
|------|------|
| Bioschemas export keys | `app/layer_1/schemas/bioschemas/export_fields.py` |
| Minimum / Recommended / Optional | `app/layer_1/schemas/bioschemas/profiles.py` |
| Schema registration | `app/layer_1/schemas/definitions.py` |
| Domain routing | `app/layer_2/use_cases/domain_schema.py` |
| Pipeline composer | `app/layer_3/composers/pipeline_composer.py` |
| Training GitHub profile | `app/layer_3/composers/profiles/training_github_bioschemas.py` |
| Training file step bundle | `app/layer_3/steps/step_bundles/training_file_steps.py` |
| README training parser | `app/layer_3/steps/extract_steps/services/files/training/helpers/readme_training_parser.py` |
| Merge training fields | `app/layer_3/steps/merge_steps/training/merge_training_readme_fields_step.py` |
| JSON-LD builder | `app/layer_3/builders/jsonld_builder.py` |
| Enriched API shaping | `app/layer_4/builders/enriched_metadata.py` |
| API schemas list | `app/layer_4/constants.py` → `SUPPORTED_SCHEMAS` |

### Fields commonly filled for Bioschemas

- **Minimum:** `name`, `description`, `keywords` (+ hardcoded `dct:conformsTo`)
- **From training README parsing (when present):** `abstract`, `teaches`, `competencyRequired`, `audience`, `educationalLevel`, `learningResourceType`, `inLanguage` (only if detected — not hardcoded to English)
- **Fallback:** if `description` is empty but `abstract` exists, description is filled from abstract

---

## Architecture

Four layers under `app/`:

| Layer | Location | Role |
|-------|----------|------|
| **1** | `app/layer_1/` | Domain models, schemas (Bioschemas / maSMP / CodeMeta), provenance |
| **2** | `app/layer_2/use_cases/` | Orchestration (`ExtractMetadataUseCase`, domain/schema resolution) |
| **3** | `app/layer_3/` | Extraction pipelines, steps, JSON-LD builder, FAIR evaluator |
| **4** | `app/layer_4/` | FastAPI routes, API schemas, response builders, CLI wiring |

Layer 3 layout (high level):

- `steps/contracts/` — `StepContext`, `StepState`, `ExtractionPipeline`
- `steps/extract_steps/` — platform adapters, file parsers, external APIs
- `steps/merge_steps/software/` — merge candidates for software fields
- `steps/merge_steps/training/` — merge training / Bioschemas fields
- `composers/profiles/` — GitHub/GitLab × schema pipelines (including `training_github_bioschemas`)
- `extraction_metadata/` — provenance collector and `record_field_provenance`
- `builders/jsonld_builder.py` — export internal metadata to JSON-LD

Internal entity name is still `SoftwareMetadata` (inherited); Bioschemas training fields were added onto it for now.

Full documentation: run `mkdocs serve` in this directory (see [Getting started](docs/getting-started.md)) or read the pages under `docs/`.

---

## Prerequisites

- **Python 3.10+**
- A GitHub personal access token for regular use (avoids API rate limits)

```bash
export GITHUB_TOKEN=ghp_...      # recommended for GitHub repos
export GITLAB_TOKEN=glpat_...    # for GitLab repos (software schemas)
```

**Note:** The HTTP API uses the `access_token` query parameter (from the UI or curl). The **CLI** falls back to `GITHUB_TOKEN` / `GITLAB_TOKEN` when `--token` is omitted. Docker Compose does not inject these env vars unless you add them.

---

## Installation

From `backend-migration/`:

```bash
pip install -r requirements.txt
```

---

## Run the API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Swagger: http://localhost:8000/docs  
- Health: http://localhost:8000/api/health  

### Useful endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /api/metadata` | Plain JSON-LD |
| `GET /api/metadata/enriched` | JSON-LD + source / confidence / category |
| `GET /api/metadata/stream` | Same as enriched, with SSE progress |
| `GET /api/metadata/property` | Single property |
| `GET /api/fairness` | FAIR report (**software-oriented**; see Known gaps) |

### Example — Bioschemas (training)

```bash
curl "http://localhost:8000/api/metadata/enriched?repo_url=https://github.com/owner/repo&schema=Bioschemas&access_token=$GITHUB_TOKEN"
```

### Example — maSMP (software, inherited)

```bash
curl "http://localhost:8000/api/metadata/enriched?repo_url=https://github.com/owner/repo&schema=maSMP&access_token=$GITHUB_TOKEN"
```

---

## CLI (`comet-rs`)

Package/CLI name is still **`comet-rs`** (inherited). From this backend (or after `pip install` of the package):

```bash
# Training materials (primary for this fork)
comet-rs extract https://github.com/owner/repo Bioschemas --with-enrichment --token "$GITHUB_TOKEN"

# Software schemas (still supported)
comet-rs extract https://github.com/owner/repo maSMP --with-enrichment
comet-rs extract https://github.com/owner/repo CODEMETA

# Single property
comet-rs extract_property https://github.com/owner/repo abstract --schema Bioschemas
```

`fairness` CLI currently accepts **maSMP** / **CODEMETA** only.

See also [README_PYPI.md](./README_PYPI.md).

---

## Run tests

From `backend-migration/`:

```bash
pytest
```

Training-related tests include:

- `tests/test_readme_training_parser.py`
- `tests/test_training_file_pipeline.py`
- Composer coverage in `tests/test_layer3_pipeline_contracts.py`

---

## Documentation (MkDocs)

```bash
mkdocs serve
```

Open http://127.0.0.1:8002/ (port **8002** avoids clashing with the API on **8000**).

Layer guides under `docs/` still describe the CoMET-RS layered design; Bioschemas/training details in those pages may lag this README.

---

## Known gaps / keep in mind

- **Bioschemas + GitLab** is not implemented yet (GitHub only for training)
- **FAIR assessment** scoring is still software-oriented; using it with Bioschemas can be misleading
- **Glittr.org** / bulk repo lists are not wired into the pipeline yet
- **Zenodo** extraction is planned, not implemented
- Some training provenance still lives under `provenance/software/`
- Package and CLI naming remain **`comet-rs`**

---

## Related docs

- Root project overview: [../README.md](../README.md)
- PyPI / library usage: [README_PYPI.md](./README_PYPI.md)
- Layer docs: [docs/](./docs/)
