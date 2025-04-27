"""Tool to generate slide master and layout type definitions from PowerPoint."""

import argparse
import os
from pathlib import Path
from typing import Any

from pptx import Presentation as PptxPresentation
from pydantic_ai import Agent

import tppt

agent = Agent()


@agent.tool_plain
def analyze_slide_structure(pptx_path: tppt.types.FilePath) -> dict[str, Any]:
    """PowerPointファイルからスライドマスターとレイアウト情報を分析します。

    Args:
        pptx_path: PowerPointファイルのパス
    """
    pptx_path = Path(pptx_path)

    if not pptx_path.exists():
        raise FileNotFoundError(f"PPTX file not found: {pptx_path}")

    # プレゼンテーションの読み込み
    presentation = tppt.Presentation.from_pptx(PptxPresentation(os.fspath(pptx_path)))

    # ツリー構造の取得
    tree = presentation.tree
    return tree


@agent.tool_plain
def generate_layout_class(layout_name: str, placeholders: dict[str, Any]) -> str:
    """スライドレイアウトクラスを生成します。

    Args:
        layout_name: レイアウト名
        placeholders: プレースホルダー情報
    """
    class_name = f"{layout_name.replace(' ', '')}SlideLayout"

    placeholder_definitions = []
    for name, data in placeholders.items():
        field_name = name.lower().replace(" ", "_")

        # プレースホルダーの型を判断
        if "date" in field_name:
            field_type = "tppt.Placeholder[datetime.date | None] = None"
        elif "number" in field_name:
            field_type = 'tppt.Placeholder[Literal["‹#›"] | int | None] = None'
        elif "title" in field_name:
            field_type = "tppt.Placeholder[str]"
        elif "content" in field_name or "text" in field_name:
            field_type = "tppt.Placeholder[str]"
        elif "picture" in field_name or "image" in field_name:
            field_type = "tppt.Placeholder[tppt.types.FilePath]"
        else:
            field_type = "tppt.Placeholder[str | None] = None"

        placeholder_definitions.append(f"    {field_name}: {field_type}")

    class_docstring = f'"""{layout_name} slide layout."""'

    return (
        f"class {class_name}(tppt.SlideLayout):\n    {class_docstring}\n\n"
        + "\n".join(placeholder_definitions)
    )


@agent.tool_plain
def generate_master_class(master_name: str, layouts: list[str]) -> str:
    """スライドマスタークラスを生成します。

    Args:
        master_name: マスター名
        layouts: 含まれるレイアウト名のリスト
    """
    class_name = f"{master_name.replace(' ', '')}SlideMaster"

    layout_definitions = []
    for layout in layouts:
        layout_class_name = f"{layout.replace(' ', '')}SlideLayout"
        layout_field_name = f"{layout.replace(' ', '')}Layout"
        layout_definitions.append(
            f"    {layout_field_name}: tppt.Layout[{layout_class_name}]"
        )

    return (
        f'@tppt.slide_master("{master_name.lower()}")\nclass {class_name}(tppt.SlideMaster):\n'
        + "\n".join(layout_definitions)
    )


def generate_template_file(
    pptx_path: tppt.types.FilePath,
    *,
    output_path: tppt.types.FilePath | None = None,
) -> None:
    """PowerPointファイルからスライドマスターとレイアウト定義を生成してPythonファイルとして保存します。

    Args:
        pptx_path: PowerPointファイルのパス
        output_path: 出力するPythonファイルのパス（デフォルト: 入力ファイルと同じ場所に.pyファイルとして保存）
    """
    pptx_path = Path(pptx_path)

    # スライド構造の分析
    tree = analyze_slide_structure(pptx_path)

    # マスターとレイアウト情報の抽出
    master_name = pptx_path.stem.replace(" ", "")
    layouts = []
    placeholder_info = {}

    # treeからレイアウト情報を抽出する処理
    # 実際のtree構造によって調整が必要
    for slide in tree.get("slides", []):
        layout = slide.get("layout", "")
        if layout and layout not in layouts:
            layouts.append(layout)
            placeholder_info[layout] = slide.get("placeholders", {})

    # ファイルの生成
    imports = ["import datetime", "from typing import Literal", "", "import tppt", ""]

    layout_classes = []
    for layout in layouts:
        layout_classes.append(
            generate_layout_class(layout, placeholder_info.get(layout, {}))
        )

    master_class = generate_master_class(master_name, layouts)

    content = (
        "\n".join(imports)
        + "\n\n"
        + "\n\n".join(layout_classes)
        + "\n\n\n"
        + master_class
    )

    if output_path:
        output_path = Path(output_path)
    else:
        output_path = pptx_path.with_suffix(".py")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Template file generated at: {output_path}")


if __name__ == "__main__":
    try:
        from rich_argparse import RichHelpFormatter

        formatter_class = RichHelpFormatter
    except ImportError:
        formatter_class = argparse.HelpFormatter

    parser = argparse.ArgumentParser(
        description="Generate slide master and layout type definitions from PowerPoint",
        formatter_class=formatter_class,
    )
    parser.add_argument("pptx_path", help="Path to the PPTX file")
    parser.add_argument(
        "-o", "--output", default=None, help="Path to save the generated Python file"
    )

    args = parser.parse_args()

    generate_template_file(args.pptx_path, output_path=args.output)
