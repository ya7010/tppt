from typing_extensions import TypeVar, dataclass_transform

from tppt.exception import (
    SlideMasterAttributeMustBeSlideLayoutError,
    SlideMasterAttributeNotFoundError,
)

from .slide_layout import (
    DefaultBlankSlide,
    DefaultComparisonSlide,
    DefaultContentWithCaptionSlide,
    DefaultMasterSlide,
    DefaultPictureWithCaptionSlide,
    DefaultSectionHeaderSlide,
    DefaultTitleAndContentSlide,
    DefaultTitleAndVerticalTextSlide,
    DefaultTitleOnlySlide,
    DefaultTitleSlide,
    DefaultTwoContentSlide,
    DefaultVerticalTitleAndTextSlide,
    TpptSlideLayout,
)


class TpptSlideMasterMeta(type):
    def __getattr__(self, key: str) -> "type[TpptSlideLayout]":
        if key in self.__annotations__:
            annotation = self.__annotations__[key]
            if issubclass(annotation, TpptSlideLayout):
                return annotation
            else:
                raise SlideMasterAttributeMustBeSlideLayoutError(key)

        raise SlideMasterAttributeNotFoundError(key)


@dataclass_transform(
    eq_default=True,
    order_default=False,
    field_specifiers=(),
)
class TpptSlideMaster(metaclass=TpptSlideMasterMeta): ...


class DefaultSlideMaster(TpptSlideMaster):
    Master: DefaultMasterSlide
    Title: DefaultTitleSlide
    TitleAndContent: DefaultTitleAndContentSlide
    SectionHeader: DefaultSectionHeaderSlide
    TwoContent: DefaultTwoContentSlide
    Comparison: DefaultComparisonSlide
    TitleOnly: DefaultTitleOnlySlide
    Blank: DefaultBlankSlide
    ContentWithCaption: DefaultContentWithCaptionSlide
    PictureWithCaption: DefaultPictureWithCaptionSlide
    TitleAndVerticalText: DefaultTitleAndVerticalTextSlide
    VerticalTitleAndText: DefaultVerticalTitleAndTextSlide


GenericTpptSlideMaster = TypeVar(
    "GenericTpptSlideMaster",
    bound=TpptSlideMaster,
)
