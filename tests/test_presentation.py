import os
import unittest
from pathlib import Path

from pptxr import (
    Align,
    Chart,
    Container,
    Image,
    Inch,
    Justify,
    Layout,
    LayoutType,
    Point,
    Presentation,
    Slide,
    SlideLayout,
    Text,
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
                Slide(
                    layout=SlideLayout.TITLE_AND_CONTENT,
                    title=Text("シンプルなスライド", size=Point(44), bold=True),
                    containers=[
                        Container(
                            components=[
                                Text(
                                    "これはテストテキストです",
                                    size=Point(24),
                                    layout=Layout(width=Inch(4), height=Inch(1)),
                                )
                            ],
                            layout=Layout(
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
                Slide(
                    layout=SlideLayout.TITLE_AND_CONTENT,
                    title=Text("複雑なレイアウト", size=Point(44), bold=True),
                    containers=[
                        # 横並びのコンテナ
                        Container(
                            components=[
                                Text(
                                    "左側のテキスト",
                                    size=Point(20),
                                    layout=Layout(width=Inch(3), height=Inch(1)),
                                ),
                                Text(
                                    "右側のテキスト",
                                    size=Point(20),
                                    layout=Layout(width=Inch(3), height=Inch(1)),
                                ),
                            ],
                            layout=Layout(
                                type=LayoutType.FLEX,
                                direction="row",
                                justify=Justify.SPACE_BETWEEN,
                                gap=Inch(0.5),
                            ),
                        ),
                        # 縦並びのコンテナ
                        Container(
                            components=[
                                Text(
                                    "上段のテキスト",
                                    size=Point(20),
                                    layout=Layout(width=Inch(6), height=Inch(1)),
                                ),
                                Text(
                                    "下段のテキスト",
                                    size=Point(20),
                                    layout=Layout(width=Inch(6), height=Inch(1)),
                                ),
                            ],
                            layout=Layout(
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
                Slide(
                    layout=SlideLayout.TITLE_AND_CONTENT,
                    title=Text("画像付きスライド", size=Point(44), bold=True),
                    containers=[
                        Container(
                            components=[
                                Image(
                                    path=str(test_image_path),
                                    width=Inch(4),
                                    height=Inch(3),
                                    layout=Layout(width=Inch(4), height=Inch(3)),
                                ),
                                Text(
                                    "画像の説明",
                                    size=Point(20),
                                    layout=Layout(width=Inch(4), height=Inch(1)),
                                ),
                            ],
                            layout=Layout(
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
                Slide(
                    layout=SlideLayout.TITLE_AND_CONTENT,
                    title=Text("チャート付きスライド", size=Point(44), bold=True),
                    containers=[
                        Container(
                            components=[
                                Chart(
                                    type="bar",
                                    data=[
                                        {"category": "A", "value": 10},
                                        {"category": "B", "value": 20},
                                        {"category": "C", "value": 30},
                                    ],
                                    width=Inch(6),
                                    height=Inch(4),
                                    layout=Layout(width=Inch(6), height=Inch(4)),
                                )
                            ],
                            layout=Layout(
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


if __name__ == "__main__":
    unittest.main()
