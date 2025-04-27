from tppt.slide_layout import (
    DefaultBlankSlide,
    DefaultComparisonSlide,
    DefaultContentWithCaptionSlide,
    DefaultPictureWithCaptionSlide,
    DefaultSectionHeaderSlide,
    DefaultTitleAndContentSlide,
    DefaultTitleAndVerticalTextSlide,
    DefaultTitleOnlySlide,
    DefaultTitleSlide,
    DefaultTwoContentSlide,
    DefaultVerticalTitleAndTextSlide,
    Placeholder,
)
from tppt.slide_master import DefaultSlideMaster, Layout, get_layouts


class TestSlideMaster(DefaultSlideMaster):
    title: Placeholder[str]
    content: Placeholder[str]

    Title: Layout[DefaultTitleSlide]
    TitleAndContent: Layout[DefaultTitleAndContentSlide]
    SectionHeader: Layout[DefaultSectionHeaderSlide]
    TwoContent: Layout[DefaultTwoContentSlide]
    Comparison: Layout[DefaultComparisonSlide]
    TitleOnly: Layout[DefaultTitleOnlySlide]
    Blank: Layout[DefaultBlankSlide]
    ContentWithCaption: Layout[DefaultContentWithCaptionSlide]
    PictureWithCaption: Layout[DefaultPictureWithCaptionSlide]
    TitleAndVerticalText: Layout[DefaultTitleAndVerticalTextSlide]
    VerticalTitleAndText: Layout[DefaultVerticalTitleAndTextSlide]


def test_get_layouts():
    """Test that get_layouts function correctly retrieves the list of Layouts"""
    layouts = get_layouts(TestSlideMaster)

    # Verify that all Layouts are included
    expected_layouts = [
        DefaultTitleSlide,
        DefaultTitleAndContentSlide,
        DefaultSectionHeaderSlide,
        DefaultTwoContentSlide,
        DefaultComparisonSlide,
        DefaultTitleOnlySlide,
        DefaultBlankSlide,
        DefaultContentWithCaptionSlide,
        DefaultPictureWithCaptionSlide,
        DefaultTitleAndVerticalTextSlide,
        DefaultVerticalTitleAndTextSlide,
    ]

    # Convert to sets for comparison as the order is not guaranteed
    assert set(layouts) == set(expected_layouts)

    # Verify that MasterLayout is not included
    assert str not in layouts
