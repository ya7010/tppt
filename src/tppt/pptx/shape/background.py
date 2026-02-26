from typing import TYPE_CHECKING

from pptx.slide import _Background as PptxBackground

from tppt.pptx.converter import PptxConvertible

if TYPE_CHECKING:
    from tppt.pptx.dml.fill import FillFormat


class Background(PptxConvertible[PptxBackground]):
    """Background of the slide."""

    @property
    def fill(self) -> "FillFormat":
        """Fill format of the background."""
        from tppt.pptx.dml.fill import FillFormat

        return FillFormat(self._pptx.fill)
