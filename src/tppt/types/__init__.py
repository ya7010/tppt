"""Types module for tppt."""

import pathlib
from typing import Literal, TypeAlias

from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE

from tppt.pptx.shape import RangeProps as _RangeProps
from tppt.pptx.shape.table import TableCellStyle as TableCellStyle

from ._color import Color as Color
from ._length import (
    CentiMeters as CentiMeters,
)
from ._length import (
    EnglishMetricUnits as EnglishMetricUnits,
)
from ._length import (
    Inchs as Inchs,
)
from ._length import (
    Length as Length,
)
from ._length import (
    LiteralLength as LiteralLength,
)
from ._length import (
    MilliMeters as MilliMeters,
)
from ._length import (
    Points as Points,
)
from ._length import (
    to_length as to_length,
)
from ._length import (
    to_point as to_point,
)

FilePath = str | pathlib.Path
ShapeType: TypeAlias = MSO_AUTO_SHAPE_TYPE
Range: TypeAlias = _RangeProps

SlideLayoutType: TypeAlias = Literal[
    "TITLE",
    "TITLE_AND_CONTENT",
    "SECTION_HEADER",
    "TWO_CONTENT",
    "COMPARISON",
    "TITLE_ONLY",
    "BLANK",
    "CONTENT_WITH_CAPTION",
    "PICTURE_WITH_CAPTION",
    "TITLE_AND_VERTICAL_TEXT",
    "VERTICAL_TITLE_AND_TEXT",
]
