"""Shape wrapper implementation."""

from typing import TYPE_CHECKING, Self, TypedDict

from pptx.shapes.autoshape import Shape as PptxShape
from pptx.shapes.base import BaseShape as PptxBaseShape
from typing_extensions import TypeVar

from tppt.pptx.converter import PptxConvertible
from tppt.types._length import Length, LiteralLength

if TYPE_CHECKING:
    from ..text.text_frame import TextFrame

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
    def __init__(self, pptx_shape: GenericPptxShape) -> None:
        self._pptx: GenericPptxShape = pptx_shape

    @property
    def text(self) -> str:
        return self._pptx.text

    @text.setter
    def text(self, text: str) -> None:
        self._pptx.text = text

    @property
    def text_frame(self) -> "TextFrame":
        from ..text.text_frame import TextFrame

        return TextFrame(self._pptx.text_frame)


class RangeProps(TypedDict):
    """Range properties."""

    left: Length | LiteralLength
    top: Length | LiteralLength
    width: Length | LiteralLength
    height: Length | LiteralLength
