import datetime
from typing import (
    TYPE_CHECKING,
    Annotated,
    Any,
    ClassVar,
    OrderedDict,
    Self,
    TypeAlias,
    TypeVar,
    dataclass_transform,
    get_args,
    get_origin,
    get_type_hints,
    overload,
)

from tppt.types import FilePath

if TYPE_CHECKING:
    from tppt.pptx.slide import SlideBuilder
    from tppt.pptx.slide_layout import SlideLayout as PptxConvertibleSlideLayout


AnyType = TypeVar("AnyType")


if TYPE_CHECKING:
    Placeholder: TypeAlias = Annotated[AnyType, ...]
else:

    class Placeholder:
        @classmethod
        def __class_getitem__(cls, item: AnyType) -> AnyType:
            return Annotated[item, cls()]


class _SlideLayoutMeta(type):
    """Meta class for TpptSlideLayout.

    Tracks fields annotated as placeholders.
    """

    def __new__(
        mcs, name: str, bases: tuple[type, ...], namespace: dict[str, Any]
    ) -> type:
        cls = super().__new__(mcs, name, bases, namespace)

        # Collect placeholder fields
        annotations = get_type_hints(cls, include_extras=True)
        placeholders = {}

        # Inherit placeholders from base classes
        for base in bases:
            if hasattr(base, "__placeholders__"):
                placeholders.update(base.__placeholders__)

        for field_name, field_type in annotations.items():
            # Search for Annotated fields
            if get_origin(field_type) is Annotated:
                args = get_args(field_type)
                # Check metadata
                metadata_args = args[1:]

                # Search for fields directly marked as Placeholder
                if any(
                    isinstance(arg, Placeholder)  # type: ignore
                    or arg is Placeholder
                    for arg in metadata_args
                ):
                    placeholders[field_name] = args[0]  # Actual type
                    continue

                # Check nested Annotated (Placeholder[T] pattern)
                # Detect the pattern Placeholder[T] = Annotated[T, Placeholder]
                base_type = args[0]
                if get_origin(base_type) is Annotated:
                    nested_args = get_args(base_type)
                    if any(
                        isinstance(arg, Placeholder)  # type: ignore
                        or arg is Placeholder
                        for arg in nested_args[1:]
                    ):
                        placeholders[field_name] = nested_args[0]  # Actual type
                        continue

        # Save placeholder information to the class
        setattr(cls, "__placeholders__", placeholders)
        return cls


@dataclass_transform(
    eq_default=True,
    order_default=False,
    field_specifiers=(),
)
class SlideLayout(metaclass=_SlideLayoutMeta):
    """Base class for slide layouts"""

    __placeholders__: ClassVar[OrderedDict[str, Any]] = OrderedDict()

    def __init__(self, **kwargs) -> None:
        # Set values for all fields
        for field_name, field_value in kwargs.items():
            if field_name in self.__class__.__placeholders__:
                # For placeholder fields
                setattr(self, field_name, field_value)
            elif field_name in self.__class__.__annotations__:
                setattr(self, field_name, field_value)
            else:
                raise TypeError(
                    f"'{self.__class__.__name__}' got an unexpected keyword argument '{field_name}'"
                )

    @overload
    def __get__(self, instance: None, objtype: type[Any]) -> type[Self]: ...

    @overload
    def __get__(self, instance: object, objtype: type[Any]) -> Self: ...

    def __get__(self, instance: object | None, objtype: type[Any]) -> type[Self] | Self:
        if instance is None:
            return type(self)

        else:
            return self

    def builder(self) -> "SlideBuilder":
        from tppt.pptx.slide import SlideBuilder

        return SlideBuilder()


class SlideLayoutProxy:
    def __init__(
        self,
        origin: type[SlideLayout],
        slide_layout: "PptxConvertibleSlideLayout",
    ) -> None:
        self._slide_layout = origin
        self._pptx = slide_layout

    def __getattr__(self, item: str) -> Any:
        return getattr(self._slide_layout, item)

    def builder(self) -> "SlideBuilder":
        self._presentation.slide_master.slide_layouts

        return SlideBuilder(self._pptx)


class DefaultTitleSlide(SlideLayout):
    """Title slide layout."""

    title: Placeholder[str]
    subtitle: Placeholder[str | None] = None
    date: Placeholder[datetime.date | None] = None
    footer: Placeholder[str | None] = None


class DefaultTitleAndContentSlide(SlideLayout):
    """Title and content slide layout."""

    title: Placeholder[str]
    content: Placeholder[str]
    date: Placeholder[datetime.date | None] = None
    footer: Placeholder[str | None] = None


class DefaultSectionHeaderSlide(SlideLayout):
    """Section header slide layout."""

    title: Placeholder[str]
    text: Placeholder[str]
    date: Placeholder[datetime.date | None] = None
    footer: Placeholder[str | None] = None


class DefaultTwoContentSlide(SlideLayout):
    """Two content slide layout."""

    title: Placeholder[str]
    left_content: Placeholder[str]
    right_content: Placeholder[str]
    date: Placeholder[datetime.date | None] = None
    footer: Placeholder[str | None] = None


class DefaultComparisonSlide(SlideLayout):
    """Comparison slide layout."""

    title: Placeholder[str]
    left_title: Placeholder[str]
    left_content: Placeholder[str]
    right_title: Placeholder[str]
    right_content: Placeholder[str]
    date: Placeholder[datetime.date | None] = None
    footer: Placeholder[str | None] = None


class DefaultTitleOnlySlide(SlideLayout):
    """Title only slide layout."""

    title: Placeholder[str]
    date: Placeholder[datetime.date | None] = None
    footer: Placeholder[str | None] = None


class DefaultBlankSlide(SlideLayout):
    """Blank slide layout."""

    date: Placeholder[datetime.date | None] = None
    footer: Placeholder[str | None] = None


class DefaultContentWithCaptionSlide(SlideLayout):
    """Content with caption slide layout."""

    title: Placeholder[str]
    content: Placeholder[str]
    date: Placeholder[datetime.date | None] = None
    footer: Placeholder[str | None] = None


class DefaultPictureWithCaptionSlide(SlideLayout):
    """Picture with caption slide layout."""

    title: Placeholder[str]
    picture_path: Placeholder[FilePath]
    date: Placeholder[datetime.date | None] = None
    footer: Placeholder[str | None] = None


class DefaultTitleAndVerticalTextSlide(SlideLayout):
    """Title and vertical text slide layout."""

    title: Placeholder[str]
    vertical_text: Placeholder[str]
    date: Placeholder[datetime.date | None] = None
    footer: Placeholder[str | None] = None


class DefaultVerticalTitleAndTextSlide(SlideLayout):
    """Vertical title and text slide layout."""

    vertical_title: Placeholder[str]
    text: Placeholder[str]
    date: Placeholder[datetime.date | None]
    footer: Placeholder[str | None]


def get_placeholders(slide_layout: type[SlideLayout]) -> OrderedDict[str, Any]:
    return slide_layout.__placeholders__
