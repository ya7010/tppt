from typing import cast

import pytest

from pptxr import (
    Component,
    Container,
    Presentation,
    Slide,
    SlideTemplate,
    Text,
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

    def __init__(
        self,
        *,
        title: Text,
        left_content: Text,
        right_content: Text,
    ) -> None:
        self.title = title
        self.left_content = left_content
        self.right_content = right_content

    def build(self) -> Slide:
        return slide(
            layout="TITLE_AND_CONTENT",
            title=self.title,
            containers=[
                Container(
                    components=[
                        self.left_content,
                        self.right_content,
                    ],
                    layout=layout(
                        type="flex",
                        direction="row",
                        justify="space-between",
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

    def __init__(
        self,
        *,
        title: Text,
        features: list[Text],
    ) -> None:
        self.title = title
        self.features = features

    def build(self) -> Slide:
        if self.features and len(self.features) > 4:
            raise ValueError("Maximum 4 features allowed")

        default_features = [
            text("Feature 1"),
            text("Feature 2"),
            text("Feature 3"),
            text("Feature 4"),
        ]

        return slide(
            layout="TITLE_AND_CONTENT",
            title=self.title,
            containers=[
                Container(
                    components=cast(list[Component], self.features or default_features),
                    layout=layout(type="grid", gap=(0.5, "in")),
                )
            ],
        )


def test_two_column_template():
    """Test TwoColumnTemplate"""
    template = TwoColumnTemplate(
        title=text("Title"),
        left_content=text("Left"),
        right_content=text("Right"),
    )

    slide = template.build()
    assert slide.get("title") == text("Title")
    containers = slide.get("containers", [])
    assert len(containers) > 0
    assert containers[0].get("components") == [text("Left"), text("Right")]


def test_feature_cards_template():
    """Test FeatureCardsTemplate"""
    # Test 1: Normal features
    template = FeatureCardsTemplate(
        title=text("Title"),
        features=[
            text("Feature 1"),
            text("Feature 2"),
            text("Feature 3"),
            text("Feature 4"),
        ],
    )

    slide_obj = template.build()
    assert slide_obj.get("layout") == "TITLE_AND_CONTENT"
    containers = slide_obj.get("containers", [])
    assert len(containers) == 1
    assert len(containers[0].get("components", [])) == 4
    layout = containers[0].get("layout", {})
    assert layout.get("type") == "grid"
    assert layout.get("gap") == (0.5, "in")

    # Test 2: With custom values
    features = [
        text("Feature 1"),
        text("Feature 2"),
        text("Feature 3"),
    ]
    template = FeatureCardsTemplate(
        title=text("Custom Title"),
        features=features,
    )

    slide_obj = template.build()

    assert slide_obj.get("title") == text("Custom Title")
    containers = slide_obj.get("containers", [])
    assert containers[0].get("components") == features

    # Test 3: With too many features
    template = FeatureCardsTemplate(
        title=text("Too Many"),
        features=[text(f"Feature {i}") for i in range(1, 6)],  # 5 features
    )

    with pytest.raises(ValueError):
        template.build()


def test_template_in_presentation():
    """Test using templates in presentation"""
    presentation = (
        Presentation.builder()
        .add_slide(
            TwoColumnTemplate(
                title=text("Two Column"),
                left_content=text("Left"),
                right_content=text("Right"),
            )
        )
        .add_slide(
            FeatureCardsTemplate(
                title=text("Features"),
                features=[text("Feature 1"), text("Feature 2")],
            )
        )
        .build()
    )

    assert len(presentation.slides) == 3
