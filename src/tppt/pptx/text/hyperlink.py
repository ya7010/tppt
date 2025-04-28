from typing import Self

from pptx.text.text import _Hyperlink as PptxHyperlink

from tppt.pptx.converter import PptxConvertible


class Hyperlink(PptxConvertible[PptxHyperlink]):
    def __init__(self, pptx_obj: PptxHyperlink) -> None:
        self._pptx = pptx_obj

    @property
    def address(self) -> str | None:
        return self._pptx.address

    @address.setter
    def address(self, address: str | None) -> None:
        self._pptx.address = address

    def builder(self) -> "HyperlinkBuilder":
        return HyperlinkBuilder(self._pptx)

    def to_pptx(self) -> PptxHyperlink:
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxHyperlink) -> Self:
        return cls(pptx_obj)


class HyperlinkBuilder:
    def __init__(self, pptx_obj: PptxHyperlink) -> None:
        self._pptx = pptx_obj

    def _build(self) -> Hyperlink:
        return Hyperlink(self._pptx)
