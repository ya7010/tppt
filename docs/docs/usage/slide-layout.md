# スライドレイアウト

TPPTでは、スライドのレイアウトを柔軟にカスタマイズすることができます。ここでは、基本的なレイアウトの設定方法と、よく使用されるパターンについて説明します。

## 基本的なレイアウト設定

### 1. スライドサイズの設定
```python
from tppt import Presentation

# 16:9のワイドスクリーン形式
presentation = Presentation(slide_width=16, slide_height=9)

# 4:3の標準形式
presentation = Presentation(slide_width=4, slide_height=3)
```

### 2. マージンの設定
```python
# スライドの余白を設定
slide = presentation.add_slide()
slide.set_margins(left=1.0, right=1.0, top=0.5, bottom=0.5)
```

## 一般的なレイアウトパターン

### 1. タイトルスライド
```python
slide = presentation.add_slide()
slide.add_title("プレゼンテーションのタイトル")
slide.add_subtitle("サブタイトル")
```

### 2. 2カラムレイアウト
```python
slide = presentation.add_slide()
left_column = slide.add_column(width=0.5)
right_column = slide.add_column(width=0.5)

left_column.add_text("左側のコンテンツ")
right_column.add_text("右側のコンテンツ")
```

### 3. 画像とテキストの組み合わせ
```python
slide = presentation.add_slide()
slide.add_image("path/to/image.png", width=0.6)
slide.add_text("画像の説明文", position="bottom")
```

## レイアウトのカスタマイズ

### 1. グリッドシステムの利用
```python
slide = presentation.add_slide()
grid = slide.add_grid(rows=2, cols=2)
grid[0, 0].add_text("セル1")
grid[0, 1].add_text("セル2")
grid[1, 0].add_text("セル3")
grid[1, 1].add_text("セル4")
```

### 2. フレックスボックスレイアウト
```python
slide = presentation.add_slide()
flex = slide.add_flex_container()
flex.add_item("アイテム1", flex_grow=1)
flex.add_item("アイテム2", flex_grow=2)
```

## ベストプラクティス

1. **一貫性の維持**
   - 同じ種類のスライドでは、常に同じレイアウトを使用する
   - マージンやパディングの値を統一する

2. **視覚的な階層構造**
   - 重要な情報は大きく、目立つように配置
   - 補足情報は小さく、控えめに配置

3. **余白の活用**
   - 適切な余白を確保し、見やすいレイアウトを心がける
   - 要素同士の間隔を適切に設定する

4. **レスポンシブ対応**
   - 異なる画面サイズでも見やすいレイアウトを考慮
   - コンテンツの自動調整機能を活用する
