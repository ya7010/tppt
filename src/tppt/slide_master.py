from typing import TYPE_CHECKING, Annotated, TypeAlias, get_args, get_origin

from typing_extensions import TypeVar, dataclass_transform

from tppt.exception import (
    SlideMasterAttributeMustBeSlideLayoutError,
    SlideMasterAttributeNotFoundError,
    SlideMasterDoesNotHaveAttributesError,
)

from .slide_layout import (
    AnyType,
    DefaultBlankSlide,
    DefaultComparisonSlide,
    DefaultContentWithCaptionSlide,
    DefaultPictureWithCaptionSlide,
    DefaultSectionHeaderSlide,
    DefaultTitleAndContentSlide,
    DefaultTitleAndVerticalTextSlide,
    DefaultTitleOnlySlide,
    DefaultTitleSlide,
    DefaultTwoContentSlide,
    DefaultVerticalTitleAndTextSlide,
    SlideLayout,
)


class _SlideMasterMeta(type):
    def __getattr__(self, key: str) -> "type[SlideLayout]":
        # 1. Check the class's own attributes
        if key in self.__dict__:
            value = self.__dict__[key]
            if isinstance(value, type) and issubclass(value, SlideLayout):
                return value

        # 2. Check annotations
        if annotations := getattr(self, "__annotations__", None):
            if annotation := annotations.get(key):
                # Extract from Annotated type
                origin = get_origin(annotation)
                if origin is Annotated:
                    args = get_args(annotation)
                    if (
                        args
                        and isinstance(args[0], type)
                        and issubclass(args[0], SlideLayout)
                    ):
                        return args[0]
                    else:
                        raise SlideMasterAttributeMustBeSlideLayoutError(key)
                # Direct check for class type
                elif isinstance(annotation, type) and issubclass(
                    annotation, SlideLayout
                ):
                    return annotation
                else:
                    return annotation
            elif (attributes := getattr(self, "__annotations__", None)) and hasattr(
                attributes, key
            ):
                return getattr(attributes, key)
            else:
                raise SlideMasterAttributeNotFoundError(key)
        else:
            raise SlideMasterDoesNotHaveAttributesError()


@dataclass_transform(
    eq_default=True,
    order_default=False,
    field_specifiers=(),
)
class SlideMaster(metaclass=_SlideMasterMeta): ...


if TYPE_CHECKING:
    Layout: TypeAlias = Annotated[AnyType, ...]
else:

    class Layout:
        @classmethod
        def __class_getitem__(cls, item: AnyType) -> AnyType:
            return Annotated[item, cls()]


class DefaultSlideMaster(SlideMaster):
    Title: Layout[DefaultTitleSlide]
    TitleAndContent: Layout[DefaultTitleAndContentSlide]
    SectionHeader: Layout[DefaultSectionHeaderSlide]
    TwoContent: Layout[DefaultTwoContentSlide]
    Comparison: Layout[DefaultComparisonSlide]
    TitleOnly: Layout[DefaultTitleOnlySlide]
    Blank: Layout[DefaultBlankSlide]
    ContentWithCaption: Layout[DefaultContentWithCaptionSlide]
    PictureWithCaption: Layout[DefaultPictureWithCaptionSlide]
    TitleAndVerticalText: Layout[DefaultTitleAndVerticalTextSlide]
    VerticalTitleAndText: Layout[DefaultVerticalTitleAndTextSlide]


GenericTpptSlideMaster = TypeVar(
    "GenericTpptSlideMaster",
    bound=SlideMaster,
)


def get_layouts(slide_master: type[SlideMaster]) -> list[type[SlideLayout]]:
    """Get an array of slides tagged with Layout."""
    layouts = []

    for attr_name, annotation in slide_master.__annotations__.items():
        origin = get_origin(annotation)
        if origin is Annotated:
            args = get_args(annotation)
            # Identify Layout using class comparison instead of string name
            if len(args) > 1:
                if args[1].__class__ is Layout:
                    layouts.append(getattr(slide_master, attr_name))

    return layouts
