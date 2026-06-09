"""Parse training-material signals from README text for Bioschemas export."""

from __future__ import annotations

import re
from typing import Any

_SECTION_HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
_BULLET = re.compile(r"^[\s>*-]*(?:\d+\.|[-*+])\s+(.+?)\s*$", re.MULTILINE)
_LEVEL = re.compile(r"\b(beginner|intermediate|advanced)\b", re.IGNORECASE)
_RESOURCE_TYPE_HINTS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\btutorial\b", re.I), "tutorial"),
    (re.compile(r"\bworkshop\b", re.I), "workshop"),
    (re.compile(r"\bslides?\b", re.I), "slides"),
    (re.compile(r"\bhandout\b", re.I), "handout"),
    (re.compile(r"\blesson\b", re.I), "lesson"),
    (re.compile(r"\bcourse\b", re.I), "course"),
    (re.compile(r"\bwebinar\b", re.I), "webinar"),
    (re.compile(r"\bnotebook\b", re.I), "notebook"),
    (re.compile(r"\bexercise\b", re.I), "exercise"),
)


def _normalize_heading(heading: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", heading.lower()).strip()


def _section_content(content: str, heading_aliases: tuple[str, ...]) -> str:
    aliases = {_normalize_heading(item) for item in heading_aliases}
    matches = list(_SECTION_HEADING.finditer(content))
    for index, match in enumerate(matches):
        title = _normalize_heading(match.group(1))
        if title not in aliases and not any(alias in title for alias in aliases):
            continue
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        return content[start:end].strip()
    return ""


def _bullet_items(section: str) -> list[str]:
    items = [match.group(1).strip() for match in _BULLET.finditer(section)]
    return [item for item in items if item and len(item) > 2]


def _first_paragraph(content: str) -> str:
    lines: list[str] = []
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped:
            if lines:
                break
            continue
        if stripped.startswith(("#", "!", "[!", "<")):
            continue
        if stripped.startswith("```"):
            break
        lines.append(stripped)
    paragraph = " ".join(lines).strip()
    return paragraph if len(paragraph) >= 40 else ""


def parse_training_readme(content: str) -> dict[str, Any]:
    """Return Bioschemas-oriented fields parsed from README markdown."""
    if not content or not content.strip():
        return {}

    parsed: dict[str, Any] = {}

    abstract_section = _section_content(
        content,
        ("abstract", "summary", "overview"),
    )
    abstract = abstract_section.split("\n\n")[0].strip() if abstract_section else _first_paragraph(content)
    if abstract:
        parsed["abstract"] = abstract[:2000]

    teaches_section = _section_content(
        content,
        (
            "learning outcomes",
            "learning objectives",
            "objectives",
            "you will learn",
            "teaches",
            "goals",
            "what you will learn",
        ),
    )
    teaches = _bullet_items(teaches_section) if teaches_section else []
    if teaches:
        parsed["teaches"] = teaches[:20]

    competency_section = _section_content(
        content,
        (
            "prerequisites",
            "requirements",
            "prior knowledge",
            "before you begin",
            "competency required",
            "what you need",
        ),
    )
    competency = _bullet_items(competency_section) if competency_section else []
    if competency:
        parsed["competencyRequired"] = competency[:15]

    audience_section = _section_content(
        content,
        ("audience", "target audience", "who is this for", "intended audience"),
    )
    if audience_section:
        audience_text = " ".join(audience_section.split()).strip()
        if audience_text:
            parsed["audience"] = {
                "@type": "Audience",
                "audienceType": audience_text[:500],
            }

    level_match = _LEVEL.search(content)
    if level_match:
        parsed["educationalLevel"] = level_match.group(1).capitalize()

    resource_types: list[str] = []
    for pattern, label in _RESOURCE_TYPE_HINTS:
        if pattern.search(content) and label not in resource_types:
            resource_types.append(label)
    if resource_types:
        parsed["learningResourceType"] = resource_types[:5]

    parsed["inLanguage"] = ["en"]

    return parsed
