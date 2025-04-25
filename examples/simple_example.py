"""Simple example of using pptxr."""

from pptxr import Presentation, SlideBuilder


def main():
    """Run the example."""
    # Create a slide master

    # Create a presentation using the builder pattern
    presentation = (
        Presentation.builder()
        .slide(
            SlideBuilder().text(
                "Hello, world!",
                left=(100, "pt"),
                top=(100, "pt"),
                width=(100, "pt"),
                height=(100, "pt"),
            )
        )
        .build()
    )

    # Save the presentation
    presentation.save("examples/output.pptx")

    print("Presentation created successfully!")


if __name__ == "__main__":
    main()
