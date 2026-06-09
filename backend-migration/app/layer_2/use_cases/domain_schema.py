"""Map API schema names to extraction domain and normalized schema keys."""

from app.layer_1.schemas.definitions import normalize_schema_key


def resolve_extraction_context(schema: str) -> tuple[str, str]:
    """
    Return (domain, normalized_schema_key) for pipeline composition and export.

    Bioschemas / TrainingMaterial requests use the training domain; maSMP and
    CodeMeta use the software domain.
    """
    normalized = normalize_schema_key(schema)
    if normalized == "bioschemas":
        return "training", "bioschemas"
    return "software", normalized
