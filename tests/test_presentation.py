import os
import unittest
from pathlib import Path
from pptxr import (
    create_presentation, Slide, SlideLayout, Text, Image, Chart,
    Component, Container, Layout, LayoutType, Align, Justify
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
            create_presentation()
            .add_slide(
                Slide(
                    layout=SlideLayout.TITLE_AND_CONTENT,
                    title=Text("シンプルなスライド", size=44, bold=True),
                    containers=[
                        Container(
                            components=[
                                Component(
                                    type="text",
                                    content=Text("これはテストテキストです", size=24),
                                    layout=Layout(width=4, height=1)
                                )
                            ],
                            layout=Layout(
                                type=LayoutType.FLEX,
                                direction="column",
                                align=Align.CENTER
                            )
                        )
                    ]
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
            create_presentation()
            .add_slide(
                Slide(
                    layout=SlideLayout.TITLE_AND_CONTENT,
                    title=Text("複雑なレイアウト", size=44, bold=True),
                    containers=[
                        # 横並びのコンテナ
                        Container(
                            components=[
                                Component(
                                    type="text",
                                    content=Text("左側のテキスト", size=20),
                                    layout=Layout(width=3, height=1)
                                ),
                                Component(
                                    type="text",
                                    content=Text("右側のテキスト", size=20),
                                    layout=Layout(width=3, height=1)
                                )
                            ],
                            layout=Layout(
                                type=LayoutType.FLEX,
                                direction="row",
                                justify=Justify.SPACE_BETWEEN,
                                gap=0.5
                            )
                        ),
                        # 縦並びのコンテナ
                        Container(
                            components=[
                                Component(
                                    type="text",
                                    content=Text("上段のテキスト", size=20),
                                    layout=Layout(width=6, height=1)
                                ),
                                Component(
                                    type="text",
                                    content=Text("下段のテキスト", size=20),
                                    layout=Layout(width=6, height=1)
                                )
                            ],
                            layout=Layout(
                                type=LayoutType.FLEX,
                                direction="column",
                                align=Align.CENTER,
                                gap=0.5
                            )
                        )
                    ]
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
            img = PILImage.new('RGB', (100, 100), color='red')
            img.save(str(test_image_path))

        presentation = (
            create_presentation()
            .add_slide(
                Slide(
                    layout=SlideLayout.TITLE_AND_CONTENT,
                    title=Text("画像付きスライド", size=44, bold=True),
                    containers=[
                        Container(
                            components=[
                                Component(
                                    type="image",
                                    content=Image(
                                        path=str(test_image_path),
                                        width=4,
                                        height=3
                                    ),
                                    layout=Layout(width=4, height=3)
                                ),
                                Component(
                                    type="text",
                                    content=Text("画像の説明", size=20),
                                    layout=Layout(width=4, height=1)
                                )
                            ],
                            layout=Layout(
                                type=LayoutType.FLEX,
                                direction="column",
                                align=Align.CENTER,
                                gap=0.5
                            )
                        )
                    ]
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
            create_presentation()
            .add_slide(
                Slide(
                    layout=SlideLayout.TITLE_AND_CONTENT,
                    title=Text("チャート付きスライド", size=44, bold=True),
                    containers=[
                        Container(
                            components=[
                                Component(
                                    type="chart",
                                    content=Chart(
                                        type="bar",
                                        data=[
                                            {"category": "A", "value": 10},
                                            {"category": "B", "value": 20},
                                            {"category": "C", "value": 30}
                                        ],
                                        width=6,
                                        height=4
                                    ),
                                    layout=Layout(width=6, height=4)
                                )
                            ],
                            layout=Layout(
                                type=LayoutType.FLEX,
                                direction="column",
                                align=Align.CENTER
                            )
                        )
                    ]
                )
            )
            .build()
        )
        
        output_path = self.output_dir / "with_chart.pptx"
        presentation.save(str(output_path))
        self.assertTrue(output_path.exists())

if __name__ == '__main__':
    unittest.main() 