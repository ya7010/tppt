"""Types module for tppt."""

import pathlib
from typing import TypeAlias

from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE as _MSO_AUTO_SHAPE_TYPE

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

FilePath = str | pathlib.Path
ShapeType: TypeAlias = _MSO_AUTO_SHAPE_TYPE
Range: TypeAlias = _RangeProps
