"""Shape wrapper implementation."""

from typing import TYPE_CHECKING, Self, TypedDict

from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.opc.package import XmlPart
from pptx.shapes import Subshape as PptxSubshape
from pptx.shapes.autoshape import Shape as PptxShape
from pptx.shapes.base import BaseShape as PptxBaseShape
from typing_extensions import TypeVar

from tppt.pptx.converter import PptxConvertible
from tppt.types._length import Length, LiteralLength

if TYPE_CHECKING:
    from tppt.pptx.dml.fill import FillFormat
    from tppt.pptx.dml.line import LineFormat
    from tppt.pptx.text.text_frame import TextFrame


GenericPptxBaseShape = TypeVar(
    "GenericPptxBaseShape",
    bound=PptxBaseShape,
    default=PptxBaseShape,
)

GenericPptxShape = TypeVar(
    "GenericPptxShape",
    bound=PptxShape,
    default=PptxShape,
)


class BaseShape(PptxConvertible[GenericPptxBaseShape]):
    def __init__(self, pptx_shape: GenericPptxBaseShape) -> None:
        self._pptx: GenericPptxBaseShape = pptx_shape

    def to_pptx(self) -> GenericPptxBaseShape:
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: GenericPptxBaseShape) -> Self:
        return cls(pptx_obj)


class Shape(BaseShape[GenericPptxShape]):
    @property
    def adjustments(self) -> list[float]:
        return [self._pptx.adjustments[i] for i in range(len(self._pptx.adjustments))]

    @property
    def auto_shape_type(self) -> MSO_AUTO_SHAPE_TYPE | None:
        return self._pptx.auto_shape_type

    @property
    def fill(self) -> "FillFormat":
        from tppt.pptx.dml.fill import FillFormat

        return FillFormat(self._pptx.fill)

    @property
    def line(self) -> "LineFormat":
        from tppt.pptx.dml.line import LineFormat

        return LineFormat(self._pptx.line)

    @property
    def text(self) -> str:
        return self._pptx.text

    @text.setter
    def text(self, text: str) -> None:
        self._pptx.text = text

    @property
    def text_frame(self) -> "TextFrame":
        from tppt.pptx.text.text_frame import TextFrame

        return TextFrame(self._pptx.text_frame)


_GenericPptxSubshape = TypeVar("_GenericPptxSubshape", bound=PptxSubshape)


class SubShape(PptxConvertible[_GenericPptxSubshape]):
    def __init__(self, pptx_shape: _GenericPptxSubshape) -> None:
        self._pptx: _GenericPptxSubshape = pptx_shape

    @property
    def part(self) -> XmlPart:
        return self._pptx.part

    def to_pptx(self) -> _GenericPptxSubshape:
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: _GenericPptxSubshape) -> Self:
        return cls(pptx_obj)


class RangeProps(TypedDict):
    """Range properties."""

    left: Length | LiteralLength
    top: Length | LiteralLength
    width: Length | LiteralLength
    height: Length | LiteralLength
