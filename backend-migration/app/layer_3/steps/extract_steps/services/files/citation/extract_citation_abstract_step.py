"""Extract abstract from CITATION.cff into step state."""

from app.layer_3.steps.contracts import StepContext, StepState
from app.layer_3.steps.contracts.step import ExtractionStep
from app.layer_3.steps.extract_steps.services.files.citation.helpers import ensure_cff_yaml_loaded


class ExtractCitationAbstractStep(ExtractionStep):
    name = "citation.extract_abstract"

    def run(self, context: StepContext, state: StepState) -> StepState:
        ensure_cff_yaml_loaded(context, state)
        if not state.data.get("valid"):
            return state
        abstract = state.data["cff_data"].get("abstract")
        if abstract:
            state.data["extracted_citation_abstract"] = str(abstract).strip()
        return state


__all__ = ["ExtractCitationAbstractStep"]
