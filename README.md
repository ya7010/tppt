# tppt

tpptは型安全なPowerPointプレゼンテーションビルダーです。このライブラリを使用すると、Pythonコードからパワーポイントを簡単に生成できます。

## インストール

```bash
pip install tppt
```

## 使用例

```python
from pathlib import Path
import tppt
from tppt.types import Color

# ビルダーパターンを使用してプレゼンテーションを作成
presentation = (
    tppt.Presentation.builder()
    .slide(
        tppt.SlideBuilder()
        .text(
            "Amazing Presentation",
            left=(50, "pt"),
            top=(50, "pt"),
            width=(400, "pt"),
            height=(50, "pt"),
            size=(60, "pt"),
            bold=True,
            italic=True,
            color=Color("#0000FF"),
        )
        .text(
            "Example of using tppt library",
            left=(50, "pt"),
            top=(120, "pt"),
            width=(400, "pt"),
            height=(30, "pt"),
        )
    )
    .slide(
        tppt.SlideBuilder()
        .text(
            "画像の例",
            left=(50, "pt"),
            top=(50, "pt"),
            width=(300, "pt"),
            height=(40, "pt"),
        )
        .picture(
            "image.png",
            left=(50, "pt"),
            top=(100, "pt"),
            width=(300, "pt"),
            height=(80, "pt"),
        )
    )
    .slide(
        tppt.SlideBuilder()
        .text(
            "表の例",
            left=(50, "pt"),
            top=(50, "pt"),
            width=(300, "pt"),
            height=(40, "pt"),
        )
        .table(
            [
                ["製品", "価格", "在庫"],
                ["製品A", "¥1,000", "10個"],
                ["製品B", "¥2,500", "5個"],
            ],
            left=(50, "pt"),
            top=(100, "pt"),
            width=(400, "pt"),
            height=(200, "pt"),
        )
    )
    .build()
)

# プレゼンテーションを保存
presentation.save("output.pptx")
```

## 特徴

- 型安全なインターフェース
- ビルダーパターンによる直感的なAPI
- テキスト、画像、表などの要素を簡単に配置
- 位置やサイズの細かな調整が可能
- テキストのスタイル（サイズ、太字、斜体、色）のカスタマイズ

## アーキテクチャ

このライブラリは以下のモジュールで構成されています：

- `types`: 長さや色などの型安全な基本型
- `_data`: データクラス
- `_builders`: ビルダーパターンの実装
- `_presentation`: プレゼンテーションクラス
- `_slide_master`: スライドマスタークラス
- `_tppt`: python-pptxとのインターフェース

## ライセンス

MIT
