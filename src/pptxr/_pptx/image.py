"""Data classes for PowerPoint presentation."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from pptxr.types import Length


@dataclass
class Image:
    """Image data class."""

    path: Union[str, Path]
    width: Optional[Length] = None
    height: Optional[Length] = None
