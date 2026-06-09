"""Tests for training README parsing (Bioschemas-oriented fields)."""

from app.layer_3.steps.extract_steps.services.files.training.helpers.readme_training_parser import (
    parse_training_readme,
)


def test_parse_training_readme_extracts_sections_and_level():
    content = """
# Galaxy Training Tutorial

**Level:** Beginner

## Abstract
Short summary of this hands-on tutorial for new users.

## Learning outcomes
- The learner can upload data to Galaxy
- The learner can run a basic workflow

## Prerequisites
- Basic command line skills
- A web browser

## Audience
PhD students and early-career bioinformaticians
"""

    parsed = parse_training_readme(content)

    assert parsed["abstract"].startswith("Short summary")
    assert parsed["educationalLevel"] == "Beginner"
    assert len(parsed["teaches"]) == 2
    assert "Basic command line skills" in parsed["competencyRequired"]
    assert parsed["audience"]["audienceType"].startswith("PhD students")
    assert "tutorial" in parsed["learningResourceType"]


def test_parse_training_readme_returns_empty_for_blank_content():
    assert parse_training_readme("") == {}
    assert parse_training_readme("   ") == {}
