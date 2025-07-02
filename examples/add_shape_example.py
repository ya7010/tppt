"""Example of adding shapes with background and text."""

from pathlib import Path

from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.util import Inches

import tppt


def main():
    """Create a PowerPoint with box shapes that have background color and text."""
    tppt.Presentation.builder().slide(
        lambda slide: slide.BlankLayout()
        .builder()
        .add_shape(
            MSO_AUTO_SHAPE_TYPE.RECTANGLE,
            lambda shape: (
                shape.fill.solid().fore_color.set_rgb("#0066ff"),
                shape.set_text("Sample Box with Text"),
            )[-1],
            left=Inches(1),
            top=Inches(1),
            width=Inches(4),
            height=Inches(2),
        )
        .add_shape(
            MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE,
            lambda shape: (
                shape.fill.solid().fore_color.set_rgb("#ff6600"),
                shape.set_text("Rounded Box"),
            )[-1],
            left=Inches(6),
            top=Inches(1),
            width=Inches(3),
            height=Inches(1.5),
        )
        .add_shape(
            MSO_AUTO_SHAPE_TYPE.OVAL,
            lambda shape: (
                shape.fill.solid().fore_color.set_rgb("#00ff00"),
                shape.set_text("Circle"),
            )[-1],
            left=Inches(1),
            top=Inches(4),
            width=Inches(2),
            height=Inches(2),
        )
    ).save(Path(__file__).with_suffix(".pptx"))


if __name__ == "__main__":
    main()
