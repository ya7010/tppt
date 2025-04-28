"""Simple example of using tppt."""

from pathlib import Path

import tppt
import tppt.pptx.shape.text

EXAMPLE_DIR = Path(__file__).parent


def main():
    def colorize(text: tppt.pptx.shape.text.Text) -> tppt.pptx.shape.text.Text:
        run = text.text_frame().add_paragraph().add_run()
        run.text = "Hello, world!"
        font = run.font
        font.color.rgb = "#0000FF"
        font.italic = True

        return text

    """Run the example."""
    # Create a presentation using the builder pattern
    presentation = (
        tppt.Presentation.builder()
        .slide(
            lambda slide: slide.BlankLayout()
            .builder()
            .text(
                # Pattern custom function
                colorize,
                left=(50, "pt"),
                top=(50, "pt"),
                width=(400, "pt"),
                height=(50, "pt"),
            )
            .text(
                # Builder pattern.
                lambda text: text.builder().text_frame(
                    lambda text_frame: text_frame.builder().paragraph(
                        lambda paragraph: paragraph.builder().run(
                            lambda run: run.builder()
                            .text("Hello, world!")
                            .font(
                                lambda font: font.builder()
                                .color(lambda color: color.builder().rgb("#00FF00"))
                                .italic(True)
                            )
                        )
                    ),
                ),
                left=(50, "pt"),
                top=(200, "pt"),
                width=(400, "pt"),
                height=(50, "pt"),
            )
        )
        .build()
    )

    # Save the presentation
    presentation.save(Path(__file__).with_suffix(".pptx"))

    print("Rich Text presentation created successfully!")


if __name__ == "__main__":
    main()
