"""Extract Bioschemas-oriented training fields from README into step state."""

from app.layer_3.steps.contracts import StepContext, StepState
from app.layer_3.steps.contracts.step import ExtractionStep
from app.layer_3.steps.extract_steps.services.files.helpers.repository_files import (
    repository_file_content,
)
from app.layer_3.steps.extract_steps.services.files.training.helpers.readme_training_parser import (
    parse_training_readme,
)


class ExtractTrainingReadmeFieldsStep(ExtractionStep):
    name = "training.readme.extract_fields"

    def run(self, context: StepContext, state: StepState) -> StepState:
        content = repository_file_content(
            context,
            state,
            "readme_content",
            ("README.md", "README.rst", "README.txt", "README"),
        )
        state.data["extracted_training_readme_fields"] = parse_training_readme(content)
        return state


__all__ = ["ExtractTrainingReadmeFieldsStep"]
