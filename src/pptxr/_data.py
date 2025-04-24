from dataclasses import dataclass
from typing import TypeAlias

from pptxr import Image, Text

Component: TypeAlias = Text | Image


@dataclass
class Placeholder: ...


@dataclass
class Slide:
    layout: int
    placeholders: list[Placeholder]
    components: list[Component]
    title: Text | None = None
