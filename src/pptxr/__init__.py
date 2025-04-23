from pptx import Presentation
from typing import List, Optional, Union
from dataclasses import dataclass
from enum import Enum

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
class Slide:
    layout: SlideLayout
    title: Optional[Text] = None
    shapes: List[Shape] = None

class PresentationBuilder:
    def __init__(self):
        self.presentation = Presentation()
        self.slides: List[Slide] = []

    def add_slide(self, slide: Slide) -> 'PresentationBuilder':
        self.slides.append(slide)
        return self

    def build(self) -> Presentation:
        for slide in self.slides:
            slide_layout = self.presentation.slide_layouts[slide.layout.value]
            slide_obj = self.presentation.slides.add_slide(slide_layout)
            
            if slide.title:
                title_shape = slide_obj.shapes.title
                title_shape.text = slide.title.text
                if slide.title.size:
                    title_shape.text_frame.paragraphs[0].font.size = slide.title.size
                if slide.title.bold:
                    title_shape.text_frame.paragraphs[0].font.bold = True
                if slide.title.italic:
                    title_shape.text_frame.paragraphs[0].font.italic = True

            if slide.shapes:
                for shape in slide.shapes:
                    shape_obj = slide_obj.shapes.add_shape(
                        shape.type,
                        shape.left,
                        shape.top,
                        shape.width,
                        shape.height
                    )
                    if shape.text:
                        shape_obj.text = shape.text.text
                        if shape.text.size:
                            shape_obj.text_frame.paragraphs[0].font.size = shape.text.size
                        if shape.text.bold:
                            shape_obj.text_frame.paragraphs[0].font.bold = True
                        if shape.text.italic:
                            shape_obj.text_frame.paragraphs[0].font.italic = True

        return self.presentation

def create_presentation() -> PresentationBuilder:
    return PresentationBuilder()
