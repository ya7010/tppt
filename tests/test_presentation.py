"""Tests for presentation module."""

import pathlib

import pptxr


def test_create_presentation(output: pathlib.Path) -> None:
    """Test creating a presentation."""
    presentation = (
        pptxr.Presentation.builder()
        .slide(
            pptxr.SlideBuilder().text(
                "text",
                left=(100, "pt"),
                top=(100, "pt"),
                width=(100, "pt"),
                height=(100, "pt"),
            )
        )
        .build()
    )
    presentation.save(output / "text_only.pptx")
