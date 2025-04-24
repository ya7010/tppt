"""Simple example of using pptxr."""

from pptxr import Presentation, SlideBuilder, SlideMaster, SlideTemplate


class MySlideTemplate(SlideTemplate):
    """Custom slide template."""

    pass


class MyTitleSlide(MySlideTemplate):
    """Custom title slide."""

    pass


def main():
    """Run the example."""
    # Create a slide master
    sm = SlideMaster(template_class=MySlideTemplate)

    # Create a presentation using the builder pattern
    presentation = (
        Presentation.builder(sm)
        .slide(
            SlideBuilder()
            .text("Hello, world!", x=(100, "pt"), y=(100, "pt"))
            .image(path="examples/example.png", width=(100, "pt"), height=(100, "pt"))
        )
        .build()
    )

    # Save the presentation
    presentation.save("examples/output.pptx")

    print("Presentation created successfully!")


if __name__ == "__main__":
    main()
