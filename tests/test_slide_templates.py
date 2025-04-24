from pptxr import (
    DefaultSlideBuilder,
    Presentation,
    Slide,
    SlideBuilder,
    SlideTemplate,
    Text,
)


class TwoColumnSlideTemplate(SlideTemplate):
    """Template for two-column layout

    Args:
        left_content (Text): Content for left column
        right_content (Text): Content for right column
    """

    def __init__(
        self,
        *,
        title: Text | str,
        left_content: Text | str,
        right_content: Text | str,
    ) -> None:
        self.title = title
        self.left_content = left_content
        self.right_content = right_content

    def builder(self) -> DefaultSlideBuilder:
        return DefaultSlideBuilder(
            slide=Slide(
                layout=1,
                placeholders=[],
                components=[],
            )
        )


class FeatureCardsTemplate(SlideBuilder):
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

    def buildr(self) -> DefaultSlideBuilder:
        return DefaultSlideBuilder(
            slide=Slide(
                layout=2,
                placeholders=[],
                components=[],
            )
        )


def test_two_column_template():
    """Test TwoColumnTemplate"""

    presentation = (
        Presentation.builder()
        .add_slide(
            TwoColumnSlideTemplate(
                title="Title",
                left_content="Left",
                right_content="Right",
            )
        )
        .build()
    )

    slide = presentation.slides[0]
    assert slide


def test_feature_cards_template():
    """Test FeatureCardsTemplate"""

    presentation = (
        Presentation.builder()
        .add_slide(
            FeatureCardsTemplate(
                title=text("Title"),
                features=[
                    text("Feature 1"),
                    text("Feature 2"),
                    text("Feature 3"),
                    text("Feature 4"),
                ],
            )
        )
        .add_slide(
            FeatureCardsTemplate(
                title=text("Title"),
                features=[
                    text("Feature 1"),
                    text("Feature 2"),
                    text("Feature 3"),
                    text("Feature 4"),
                ],
            )
        )
        .build()
    )

    slide = presentation.slides[0]
    assert slide


def test_template_in_presentation():
    """Test using templates in presentation"""
    presentation = (
        Presentation.builder()
        .add_slide(
            TwoColumnSlideTemplate(
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

    assert len(presentation.slides) == 2
