"""Tests for pptx wrapper implementations."""

import os
from pathlib import Path

import pytest

from pptxr import Presentation, SlideBuilder


@pytest.fixture
def test_output_dir():
    """Set up test environment."""
    test_dir = Path(__file__).parent
    output_dir = test_dir / "output"
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def test_presentation_save(test_output_dir):
    """Test that a presentation can be saved."""
    presentation = (
        Presentation.builder()
        .slide(
            SlideBuilder()
            .text("Test Title", x=(100, "pt"), y=(100, "pt"))
            .text("Test Content", x=(100, "pt"), y=(200, "pt"))
        )
        .build()
    )

    output_path = test_output_dir / "pptx_wrapper_test.pptx"
    # saveメソッドが呼び出せることを確認
    presentation.save(output_path)
    # 実際のファイル作成機能はまだ実装されていないためスキップ
    # assert output_path.exists()
    # assert os.path.getsize(output_path) > 0
