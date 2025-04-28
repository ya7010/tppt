from typing import Self

from pptx.dml.color import ColorFormat as PptxColorFormat
from pptx.enum.dml import MSO_THEME_COLOR

from tppt.pptx.converter import PptxConvertible, to_pptx_rgb_color, to_tppt_color
from tppt.types import Color, LiteralColor


class ColorFormat(PptxConvertible[PptxColorFormat]):
    def __init__(self, pptx_obj: PptxColorFormat) -> None:
        self._pptx = pptx_obj

    @property
    def brightness(self) -> float:
        """
        Read/write float value between -1.0 and 1.0 indicating the brightness
        adjustment for this color, e.g. -0.25 is 25% darker and 0.4 is 40%
        lighter. 0 means no brightness adjustment.
        """
        return self._pptx.brightness

    @brightness.setter
    def brightness(self, value: float) -> None:
        self._pptx.brightness = value

    @property
    def rgb(self) -> Color | None:
        return to_tppt_color(self._pptx.rgb)

    @rgb.setter
    def rgb(self, color: Color | LiteralColor):
        self._pptx.rgb = to_pptx_rgb_color(color)

    @property
    def theme_color(self) -> MSO_THEME_COLOR:
        """Theme color value of this color.

        Value is a member of :ref:`MsoThemeColorIndex`, e.g.
        ``MSO_THEME_COLOR.ACCENT_1``. Raises AttributeError on access if the
        color is not type ``MSO_COLOR_TYPE.SCHEME``. Assigning a member of
        :ref:`MsoThemeColorIndex` causes the color's type to change to
        ``MSO_COLOR_TYPE.SCHEME``.
        """
        return self._pptx.theme_color

    @theme_color.setter
    def theme_color(self, value: MSO_THEME_COLOR) -> None:
        self._pptx.theme_color = value

    def to_pptx(self) -> PptxColorFormat:
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxColorFormat) -> Self:
        return cls(pptx_obj)
