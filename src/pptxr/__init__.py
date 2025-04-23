from pptx import Presentation
from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE

class SlideLayout(Enum):
    TITLE = 0
    TITLE_AND_CONTENT = 1
    SECTION_HEADER = 2
    TWO_CONTENT = 3
    COMPARISON = 4
    TITLE_ONLY = 5
    BLANK = 6
    CONTENT_WITH_CAPTION = 7
    PICTURE_WITH_CAPTION = 8
    TITLE_AND_VERTICAL_TEXT = 9
    VERTICAL_TITLE_AND_TEXT = 10

class LayoutType(Enum):
    FLEX = "flex"
    GRID = "grid"
    ABSOLUTE = "absolute"

class Align(Enum):
    START = "start"
    CENTER = "center"
    END = "end"

class Justify(Enum):
    START = "start"
    CENTER = "center"
    END = "end"
    SPACE_BETWEEN = "space-between"
    SPACE_AROUND = "space-around"

@dataclass
class Text:
    text: str
    size: Optional[int] = None
    bold: bool = False
    italic: bool = False
    color: Optional[str] = None

@dataclass
class Shape:
    type: str
    left: int
    top: int
    width: int
    height: int
    text: Optional[Text] = None

@dataclass
class Layout:
    type: LayoutType = LayoutType.FLEX
    direction: str = "row"  # "row" or "column"
    align: Align = Align.START
    justify: Justify = Justify.START
    gap: float = 0.1  # in inches
    padding: Dict[str, float] = None  # top, right, bottom, left in inches
    width: Optional[float] = None  # in inches
    height: Optional[float] = None  # in inches

@dataclass
class Image:
    path: str
    width: Optional[float] = None  # in inches
    height: Optional[float] = None  # in inches
    layout: Optional[Layout] = None

@dataclass
class Chart:
    type: str  # "bar", "line", "pie", etc.
    data: List[Dict[str, Any]]
    width: Optional[float] = None  # in inches
    height: Optional[float] = None  # in inches
    layout: Optional[Layout] = None

@dataclass
class Component:
    type: str  # "text", "image", "chart"
    content: Union[Text, Image, Chart]
    layout: Optional[Layout] = None

@dataclass
class Container:
    components: List[Component]
    layout: Layout

@dataclass
class Slide:
    layout: SlideLayout
    title: Optional[Text] = None
    containers: List[Container] = None

class PresentationBuilder:
    def __init__(self):
        self.presentation = Presentation()
        self.slides: List[Slide] = []

    def add_slide(self, slide: Slide) -> 'PresentationBuilder':
        self.slides.append(slide)
        return self

    def _apply_layout(self, shape, layout: Layout):
        if layout.width:
            shape.width = Inches(layout.width)
        if layout.height:
            shape.height = Inches(layout.height)

    def _add_component(self, slide_obj, component: Component, left: float, top: float):
        if component.type == "text":
            shape = slide_obj.shapes.add_textbox(
                Inches(left),
                Inches(top),
                Inches(component.layout.width) if component.layout and component.layout.width else Inches(3),
                Inches(component.layout.height) if component.layout and component.layout.height else Inches(1)
            )
            text_frame = shape.text_frame
            text_frame.text = component.content.text
            if component.content.size:
                text_frame.paragraphs[0].font.size = Pt(component.content.size)
            if component.content.bold:
                text_frame.paragraphs[0].font.bold = True
            if component.content.italic:
                text_frame.paragraphs[0].font.italic = True

        elif component.type == "image":
            shape = slide_obj.shapes.add_picture(
                component.content.path,
                Inches(left),
                Inches(top),
                Inches(component.content.width) if component.content.width else None,
                Inches(component.content.height) if component.content.height else None
            )

        elif component.type == "chart":
            chart_data = ChartData()
            chart_data.categories = [item["category"] for item in component.content.data]
            chart_data.add_series('Series 1', [item["value"] for item in component.content.data])

            x, y = Inches(left), Inches(top)
            cx = Inches(component.layout.width) if component.layout and component.layout.width else Inches(6)
            cy = Inches(component.layout.height) if component.layout and component.layout.height else Inches(4)

            shape = slide_obj.shapes.add_chart(
                XL_CHART_TYPE.BAR_CLUSTERED if component.content.type == "bar" else XL_CHART_TYPE.LINE,
                x, y, cx, cy,
                chart_data
            )

        if component.layout:
            self._apply_layout(shape, component.layout)

    def _add_container(self, slide_obj, container: Container, left: float, top: float):
        current_left = left
        current_top = top

        for component in container.components:
            self._add_component(slide_obj, component, current_left, current_top)
            
            if container.layout.type == LayoutType.FLEX:
                if container.layout.direction == "row":
                    current_left += (component.layout.width if component.layout and component.layout.width else 3) + container.layout.gap
                else:
                    current_top += (component.layout.height if component.layout and component.layout.height else 1) + container.layout.gap

    def build(self) -> Presentation:
        for slide in self.slides:
            slide_layout = self.presentation.slide_layouts[slide.layout.value]
            slide_obj = self.presentation.slides.add_slide(slide_layout)
            
            if slide.title:
                title_shape = slide_obj.shapes.title
                title_shape.text = slide.title.text
                if slide.title.size:
                    title_shape.text_frame.paragraphs[0].font.size = Pt(slide.title.size)
                if slide.title.bold:
                    title_shape.text_frame.paragraphs[0].font.bold = True
                if slide.title.italic:
                    title_shape.text_frame.paragraphs[0].font.italic = True

            if slide.containers:
                for container in slide.containers:
                    self._add_container(slide_obj, container, 1, 2)  # デフォルトの位置

        return self.presentation

def create_presentation() -> PresentationBuilder:
    return PresentationBuilder()
