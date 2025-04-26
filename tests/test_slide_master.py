
from tppt.slide_layout import (
    DefaultBlankSlide,
    DefaultComparisonSlide,
    DefaultContentWithCaptionSlide,
    DefaultMasterSlide,
    DefaultPictureWithCaptionSlide,
    DefaultSectionHeaderSlide,
    DefaultTitleAndContentSlide,
    DefaultTitleAndVerticalTextSlide,
    DefaultTitleOnlySlide,
    DefaultTitleSlide,
    DefaultTwoContentSlide,
    DefaultVerticalTitleAndTextSlide,
)
from tppt.slide_master import DefaultSlideMaster, get_layouts, get_master_layout


def test_get_master_layout():
    """Test that get_master_layout function correctly retrieves the MasterLayout"""
    master_layout = get_master_layout(DefaultSlideMaster)
    assert master_layout == DefaultMasterSlide


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
    assert DefaultMasterSlide not in layouts
