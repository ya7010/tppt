import datetime
from typing import Any, Self, overload


class TpptSlideLayout:
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
