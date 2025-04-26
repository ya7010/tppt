from abc import ABC

from tppt._pptx.slide import SlideBuilder


class TttpSlideLayout(ABC):
    @classmethod
    def builder(cls) -> "SlideBuilder":
        raise NotImplementedError("tppt.SlideLayout.builder must be implemented")


class TitleSlide(TttpSlideLayout):
    @classmethod
    def builder(cls) -> "SlideBuilder":
        return SlideBuilder()
