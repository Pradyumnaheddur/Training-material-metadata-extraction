"""
Allowed JSON-LD keys for Bioschemas TrainingMaterial 1.0-RELEASE export.

Profile: https://bioschemas.org/profiles/TrainingMaterial/1.0-RELEASE
"""
from typing import FrozenSet

BIOSCHEMAS_TRAINING_MATERIAL_PROFILE_URL = (
    "https://bioschemas.org/profiles/TrainingMaterial/1.0-RELEASE"
)

BIOSCHEMAS_TRAINING_MATERIAL_EXPORT_KEYS: FrozenSet[str] = frozenset({
    # Minimum
    "dct:conformsTo",
    "description",
    "keywords",
    "name",
    # Recommended
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
    # Optional
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
})
