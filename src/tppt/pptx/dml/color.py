from typing import Self, cast

from lxml.etree import _Element
from pptx.dml.color import ColorFormat as PptxColorFormat
from pptx.dml.color import RGBColor as PptxRGBColor
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.oxml.xmlchemy import OxmlElement

from tppt.pptx.converter import PptxConvertible, to_pptx_rgb_color, to_tppt_rgb_color
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
    def rgb(self) -> Color:
        solid_fill = cast(
            _Element, self._pptx._xFill.solidFill.get_or_change_to_srgbClr()
        )
        alpha = solid_fill.find("a:alpha", None)
        if alpha is not None:
            alpha = alpha.attrib["val"]
        return to_tppt_rgb_color(cast(PptxRGBColor, self._pptx.rgb), alpha=alpha)

    @rgb.setter
    def rgb(self, color: Color | LiteralColor):
        pptx_color, alpha = to_pptx_rgb_color(color)
        self._pptx.rgb = pptx_color
        if alpha:
            solid_fill = cast(
                _Element, self._pptx._xFill.solidFill.get_or_change_to_srgbClr()
            )
            element = OxmlElement("a:alpha")
            element.attrib["val"] = str(alpha)
            solid_fill.append(element)

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
