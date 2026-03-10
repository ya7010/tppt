from typing import TYPE_CHECKING

from pptx.slide import NotesSlide as PptxNotesSlide

from tppt.pptx.converter import PptxConvertible

if TYPE_CHECKING:
    from tppt.pptx.shape import BaseShape
    from tppt.pptx.shape.placeholder import NotesSlidePlaceholder, SlidePlaceholder
    from tppt.pptx.text.text_frame import TextFrame


class NotesSlide(PptxConvertible[PptxNotesSlide]):
    """Notes slide."""

    @property
    def notes_text_frame(self) -> "TextFrame":
        """Text frame of the notes body placeholder."""
        from tppt.pptx.text.text_frame import TextFrame

        text_frame = self._pptx.notes_text_frame
        assert text_frame is not None
        return TextFrame(text_frame)

    @property
    def notes_placeholder(self) -> "NotesSlidePlaceholder":
        """Notes body placeholder shape."""
        from tppt.pptx.shape.placeholder import NotesSlidePlaceholder

        placeholder = self._pptx.notes_placeholder
        assert placeholder is not None
        return NotesSlidePlaceholder(placeholder)

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
