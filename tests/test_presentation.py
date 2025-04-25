"""Tests for presentation module."""

import pathlib

import pptxr


def test_create_presentation(output: pathlib.Path) -> None:
    """Test creating a presentation."""
    presentation = (
        pptxr.Presentation.builder().slide(pptxr.SlideBuilder().text("text")).build()
    )
    presentation.save(output / "text_only.pptx")
