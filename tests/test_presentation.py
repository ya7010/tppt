import os
import unittest
from pathlib import Path

from pptxr import (
    Container,
    Presentation,
    chart,
    image,
    layout,
    slide,
    text,
)


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
            .add_slide(
                slide(
                    layout="TITLE_AND_CONTENT",
                    title=text("Simple Slide", size=(44, "pt"), bold=True),
                    containers=[
                        Container(
                            components=[
                                text(
                                    "This is a test text",
                                    size=(24, "pt"),
                                    layout=layout(width=(4, "in"), height=(1, "in")),
                                )
                            ],
                            layout=layout(
                                type="flex",
                                direction="column",
                                align="center",
                            ),
                        )
                    ],
                )
            )
            .build()
        )

        output_path = self.output_dir / "simple.pptx"
        presentation.save(output_path)
        self.assertTrue(output_path.exists())

    def test_create_complex_presentation(self):
        """Test creating a presentation with complex layout"""
        presentation = (
            Presentation.builder()
            .add_slide(
                slide(
                    layout="TITLE_AND_CONTENT",
                    title=text("Complex Layout", size=(44, "pt"), bold=True),
                    containers=[
                        # Horizontal container
                        Container(
                            components=[
                                text(
                                    "Left text",
                                    size=(20, "pt"),
                                    layout=layout(width=(3, "in"), height=(1, "in")),
                                ),
                                text(
                                    "Right text",
                                    size=(20, "pt"),
                                    layout=layout(width=(3, "in"), height=(1, "in")),
                                ),
                            ],
                            layout=layout(
                                type="flex",
                                direction="row",
                                justify="space-between",
                                gap=(0.5, "in"),
                            ),
                        ),
                        # Vertical container
                        Container(
                            components=[
                                text(
                                    "Top text",
                                    size=(20, "pt"),
                                    layout=layout(width=(6, "in"), height=(1, "in")),
                                ),
                                text(
                                    "Bottom text",
                                    size=(20, "pt"),
                                    layout=layout(width=(6, "in"), height=(1, "in")),
                                ),
                            ],
                            layout=layout(
                                type="flex",
                                direction="column",
                                align="center",
                                gap=(0.5, "in"),
                            ),
                        ),
                    ],
                )
            )
            .build()
        )

        output_path = self.output_dir / "complex.pptx"
        presentation.save(output_path)
        self.assertTrue(output_path.exists())

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
            .add_slide(
                slide(
                    layout="TITLE_AND_CONTENT",
                    title=text("Slide with Image", size=(44, "pt"), bold=True),
                    containers=[
                        Container(
                            components=[
                                image(
                                    path=str(test_image_path),
                                    width=(4, "in"),
                                    height=(3, "in"),
                                    layout=layout(width=(4, "in"), height=(3, "in")),
                                ),
                                text(
                                    "Image description",
                                    size=(20, "pt"),
                                    layout=layout(width=(4, "in"), height=(1, "in")),
                                ),
                            ],
                            layout=layout(
                                type="flex",
                                direction="column",
                                align="center",
                                gap=(0.5, "in"),
                            ),
                        )
                    ],
                )
            )
            .build()
        )

        output_path = self.output_dir / "with_image.pptx"
        presentation.save(output_path)
        self.assertTrue(output_path.exists())

    def test_create_presentation_with_chart(self):
        """Test creating a presentation with chart"""
        presentation = (
            Presentation.builder()
            .add_slide(
                slide(
                    layout="TITLE_AND_CONTENT",
                    title=text("Slide with Chart", size=(44, "pt"), bold=True),
                    containers=[
                        Container(
                            components=[
                                chart(
                                    chart_type="bar",
                                    data=[
                                        {"category": "A", "value": 10},
                                        {"category": "B", "value": 20},
                                        {"category": "C", "value": 30},
                                    ],
                                    width=(6, "in"),
                                    height=(4, "in"),
                                    layout=layout(width=(6, "in"), height=(4, "in")),
                                )
                            ],
                            layout=layout(
                                type="flex",
                                direction="column",
                                align="center",
                            ),
                        )
                    ],
                )
            )
            .build()
        )

        output_path = self.output_dir / "with_chart.pptx"
        presentation.save(output_path)
        self.assertTrue(output_path.exists())

    def test_create_presentation_with_keyword_args(self):
        """Test creating a presentation using keyword arguments"""
        presentation = (
            Presentation.builder()
            .add_slide(
                layout="TITLE_AND_CONTENT",
                title=text("Keyword Arguments Test", size=(44, "pt"), bold=True),
                containers=[
                    Container(
                        components=[
                            text(
                                "Slide created with keyword arguments",
                                size=(24, "pt"),
                                layout=layout(width=(4, "in"), height=(1, "in")),
                            )
                        ],
                        layout=layout(
                            type="flex",
                            direction="column",
                            align="center",
                        ),
                    )
                ],
            )
            .build()
        )

        output_path = self.output_dir / "keyword_args.pptx"
        presentation.save(output_path)
        self.assertTrue(output_path.exists())


if __name__ == "__main__":
    unittest.main()
