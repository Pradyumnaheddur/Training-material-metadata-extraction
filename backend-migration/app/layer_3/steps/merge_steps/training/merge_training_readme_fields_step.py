"""Merge README/CFF training fields into metadata for Bioschemas export."""

from typing import Any

from app.layer_1.provenance.software.defaults import (
    CONFIDENCE_CITATION,
    CONFIDENCE_README,
    SOURCE_CITATION_CFF,
    SOURCE_README_PARSER,
)
from app.layer_3.extraction_metadata.record import record_field_provenance
from app.layer_3.steps.contracts import StepContext, StepState
from app.layer_3.steps.contracts.step import ExtractionStep


class MergeTrainingReadmeFieldsStep(ExtractionStep):
    name = "training.merge_readme_fields"

    def run(self, context: StepContext, state: StepState) -> StepState:
        readme_fields: dict[str, Any] = state.data.get("extracted_training_readme_fields") or {}
        citation_abstract = state.data.get("extracted_citation_abstract")

        if citation_abstract:
            state.metadata.abstract = citation_abstract
            record_field_provenance(state, "abstract", SOURCE_CITATION_CFF, CONFIDENCE_CITATION)
        elif readme_fields.get("abstract"):
            state.metadata.abstract = readme_fields["abstract"]
            record_field_provenance(state, "abstract", SOURCE_README_PARSER, CONFIDENCE_README)

        for field in (
            "teaches",
            "learningResourceType",
            "educationalLevel",
            "competencyRequired",
            "inLanguage",
            "audience",
        ):
            value = readme_fields.get(field)
            if value is not None and getattr(state.metadata, field, None) in (None, [], ""):
                setattr(state.metadata, field, value)
                record_field_provenance(state, field, SOURCE_README_PARSER, CONFIDENCE_README)

        return state


__all__ = ["MergeTrainingReadmeFieldsStep"]
