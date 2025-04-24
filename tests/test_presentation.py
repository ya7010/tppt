import os
import unittest
from pathlib import Path

from pptxr import (
    Align,
    Container,
    Inch,
    Justify,
    LayoutType,
    Point,
    Presentation,
    SlideLayout,
    create_chart,
    create_image,
    create_layout,
    create_slide,
    create_text,
)


class TestPresentation(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(__file__).parent
        self.resources_dir = self.test_dir / "resources"
        self.output_dir = self.test_dir / "output"
        os.makedirs(self.resources_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def test_create_simple_presentation(self):
        # シンプルなプレゼンテーションの作成
        presentation = (
            Presentation.builder()
            .add_slide(
                create_slide(
                    layout=SlideLayout.TITLE_AND_CONTENT,
                    title=create_text("シンプルなスライド", size=Point(44), bold=True),
                    containers=[
                        Container(
                            components=[
                                create_text(
                                    "これはテストテキストです",
                                    size=Point(24),
                                    layout=create_layout(width=Inch(4), height=Inch(1)),
                                )
                            ],
                            layout=create_layout(
                                type=LayoutType.FLEX,
                                direction="column",
                                align=Align.CENTER,
                            ),
                        )
                    ],
                )
            )
            .build()
        )

        output_path = self.output_dir / "simple.pptx"
        presentation.save(str(output_path))
        self.assertTrue(output_path.exists())

    def test_create_complex_presentation(self):
        # より複雑なレイアウトのプレゼンテーション
        presentation = (
            Presentation.builder()
            .add_slide(
                create_slide(
                    layout=SlideLayout.TITLE_AND_CONTENT,
                    title=create_text("複雑なレイアウト", size=Point(44), bold=True),
                    containers=[
                        # 横並びのコンテナ
                        Container(
                            components=[
                                create_text(
                                    "左側のテキスト",
                                    size=Point(20),
                                    layout=create_layout(width=Inch(3), height=Inch(1)),
                                ),
                                create_text(
                                    "右側のテキスト",
                                    size=Point(20),
                                    layout=create_layout(width=Inch(3), height=Inch(1)),
                                ),
                            ],
                            layout=create_layout(
                                type=LayoutType.FLEX,
                                direction="row",
                                justify=Justify.SPACE_BETWEEN,
                                gap=Inch(0.5),
                            ),
                        ),
                        # 縦並びのコンテナ
                        Container(
                            components=[
                                create_text(
                                    "上段のテキスト",
                                    size=Point(20),
                                    layout=create_layout(width=Inch(6), height=Inch(1)),
                                ),
                                create_text(
                                    "下段のテキスト",
                                    size=Point(20),
                                    layout=create_layout(width=Inch(6), height=Inch(1)),
                                ),
                            ],
                            layout=create_layout(
                                type=LayoutType.FLEX,
                                direction="column",
                                align=Align.CENTER,
                                gap=Inch(0.5),
                            ),
                        ),
                    ],
                )
            )
            .build()
        )

        output_path = self.output_dir / "complex.pptx"
        presentation.save(str(output_path))
        self.assertTrue(output_path.exists())

    def test_create_presentation_with_image(self):
        # 画像を含むプレゼンテーション
        # 注意: テスト用の画像ファイルが必要です
        test_image_path = self.resources_dir / "test_image.jpg"
        if not test_image_path.exists():
            # テスト用のダミー画像を作成
            from PIL import Image as PILImage

            img = PILImage.new("RGB", (100, 100), color="red")
            img.save(str(test_image_path))

        presentation = (
            Presentation.builder()
            .add_slide(
                create_slide(
                    layout=SlideLayout.TITLE_AND_CONTENT,
                    title=create_text("画像付きスライド", size=Point(44), bold=True),
                    containers=[
                        Container(
                            components=[
                                create_image(
                                    path=str(test_image_path),
                                    width=Inch(4),
                                    height=Inch(3),
                                    layout=create_layout(width=Inch(4), height=Inch(3)),
                                ),
                                create_text(
                                    "画像の説明",
                                    size=Point(20),
                                    layout=create_layout(width=Inch(4), height=Inch(1)),
                                ),
                            ],
                            layout=create_layout(
                                type=LayoutType.FLEX,
                                direction="column",
                                align=Align.CENTER,
                                gap=Inch(0.5),
                            ),
                        )
                    ],
                )
            )
            .build()
        )

        output_path = self.output_dir / "with_image.pptx"
        presentation.save(str(output_path))
        self.assertTrue(output_path.exists())

    def test_create_presentation_with_chart(self):
        # チャートを含むプレゼンテーション
        presentation = (
            Presentation.builder()
            .add_slide(
                create_slide(
                    layout=SlideLayout.TITLE_AND_CONTENT,
                    title=create_text(
                        "チャート付きスライド", size=Point(44), bold=True
                    ),
                    containers=[
                        Container(
                            components=[
                                create_chart(
                                    chart_type="bar",
                                    data=[
                                        {"category": "A", "value": 10},
                                        {"category": "B", "value": 20},
                                        {"category": "C", "value": 30},
                                    ],
                                    width=Inch(6),
                                    height=Inch(4),
                                    layout=create_layout(width=Inch(6), height=Inch(4)),
                                )
                            ],
                            layout=create_layout(
                                type=LayoutType.FLEX,
                                direction="column",
                                align=Align.CENTER,
                            ),
                        )
                    ],
                )
            )
            .build()
        )

        output_path = self.output_dir / "with_chart.pptx"
        presentation.save(str(output_path))
        self.assertTrue(output_path.exists())

    def test_create_presentation_with_keyword_args(self):
        # キーワード引数を使用したプレゼンテーションの作成
        presentation = (
            Presentation.builder()
            .add_slide(
                layout=SlideLayout.TITLE_AND_CONTENT,
                title=create_text("キーワード引数テスト", size=Point(44), bold=True),
                containers=[
                    Container(
                        components=[
                            create_text(
                                "キーワード引数で作成したスライド",
                                size=Point(24),
                                layout=create_layout(width=Inch(4), height=Inch(1)),
                            )
                        ],
                        layout=create_layout(
                            type=LayoutType.FLEX,
                            direction="column",
                            align=Align.CENTER,
                        ),
                    )
                ],
            )
            .build()
        )

        output_path = self.output_dir / "keyword_args.pptx"
        presentation.save(str(output_path))
        self.assertTrue(output_path.exists())


if __name__ == "__main__":
    unittest.main()
