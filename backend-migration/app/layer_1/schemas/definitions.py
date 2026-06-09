"""Schema output definitions used by schema-driven JSON-LD rendering."""

from dataclasses import dataclass

from app.layer_1.schemas.bioschemas.export_fields import BIOSCHEMAS_TRAINING_MATERIAL_EXPORT_KEYS
from app.layer_1.schemas.codemeta.export_fields import CODEMETA_SOFTWARE_SOURCE_CODE_EXPORT_KEYS
from app.layer_1.schemas.masmp.export_fields import (
    MASMP_SOFTWARE_APPLICATION_EXPORT_KEYS,
    MASMP_SOFTWARE_SOURCE_CODE_EXPORT_KEYS,
)


@dataclass(frozen=True)
class SchemaNodeDefinition:
    key: str
    context: list[object]
    type_value: str
    export_keys: frozenset[str]


@dataclass(frozen=True)
class SchemaDefinition:
    schema_key: str
    nodes: tuple[SchemaNodeDefinition, ...]
    include_has_release: bool = False
    has_release_key: str = "hasRelease"


SCHEMA_DEFINITIONS: dict[str, SchemaDefinition] = {
    "codemeta": SchemaDefinition(
        schema_key="codemeta",
        nodes=(
            SchemaNodeDefinition(
                key="__root__",
                context=["http://schema.org/", {"codemeta": "https://w3id.org/codemeta/3.0"}],
                type_value="SoftwareSourceCode",
                export_keys=CODEMETA_SOFTWARE_SOURCE_CODE_EXPORT_KEYS,
            ),
        ),
    ),
    "masmp": SchemaDefinition(
        schema_key="masmp",
        include_has_release=True,
        nodes=(
            SchemaNodeDefinition(
                key="maSMP:SoftwareSourceCode",
                context=[
                    "http://schema.org/",
                    {"codemeta": "https://w3id.org/codemeta/3.0"},
                    {"maSMP": "https://discovery.biothings.io/ns/maSMPProfiles/"},
                ],
                type_value="maSMP:SoftwareSourceCode",
                export_keys=MASMP_SOFTWARE_SOURCE_CODE_EXPORT_KEYS,
            ),
            SchemaNodeDefinition(
                key="maSMP:SoftwareApplication",
                context=[
                    "http://schema.org/",
                    {"codemeta": "https://w3id.org/codemeta/3.0"},
                    {"maSMP": "https://discovery.biothings.io/ns/maSMPProfiles/"},
                ],
                type_value="maSMP:SoftwareApplication",
                export_keys=MASMP_SOFTWARE_APPLICATION_EXPORT_KEYS,
            ),
        ),
    ),
    "bioschemas": SchemaDefinition(
        schema_key="bioschemas",
        nodes=(
            SchemaNodeDefinition(
                key="__root__",
                context=[
                    "https://schema.org/",
                    {"dct": "http://purl.org/dc/terms/"},
                ],
                type_value="LearningResource",
                export_keys=BIOSCHEMAS_TRAINING_MATERIAL_EXPORT_KEYS,
            ),
        ),
    ),
}

SCHEMA_DEFINITIONS["trainingmaterial"] = SCHEMA_DEFINITIONS["bioschemas"]


def normalize_schema_key(schema: str) -> str:
    normalized = schema.strip().lower().replace("_", "").replace("-", "")
    if normalized == "trainingmaterial":
        return "bioschemas"
    return normalized


def get_schema_definition(schema: str) -> SchemaDefinition:
    normalized = normalize_schema_key(schema)
    if normalized not in SCHEMA_DEFINITIONS:
        raise ValueError(f"Unsupported schema: {schema!r}")
    return SCHEMA_DEFINITIONS[normalized]
