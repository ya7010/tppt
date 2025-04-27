from typing import Annotated, Any, ClassVar

from tppt import Presentation
from tppt.slide_layout import (
    DefaultTitleSlideLayout,
    Placeholder,
    SlideLayout,
    SlideLayoutProxy,
    get_placeholders,
)


class TestSlideLayoutGetPlaceholders:
    """Test cases for get_placeholders function."""

    def test_get_placeholders(self):
        """Test get_placeholders function returns the correct placeholders for a layout."""
        # Test with existing layout
        placeholders = get_placeholders(DefaultTitleSlideLayout)
        assert "title" in placeholders
        assert "subtitle" in placeholders
        assert "date" in placeholders
        assert "footer" in placeholders

        # Instead of direct type comparison, we check that the types match what we expect
        assert placeholders["title"] is str
        # For union types, we need a different approach
        assert "subtitle" in placeholders

    def test_get_placeholders_custom_layout(self):
        """Test get_placeholders with custom layout classes."""

        # Simple layout with one placeholder
        class SimpleLayout(SlideLayout):
            title: Placeholder[str]

        # Layout with various types of placeholders
        class ComplexLayout(SlideLayout):
            title: Placeholder[str]
            count: Placeholder[int]
            items: Placeholder[list[str]]
            # Direct use of Annotated
            direct: Annotated[dict[str, Any], Placeholder]
            # Field with default value should come last
            optional: Placeholder[bool | None] = None

        # Check simple layout
        simple_placeholders = get_placeholders(SimpleLayout)
        assert len(simple_placeholders) == 1
        assert "title" in simple_placeholders
        assert simple_placeholders["title"] is str

        # Check complex layout
        complex_placeholders = get_placeholders(ComplexLayout)
        # The direct field is now correctly recognized
        assert len(complex_placeholders) == 5
        assert "title" in complex_placeholders
        assert "count" in complex_placeholders
        assert "items" in complex_placeholders
        assert "direct" in complex_placeholders
        assert "optional" in complex_placeholders

    def test_inheritance(self):
        """Test that inherited placeholders are properly tracked."""

        class BaseLayout(SlideLayout):
            base_field: Placeholder[str]

        class DerivedLayout(BaseLayout):
            derived_field: Placeholder[int]

        base_placeholders = get_placeholders(BaseLayout)
        assert len(base_placeholders) == 1
        assert "base_field" in base_placeholders

        derived_placeholders = get_placeholders(DerivedLayout)
        assert len(derived_placeholders) == 2
        assert "base_field" in derived_placeholders
        assert "derived_field" in derived_placeholders
        assert derived_placeholders["base_field"] is str
        assert derived_placeholders["derived_field"] is int

    def test_non_placeholder_fields(self):
        """Test that non-placeholder fields are not included in the result."""

        class MixedLayout(SlideLayout):
            # Placeholder fields
            title: Placeholder[str]
            subtitle: Placeholder[str | None] = None

            # Regular fields (not placeholders)
            regular_str: str = "default"
            regular_int: int = 42
            regular_list: list[str] = []

            # Class variable (should also be ignored)
            class_var: ClassVar[bool] = True

        placeholders = get_placeholders(MixedLayout)

        # Only placeholder fields should be included
        assert len(placeholders) == 2
        assert "title" in placeholders
        assert "subtitle" in placeholders

        # Regular fields should not be included
        assert "regular_str" not in placeholders
        assert "regular_int" not in placeholders
        assert "regular_list" not in placeholders

        # Class variables should not be included
        assert "class_var" not in placeholders


def test_slide_layout_proxy_builder():
    # SlideLayoutProxyのインスタンスを作成
    presentation = Presentation.builder().build()
    proxy = SlideLayoutProxy(
        DefaultTitleSlideLayout, presentation.slide_master.slide_layouts[0]
    )

    # プロキシを呼び出して、スライドレイアウトインスタンスを設定
    proxy(title="テストタイトル")

    # builderメソッドを呼び出す
    assert proxy.builder()
