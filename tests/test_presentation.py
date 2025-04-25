"""Tests for presentation module."""

from pathlib import Path

from pptx import Presentation as PptxPresentation
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE

from pptxr._data import Presentation, Shape
from pptxr.types import pt


def test_create_presentation() -> None:
    """Test creating a presentation."""
    presentation = Presentation()
    assert presentation is not None


def test_add_slide() -> None:
    """Test adding a slide."""
    presentation = Presentation()
    slide = presentation.add_slide("TITLE")
    assert slide is not None
    assert len(presentation.get_slides()) == 1


def test_add_shape() -> None:
    """Test adding a shape."""
    presentation = Presentation()
    slide = presentation.add_slide("TITLE")
    shape = Shape(
        type=MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        left=pt(0),
        top=pt(0),
        width=pt(100),
        height=pt(100),
    )
    slide.shapes.append(shape)
    assert len(slide.shapes) == 1


def test_save_presentation(output: Path) -> None:
    """Test saving a presentation."""
    presentation = Presentation()
    slide = presentation.add_slide("TITLE")
    shape = Shape(
        type=MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        left=pt(0),
        top=pt(0),
        width=pt(100),
        height=pt(100),
        text="Test",
    )
    slide.shapes.append(shape)
    # データオブジェクトに追加したshapeを実際のプレゼンテーションラッパーに反映
    wrapper = presentation._wrapper
    assert wrapper is not None
    wrapper._add_shape(wrapper._presentation.slides[0], shape)
    path = output / "test.pptx"
    presentation.save(path)
    assert path.exists()

    # 保存したPPTXを開いて内容を検証
    pptx_presentation = PptxPresentation(str(path))
    slides = pptx_presentation.slides
    assert len(slides) == 1

    # shape.text を持つシェイプを探して検証
    found = False
    for s in slides[0].shapes:
        if getattr(s, "text", None) == "Test":
            found = True
            break
    assert found
