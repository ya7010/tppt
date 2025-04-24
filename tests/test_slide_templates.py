from typing import Optional

import pytest

from pptxr import (
    Align,
    Chart,
    Inch,
    Justify,
    LayoutType,
    Presentation,
    Slide,
    SlideLayout,
    SlideTemplate,
    Text,
    chart,
    layout,
    slide,
    text,
)


class TwoColumnTemplate(SlideTemplate):
    """Template for two-column layout

    Args:
        left_content (Text): Content for left column
        right_content (Text): Content for right column
    """

    def build(
        self,
        title: Optional[Text] = None,
        left_content: Text = None,
        right_content: Text = None,
        **kwargs,
    ) -> Slide:
        return slide(
            layout=SlideLayout.TITLE_AND_CONTENT,
            title=title,
            containers=[
                {
                    "components": [
                        left_content or text("Left Column"),
                        right_content or text("Right Column"),
                    ],
                    "layout": layout(
                        type=LayoutType.FLEX,
                        direction="row",
                        justify=Justify.SPACE_BETWEEN,
                        gap=Inch(0.5),
                    ),
                }
            ],
        )


class ChartWithDescriptionTemplate(SlideTemplate):
    """Template for chart with description

    Args:
        chart (Chart): Chart component
        description (Text): Description text
    """

    def build(
        self,
        title: Optional[Text] = None,
        chart: Chart = None,
        description: Text = None,
        **kwargs,
    ) -> Slide:
        return slide(
            layout=SlideLayout.TITLE_AND_CONTENT,
            title=title,
            containers=[
                {
                    "components": [
                        chart or chart("bar", []),
                        description or text("Chart Description"),
                    ],
                    "layout": layout(
                        type=LayoutType.FLEX,
                        direction="column",
                        align=Align.CENTER,
                        gap=Inch(0.5),
                    ),
                }
            ],
        )


class FeatureCardsTemplate(SlideTemplate):
    """Template for 2x2 feature cards

    Args:
        features (list[Text]): List of feature descriptions (max 4)
    """

    def build(
        self, title: Optional[Text] = None, features: list[Text] = None, **kwargs
    ) -> Slide:
        if features and len(features) > 4:
            raise ValueError("Maximum 4 features allowed")

        default_features = [
            text("Feature 1"),
            text("Feature 2"),
            text("Feature 3"),
            text("Feature 4"),
        ]

        return slide(
            layout=SlideLayout.TITLE_AND_CONTENT,
            title=title,
            containers=[
                {
                    "components": features or default_features,
                    "layout": layout(type=LayoutType.GRID, gap=Inch(0.5)),
                }
            ],
        )


def test_two_column_template():
    """Test TwoColumnTemplate"""
    template = TwoColumnTemplate()

    # Test with default values
    slide = template.build()
    assert slide["layout"] == SlideLayout.TITLE_AND_CONTENT
    assert len(slide["containers"]) == 1
    assert len(slide["containers"][0]["components"]) == 2
    assert slide["containers"][0]["layout"]["type"] == LayoutType.FLEX
    assert slide["containers"][0]["layout"]["direction"] == "row"
    assert slide["containers"][0]["layout"]["justify"] == Justify.SPACE_BETWEEN
    assert slide["containers"][0]["layout"]["gap"] == Inch(0.5)

    # Test with custom values
    left_content = text("Custom Left")
    right_content = text("Custom Right")
    title = text("Custom Title")

    slide = template.build(
        title=title, left_content=left_content, right_content=right_content
    )

    assert slide["title"] == title
    assert slide["containers"][0]["components"][0] == left_content
    assert slide["containers"][0]["components"][1] == right_content


def test_chart_with_description_template():
    """Test ChartWithDescriptionTemplate"""
    template = ChartWithDescriptionTemplate()

    # Test with default values
    slide = template.build()
    assert slide["layout"] == SlideLayout.TITLE_AND_CONTENT
    assert len(slide["containers"]) == 1
    assert len(slide["containers"][0]["components"]) == 2
    assert slide["containers"][0]["layout"]["type"] == LayoutType.FLEX
    assert slide["containers"][0]["layout"]["direction"] == "column"
    assert slide["containers"][0]["layout"]["align"] == Align.CENTER
    assert slide["containers"][0]["layout"]["gap"] == Inch(0.5)

    # Test with custom values
    chart = chart("bar", [{"value": 1}, {"value": 2}])
    description = text("Custom Description")
    title = text("Custom Title")

    slide = template.build(title=title, chart=chart, description=description)

    assert slide["title"] == title
    assert slide["containers"][0]["components"][0] == chart
    assert slide["containers"][0]["components"][1] == description


def test_feature_cards_template():
    """Test FeatureCardsTemplate"""
    template = FeatureCardsTemplate()

    # Test with default values
    slide = template.build()
    assert slide["layout"] == SlideLayout.TITLE_AND_CONTENT
    assert len(slide["containers"]) == 1
    assert len(slide["containers"][0]["components"]) == 4
    assert slide["containers"][0]["layout"]["type"] == LayoutType.GRID
    assert slide["containers"][0]["layout"]["gap"] == Inch(0.5)

    # Test with custom values
    features = [
        text("Feature 1"),
        text("Feature 2"),
        text("Feature 3"),
    ]
    title = text("Custom Title")

    slide = template.build(title=title, features=features)

    assert slide["title"] == title
    assert slide["containers"][0]["components"] == features

    # Test with too many features
    with pytest.raises(ValueError):
        template.build(features=[text(f"Feature {i}") for i in range(5)])


def test_template_in_presentation():
    """Test using templates in presentation"""
    presentation = (
        Presentation.builder()
        .add_slide(
            TwoColumnTemplate(),
            title=text("Two Column"),
            left_content=text("Left"),
            right_content=text("Right"),
        )
        .add_slide(
            ChartWithDescriptionTemplate(),
            title=text("Chart"),
            chart=chart("bar", [{"value": 1}]),
            description=text("Description"),
        )
        .add_slide(
            FeatureCardsTemplate(),
            title=text("Features"),
            features=[text("Feature 1"), text("Feature 2")],
        )
        .build()
    )

    assert len(presentation.slides) == 3
