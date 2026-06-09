"""Training material + GitHub + Bioschemas pipeline profile."""

from app.layer_3.steps.contracts.pipeline import ExtractionPipeline
from app.layer_3.steps.extract_steps.adapters.platform.common import common_platform_steps
from app.layer_3.steps.extract_steps.adapters.platform.github.extract_github_contributors_step import (
    github_contributor_steps,
)
from app.layer_3.steps.extract_steps.adapters.platform.github.extract_github_dates_step import (
    github_date_steps,
)
from app.layer_3.steps.extract_steps.adapters.platform.github.extract_github_keywords_step import (
    github_keyword_steps,
)
from app.layer_3.steps.extract_steps.adapters.platform.github.extract_github_license_step import (
    github_license_steps,
)
from app.layer_3.steps.extract_steps.adapters.platform.github.extract_github_repository_property_steps import (
    github_basic_info_steps,
)
from app.layer_3.steps.step_bundles.training_file_steps import training_file_steps


def build_training_github_bioschemas_pipeline() -> ExtractionPipeline:
    return ExtractionPipeline(
        steps=(
            common_platform_steps()
            + github_basic_info_steps()
            + github_date_steps()
            + github_contributor_steps()
            + github_keyword_steps()
            + github_license_steps()
            + training_file_steps()
        )
    )
