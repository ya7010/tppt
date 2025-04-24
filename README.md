# pptxr

pptxrは型安全なPowerPointプレゼンテーションビルダーです。このライブラリを使用すると、Pythonコードからパワーポイントを簡単に生成できます。

## インストール

```bash
pip install pptxr
```

## 使用例

```python
from pptxr import Presentation, SlideTemplate, SlideMaster, SlideBuilder


class MySlideTemplate(SlideTemplate):
    """Custom slide template."""
    pass


class MyTitleSlide(MySlideTemplate):
    """Custom title slide."""
    pass


# スライドマスターを作成
sm = SlideMaster(template_class=MySlideTemplate)

# ビルダーパターンを使用してプレゼンテーションを作成
presentation = (
    Presentation.builder(sm)
    .slide(
        SlideBuilder()
        .text("Hello, world!", x=(100, "pt"), y=(100, "pt"))
        .image(path="image.png", width=(100, "pt"), height=(100, "pt"))
    )
    .build()
)

# プレゼンテーションを保存
presentation.save("output.pptx")
```

## 特徴

- 型安全なインターフェース
- ビルダーパターンによる直感的なAPI
- カスタムスライドテンプレートのサポート

## アーキテクチャ

このライブラリは以下のモジュールで構成されています：

- `types`: 長さや色などの型安全な基本型
- `_data`: データクラス
- `_builders`: ビルダーパターンの実装
- `_presentation`: プレゼンテーションクラス
- `_slide_master`: スライドマスタークラス
- `_pptxr`: python-pptxとのインターフェース

## ライセンス

MIT
