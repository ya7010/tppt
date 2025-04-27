from tppt.slide_layout import (
    DefaultBlankSlideLayout,
    DefaultComparisonSlideLayout,
    DefaultContentWithCaptionSlideLayout,
    DefaultPictureWithCaptionSlideLayout,
    DefaultSectionHeaderSlideLayout,
    DefaultTitleAndContentSlideLayout,
    DefaultTitleAndVerticalTextSlideLayout,
    DefaultTitleOnlySlideLayout,
    DefaultTitleSlideLayout,
    DefaultTwoContentSlideLayout,
    DefaultVerticalTitleAndTextSlideLayout,
    Placeholder,
)
from tppt.slide_master import DefaultSlideMaster, Layout, get_layouts


class TestSlideMaster(DefaultSlideMaster):
    title: Placeholder[str]
    content: Placeholder[str]

    Title: Layout[DefaultTitleSlideLayout]
    TitleAndContent: Layout[DefaultTitleAndContentSlideLayout]
    SectionHeader: Layout[DefaultSectionHeaderSlideLayout]
    TwoContent: Layout[DefaultTwoContentSlideLayout]
    Comparison: Layout[DefaultComparisonSlideLayout]
    TitleOnly: Layout[DefaultTitleOnlySlideLayout]
    Blank: Layout[DefaultBlankSlideLayout]
    ContentWithCaption: Layout[DefaultContentWithCaptionSlideLayout]
    PictureWithCaption: Layout[DefaultPictureWithCaptionSlideLayout]
    TitleAndVerticalText: Layout[DefaultTitleAndVerticalTextSlideLayout]
    VerticalTitleAndText: Layout[DefaultVerticalTitleAndTextSlideLayout]


def test_get_layouts():
    """Test that get_layouts function correctly retrieves the list of Layouts"""
    layouts = get_layouts(TestSlideMaster)

    # Verify that all Layouts are included
    expected_layouts = [
        DefaultTitleSlideLayout,
        DefaultTitleAndContentSlideLayout,
        DefaultSectionHeaderSlideLayout,
        DefaultTwoContentSlideLayout,
        DefaultComparisonSlideLayout,
        DefaultTitleOnlySlideLayout,
        DefaultBlankSlideLayout,
        DefaultContentWithCaptionSlideLayout,
        DefaultPictureWithCaptionSlideLayout,
        DefaultTitleAndVerticalTextSlideLayout,
        DefaultVerticalTitleAndTextSlideLayout,
    ]

    # Convert to sets for comparison as the order is not guaranteed
    assert set(layouts) == set(expected_layouts)

    # Verify that MasterLayout is not included
    assert str not in layouts
