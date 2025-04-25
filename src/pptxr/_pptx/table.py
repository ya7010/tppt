"""Table wrapper implementation."""

from typing import Literal, NotRequired, Self, TypedDict

from pptx.shapes.graphfrm import GraphicFrame

from pptxr.types._length import Length, LiteralLength

from .converter import PptxConvertible


class TableProps(TypedDict):
    """Table properties."""

    left: Length | LiteralLength
    top: Length | LiteralLength
    width: Length | LiteralLength
    height: Length | LiteralLength
    data: NotRequired[list[list[str]]]


class TableData(TableProps):
    """Table data."""

    type: Literal["table"]
    rows: int
    cols: int


class Table(PptxConvertible[GraphicFrame]):
    """Table data class."""

    def __init__(
        self,
        pptx_obj: GraphicFrame,
        data: TableData | None = None,
        /,
    ) -> None:
        self._pptx = pptx_obj

        if data and "data" in data:
            table_data = data["data"]
            table = pptx_obj.table
            for i, row in enumerate(table_data):
                if i < len(table.rows):
                    for j, cell_text in enumerate(row):
                        if j < len(table.columns):
                            table.cell(i, j).text = cell_text

    def to_pptx(self) -> GraphicFrame:
        """Convert to pptx table frame."""
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: GraphicFrame) -> Self:
        """Create from pptx table frame."""
        return cls(pptx_obj)
