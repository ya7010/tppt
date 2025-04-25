"""Shape wrapper implementation."""

from typing import Self

from pptx.shapes.base import BaseShape as PptxBaseShape
from typing_extensions import TypeVar

from pptxr._pptx.converter import PptxConvertible

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
