"""Integration tests for training file parsing steps."""

from app.layer_1.entities.software_metadata import SoftwareMetadata
from app.layer_3.steps.contracts import StepContext, StepState
from app.layer_3.steps.extract_steps.services.files.training.extract_training_readme_fields_step import (
    ExtractTrainingReadmeFieldsStep,
)
from app.layer_3.steps.merge_steps.training.merge_training_readme_fields_step import (
    MergeTrainingReadmeFieldsStep,
)


def test_training_readme_fields_merge_into_metadata(monkeypatch):
    readme = """
## Learning outcomes
- Recall shell commands
- Write scripts to copy files

## Prerequisites
- Basic Linux usage
"""
    monkeypatch.setattr(
        "app.layer_3.steps.extract_steps.services.files.training.extract_training_readme_fields_step.repository_file_content",
        lambda *args, **kwargs: readme,
    )

    context = StepContext(
        repo_url="https://github.com/example/training",
        domain="training",
        schema="bioschemas",
        platform="github",
    )
    state = StepState(metadata=SoftwareMetadata(), data={"record_field": lambda *a, **k: None})

    state = ExtractTrainingReadmeFieldsStep().run(context, state)
    state = MergeTrainingReadmeFieldsStep().run(context, state)

    assert state.metadata.teaches == ["Recall shell commands", "Write scripts to copy files"]
    assert state.metadata.competencyRequired == ["Basic Linux usage"]
