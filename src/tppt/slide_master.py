from typing import (
    TYPE_CHECKING,
    Annotated,
    Callable,
    ClassVar,
    Literal,
    TypeAlias,
    TypeVar,
    get_args,
    get_origin,
)

from typing_extensions import dataclass_transform

from tppt.exception import (
    SlideMasterAttributeMustBeSlideLayoutError,
    SlideMasterAttributeNotFoundError,
    SlideMasterDoesNotHaveAttributesError,
)
from tppt.types import FilePath

from .slide_layout import (
    AnyType,
    DefaultBlankSlideLayout,
    DefaultComparisonSlideLayout,
    DefaultContentWithCaptionSlideLayout,
    DefaultPictureWithCaptionSlideLayout,
    DefaultSectionHeaderSlideLayout,
    DefaultTitleAndContentSlideLayout,
    DefaultTitleAndVerticalTextSlideLayout,
    DefaultTitleOnlySlideLayout,
    DefaultTitleSlideLayout,
    DefaultTwoContentSlideLayout,
    DefaultVerticalTitleAndTextSlideLayout,
    SlideLayout,
)

GenericSlideMaster = TypeVar("GenericSlideMaster", bound="type[SlideMaster]")


class _SlideMasterMeta(type):
    __slide_master_source__: ClassVar[Literal["default"] | FilePath]

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


def slide_master(
    source: Literal["default"] | FilePath,
) -> Callable[[GenericSlideMaster], GenericSlideMaster]:
    """Decorator that sets the slide master source.

    Args:
        source: Either "default" or a path to a PowerPoint file containing the slide master
    """

    def decorator(cls: GenericSlideMaster) -> GenericSlideMaster:
        setattr(cls, "__slide_master_source__", source)
        return cls

    return decorator


@slide_master("default")
class DefaultSlideMaster(SlideMaster):
    TitleLayout: Layout[DefaultTitleSlideLayout]
    TitleAndContentLayout: Layout[DefaultTitleAndContentSlideLayout]
    SectionHeaderLayout: Layout[DefaultSectionHeaderSlideLayout]
    TwoContentLayout: Layout[DefaultTwoContentSlideLayout]
    ComparisonLayout: Layout[DefaultComparisonSlideLayout]
    TitleOnlyLayout: Layout[DefaultTitleOnlySlideLayout]
    BlankLayout: Layout[DefaultBlankSlideLayout]
    ContentWithCaptionLayout: Layout[DefaultContentWithCaptionSlideLayout]
    PictureWithCaptionLayout: Layout[DefaultPictureWithCaptionSlideLayout]
    TitleAndVerticalTextLayout: Layout[DefaultTitleAndVerticalTextSlideLayout]
    VerticalTitleAndTextLayout: Layout[DefaultVerticalTitleAndTextSlideLayout]


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
