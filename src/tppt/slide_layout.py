import datetime
from inspect import isclass
from typing import (
    TYPE_CHECKING,
    Annotated,
    Any,
    ClassVar,
    Self,
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

_AnyType = TypeVar("_AnyType")


class _Placeholder:
    def __init__(self, description: str = ""):
        self.description = description
        self.value = None

    def __repr__(self) -> str:
        return f"Placeholder({self.description!r})"

    @classmethod
    def __class_getitem__(cls, item: Any) -> Any:
        return Annotated[item, cls()]


Placeholder = Annotated[_AnyType, _Placeholder]


class TpptSlideLayoutMeta(type):
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

        for field_name, field_type in annotations.items():
            # Search for Annotated fields
            if get_origin(field_type) is Annotated:
                args = get_args(field_type)
                # Check metadata
                metadata_args = args[1:]

                # Search for fields directly marked as Placeholder
                if any(
                    arg is _Placeholder
                    or (isclass(arg) and arg.__name__ == "_Placeholder")
                    for arg in metadata_args
                ):
                    placeholders[field_name] = args[0]  # Actual type
                    continue

                # Check nested Annotated (Placeholder[T] pattern)
                # Detect the pattern Placeholder[T] = Annotated[T, _Placeholder]
                base_type = args[0]
                if get_origin(base_type) is Annotated:
                    nested_args = get_args(base_type)
                    if any(
                        arg is _Placeholder
                        or (isclass(arg) and arg.__name__ == "_Placeholder")
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
class TpptSlideLayout(metaclass=TpptSlideLayoutMeta):
    """Base class for slide layouts"""

    __placeholders__: ClassVar[dict[str, Any]] = {}

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


class DefaultMasterSlide(TpptSlideLayout):
    """Default master slide layout."""

    title: Placeholder[str]
    text: Placeholder[str]
    date: Placeholder[datetime.date | None] = None
    footer: Placeholder[str | None] = None


class DefaultTitleSlide(TpptSlideLayout):
    """Title slide layout."""

    title: Placeholder[str]
    subtitle: Placeholder[str | None] = None
    date: Placeholder[datetime.date | None] = None
    footer: Placeholder[str | None] = None


class DefaultTitleAndContentSlide(TpptSlideLayout):
    """Title and content slide layout."""

    title: Placeholder[str]
    content: Placeholder[str]
    date: Placeholder[datetime.date | None] = None
    footer: Placeholder[str | None] = None


class DefaultSectionHeaderSlide(TpptSlideLayout):
    """Section header slide layout."""

    title: Placeholder[str]
    text: Placeholder[str]
    date: Placeholder[datetime.date | None] = None
    footer: Placeholder[str | None] = None


class DefaultTwoContentSlide(TpptSlideLayout):
    """Two content slide layout."""

    title: Placeholder[str]
    left_content: Placeholder[str]
    right_content: Placeholder[str]
    date: Placeholder[datetime.date | None] = None
    footer: Placeholder[str | None] = None


class DefaultComparisonSlide(TpptSlideLayout):
    """Comparison slide layout."""

    title: Placeholder[str]
    left_title: Placeholder[str]
    left_content: Placeholder[str]
    right_title: Placeholder[str]
    right_content: Placeholder[str]
    date: Placeholder[datetime.date | None] = None
    footer: Placeholder[str | None] = None


class DefaultTitleOnlySlide(TpptSlideLayout):
    """Title only slide layout."""

    title: Placeholder[str]
    date: Placeholder[datetime.date | None] = None
    footer: Placeholder[str | None] = None


class DefaultBlankSlide(TpptSlideLayout):
    """Blank slide layout."""

    date: Placeholder[datetime.date | None] = None
    footer: Placeholder[str | None] = None


class DefaultContentWithCaptionSlide(TpptSlideLayout):
    """Content with caption slide layout."""

    title: Placeholder[str]
    content: Placeholder[str]
    date: Placeholder[datetime.date | None] = None
    footer: Placeholder[str | None] = None


class DefaultPictureWithCaptionSlide(TpptSlideLayout):
    """Picture with caption slide layout."""

    title: Placeholder[str]
    picture_path: Placeholder[FilePath]
    date: Placeholder[datetime.date | None] = None
    footer: Placeholder[str | None] = None


class DefaultTitleAndVerticalTextSlide(TpptSlideLayout):
    """Title and vertical text slide layout."""

    title: Placeholder[str]
    vertical_text: Placeholder[str]
    date: Placeholder[datetime.date | None] = None
    footer: Placeholder[str | None] = None


class DefaultVerticalTitleAndTextSlide(TpptSlideLayout):
    """Vertical title and text slide layout."""

    vertical_title: Placeholder[str]
    text: Placeholder[str]
    date: Placeholder[datetime.date | None]
    footer: Placeholder[str | None]
