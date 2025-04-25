"""Tests for presentation module."""

import pathlib
import subprocess
import sys

import pytest

import pptxr
from pptxr.types import TableCellStyle


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


def test_create_presentation_with_table(output: pathlib.Path) -> None:
    """Test creating a presentation with a table."""
    table_data = [
        ["Header 1", "Header 2", "Header 3"],
        ["Cell 1,1", "Cell 1,2", "Cell 1,3"],
        ["Cell 2,1", "Cell 2,2", "Cell 2,3"],
    ]

    presentation = (
        pptxr.Presentation.builder()
        .slide(
            pptxr.SlideBuilder().table(
                table_data,
                left=(100, "pt"),
                top=(100, "pt"),
                width=(400, "pt"),
                height=(200, "pt"),
            )
        )
        .build()
    )
    presentation.save(output / "table_only.pptx")


def test_create_presentation_with_styled_table(output: pathlib.Path) -> None:
    """Test creating a presentation with a styled table."""
    data = [
        ["Header 1", "Header 2", "Header 3"],
        ["Cell 1,1", "Cell 1,2", "Cell 1,3"],
        ["Cell 2,1", "Cell 2,2", "Cell 2,3"],
    ]

    cell_styles: list[list[TableCellStyle]] = [
        [
            {"bold": True, "font_size": 14, "text_align": "center"},
            {"bold": True, "font_size": 14, "text_align": "center"},
            {"bold": True, "font_size": 14, "text_align": "center"},
        ],
        [
            {"text_align": "left", "vertical_align": "middle"},
            {"text_align": "center", "vertical_align": "middle", "italic": True},
            {"text_align": "right", "vertical_align": "middle"},
        ],
        [
            {"text_align": "left", "vertical_align": "bottom"},
            {"text_align": "center", "vertical_align": "bottom"},
            {"text_align": "right", "vertical_align": "bottom", "font_name": "Arial"},
        ],
    ]

    presentation = (
        pptxr.Presentation.builder()
        .slide(
            pptxr.SlideBuilder().table(
                data,
                left=(100, "pt"),
                top=(100, "pt"),
                width=(400, "pt"),
                height=(200, "pt"),
                cell_styles=cell_styles,
                first_row_header=True,
            )
        )
        .build()
    )
    presentation.save(output / "styled_table.pptx")


@pytest.mark.parametrize(
    "example_file",
    [f for f in pathlib.Path(__file__).parent.parent.joinpath("examples").glob("*.py")],
)
def test_example_files(example_file: pathlib.Path) -> None:
    """Test that example Python files run without errors.

    Args:
        example_file: Path to the example Python file.
    """
    # Run the example script as a subprocess
    result = subprocess.run(
        [sys.executable, str(example_file)],
        capture_output=True,
        text=True,
        check=False,
    )

    # Check that the script ran successfully
    assert result.returncode == 0, (
        f"Example {example_file.name} failed with error: {result.stderr}"
    )

    # Also check that the output PPTX file was created
    expected_pptx = example_file.with_suffix(".pptx")
    assert expected_pptx.exists(), (
        f"Expected output file {expected_pptx} was not created"
    )
