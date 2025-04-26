from typing import TYPE_CHECKING, Annotated, TypeAlias, get_args, get_origin

from typing_extensions import TypeVar, dataclass_transform

from tppt.exception import (
    MasterLayoutNotFoundError,
    MultipleMasterLayoutsError,
    SlideMasterAttributeMustBeSlideLayoutError,
    SlideMasterAttributeNotFoundError,
)

from .slide_layout import (
    AnyType,
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
        if hasattr(self, "__annotations__") and key in self.__annotations__:
            annotation = self.__annotations__[key]

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
            elif isinstance(annotation, type) and issubclass(annotation, SlideLayout):
                return annotation
            else:
                raise SlideMasterAttributeMustBeSlideLayoutError(key)

        raise SlideMasterAttributeNotFoundError(key)


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


if TYPE_CHECKING:
    MasterLayout: TypeAlias = Annotated[AnyType, ...]
else:

    class MasterLayout(Layout):
        pass


class DefaultSlideMaster(SlideMaster):
    Master: MasterLayout[DefaultMasterSlide]
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

def get_master_layout(slide_master: type[SlideMaster]) -> type[SlideLayout]:
    """Get the slide tagged with MasterLayout."""
    master_layouts = []
    master_layout_names = []

    for attr_name, annotation in slide_master.__annotations__.items():
        origin = get_origin(annotation)
        if origin is Annotated:
            args = get_args(annotation)
            # Check the class name instead of directly checking the type of args[1]
            if len(args) > 1 and args[1].__class__.__name__ == "MasterLayout":
                master_layouts.append(getattr(slide_master, attr_name))
                master_layout_names.append(attr_name)

    if not master_layouts:
        raise MasterLayoutNotFoundError(slide_master.__name__)

    if len(master_layouts) > 1:
        raise MultipleMasterLayoutsError(slide_master.__name__, master_layout_names)

    return master_layouts[0]


def get_layouts(slide_master: type[SlideMaster]) -> list[type[SlideLayout]]:
    """Get an array of slides tagged with Layout."""
    layouts = []

    for attr_name, annotation in slide_master.__annotations__.items():
        origin = get_origin(annotation)
        if origin is Annotated:
            args = get_args(annotation)
            # Identify Layout and MasterLayout using class names
            if len(args) > 1:
                if args[1].__class__.__name__ == "Layout":
                    layouts.append(getattr(slide_master, attr_name))
                elif args[1].__class__.__name__ == "MasterLayout":
                    # Exclude MasterLayout
                    pass

    return layouts
