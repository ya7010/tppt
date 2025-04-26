"""Shape wrapper implementation."""

from typing import Self, TypedDict

from pptx.shapes.base import BaseShape as PptxBaseShape
from typing_extensions import TypeVar

from tppt._pptx.converter import PptxConvertible
from tppt.types._length import Length, LiteralLength

GenericPptxShape = TypeVar(
    "GenericPptxShape",
    bound=PptxBaseShape,
    default=PptxBaseShape,
)


class Shape(PptxConvertible[GenericPptxShape]):
    def __init__(self, pptx_shape: GenericPptxShape) -> None:
        self._pptx: GenericPptxShape = pptx_shape

    def to_pptx(self) -> GenericPptxShape:
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: GenericPptxShape) -> Self:
        return cls(pptx_obj)


class RangeProps(TypedDict):
    """Range properties."""

    left: Length | LiteralLength
    top: Length | LiteralLength
    width: Length | LiteralLength
    height: Length | LiteralLength
