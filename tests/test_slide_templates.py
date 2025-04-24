from typing import Optional, cast

import pytest

from pptxr import (
    Align,
    Chart,
    Component,
    Container,
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
        left_content: Optional[Text] = None,
        right_content: Optional[Text] = None,
        **kwargs,
    ) -> Slide:
        return slide(
            layout=SlideLayout.TITLE_AND_CONTENT,
            title=title,
            containers=[
                Container(
                    components=[
                        left_content or text("Left Column"),
                        right_content or text("Right Column"),
                    ],
                    layout=layout(
                        type=LayoutType.FLEX,
                        direction="row",
                        justify=Justify.SPACE_BETWEEN,
                        gap=(0.5, "in"),
                    ),
                )
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
        chart_data: Optional[Chart] = None,
        description: Optional[Text] = None,
        **kwargs,
    ) -> Slide:
        default_chart = chart("bar", [])
        return slide(
            layout=SlideLayout.TITLE_AND_CONTENT,
            title=title,
            containers=[
                Container(
                    components=[
                        chart_data if chart_data is not None else default_chart,
                        description or text("Chart Description"),
                    ],
                    layout=layout(
                        type=LayoutType.FLEX,
                        direction="column",
                        align=Align.CENTER,
                        gap=(0.5, "in"),
                    ),
                )
            ],
        )


class FeatureCardsTemplate(SlideTemplate):
    """Template for 2x2 feature cards

    Args:
        features (list[Text]): List of feature descriptions (max 4)
    """

    def build(
        self,
        title: Optional[Text] = None,
        features: Optional[list[Text]] = None,
        **kwargs,
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
                Container(
                    components=cast(list[Component], features or default_features),
                    layout=layout(type=LayoutType.GRID, gap=(0.5, "in")),
                )
            ],
        )


def test_two_column_template():
    """Test TwoColumnTemplate"""
    template = TwoColumnTemplate()

    # Test with default values
    slide_obj = template.build()
    assert slide_obj["layout"] == SlideLayout.TITLE_AND_CONTENT
    containers = slide_obj.get("containers", [])
    assert len(containers) == 1
    assert len(containers[0]["components"]) == 2
    layout = containers[0]["layout"]
    assert layout.get("type") == LayoutType.FLEX
    assert layout.get("direction") == "row"
    assert layout.get("justify") == Justify.SPACE_BETWEEN
    assert layout.get("gap") == (0.5, "in")

    # Test with custom values
    left_content = text("Custom Left")
    right_content = text("Custom Right")
    title = text("Custom Title")

    slide_obj = template.build(
        title=title, left_content=left_content, right_content=right_content
    )

    assert slide_obj.get("title") == title
    containers = slide_obj.get("containers", [])
    assert containers[0]["components"][0] == left_content
    assert containers[0]["components"][1] == right_content


def test_chart_with_description_template():
    """Test ChartWithDescriptionTemplate"""
    template = ChartWithDescriptionTemplate()

    # Test with default values
    slide_obj = template.build()
    assert slide_obj["layout"] == SlideLayout.TITLE_AND_CONTENT
    containers = slide_obj.get("containers", [])
    assert len(containers) == 1
    assert len(containers[0]["components"]) == 2
    layout = containers[0]["layout"]
    assert layout.get("type") == LayoutType.FLEX
    assert layout.get("direction") == "column"
    assert layout.get("align") == Align.CENTER
    assert layout.get("gap") == (0.5, "in")

    # Test with custom values
    chart_data = chart("bar", [{"value": 1}, {"value": 2}])
    description = text("Custom Description")
    title = text("Custom Title")

    slide_obj = template.build(
        title=title, chart_data=chart_data, description=description
    )

    assert slide_obj.get("title") == title
    containers = slide_obj.get("containers", [])
    assert containers[0]["components"][0] == chart_data
    assert containers[0]["components"][1] == description


def test_feature_cards_template():
    """Test FeatureCardsTemplate"""
    template = FeatureCardsTemplate()

    # Test with default values
    slide_obj = template.build()
    assert slide_obj["layout"] == SlideLayout.TITLE_AND_CONTENT
    containers = slide_obj.get("containers", [])
    assert len(containers) == 1
    assert len(containers[0]["components"]) == 4
    layout = containers[0]["layout"]
    assert layout.get("type") == LayoutType.GRID
    assert layout.get("gap") == (0.5, "in")

    # Test with custom values
    features = [
        text("Feature 1"),
        text("Feature 2"),
        text("Feature 3"),
    ]
    title = text("Custom Title")

    slide_obj = template.build(title=title, features=features)

    assert slide_obj.get("title") == title
    containers = slide_obj.get("containers", [])
    assert containers[0]["components"] == features

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
            chart_data=chart("bar", [{"category": "A", "value": 1}]),
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
