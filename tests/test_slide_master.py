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
)
from tppt.slide_master import DefaultSlideMaster, get_layouts


def test_get_layouts():
    """Test that get_layouts function correctly retrieves the list of Layouts"""
    layouts = get_layouts(DefaultSlideMaster)

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
