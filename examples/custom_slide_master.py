from pathlib import Path

import tppt


def main():
    class CustomMasterSlideLayout(tppt.SlideLayout):
        title: tppt.Placeholder[str]
        text: tppt.Placeholder[str]

    class CustomTitleSlideLayout(tppt.SlideLayout):
        title: tppt.Placeholder[str]
        subtitle: tppt.Placeholder[str | None] = None

    class CustomSlideMaster(tppt.SlideMaster):
        MasterLayout = tppt.Layout[CustomMasterSlideLayout]
        TitleLayout = tppt.Layout[CustomTitleSlideLayout]

    presentation = (
        tppt.Presentation.builder(CustomSlideMaster)
        .slide(
            lambda slide: slide.MasterLayout(
                title="Custom Master Title",
                text="Custom Master Text",
            )
            .builder()
            .text(
                "sample text",
                left=(100, "pt"),
                top=(100, "pt"),
                width=(100, "pt"),
                height=(100, "pt"),
            )
        )
        .slide(lambda slide: slide.TitleLayout(title="Custom Title"))
        .build()
    )

    presentation.save(Path(__file__).with_suffix(".pptx"))


if __name__ == "__main__":
    main()
