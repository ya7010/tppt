from pathlib import Path

import tppt
from tppt._tppt.slide_layout import DefaultMasterSlide, DefaultTitleSlide


def main():
    class CustomMasterSlide(DefaultMasterSlide):
        pass

    class CustomTitleSlide(DefaultTitleSlide):
        pass

    class CustomSlideMaster(tppt.TpptSlideMaster):
        Master = CustomMasterSlide
        Title = CustomTitleSlide

    presentation = (
        tppt.Presentation.builder(CustomSlideMaster)
        .slide(
            lambda layout: layout.Master(
                title="Custom Master Title",
                text="Custom Master Text",
            )
            .builder()
            .text(
                "a",
                left=(100, "pt"),
                top=(100, "pt"),
                width=(100, "pt"),
                height=(100, "pt"),
            )
        )
        .slide(lambda layout: layout.Title(title="Custom Title"))
        .build()
    )

    presentation.save(Path(__file__).with_suffix(".pptx"))


if __name__ == "__main__":
    main()
