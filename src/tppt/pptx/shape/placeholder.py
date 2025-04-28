from typing import Self

from pptx.shapes.placeholder import LayoutPlaceholder as PptxLayoutPlaceholder
from pptx.shapes.placeholder import SlidePlaceholder as PptxSlidePlaceholder

from tppt.pptx.converter import to_pptx_length, to_tppt_length
from tppt.pptx.presentation import PptxConvertible
from tppt.types._length import Length

from . import Shape


class SlidePlaceholder(Shape[PptxSlidePlaceholder]):
    def __init__(self, pptx_obj: PptxSlidePlaceholder) -> None:
        self._pptx = pptx_obj

    @property
    def left(self) -> Length | None:
        return to_tppt_length(self._pptx.left)

    @left.setter
    def left(self, value: Length | None) -> None:
        self._pptx.left = to_pptx_length(value)

    @property
    def top(self) -> Length | None:
        return to_tppt_length(self._pptx.top)

    @top.setter
    def top(self, value: Length | None) -> None:
        self._pptx.top = to_pptx_length(value)

    @property
    def height(self) -> Length | None:
        return to_tppt_length(self._pptx.height)

    @height.setter
    def height(self, value: Length | None) -> None:
        self._pptx.height = to_pptx_length(value)

    @property
    def width(self) -> Length | None:
        return to_tppt_length(self._pptx.width)

    @width.setter
    def width(self, value: Length | None) -> None:
        self._pptx.width = to_pptx_length(value)

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
