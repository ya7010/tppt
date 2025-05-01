from pptx.shapes.placeholder import LayoutPlaceholder as _PptxLayoutPlaceholder
from pptx.shapes.placeholder import MasterPlaceholder as _PptxMasterPlaceholder
from pptx.shapes.placeholder import SlidePlaceholder as _PptxSlidePlaceholder

from tppt.pptx.converter import to_pptx_length, to_tppt_length
from tppt.pptx.presentation import PptxConvertible
from tppt.types._length import Length

from . import Shape


class LayoutPlaceholder(PptxConvertible[_PptxLayoutPlaceholder]): ...


class MasterPlaceholder(PptxConvertible[_PptxMasterPlaceholder]): ...


class SlidePlaceholder(Shape[_PptxSlidePlaceholder]):
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
