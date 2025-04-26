import datetime
from typing import Any, Self, overload


class TpptSlideLayout:
    """Base class for all slide layouts."""

    @overload
    def __get__(self, instance: None, objtype: type[Any]) -> type[Self]: ...

    @overload
    def __get__(self, instance: object, objtype: type[Any]) -> Self: ...

    def __get__(self, instance: object | None, objtype: type[Any]) -> type[Self] | Self:
        if instance is None:
            return type(self)

        else:
            return self


class DefaultMasterSlide(TpptSlideLayout):
    """Default master slide layout."""

    def __init__(
        self,
        *,
        title: str,
        text: str,
        date: datetime.date | None = None,
        footer: str | None = None,
        slide_number: bool = True,
    ) -> None:
        self.title = title
        self.text = text
        self.date = date
        self.footer = footer
        self.slide_number = slide_number


class DefaultTitleSlide(TpptSlideLayout):
    """Title slide layout."""

    def __init__(
        self,
        *,
        title: str,
        subtitle: str | None = None,
        date: datetime.date | None = None,
        footer: str | None = None,
        slide_number: bool = True,
    ) -> None:
        self.title = title
        self.subtitle = subtitle
        self.date = date
        self.footer = footer
        self.slide_number = slide_number


class DefaultTitleAndContentSlide(TpptSlideLayout):
    """Title and content slide layout."""

    def __init__(
        self,
        *,
        title: str,
        content: str | None = None,
        date: datetime.date | None = None,
        footer: str | None = None,
        slide_number: bool = True,
    ) -> None:
        self.title = title
        self.content = content
        self.date = date
        self.footer = footer
        self.slide_number = slide_number


class DefaultSectionHeaderSlide(TpptSlideLayout):
    """Section header slide layout."""

    def __init__(
        self,
        *,
        title: str,
        text: str | None = None,
        date: datetime.date | None = None,
        footer: str | None = None,
        slide_number: bool = True,
    ) -> None:
        self.title = title
        self.text = text
        self.date = date
        self.footer = footer
        self.slide_number = slide_number


class DefaultTwoContentSlide(TpptSlideLayout):
    """Two content slide layout."""

    def __init__(
        self,
        *,
        title: str,
        left_content: str | None = None,
        right_content: str | None = None,
        date: datetime.date | None = None,
        footer: str | None = None,
        slide_number: bool = True,
    ) -> None:
        self.title = title
        self.left_content = left_content
        self.right_content = right_content
        self.date = date
        self.footer = footer
        self.slide_number = slide_number


class DefaultComparisonSlide(TpptSlideLayout):
    """Comparison slide layout."""

    def __init__(
        self,
        *,
        title: str,
        left_title: str | None = None,
        left_content: str | None = None,
        right_title: str | None = None,
        right_content: str | None = None,
        date: datetime.date | None = None,
        footer: str | None = None,
        slide_number: bool = True,
    ) -> None:
        self.title = title
        self.left_title = left_title
        self.left_content = left_content
        self.right_title = right_title
        self.right_content = right_content
        self.date = date
        self.footer = footer
        self.slide_number = slide_number


class DefaultTitleOnlySlide(TpptSlideLayout):
    """Title only slide layout."""

    def __init__(
        self,
        *,
        title: str,
        date: datetime.date | None = None,
        footer: str | None = None,
        slide_number: bool = True,
    ) -> None:
        self.title = title
        self.date = date
        self.footer = footer
        self.slide_number = slide_number


class DefaultBlankSlide(TpptSlideLayout):
    """Blank slide layout."""

    def __init__(
        self,
        *,
        date: datetime.date | None = None,
        footer: str | None = None,
        slide_number: bool = True,
    ) -> None:
        self.date = date
        self.footer = footer
        self.slide_number = slide_number


class DefaultContentWithCaptionSlide(TpptSlideLayout):
    """Content with caption slide layout."""

    def __init__(
        self,
        *,
        title: str,
        content: str | None = None,
        date: datetime.date | None = None,
        footer: str | None = None,
        slide_number: bool = True,
    ) -> None:
        self.title = title
        self.content = content
        self.date = date
        self.footer = footer
        self.slide_number = slide_number


class DefaultPictureWithCaptionSlide(TpptSlideLayout):
    """Picture with caption slide layout."""

    def __init__(
        self,
        *,
        title: str,
        picture_path: str | None = None,
        date: datetime.date | None = None,
        footer: str | None = None,
        slide_number: bool = True,
    ) -> None:
        self.title = title
        self.picture_path = picture_path
        self.date = date
        self.footer = footer
        self.slide_number = slide_number


class DefaultTitleAndVerticalTextSlide(TpptSlideLayout):
    """Title and vertical text slide layout."""

    def __init__(
        self,
        *,
        title: str,
        vertical_text: str | None = None,
        date: datetime.date | None = None,
        footer: str | None = None,
        slide_number: bool = True,
    ) -> None:
        self.title = title
        self.vertical_text = vertical_text
        self.date = date
        self.footer = footer
        self.slide_number = slide_number


class DefaultVerticalTitleAndTextSlide(TpptSlideLayout):
    """Vertical title and text slide layout."""

    def __init__(
        self,
        *,
        vertical_title: str,
        text: str | None = None,
        date: datetime.date | None = None,
        footer: str | None = None,
        slide_number: bool = True,
    ) -> None:
        self.vertical_title = vertical_title
        self.text = text
        self.date = date
        self.footer = footer
        self.slide_number = slide_number
