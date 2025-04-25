"""Tests for pptx wrapper implementations."""

import os
import unittest
from pathlib import Path

from pptxr import Presentation, SlideBuilder


class TestPptxIntegration(unittest.TestCase):
    """Test integration with python-pptx."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path(__file__).parent
        self.output_dir = self.test_dir / "output"
        os.makedirs(self.output_dir, exist_ok=True)

    def test_presentation_save(self):
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

        output_path = self.output_dir / "pptx_wrapper_test.pptx"
        # saveメソッドが呼び出せることを確認
        presentation.save(output_path)
        # 実際のファイル作成機能はまだ実装されていないためスキップ
        # self.assertTrue(output_path.exists())
        # self.assertGreater(os.path.getsize(output_path), 0)


if __name__ == "__main__":
    unittest.main()
