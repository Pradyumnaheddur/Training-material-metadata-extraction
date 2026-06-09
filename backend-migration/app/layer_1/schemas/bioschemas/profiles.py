"""
Bioschemas TrainingMaterial 1.0-RELEASE property categories (UI + enrichment).
"""
from typing import Dict, List

BIOSCHEMAS_TRAINING_MATERIAL: Dict[str, List[str]] = {
    "minimum": [
        "description",
        "keywords",
        "name",
    ],
    "recommended": [
        "about",
        "abstract",
        "audience",
        "author",
        "competencyRequired",
        "educationalLevel",
        "identifier",
        "inLanguage",
        "learningResourceType",
        "license",
        "mentions",
        "teaches",
        "timeRequired",
        "url",
    ],
    "optional": [
        "accessibilitySummary",
        "contributor",
        "creativeWorkStatus",
        "dateCreated",
        "dateModified",
        "datePublished",
        "hasPart",
        "isPartOf",
        "recordedAt",
        "version",
        "workTranslation",
    ],
}


def get_category_for_key(prop_key: str) -> str:
    """Return 'minimum', 'recommended', or 'optional' for a TrainingMaterial property."""
    if prop_key in BIOSCHEMAS_TRAINING_MATERIAL.get("minimum", []):
        return "minimum"
    if prop_key in BIOSCHEMAS_TRAINING_MATERIAL.get("recommended", []):
        return "recommended"
    return "optional"
