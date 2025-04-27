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
    """Analyzes slide master and layout information from a PowerPoint file.

    Args:
        pptx_path: Path to the PowerPoint file
    """
    pptx_path = Path(pptx_path)

    if not pptx_path.exists():
        raise FileNotFoundError(f"PPTX file not found: {pptx_path}")

    # Load the presentation
    presentation = tppt.Presentation.from_pptx(PptxPresentation(os.fspath(pptx_path)))

    # Get the tree structure
    tree = presentation.tree
    return tree


@agent.tool_plain
def generate_layout_class(layout_name: str, placeholders: list[dict[str, Any]]) -> str:
    """Generates a slide layout class.

    Args:
        layout_name: Name of the layout
        placeholders: List of placeholder information
    """
    class_name = f"Custom{layout_name.replace(' ', '')}Layout"

    placeholder_definitions = []
    placeholder_names = set()

    for placeholder in placeholders:
        name = placeholder.get("name", "")
        if not name:
            continue

        field_name = name.lower().replace(" ", "_").replace("_placeholder", "")
        # Avoid duplicate field names
        if field_name in placeholder_names:
            continue
        placeholder_names.add(field_name)

        # Determine placeholder type
        placeholder_type = placeholder.get("placeholder_type", 0)

        if "date" in field_name or placeholder_type == 16:  # Date
            field_type = "tppt.Placeholder[datetime.date | None] = None"
        elif "number" in field_name or placeholder_type == 13:  # Slide number
            field_type = 'tppt.Placeholder[Literal["‹#›"] | int | None] = None'
        elif "title" in field_name or placeholder_type in [1, 3]:  # Title
            field_type = "tppt.Placeholder[str]"
        elif "subtitle" in field_name or placeholder_type == 4:  # Subtitle
            field_type = "tppt.Placeholder[str | None] = None"
        elif (
            "content" in field_name
            or "text" in field_name
            or placeholder_type in [2, 7]
        ):  # Content, Text
            field_type = "tppt.Placeholder[str | None] = None"
        elif (
            "picture" in field_name or "image" in field_name or placeholder_type == 18
        ):  # Picture
            field_type = "tppt.Placeholder[tppt.types.FilePath | None] = None"
        elif "footer" in field_name or placeholder_type == 15:  # Footer
            field_type = "tppt.Placeholder[str | None] = None"
        else:
            field_type = "tppt.Placeholder[str | None] = None"

        placeholder_definitions.append(f"    {field_name}: {field_type}")

    class_docstring = f'"""{layout_name} layout."""'

    return (
        f"class {class_name}(tppt.SlideLayout):\n    {class_docstring}\n\n"
        + "\n\n".join(placeholder_definitions)
    )


@agent.tool_plain
def generate_master_class(master_name: str, layouts: list[str]) -> str:
    """Generates a slide master class.

    Args:
        master_name: Name of the master
        layouts: List of layout names included in the master
    """
    # Convert master_name to PascalCase
    class_prefix = "".join(
        word.capitalize() for word in master_name.replace("-", "_").split("_")
    )
    class_name = f"{class_prefix}SlideMaster"

    layout_definitions = []
    for layout in layouts:
        layout_class_name = f"{class_prefix}{layout.replace(' ', '')}Layout"
        layout_field_name = f"{layout.replace(' ', '')}Layout"
        layout_definitions.append(
            f"    {layout_field_name}: tppt.Layout[{layout_class_name}]"
        )

    class_docstring = '"""Custom slide master class."""'

    return (
        f'@tppt.slide_master("{master_name}.pptx")\nclass {class_name}(tppt.SlideMaster):\n    {class_docstring}\n\n'
        + "\n\n".join(layout_definitions)
    )


def generate_template_file(
    pptx_path: tppt.types.FilePath,
    *,
    output_path: tppt.types.FilePath | None = None,
) -> None:
    """Generates slide master and layout definitions from a PowerPoint file and saves them as a Python file.

    Args:
        pptx_path: Path to the PowerPoint file
        output_path: Path to save the generated Python file (default: prints to standard output)
    """
    pptx_path = Path(pptx_path)

    # Analyze slide structure
    tree = analyze_slide_structure(pptx_path)

    # Extract master and layout information
    master_name = pptx_path.stem
    layout_info = {}

    # Extract layout information from slide masters
    if "slide_masters" in tree and tree["slide_masters"]:
        slide_master = tree["slide_masters"][0]
        if "slide_layouts" in slide_master:
            for layout in slide_master["slide_layouts"]:
                layout_name = layout.get("name", "")
                if layout_name:
                    layout_info[layout_name] = layout.get("placeholders", [])

    # Fallback if no layouts were extracted
    if not layout_info:
        for slide in tree.get("slides", []):
            layout_name = slide.get("slide_layout_name", "")
            if layout_name and layout_name not in layout_info:
                layout_info[layout_name] = slide.get("placeholders", [])

    # Generate the file
    imports = [
        "import datetime",
        "from typing import Literal",
        "",
        "import tppt",
        "",
    ]

    layout_classes = []
    for layout_name, placeholders in layout_info.items():
        layout_classes.append(generate_layout_class(layout_name, placeholders))

    master_class = generate_master_class(master_name, list(layout_info.keys()))

    content = (
        "\n".join(imports)
        + "\n\n"
        + "\n\n\n".join(layout_classes)
        + "\n\n\n"
        + master_class
    )

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        print(content)

    print(f"Template file generated at: {output_path or 'standard output'}")


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
