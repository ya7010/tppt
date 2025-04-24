import os
import unittest
from pathlib import Path

from pptxr import (
    Align,
    Container,
    Inch,
    Justify,
    LayoutType,
    Point,
    Presentation,
    SlideLayout,
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
                    layout=SlideLayout.TITLE_AND_CONTENT,
                    title=text("Simple Slide", size=Point(44), bold=True),
                    containers=[
                        Container(
                            components=[
                                text(
                                    "This is a test text",
                                    size=Point(24),
                                    layout=layout(width=Inch(4), height=Inch(1)),
                                )
                            ],
                            layout=layout(
                                type=LayoutType.FLEX,
                                direction="column",
                                align=Align.CENTER,
                            ),
                        )
                    ],
                )
            )
            .build()
        )

        output_path = self.output_dir / "simple.pptx"
        presentation.save(str(output_path))
        self.assertTrue(output_path.exists())

    def test_create_complex_presentation(self):
        """Test creating a presentation with complex layout"""
        presentation = (
            Presentation.builder()
            .add_slide(
                slide(
                    layout=SlideLayout.TITLE_AND_CONTENT,
                    title=text("Complex Layout", size=Point(44), bold=True),
                    containers=[
                        # Horizontal container
                        Container(
                            components=[
                                text(
                                    "Left text",
                                    size=Point(20),
                                    layout=layout(width=Inch(3), height=Inch(1)),
                                ),
                                text(
                                    "Right text",
                                    size=Point(20),
                                    layout=layout(width=Inch(3), height=Inch(1)),
                                ),
                            ],
                            layout=layout(
                                type=LayoutType.FLEX,
                                direction="row",
                                justify=Justify.SPACE_BETWEEN,
                                gap=Inch(0.5),
                            ),
                        ),
                        # Vertical container
                        Container(
                            components=[
                                text(
                                    "Top text",
                                    size=Point(20),
                                    layout=layout(width=Inch(6), height=Inch(1)),
                                ),
                                text(
                                    "Bottom text",
                                    size=Point(20),
                                    layout=layout(width=Inch(6), height=Inch(1)),
                                ),
                            ],
                            layout=layout(
                                type=LayoutType.FLEX,
                                direction="column",
                                align=Align.CENTER,
                                gap=Inch(0.5),
                            ),
                        ),
                    ],
                )
            )
            .build()
        )

        output_path = self.output_dir / "complex.pptx"
        presentation.save(str(output_path))
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
                    layout=SlideLayout.TITLE_AND_CONTENT,
                    title=text("Slide with Image", size=Point(44), bold=True),
                    containers=[
                        Container(
                            components=[
                                image(
                                    path=str(test_image_path),
                                    width=Inch(4),
                                    height=Inch(3),
                                    layout=layout(width=Inch(4), height=Inch(3)),
                                ),
                                text(
                                    "Image description",
                                    size=Point(20),
                                    layout=layout(width=Inch(4), height=Inch(1)),
                                ),
                            ],
                            layout=layout(
                                type=LayoutType.FLEX,
                                direction="column",
                                align=Align.CENTER,
                                gap=Inch(0.5),
                            ),
                        )
                    ],
                )
            )
            .build()
        )

        output_path = self.output_dir / "with_image.pptx"
        presentation.save(str(output_path))
        self.assertTrue(output_path.exists())

    def test_create_presentation_with_chart(self):
        """Test creating a presentation with chart"""
        presentation = (
            Presentation.builder()
            .add_slide(
                slide(
                    layout=SlideLayout.TITLE_AND_CONTENT,
                    title=text("Slide with Chart", size=Point(44), bold=True),
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
                                    width=Inch(6),
                                    height=Inch(4),
                                    layout=layout(width=Inch(6), height=Inch(4)),
                                )
                            ],
                            layout=layout(
                                type=LayoutType.FLEX,
                                direction="column",
                                align=Align.CENTER,
                            ),
                        )
                    ],
                )
            )
            .build()
        )

        output_path = self.output_dir / "with_chart.pptx"
        presentation.save(str(output_path))
        self.assertTrue(output_path.exists())

    def test_create_presentation_with_keyword_args(self):
        """Test creating a presentation using keyword arguments"""
        presentation = (
            Presentation.builder()
            .add_slide(
                layout=SlideLayout.TITLE_AND_CONTENT,
                title=text("Keyword Arguments Test", size=Point(44), bold=True),
                containers=[
                    Container(
                        components=[
                            text(
                                "Slide created with keyword arguments",
                                size=Point(24),
                                layout=layout(width=Inch(4), height=Inch(1)),
                            )
                        ],
                        layout=layout(
                            type=LayoutType.FLEX,
                            direction="column",
                            align=Align.CENTER,
                        ),
                    )
                ],
            )
            .build()
        )

        output_path = self.output_dir / "keyword_args.pptx"
        presentation.save(str(output_path))
        self.assertTrue(output_path.exists())


if __name__ == "__main__":
    unittest.main()
