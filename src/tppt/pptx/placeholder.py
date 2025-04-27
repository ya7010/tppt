import datetime
from typing import Self

from pptx.shapes.placeholder import LayoutPlaceholder as PptxLayoutPlaceholder
from pptx.shapes.placeholder import SlidePlaceholder as PptxSlidePlaceholder

from tppt.exception import InvalidSetterTypeError
from tppt.pptx.presentation import PptxConvertible


class SlidePlaceholder(PptxConvertible[PptxSlidePlaceholder]):
    def __init__(self, pptx_obj: PptxSlidePlaceholder) -> None:
        self._pptx = pptx_obj

    @property
    def value(self) -> str:
        return self._pptx.text

    @value.setter
    def value(self, value: str | int | datetime.date | None):
        match value:
            case None:
                return
            case str():
                self._pptx.text = value
            case int():
                self._pptx.text = str(value)
            case datetime.date():
                self._pptx.text = value.isoformat()
            case _:
                raise InvalidSetterTypeError(str, type(value))

    def to_pptx(self) -> PptxSlidePlaceholder:
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxSlidePlaceholder) -> Self:
        return cls(pptx_obj)


class LayoutPlaceholder(PptxConvertible[PptxLayoutPlaceholder]):
    def __init__(self, pptx_obj: PptxLayoutPlaceholder) -> None:
        self._pptx = pptx_obj

    def to_pptx(self) -> PptxLayoutPlaceholder:
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxLayoutPlaceholder) -> Self:
        return cls(pptx_obj)
