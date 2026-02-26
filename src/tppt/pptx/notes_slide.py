from typing import TYPE_CHECKING

from pptx.slide import NotesSlide as PptxNotesSlide

from tppt.pptx.converter import PptxConvertible

if TYPE_CHECKING:
    from tppt.pptx.shape import BaseShape
    from tppt.pptx.shape.placeholder import SlidePlaceholder
    from tppt.pptx.text.text_frame import TextFrame


class NotesSlide(PptxConvertible[PptxNotesSlide]):
    """Notes slide."""

    @property
    def notes_text_frame(self) -> "TextFrame":
        """Text frame of the notes body placeholder."""
        from tppt.pptx.text.text_frame import TextFrame

        return TextFrame(self._pptx.notes_text_frame)

    @property
    def notes_placeholder(self) -> "SlidePlaceholder":
        """Notes body placeholder shape."""
        from tppt.pptx.shape.placeholder import SlidePlaceholder

        return SlidePlaceholder(self._pptx.notes_placeholder)

    @property
    def placeholders(self) -> "list[SlidePlaceholder]":
        """All placeholders in the notes slide."""
        from tppt.pptx.shape.placeholder import SlidePlaceholder

        return [
            SlidePlaceholder(placeholder)  # type: ignore
            for placeholder in self._pptx.placeholders
        ]

    @property
    def shapes(self) -> "list[BaseShape]":
        """All shapes in the notes slide."""
        from tppt.pptx.shape import BaseShape

        return [BaseShape(shape) for shape in self._pptx.shapes]
