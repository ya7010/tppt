from typing import TypeVar

from typing_extensions import dataclass_transform

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


GenericTpptSlideMaster = TypeVar("GenericTpptSlideMaster", bound=TpptSlideMaster)


class DefaultSlideMaster(TpptSlideMaster):
    master: DefaultMasterSlide
    title: DefaultTitleSlide
    title_and_content: DefaultTitleAndContentSlide
    section_header: DefaultSectionHeaderSlide
    two_content: DefaultTwoContentSlide
    comparison: DefaultComparisonSlide
    title_only: DefaultTitleOnlySlide
    blank: DefaultBlankSlide
    content_with_caption: DefaultContentWithCaptionSlide
    picture_with_caption: DefaultPictureWithCaptionSlide
    title_and_vertical_text: DefaultTitleAndVerticalTextSlide
    vertical_title_and_text: DefaultVerticalTitleAndTextSlide
