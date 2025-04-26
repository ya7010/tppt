import datetime
from abc import ABC

from tppt._pptx.slide import SlideBuilder


class TttpSlideLayout(ABC):
    @classmethod
    def builder(cls) -> "SlideBuilder":
        raise NotImplementedError("tppt.SlideLayout.builder must be implemented")


class TitleSlide(TttpSlideLayout):
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

    @classmethod
    def builder(cls) -> "SlideBuilder":
        return SlideBuilder()
