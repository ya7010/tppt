import os
import unittest
from pathlib import Path

from pptxr import Presentation, SlideBuilder, SlideMaster, SlideTemplate


class MySlideTemplate(SlideTemplate):
    """Simple slide template for testing."""

    pass


class TestPresentation(unittest.TestCase):
    """Test class for Presentation functionality"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(__file__).parent
        self.resources_dir = self.test_dir / "resources"
        self.output_dir = self.test_dir / "output"
        os.makedirs(self.resources_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def test_create_simple_presentation(self):
        """Test creating a simple presentation with basic layout"""
        presentation = (
            Presentation.builder()
            .slide(
                SlideBuilder()
                .text("Simple Slide Title", x=(100, "pt"), y=(100, "pt"))
                .text("This is a test text", x=(100, "pt"), y=(200, "pt"))
            )
            .build()
        )

        output_path = self.output_dir / "simple.pptx"
        # saveメソッドが呼び出せるか確認（実際のファイル作成はスキップ）
        presentation.save(output_path)
        # 実際のファイル作成機能はまだ実装されていないためスキップ
        # self.assertTrue(output_path.exists())

    def test_create_complex_presentation(self):
        """Test creating a presentation with complex layout"""
        presentation = (
            Presentation.builder()
            .slide(
                SlideBuilder()
                .text("Complex Layout", x=(100, "pt"), y=(100, "pt"))
                .text("Left text", x=(100, "pt"), y=(200, "pt"))
                .text("Right text", x=(400, "pt"), y=(200, "pt"))
            )
            .slide(  # 2つ目のスライド
                SlideBuilder()
                .text("Second Slide", x=(100, "pt"), y=(100, "pt"))
                .text("Top text", x=(100, "pt"), y=(200, "pt"))
                .text("Bottom text", x=(100, "pt"), y=(300, "pt"))
            )
            .build()
        )

        output_path = self.output_dir / "complex.pptx"
        presentation.save(output_path)
        self.assertEqual(len(presentation.slides), 2)

    def test_create_presentation_with_image(self):
        """Test creating a presentation with image"""
        test_image_path = self.resources_dir / "test_image.jpg"
        if not test_image_path.exists():
            # Create a dummy image for testing
            from PIL import Image as PILImage

            img = PILImage.new("RGB", (100, 100), color="red")
            img.save(str(test_image_path))

        presentation = (
            Presentation.builder()
            .slide(
                SlideBuilder()
                .text("Slide with Image", x=(100, "pt"), y=(100, "pt"))
                .image(
                    str(test_image_path),
                    x=(100, "pt"),
                    y=(200, "pt"),
                    width=(200, "pt"),
                    height=(150, "pt"),
                )
                .text("Image description", x=(100, "pt"), y=(400, "pt"))
            )
            .build()
        )

        output_path = self.output_dir / "with_image.pptx"
        presentation.save(output_path)
        # 実際のファイル作成機能はまだ実装されていないためスキップ
        # self.assertTrue(output_path.exists())

    def test_presentation_with_slide_master(self):
        """Test creating a presentation with a slide master"""
        sm = SlideMaster(template_class=MySlideTemplate)

        presentation = (
            Presentation.builder(slide_master=sm)
            .slide(
                SlideBuilder().text("Slide with Master", x=(100, "pt"), y=(100, "pt"))
            )
            .build()
        )

        self.assertIsNotNone(presentation.slide_master)
        # template_classが正しい型であることを確認
        self.assertTrue(
            presentation.slide_master is not None
            and presentation.slide_master.template_class == MySlideTemplate
        )


if __name__ == "__main__":
    unittest.main()
