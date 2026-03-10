from typing import TYPE_CHECKING, Literal, Self, TypedDict, assert_never

from pptx.chart.chart import Chart as PptxChart
from pptx.chart.chart import Legend as PptxLegend
from pptx.chart.data import ChartData as PptxChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION

from tppt.pptx.converter import PptxConvertible
from tppt.types._length import Length, LiteralLength

if TYPE_CHECKING:
    from tppt.pptx.text.font import Font
    from tppt.pptx.text.text_frame import TextFrame

LiteralChartType = Literal[
    "3D Area",
    "3D Stacked Area",
    "3D 100% Stacked Area",
    "3D Clustered Bar",
    "3D Stacked Bar",
    "3D 100% Stacked Bar",
    "3D Column",
    "3D Clustered Column",
    "3D Stacked Column",
    "3D 100% Stacked Column",
    "3D Line",
    "3D Pie",
    "3D Exploded Pie",
    "Area",
    "Stacked Area",
    "100% Stacked Area",
    "Clustered Bar",
    "Bar of Pie",
    "Stacked Bar",
    "100% Stacked Bar",
    "Bubble",
    "Bubble with 3D effects",
    "Clustered Column",
    "Stacked Column",
    "100% Stacked Column",
    "Clustered Cone Bar",
    "Stacked Cone Bar",
    "100% Stacked Cone Bar",
    "3D Cone Column",
    "Clustered Cone Column",
    "Stacked Cone Column",
    "100% Stacked Cone Column",
    "Clustered Cylinder Bar",
    "Stacked Cylinder Bar",
    "100% Stacked Cylinder Bar",
    "3D Cylinder Column",
    "Clustered Cylinder Column",
    "Stacked Cylinder Column",
    "100% Stacked Cylinder Column",
    "Doughnut",
    "Exploded Doughnut",
    "Line",
    "Line with Markers",
    "Stacked Line with Markers",
    "100% Stacked Line with Markers",
    "Stacked Line",
    "100% Stacked Line",
    "Pie",
    "Exploded Pie",
    "Pie of Pie",
    "Clustered Pyramid Bar",
    "Stacked Pyramid Bar",
    "100% Stacked Pyramid Bar",
    "3D Pyramid Column",
    "Clustered Pyramid Column",
    "Stacked Pyramid Column",
    "100% Stacked Pyramid Column",
    "Radar",
    "Filled Radar",
    "Radar with Data Markers",
    "High-Low-Close",
    "Open-High-Low-Close",
    "Volume-High-Low-Close",
    "Volume-Open-High-Low-Close",
    "3D Surface",
    "Surface (Top View)",
    "Surface (Top View wireframe)",
    "3D Surface (wireframe)",
    "Scatter",
    "Scatter with Lines",
    "Scatter with Lines and No Data Markers",
    "Scatter with Smoothed Lines",
    "Scatter with Smoothed Lines and No Data Markers",
]


def to_pptx_chart_type(chart_type: XL_CHART_TYPE | LiteralChartType) -> XL_CHART_TYPE:
    match chart_type:
        case XL_CHART_TYPE():
            return chart_type
        case "3D Area":
            return XL_CHART_TYPE.THREE_D_AREA
        case "3D Stacked Area":
            return XL_CHART_TYPE.THREE_D_AREA_STACKED
        case "3D 100% Stacked Area":
            return XL_CHART_TYPE.THREE_D_AREA_STACKED_100
        case "3D Clustered Bar":
            return XL_CHART_TYPE.THREE_D_BAR_CLUSTERED
        case "3D Stacked Bar":
            return XL_CHART_TYPE.THREE_D_BAR_STACKED
        case "3D 100% Stacked Bar":
            return XL_CHART_TYPE.THREE_D_BAR_STACKED_100
        case "3D Column":
            return XL_CHART_TYPE.THREE_D_COLUMN
        case "3D Clustered Column":
            return XL_CHART_TYPE.THREE_D_COLUMN_CLUSTERED
        case "3D Stacked Column":
            return XL_CHART_TYPE.THREE_D_COLUMN_STACKED
        case "3D 100% Stacked Column":
            return XL_CHART_TYPE.THREE_D_COLUMN_STACKED_100
        case "3D Line":
            return XL_CHART_TYPE.THREE_D_LINE
        case "3D Pie":
            return XL_CHART_TYPE.THREE_D_PIE
        case "3D Exploded Pie":
            return XL_CHART_TYPE.THREE_D_PIE_EXPLODED
        case "Area":
            return XL_CHART_TYPE.AREA
        case "Stacked Area":
            return XL_CHART_TYPE.AREA_STACKED
        case "100% Stacked Area":
            return XL_CHART_TYPE.AREA_STACKED_100
        case "Clustered Bar":
            return XL_CHART_TYPE.BAR_CLUSTERED
        case "Bar of Pie":
            return XL_CHART_TYPE.BAR_OF_PIE
        case "Stacked Bar":
            return XL_CHART_TYPE.BAR_STACKED
        case "100% Stacked Bar":
            return XL_CHART_TYPE.BAR_STACKED_100
        case "Bubble":
            return XL_CHART_TYPE.BUBBLE
        case "Bubble with 3D effects":
            return XL_CHART_TYPE.BUBBLE_THREE_D_EFFECT
        case "Clustered Column":
            return XL_CHART_TYPE.COLUMN_CLUSTERED
        case "Stacked Column":
            return XL_CHART_TYPE.COLUMN_STACKED
        case "100% Stacked Column":
            return XL_CHART_TYPE.COLUMN_STACKED_100
        case "Clustered Cone Bar":
            return XL_CHART_TYPE.CONE_BAR_CLUSTERED
        case "Stacked Cone Bar":
            return XL_CHART_TYPE.CONE_BAR_STACKED
        case "100% Stacked Cone Bar":
            return XL_CHART_TYPE.CONE_BAR_STACKED_100
        case "3D Cone Column":
            return XL_CHART_TYPE.CONE_COL
        case "Clustered Cone Column":
            return XL_CHART_TYPE.CONE_COL_CLUSTERED
        case "Stacked Cone Column":
            return XL_CHART_TYPE.CONE_COL_STACKED
        case "100% Stacked Cone Column":
            return XL_CHART_TYPE.CONE_COL_STACKED_100
        case "Clustered Cylinder Bar":
            return XL_CHART_TYPE.CYLINDER_BAR_CLUSTERED
        case "Stacked Cylinder Bar":
            return XL_CHART_TYPE.CYLINDER_BAR_STACKED
        case "100% Stacked Cylinder Bar":
            return XL_CHART_TYPE.CYLINDER_BAR_STACKED_100
        case "3D Cylinder Column":
            return XL_CHART_TYPE.CYLINDER_COL
        case "Clustered Cylinder Column":
            return XL_CHART_TYPE.CYLINDER_COL_CLUSTERED
        case "Stacked Cylinder Column":
            return XL_CHART_TYPE.CYLINDER_COL_STACKED
        case "100% Stacked Cylinder Column":
            return XL_CHART_TYPE.CYLINDER_COL_STACKED_100
        case "Doughnut":
            return XL_CHART_TYPE.DOUGHNUT
        case "Exploded Doughnut":
            return XL_CHART_TYPE.DOUGHNUT_EXPLODED
        case "Line":
            return XL_CHART_TYPE.LINE
        case "Line with Markers":
            return XL_CHART_TYPE.LINE_MARKERS
        case "Stacked Line with Markers":
            return XL_CHART_TYPE.LINE_MARKERS_STACKED
        case "100% Stacked Line with Markers":
            return XL_CHART_TYPE.LINE_MARKERS_STACKED_100
        case "Stacked Line":
            return XL_CHART_TYPE.LINE_STACKED
        case "100% Stacked Line":
            return XL_CHART_TYPE.LINE_STACKED_100
        case "Pie":
            return XL_CHART_TYPE.PIE
        case "Exploded Pie":
            return XL_CHART_TYPE.PIE_EXPLODED
        case "Pie of Pie":
            return XL_CHART_TYPE.PIE_OF_PIE
        case "Clustered Pyramid Bar":
            return XL_CHART_TYPE.PYRAMID_BAR_CLUSTERED
        case "Stacked Pyramid Bar":
            return XL_CHART_TYPE.PYRAMID_BAR_STACKED
        case "100% Stacked Pyramid Bar":
            return XL_CHART_TYPE.PYRAMID_BAR_STACKED_100
        case "3D Pyramid Column":
            return XL_CHART_TYPE.PYRAMID_COL
        case "Clustered Pyramid Column":
            return XL_CHART_TYPE.PYRAMID_COL_CLUSTERED
        case "Stacked Pyramid Column":
            return XL_CHART_TYPE.PYRAMID_COL_STACKED
        case "100% Stacked Pyramid Column":
            return XL_CHART_TYPE.PYRAMID_COL_STACKED_100
        case "Radar":
            return XL_CHART_TYPE.RADAR
        case "Filled Radar":
            return XL_CHART_TYPE.RADAR_FILLED
        case "Radar with Data Markers":
            return XL_CHART_TYPE.RADAR_MARKERS
        case "High-Low-Close":
            return XL_CHART_TYPE.STOCK_HLC
        case "Open-High-Low-Close":
            return XL_CHART_TYPE.STOCK_OHLC
        case "Volume-High-Low-Close":
            return XL_CHART_TYPE.STOCK_VHLC
        case "Volume-Open-High-Low-Close":
            return XL_CHART_TYPE.STOCK_VOHLC
        case "3D Surface":
            return XL_CHART_TYPE.SURFACE
        case "Surface (Top View)":
            return XL_CHART_TYPE.SURFACE_TOP_VIEW
        case "Surface (Top View wireframe)":
            return XL_CHART_TYPE.SURFACE_TOP_VIEW_WIREFRAME
        case "3D Surface (wireframe)":
            return XL_CHART_TYPE.SURFACE_WIREFRAME
        case "Scatter":
            return XL_CHART_TYPE.XY_SCATTER
        case "Scatter with Lines":
            return XL_CHART_TYPE.XY_SCATTER_LINES
        case "Scatter with Lines and No Data Markers":
            return XL_CHART_TYPE.XY_SCATTER_LINES_NO_MARKERS
        case "Scatter with Smoothed Lines":
            return XL_CHART_TYPE.XY_SCATTER_SMOOTH
        case "Scatter with Smoothed Lines and No Data Markers":
            return XL_CHART_TYPE.XY_SCATTER_SMOOTH_NO_MARKERS
        case _:
            assert_never(chart_type)


class ChartProps(TypedDict):
    """Chart properties."""

    chart_type: LiteralChartType | XL_CHART_TYPE
    x: Length | LiteralLength
    y: Length | LiteralLength
    cx: Length | LiteralLength
    cy: Length | LiteralLength
    chart_data: PptxChartData


class ChartData(ChartProps):
    """Chart data."""

    type: Literal["chart"]


class ChartTitle(PptxConvertible["PptxChartTitle"]):
    """Chart title wrapper class."""

    @property
    def has_text_frame(self) -> bool:
        """True if this chart title has a text frame."""
        return self._pptx.has_text_frame

    @property
    def text_frame(self) -> "TextFrame":
        """Text frame of the chart title."""
        from tppt.pptx.text.text_frame import TextFrame

        return TextFrame(self._pptx.text_frame)


class Legend(PptxConvertible[PptxLegend]):
    """Legend wrapper class."""

    @property
    def font(self) -> "Font":
        """Font of the legend."""
        from tppt.pptx.text.font import Font

        return Font(self._pptx.font)

    @property
    def horz_offset(self) -> float:
        """Horizontal offset of the legend as a float between -1.0 and 1.0."""
        return self._pptx.horz_offset

    @horz_offset.setter
    def horz_offset(self, value: float) -> None:
        self._pptx.horz_offset = value

    def set_horz_offset(self, value: float) -> Self:
        """Set horizontal offset and return self for method chaining."""
        self.horz_offset = value
        return self

    @property
    def include_in_layout(self) -> bool:
        """Whether the legend is included in the chart layout."""
        return self._pptx.include_in_layout

    @include_in_layout.setter
    def include_in_layout(self, value: bool) -> None:
        self._pptx.include_in_layout = value

    def set_include_in_layout(self, value: bool) -> Self:
        """Set include_in_layout and return self for method chaining."""
        self.include_in_layout = value
        return self

    @property
    def position(self) -> XL_LEGEND_POSITION:
        """Position of the legend."""
        return self._pptx.position

    @position.setter
    def position(self, value: XL_LEGEND_POSITION) -> None:
        self._pptx.position = value

    def set_position(self, value: XL_LEGEND_POSITION) -> Self:
        """Set position and return self for method chaining."""
        self.position = value
        return self


class Chart(PptxConvertible[PptxChart]):
    """Chart data class."""

    def __init__(self, pptx_obj: PptxChart, /) -> None:
        super().__init__(pptx_obj)

    @property
    def chart_style(self) -> int | None:
        """Chart style index."""
        return self._pptx.chart_style

    @chart_style.setter
    def chart_style(self, value: int | None) -> None:
        self._pptx.chart_style = value

    def set_chart_style(self, value: int | None) -> Self:
        """Set chart style and return self for method chaining."""
        self.chart_style = value
        return self

    @property
    def chart_title(self) -> ChartTitle:
        """Chart title object."""
        return ChartTitle(self._pptx.chart_title)

    @property
    def chart_type(self) -> XL_CHART_TYPE:
        """Chart type."""
        return self._pptx.chart_type

    @property
    def font(self) -> "Font":
        """Font of the chart."""
        from tppt.pptx.text.font import Font

        return Font(self._pptx.font)

    @property
    def has_legend(self) -> bool:
        """Whether the chart has a legend."""
        return self._pptx.has_legend

    @has_legend.setter
    def has_legend(self, value: bool) -> None:
        self._pptx.has_legend = value

    def set_has_legend(self, value: bool) -> Self:
        """Set has_legend and return self for method chaining."""
        self.has_legend = value
        return self

    @property
    def has_title(self) -> bool:
        """Whether the chart has a title."""
        return self._pptx.has_title

    @has_title.setter
    def has_title(self, value: bool) -> None:
        self._pptx.has_title = value

    def set_has_title(self, value: bool) -> Self:
        """Set has_title and return self for method chaining."""
        self.has_title = value
        return self

    @property
    def legend(self) -> Legend:
        """Legend of the chart."""
        return Legend(self._pptx.legend)

    def replace_data(self, chart_data: PptxChartData) -> None:
        """Replace chart data with new data."""
        self._pptx.replace_data(chart_data)
