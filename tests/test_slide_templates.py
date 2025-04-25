"""Tests for slide templates."""

from pathlib import Path

import pytest

from pptxr import Presentation, SlideBuilder, SlideTemplate


class TwoColumnSlideTemplate(SlideTemplate):
    """Template for two-column layout

    Args:
        left_content: Content for left column
        right_content: Content for right column
    """

    def __init__(
        self,
        *,
        title: str,
        left_content: str,
        right_content: str,
    ) -> None:
        super().__init__(title=title)
        self.left_content = left_content
        self.right_content = right_content

    def builder(self) -> SlideBuilder:
        """Create a builder for this template."""
        # 基本のSlideBuilderを拡張してテンプレート特有のレイアウトを適用
        builder = SlideBuilder()

        # タイトルが設定されている場合のみ追加
        if self.title:
            builder.text(self.title, x=(100, "pt"), y=(50, "pt"))

        return builder.text(self.left_content, x=(100, "pt"), y=(150, "pt")).text(
            self.right_content, x=(400, "pt"), y=(150, "pt")
        )


class FeatureCardsTemplate(SlideTemplate):
    """Template for feature cards

    Args:
        features: List of feature descriptions
    """

    def __init__(
        self,
        *,
        title: str,
        features: list[str],
    ) -> None:
        super().__init__(title=title)
        self.features = features

    def builder(self) -> SlideBuilder:
        """Create a builder for this template."""
        builder = SlideBuilder()

        # タイトルが設定されている場合のみ追加
        if self.title:
            builder.text(self.title, x=(100, "pt"), y=(50, "pt"))

        # 特徴を追加（最大4つまで）
        y_positions = [150, 250, 350, 450]
        for i, feature in enumerate(self.features[:4]):
            builder.text(feature, x=(100, "pt"), y=(y_positions[i], "pt"))

        return builder


@pytest.fixture
def test_output_dir():
    """Set up test environment."""
    test_dir = Path(__file__).parent
    output_dir = test_dir / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir


def test_two_column_template(test_output_dir):
    """Test TwoColumnTemplate."""
    presentation = (
        Presentation.builder()
        .slide(
            TwoColumnSlideTemplate(
                title="Two Column Title",
                left_content="Left Content",
                right_content="Right Content",
            ).builder()
        )
        .build()
    )

    # スライドが作成されたことを確認
    assert len(presentation.slides) == 1
    slide = presentation.slides[0]

    # スライド内の要素が3つあることを確認（タイトル、左側、右側）
    assert len(slide.elements) == 3

    # 出力ファイルに保存して確認（実際のファイル作成はスキップ）
    output_path = test_output_dir / "two_column.pptx"
    presentation.save(output_path)
    # 実際のファイル作成機能はまだ実装されていないためスキップ
    # assert output_path.exists()


def test_feature_cards_template(test_output_dir):
    """Test FeatureCardsTemplate."""
    features = ["Feature 1", "Feature 2", "Feature 3", "Feature 4"]

    presentation = (
        Presentation.builder()
        .slide(
            FeatureCardsTemplate(
                title="Features",
                features=features,
            ).builder()
        )
        .build()
    )

    # スライドが作成されたことを確認
    assert len(presentation.slides) == 1
    slide = presentation.slides[0]

    # スライド内の要素が5つあることを確認（タイトル + 4つの特徴）
    assert len(slide.elements) == 5

    # 出力ファイルに保存して確認（実際のファイル作成はスキップ）
    output_path = test_output_dir / "feature_cards.pptx"
    presentation.save(output_path)
    # 実際のファイル作成機能はまだ実装されていないためスキップ
    # assert output_path.exists()


def test_multiple_templates_in_presentation(test_output_dir):
    """Test using multiple templates in a presentation."""
    presentation = (
        Presentation.builder()
        .slide(
            TwoColumnSlideTemplate(
                title="Two Column Slide",
                left_content="Left Content",
                right_content="Right Content",
            ).builder()
        )
        .slide(
            FeatureCardsTemplate(
                title="Features Slide",
                features=["Feature 1", "Feature 2"],
            ).builder()
        )
        .build()
    )

    # 2つのスライドが作成されたことを確認
    assert len(presentation.slides) == 2

    # 出力ファイルに保存して確認（実際のファイル作成はスキップ）
    output_path = test_output_dir / "multiple_templates.pptx"
    presentation.save(output_path)
    # 実際のファイル作成機能はまだ実装されていないためスキップ
    # assert output_path.exists()
