"""File parsing steps for training-material / Bioschemas extraction."""

from app.layer_3.steps.contracts import ExtractionStep
from app.layer_3.steps.extract_steps.services.files.citation import (
    ExtractCitationAbstractStep,
    ExtractCitationAuthorsStep,
    ExtractCitationDoiStep,
    ExtractCitationKeywordsStep,
)
from app.layer_3.steps.extract_steps.services.files.readme import (
    ExtractReadmeBibtexStep,
    ExtractReadmeIdentifierStep,
)
from app.layer_3.steps.extract_steps.services.files.training import ExtractTrainingReadmeFieldsStep
from app.layer_3.steps.merge_steps.software import (
    MergeSoftwareAuthorsStep,
    MergeSoftwareIdentifiersStep,
    MergeSoftwareKeywordsStep,
)
from app.layer_3.steps.merge_steps.training import MergeTrainingReadmeFieldsStep


def training_file_steps() -> tuple[ExtractionStep, ...]:
    return (
        ExtractCitationDoiStep(),
        ExtractCitationAuthorsStep(),
        ExtractCitationKeywordsStep(),
        ExtractCitationAbstractStep(),
        ExtractReadmeIdentifierStep(),
        ExtractReadmeBibtexStep(),
        ExtractTrainingReadmeFieldsStep(),
        MergeSoftwareIdentifiersStep(),
        MergeSoftwareAuthorsStep(),
        MergeSoftwareKeywordsStep(),
        MergeTrainingReadmeFieldsStep(),
    )


__all__ = ["training_file_steps"]
