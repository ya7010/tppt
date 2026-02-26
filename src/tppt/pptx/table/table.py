"""Table wrapper implementation."""

import logging
from collections.abc import Iterator
from dataclasses import fields, is_dataclass
from typing import (
    Any,
    Literal,
    NotRequired,
    Self,
    TypeAlias,
    TypedDict,
    cast,
)

from pptx.enum.text import MSO_VERTICAL_ANCHOR, PP_ALIGN
from pptx.table import Table as PptxTable
from pptx.table import _Cell as PptxCell
from pptx.table import _Column as PptxColumn
from pptx.table import _ColumnCollection as PptxColumnCollection
from pptx.table import _Row as PptxRow
from pptx.table import _RowCollection as PptxRowCollection

from tppt._features import (
    USE_PANDAS,
    USE_POLARS,
    USE_PYDANTIC,
    Dataclass,
    PandasDataFrame,
    PolarsDataFrame,
    PolarsLazyFrame,
    PydanticModel,
)
from tppt.types._length import Length, LiteralPoints, Points

from ..converter import PptxConvertible, to_pptx_length, to_tppt_length
from ..shape import RangeProps
from .cell import Cell

logger = logging.getLogger(__name__)


# Define DataFrame type alias
DataFrame: TypeAlias = (
    list[list[str]]
    | list[Dataclass]
    | list[PydanticModel]
    | PandasDataFrame
    | PolarsDataFrame
    | PolarsLazyFrame
)


class TableCellStyle(TypedDict):
    """Table cell style properties."""

    text_align: NotRequired[Literal["left", "center", "right", "justify"]]
    vertical_align: NotRequired[Literal["top", "middle", "bottom"]]
    bold: NotRequired[bool]
    italic: NotRequired[bool]
    font_size: NotRequired[Points | LiteralPoints]
    font_name: NotRequired[str]


class TableProps(RangeProps):
    """Table properties."""

    cell_styles: NotRequired[list[list[TableCellStyle]]]
    first_row_header: NotRequired[bool]


class TableData(TableProps):
    """Table data."""

    type: Literal["table"]

    data: list[list[str]]


class Row(PptxConvertible[PptxRow]):
    """Row wrapper class."""

    @property
    def cells(self) -> list[Cell]:
        """Get all cells in this row."""
        return [Cell(cell) for cell in self._pptx.cells]

    @property
    def height(self) -> Length:
        """Height of the row."""
        return to_tppt_length(self._pptx.height)

    @height.setter
    def height(self, value: Length) -> None:
        self._pptx.height = to_pptx_length(value)

    def set_height(self, value: Length) -> Self:
        """Set height and return self for method chaining."""
        self.height = value
        return self


class Column(PptxConvertible[PptxColumn]):
    """Column wrapper class."""

    @property
    def width(self) -> Length:
        """Width of the column."""
        return to_tppt_length(self._pptx.width)

    @width.setter
    def width(self, value: Length) -> None:
        self._pptx.width = to_pptx_length(value)

    def set_width(self, value: Length) -> Self:
        """Set width and return self for method chaining."""
        self.width = value
        return self


class RowCollection(PptxConvertible[PptxRowCollection]):
    """Row collection wrapper class."""

    def __getitem__(self, idx: int) -> Row:
        return Row(self._pptx[idx])

    def __len__(self) -> int:
        return len(self._pptx)


class ColumnCollection(PptxConvertible[PptxColumnCollection]):
    """Column collection wrapper class."""

    def __getitem__(self, idx: int) -> Column:
        return Column(self._pptx[idx])

    def __len__(self) -> int:
        return len(self._pptx)


class Table(PptxConvertible[PptxTable]):
    """Table data class."""

    def __init__(
        self,
        pptx_obj: PptxTable,
        props: TableData | None = None,
        /,
    ) -> None:
        self._pptx = pptx_obj

        if not props:
            return

        table = pptx_obj

        # Apply first row as header if specified
        if (first_row := props.get("first_row_header")) is not None:
            table.first_row = first_row

        # Apply table data if provided
        if data := props.get("data"):
            # Now apply the data to the table
            for i, row in enumerate(data):
                if i < len(table.rows):
                    for j, cell_text in enumerate(row):
                        if j < len(table.columns):
                            table.cell(i, j).text = str(cell_text)

        # Apply cell styles if provided
        if (cell_styles := props.get("cell_styles")) is not None:
            for i, row_styles in enumerate(cell_styles):
                if i < len(table.rows):
                    for j, cell_style in enumerate(row_styles):
                        if j < len(table.columns):
                            cell = table.cell(i, j)

                            if (text_align := cell_style.get("text_align")) is not None:
                                align_map = {
                                    "left": PP_ALIGN.LEFT,
                                    "center": PP_ALIGN.CENTER,
                                    "right": PP_ALIGN.RIGHT,
                                    "justify": PP_ALIGN.JUSTIFY,
                                }
                                paragraph = cell.text_frame.paragraphs[0]
                                paragraph.alignment = align_map[text_align]

                            if (
                                vertical_align := cell_style.get("vertical_align")
                            ) is not None:
                                valign_map = {
                                    "top": MSO_VERTICAL_ANCHOR.TOP,
                                    "middle": MSO_VERTICAL_ANCHOR.MIDDLE,
                                    "bottom": MSO_VERTICAL_ANCHOR.BOTTOM,
                                }
                                cell.text_frame.vertical_anchor = valign_map[
                                    vertical_align
                                ]

                            # Apply text formatting
                            if any(
                                key in cell_style
                                for key in ["bold", "italic", "font_size", "font_name"]
                            ):
                                paragraph = cell.text_frame.paragraphs[0]
                                run = (
                                    paragraph.runs[0]
                                    if paragraph.runs
                                    else paragraph.add_run()
                                )

                                if "bold" in cell_style:
                                    run.font.bold = cell_style["bold"]

                                if "italic" in cell_style:
                                    run.font.italic = cell_style["italic"]

                                if "font_size" in cell_style:
                                    run.font.size = to_pptx_length(
                                        cell_style["font_size"]
                                    )

                                if "font_name" in cell_style:
                                    run.font.name = cell_style["font_name"]

    def cell(self, row_idx: int, col_idx: int) -> Cell:
        """Get cell at row_idx and col_idx."""
        return Cell(self._pptx.cell(row_idx, col_idx))

    @property
    def rows(self) -> RowCollection:
        """Get row collection."""
        return RowCollection(self._pptx.rows)

    @property
    def columns(self) -> ColumnCollection:
        """Get column collection."""
        return ColumnCollection(self._pptx.columns)

    @property
    def first_row(self) -> bool:
        """Whether the first row is styled as a header."""
        return self._pptx.first_row

    @first_row.setter
    def first_row(self, value: bool) -> None:
        self._pptx.first_row = value

    def set_first_row(self, value: bool) -> Self:
        """Set first_row and return self for method chaining."""
        self.first_row = value
        return self

    @property
    def last_row(self) -> bool:
        """Whether the last row is styled differently."""
        return self._pptx.last_row

    @last_row.setter
    def last_row(self, value: bool) -> None:
        self._pptx.last_row = value

    def set_last_row(self, value: bool) -> Self:
        """Set last_row and return self for method chaining."""
        self.last_row = value
        return self

    @property
    def first_col(self) -> bool:
        """Whether the first column is styled differently."""
        return self._pptx.first_col

    @first_col.setter
    def first_col(self, value: bool) -> None:
        self._pptx.first_col = value

    def set_first_col(self, value: bool) -> Self:
        """Set first_col and return self for method chaining."""
        self.first_col = value
        return self

    @property
    def last_col(self) -> bool:
        """Whether the last column is styled differently."""
        return self._pptx.last_col

    @last_col.setter
    def last_col(self, value: bool) -> None:
        self._pptx.last_col = value

    def set_last_col(self, value: bool) -> Self:
        """Set last_col and return self for method chaining."""
        self.last_col = value
        return self

    @property
    def horz_banding(self) -> bool:
        """Whether horizontal banding is enabled."""
        return self._pptx.horz_banding

    @horz_banding.setter
    def horz_banding(self, value: bool) -> None:
        self._pptx.horz_banding = value

    def set_horz_banding(self, value: bool) -> Self:
        """Set horz_banding and return self for method chaining."""
        self.horz_banding = value
        return self

    @property
    def vert_banding(self) -> bool:
        """Whether vertical banding is enabled."""
        return self._pptx.vert_banding

    @vert_banding.setter
    def vert_banding(self, value: bool) -> None:
        self._pptx.vert_banding = value

    def set_vert_banding(self, value: bool) -> Self:
        """Set vert_banding and return self for method chaining."""
        self.vert_banding = value
        return self

    def iter_cells(self) -> Iterator[Cell]:
        """Iterate over all cells in the table."""
        return (Cell(cell) for cell in self._pptx.iter_cells())


def dataframe2list(data: DataFrame) -> list[list[str]]:
    """Convert different DataFrame types to list of lists."""
    if USE_POLARS:
        if isinstance(data, PolarsLazyFrame):
            # For LazyFrame, collect it first
            polars_df = cast(PolarsLazyFrame, data).collect()
            columns = list(polars_df.columns)
            rows = polars_df.to_numpy().tolist()
            return [columns] + rows
        elif isinstance(data, PolarsDataFrame):
            polars_df = cast(PolarsDataFrame, data)
            columns = list(polars_df.columns)
            rows = polars_df.to_numpy().tolist()
            return [columns] + rows

    if USE_PANDAS and isinstance(data, PandasDataFrame):  # type: ignore
        # Convert pandas DataFrame to list of lists
        pandas_df = cast(PandasDataFrame, data)
        columns = pandas_df.columns.tolist()
        rows = pandas_df.values.tolist()
        return [columns] + rows

    if isinstance(data, list):
        if len(data) != 0:
            # Convert list of dataclass instances to list of lists
            first_instance = data[0]
            if is_dataclass(first_instance):
                columns = [field.name for field in fields(first_instance)]
                rows = []
                for instance in data:
                    instance = cast(Any, instance)
                    row = [
                        str(getattr(instance, field.name)) for field in fields(instance)
                    ]
                    rows.append(row)
                return [columns] + rows
            # Convert list of Pydantic model instances to list of lists
            elif USE_PYDANTIC and isinstance(first_instance, PydanticModel):
                columns = list(first_instance.__class__.model_fields.keys())  # type: ignore
                rows = []
                for instance in data:
                    instance = cast(Any, instance)
                    row = [str(getattr(instance, field)) for field in columns]
                    rows.append(row)
                return [columns] + rows
        else:
            logger.warning("Empty data of table")
            return []

    # Assume it's a list of lists
    return cast(list[list[str]], data)
