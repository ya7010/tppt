from pptx import Presentation
from typing import List, Optional, Dict, Any, Union, NewType, TypeVar, Union
from dataclasses import dataclass
from enum import Enum
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE

# Type definitions for units
Inch = NewType('Inch', float)
Point = NewType('Point', int)
Length = Union[Inch, Point]

# Constants for unit conversion
INCHES_PER_POINT = 1/72  # 1 point = 1/72 inches
POINTS_PER_INCH = 72     # 1 inch = 72 points

def to_inches(length: Length) -> Inch:
    """Convert any length to inches

    Args:
        length (Length): Length in any unit

    Returns:
        Inch: Length in inches
    """
    if isinstance(length, Point):
        return Inch(float(length) * INCHES_PER_POINT)
    return length

def to_points(length: Length) -> Point:
    """Convert any length to points

    Args:
        length (Length): Length in any unit

    Returns:
        Point: Length in points
    """
    if isinstance(length, Inch):
        return Point(int(float(length) * POINTS_PER_INCH))
    return length

class SlideLayout(Enum):
    """Enumeration defining slide layout types"""
    TITLE = 0
    """Title-only layout"""
    TITLE_AND_CONTENT = 1
    """Title and content layout"""
    SECTION_HEADER = 2
    """Section header layout"""
    TWO_CONTENT = 3
    """Layout with two content areas"""
    COMPARISON = 4
    """Comparison layout"""
    TITLE_ONLY = 5
    """Title-only layout"""
    BLANK = 6
    """Blank layout"""
    CONTENT_WITH_CAPTION = 7
    """Content with caption layout"""
    PICTURE_WITH_CAPTION = 8
    """Picture with caption layout"""
    TITLE_AND_VERTICAL_TEXT = 9
    """Title and vertical text layout"""
    VERTICAL_TITLE_AND_TEXT = 10
    """Vertical title and text layout"""

class LayoutType(Enum):
    """Enumeration defining layout types"""
    FLEX = "flex"
    """Flexbox layout"""
    GRID = "grid"
    """Grid layout"""
    ABSOLUTE = "absolute"
    """Absolute positioning layout"""

class Align(Enum):
    """Enumeration defining element alignment"""
    START = "start"
    """Align to start position"""
    CENTER = "center"
    """Align to center"""
    END = "end"
    """Align to end position"""

class Justify(Enum):
    """Enumeration defining element justification"""
    START = "start"
    """Justify to start"""
    CENTER = "center"
    """Justify to center"""
    END = "end"
    """Justify to end"""
    SPACE_BETWEEN = "space-between"
    """Distribute space between elements"""
    SPACE_AROUND = "space-around"
    """Distribute space around elements"""

@dataclass
class Text:
    """Data class representing text element"""
    text: str
    """Text content"""
    size: Optional[Length] = None
    """Font size"""
    bold: bool = False
    """Whether text is bold"""
    italic: bool = False
    """Whether text is italic"""
    color: Optional[str] = None
    """Text color"""

@dataclass
class Shape:
    """Data class representing shape"""
    type: str
    """Shape type"""
    left: Length
    """Position from left edge"""
    top: Length
    """Position from top edge"""
    width: Length
    """Width"""
    height: Length
    """Height"""
    text: Optional[Text] = None
    """Text within shape"""

@dataclass
class Layout:
    """Data class representing layout settings"""
    type: LayoutType = LayoutType.FLEX
    """Layout type"""
    direction: str = "row"
    """Layout direction ("row" or "column")"""
    align: Align = Align.START
    """Element alignment"""
    justify: Justify = Justify.START
    """Element justification"""
    gap: Length = Inch(0.1)
    """Gap between elements"""
    padding: Dict[str, Length] = None
    """Padding (top, right, bottom, left)"""
    width: Optional[Length] = None
    """Width"""
    height: Optional[Length] = None
    """Height"""

@dataclass
class Image:
    """Data class representing image element"""
    path: str
    """Path to image file"""
    width: Optional[Length] = None
    """Width"""
    height: Optional[Length] = None
    """Height"""
    layout: Optional[Layout] = None
    """Layout settings"""

@dataclass
class Chart:
    """Data class representing chart element"""
    type: str
    """Chart type ("bar", "line", "pie", etc.)"""
    data: List[Dict[str, Any]]
    """Chart data"""
    width: Optional[Length] = None
    """Width"""
    height: Optional[Length] = None
    """Height"""
    layout: Optional[Layout] = None
    """Layout settings"""

@dataclass
class Component:
    """Data class representing component"""
    type: str
    """Component type ("text", "image", "chart")"""
    content: Union[Text, Image, Chart]
    """Component content"""
    layout: Optional[Layout] = None
    """Layout settings"""

@dataclass
class Container:
    """Data class representing container"""
    components: List[Component]
    """Components within container"""
    layout: Layout
    """Layout settings"""

@dataclass
class Slide:
    """Data class representing slide"""
    layout: SlideLayout
    """Slide layout"""
    title: Optional[Text] = None
    """Slide title"""
    containers: List[Container] = None
    """Containers within slide"""

class PresentationBuilder:
    """Builder class for creating presentations"""
    def __init__(self):
        """Initialize presentation builder"""
        self.presentation = Presentation()
        self.slides: List[Slide] = []

    def add_slide(self, slide: Slide) -> 'PresentationBuilder':
        """Add a slide to the presentation

        Args:
            slide (Slide): Slide to add

        Returns:
            PresentationBuilder: Self instance for method chaining
        """
        self.slides.append(slide)
        return self

    def _apply_layout(self, shape, layout: Layout):
        """Apply layout to a shape

        Args:
            shape: Target shape
            layout (Layout): Layout settings to apply
        """
        if layout.width:
            shape.width = Inches(float(to_inches(layout.width)))
        if layout.height:
            shape.height = Inches(float(to_inches(layout.height)))

    def _add_component(self, slide_obj, component: Component, left: Length, top: Length):
        """Add a component to a slide

        Args:
            slide_obj: Target slide
            component (Component): Component to add
            left (Length): Position from left edge
            top (Length): Position from top edge
        """
        if component.type == "text":
            shape = slide_obj.shapes.add_textbox(
                Inches(float(to_inches(left))),
                Inches(float(to_inches(top))),
                Inches(float(to_inches(component.layout.width))) if component.layout and component.layout.width else Inches(3),
                Inches(float(to_inches(component.layout.height))) if component.layout and component.layout.height else Inches(1)
            )
            text_frame = shape.text_frame
            text_frame.text = component.content.text
            if component.content.size:
                text_frame.paragraphs[0].font.size = Pt(int(to_points(component.content.size)))
            if component.content.bold:
                text_frame.paragraphs[0].font.bold = True
            if component.content.italic:
                text_frame.paragraphs[0].font.italic = True

        elif component.type == "image":
            shape = slide_obj.shapes.add_picture(
                component.content.path,
                Inches(float(to_inches(left))),
                Inches(float(to_inches(top))),
                Inches(float(to_inches(component.content.width))) if component.content.width else None,
                Inches(float(to_inches(component.content.height))) if component.content.height else None
            )

        elif component.type == "chart":
            chart_data = ChartData()
            chart_data.categories = [item["category"] for item in component.content.data]
            chart_data.add_series('Series 1', [item["value"] for item in component.content.data])

            x, y = Inches(float(to_inches(left))), Inches(float(to_inches(top)))
            cx = Inches(float(to_inches(component.layout.width))) if component.layout and component.layout.width else Inches(6)
            cy = Inches(float(to_inches(component.layout.height))) if component.layout and component.layout.height else Inches(4)

            shape = slide_obj.shapes.add_chart(
                XL_CHART_TYPE.BAR_CLUSTERED if component.content.type == "bar" else XL_CHART_TYPE.LINE,
                x, y, cx, cy,
                chart_data
            )

        if component.layout:
            self._apply_layout(shape, component.layout)

    def _add_container(self, slide_obj, container: Container, left: Length, top: Length):
        """Add a container to a slide

        Args:
            slide_obj: Target slide
            container (Container): Container to add
            left (Length): Position from left edge
            top (Length): Position from top edge
        """
        current_left = left
        current_top = top

        for component in container.components:
            self._add_component(slide_obj, component, current_left, current_top)
            
            if container.layout.type == LayoutType.FLEX:
                if container.layout.direction == "row":
                    current_left = Inch(float(to_inches(current_left)) + 
                                     (float(to_inches(component.layout.width)) if component.layout and component.layout.width else 3) + 
                                     float(to_inches(container.layout.gap)))
                else:
                    current_top = Inch(float(to_inches(current_top)) + 
                                    (float(to_inches(component.layout.height)) if component.layout and component.layout.height else 1) + 
                                    float(to_inches(container.layout.gap)))

    def build(self) -> Presentation:
        """Build the presentation

        Returns:
            Presentation: Built presentation
        """
        for slide in self.slides:
            slide_layout = self.presentation.slide_layouts[slide.layout.value]
            slide_obj = self.presentation.slides.add_slide(slide_layout)
            
            if slide.title:
                title_shape = slide_obj.shapes.title
                title_shape.text = slide.title.text
                if slide.title.size:
                    title_shape.text_frame.paragraphs[0].font.size = Pt(int(to_points(slide.title.size)))
                if slide.title.bold:
                    title_shape.text_frame.paragraphs[0].font.bold = True
                if slide.title.italic:
                    title_shape.text_frame.paragraphs[0].font.italic = True

            if slide.containers:
                for container in slide.containers:
                    self._add_container(slide_obj, container, Inch(1), Inch(2))  # Default position

        return self.presentation

def create_presentation() -> PresentationBuilder:
    """Create a new presentation builder

    Returns:
        PresentationBuilder: Newly created presentation builder
    """
    return PresentationBuilder()
