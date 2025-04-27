"""Tool to generate slide master and layout type definitions from PowerPoint."""

import argparse
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from pptx import Presentation as PptxPresentation
from pydantic import BaseModel, Field

import tppt


class PlaceholderInfo(BaseModel):
    """Information about a placeholder."""

    name: str = Field(description="Name of the placeholder")
    type: int = Field(description="Type ID of the placeholder")
    field_name: Optional[str] = Field(default=None, description="Python field name")
    field_type: Optional[str] = Field(
        default=None, description="Python field type definition"
    )
    required: bool = Field(default=False, description="Whether the field is required")
    idx: Optional[int] = Field(default=None, description="Index within the layout")


class LayoutInfo(BaseModel):
    """Information about a slide layout."""

    name: str = Field(description="Name of the layout")
    placeholders: List[PlaceholderInfo] = Field(
        description="List of placeholders in the layout"
    )
    class_name: Optional[str] = Field(
        default=None, description="Python class name for this layout"
    )


class MasterInfo(BaseModel):
    """Information about a slide master."""

    name: str = Field(description="Name of the slide master")
    layouts: List[LayoutInfo] = Field(description="Layouts in this master")
    class_name: Optional[str] = Field(
        default=None, description="Python class name for this master"
    )


def extract_master_info(tree: Dict[str, Any]) -> MasterInfo:
    """Extract information about the slide master and its layouts."""

    master_name = Path(tree.get("name", "custom_template")).stem

    layouts_info = []

    # Extract layout information from slide masters
    if "slide_masters" in tree and tree["slide_masters"]:
        slide_master = tree["slide_masters"][0]
        if "slide_layouts" in slide_master:
            for layout in slide_master["slide_layouts"]:
                layout_name = layout.get("name", "")
                if layout_name:
                    placeholders = [
                        PlaceholderInfo(
                            name=p.get("name", ""),
                            type=p.get("placeholder_type", 0),
                            idx=i,
                        )
                        for i, p in enumerate(layout.get("placeholders", []))
                        if p.get("name")
                    ]
                    layouts_info.append(
                        LayoutInfo(name=layout_name, placeholders=placeholders)
                    )

    # Fallback if no layouts were extracted
    if not layouts_info:
        layout_map = {}
        for slide in tree.get("slides", []):
            layout_name = slide.get("slide_layout_name", "")
            if layout_name and layout_name not in layout_map:
                placeholders = [
                    PlaceholderInfo(
                        name=p.get("name", ""), type=p.get("placeholder_type", 0), idx=i
                    )
                    for i, p in enumerate(slide.get("placeholders", []))
                    if p.get("name")
                ]
                layout_map[layout_name] = LayoutInfo(
                    name=layout_name, placeholders=placeholders
                )
        layouts_info = list(layout_map.values())

    return MasterInfo(name=master_name, layouts=layouts_info)


def clean_field_name(name: str) -> str:
    """Clean a field name to make it suitable for a Python identifier.

    Removes numeric suffixes, converts to snake_case, and handles special characters.
    """
    # Remove numeric suffixes (e.g., "Title 1" -> "Title")
    name = re.sub(r"\s+\d+$", "", name)

    # Convert to lowercase and replace spaces/special chars with underscores
    name = name.lower().replace(" ", "_").replace("-", "_").replace(".", "_")

    # Remove "placeholder" suffix if present
    name = name.replace("_placeholder", "")

    # Ensure the name is a valid Python identifier
    if not name or not name[0].isalpha() and name[0] != "_":
        name = f"placeholder_{name}"

    # Replace any remaining invalid characters
    name = re.sub(r"[^a-z0-9_]", "_", name)

    return name


def get_field_name_from_layout_context(
    ph: PlaceholderInfo,
    placeholder_type_map: Dict[int, List[PlaceholderInfo]],
    layout_name: str,
    seen_names: Set[str],
) -> str:
    """Get appropriate field name based on layout context and placeholder type."""
    placeholder_type = ph.type
    ph_name = ph.name.lower()
    layout_name_lower = layout_name.lower()

    # Start with basic name from placeholder type
    base_name = clean_field_name(ph.name)

    # Use standard names for common placeholder types
    if placeholder_type == 1:  # Title
        base_name = "title"
    elif placeholder_type == 2:  # Body/Content
        if "content" in layout_name_lower or "text" in layout_name_lower:
            base_name = "content"
        else:
            base_name = "body"
    elif placeholder_type == 3:  # CenteredTitle
        base_name = "title"  # Simplified to just "title"
    elif placeholder_type == 4:  # Subtitle
        base_name = "subtitle"
    elif placeholder_type == 7:  # Chart
        if "chart" in ph_name:
            base_name = "chart"
        else:
            base_name = "content"  # Often used for regular content despite being type 7
    elif placeholder_type == 8:  # Table
        base_name = "table"
    elif placeholder_type == 13:  # SlideNumber
        base_name = "slide_number"
    elif placeholder_type == 15:  # Footer
        base_name = "footer"
    elif placeholder_type == 16:  # Date
        base_name = "date"
    elif placeholder_type == 18:  # Picture
        base_name = "picture"
    elif placeholder_type == 19:  # VerticalTitle
        base_name = "vertical_title"
    elif placeholder_type == 20:  # VerticalBody
        base_name = "vertical_text"

    # Handle specific layout types
    if "two content" in layout_name_lower and placeholder_type in [2, 7]:
        same_type_phs = placeholder_type_map.get(placeholder_type, [])
        if len(same_type_phs) > 1:
            idx = same_type_phs.index(ph)
            if idx == 0:
                base_name = "left_content"
            elif idx == 1:
                base_name = "right_content"

    # Handle comparison layout
    elif "comparison" in layout_name_lower:
        same_type_phs = placeholder_type_map.get(placeholder_type, [])
        if placeholder_type == 1:  # Title
            base_name = "title"
        elif placeholder_type in [2, 7]:  # Content/Body/Chart
            if len(same_type_phs) > 1:
                idx = same_type_phs.index(ph)
                if idx == 0:
                    base_name = "left_title" if "title" in ph_name else "left_content"
                elif idx == 1:
                    base_name = "left_body" if "body" in ph_name else "left_content"
                elif idx == 2:
                    base_name = "right_title" if "title" in ph_name else "right_content"
                elif idx == 3:
                    base_name = "right_body" if "body" in ph_name else "right_content"
                else:
                    base_name = f"content_{idx + 1}"

    # Custom handling for vertical layouts
    elif "vertical" in layout_name_lower:
        if placeholder_type == 19:  # VerticalTitle
            base_name = "vertical_title"
        elif placeholder_type == 20:  # VerticalBody
            base_name = "vertical_text"
        elif placeholder_type in [
            2,
            7,
        ]:  # Sometimes regular content in vertical layouts
            base_name = "content"

    # Generic handling for multiple placeholders of same type
    else:
        same_type_phs = placeholder_type_map.get(placeholder_type, [])
        if len(same_type_phs) > 1 and placeholder_type not in [
            13,
            15,
            16,
        ]:  # Not for common elements
            idx = same_type_phs.index(ph)
            if idx > 0:
                base_name = f"{base_name}_{idx + 1}"

    # Ensure uniqueness by adding numeric suffix if needed
    if base_name in seen_names:
        counter = 1
        while f"{base_name}_{counter}" in seen_names:
            counter += 1
        base_name = f"{base_name}_{counter}"

    seen_names.add(base_name)
    return base_name


def analyze_layout(layout: LayoutInfo) -> LayoutInfo:
    """Analyze layout and determine class name and field information."""

    # Generate class name in PascalCase
    layout_name_parts = layout.name.replace("-", " ").split()
    class_name = (
        "Custom" + "".join(part.capitalize() for part in layout_name_parts) + "Layout"
    )

    # Process placeholders to ensure no duplicates and proper field names
    processed_placeholders = []
    seen_field_names = set()
    placeholder_type_map = {}

    # First pass - identify placeholder types
    for ph in layout.placeholders:
        if ph.type not in placeholder_type_map:
            placeholder_type_map[ph.type] = []
        placeholder_type_map[ph.type].append(ph)

    # Second pass - generate field names and types
    for ph in layout.placeholders:
        if not ph.name:
            continue

        # Generate more context-aware field name
        field_name = get_field_name_from_layout_context(
            ph, placeholder_type_map, layout.name, seen_field_names
        )

        # Determine field type
        placeholder_type = ph.type
        required = False

        if "date" in field_name or placeholder_type == 16:  # Date
            field_type = "tppt.Placeholder[datetime.date | None]"
        elif "number" in field_name or placeholder_type == 13:  # Slide number
            field_type = 'tppt.Placeholder[Literal["‹#›"] | int | None]'
        elif "title" in field_name or placeholder_type in [
            1,
            3,
            19,
        ]:  # Title, CenteredTitle, VerticalTitle
            field_type = "tppt.Placeholder[str]"
            required = True
        elif "subtitle" in field_name or placeholder_type == 4:  # Subtitle
            field_type = "tppt.Placeholder[str | None]"
        elif (
            "picture" in field_name or "image" in field_name or placeholder_type == 18
        ):  # Picture
            field_type = "tppt.Placeholder[tppt.types.FilePath | None]"
        elif "chart" in field_name and placeholder_type == 7:  # Actual chart
            field_type = "tppt.Placeholder[tppt.types.FilePath | None]"
        elif "table" in field_name and placeholder_type == 8:  # Table
            field_type = "tppt.Placeholder[str | None]"
        elif placeholder_type in [
            2,
            7,
            20,
        ]:  # Body, Chart (used as content), VerticalBody
            field_type = "tppt.Placeholder[str | None]"
        elif "footer" in field_name or placeholder_type == 15:  # Footer
            field_type = "tppt.Placeholder[str | None]"
        else:
            field_type = "tppt.Placeholder[str | None]"

        new_ph = PlaceholderInfo(
            name=ph.name,
            type=ph.type,
            field_name=field_name,
            field_type=field_type,
            required=required,
            idx=ph.idx,
        )
        processed_placeholders.append(new_ph)

    return LayoutInfo(
        name=layout.name, placeholders=processed_placeholders, class_name=class_name
    )


def generate_layout_class(layout: LayoutInfo) -> str:
    """Generate Python code for a slide layout class."""

    class_name = layout.class_name or f"Custom{layout.name.replace(' ', '')}Layout"
    class_docstring = f'"""{layout.name} layout."""'

    # 元のインデックス順を維持する（ソートしない）
    placeholder_definitions = []
    for ph in layout.placeholders:
        if not ph.field_name or not ph.field_type:
            continue

        if ph.required:
            placeholder_definitions.append(f"    {ph.field_name}: {ph.field_type}")
        else:
            placeholder_definitions.append(
                f"    {ph.field_name}: {ph.field_type} = None"
            )

    if not placeholder_definitions:
        placeholder_definitions = ["    # No placeholders found"]

    return (
        f"class {class_name}(tppt.SlideLayout):\n"
        f"    {class_docstring}\n\n" + "\n\n".join(placeholder_definitions)
    )


def generate_master_class(master: MasterInfo) -> str:
    """Generate Python code for a slide master class."""

    # Convert master_name to PascalCase
    class_prefix = "".join(
        word.capitalize() for word in master.name.replace("-", "_").split("_")
    )
    class_name = f"{class_prefix}SlideMaster"

    layout_definitions = []
    for layout in master.layouts:
        layout_class_name = (
            layout.class_name or f"Custom{layout.name.replace(' ', '')}Layout"
        )
        layout_field_name = f"{layout.name.replace(' ', '')}Layout"
        layout_definitions.append(
            f"    {layout_field_name}: tppt.Layout[{layout_class_name}]"
        )

    if not layout_definitions:
        layout_definitions = ["    # No layouts found"]

    class_docstring = f'"""{master.name} slide master."""'

    return (
        f'@tppt.slide_master("{master.name}.pptx")\n'
        f"class {class_name}(tppt.SlideMaster):\n"
        f"    {class_docstring}\n\n" + "\n\n".join(layout_definitions)
    )


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
    tree["name"] = str(pptx_path)

    # Extract and analyze information
    master_info = extract_master_info(tree)

    # Analyze each layout
    analyzed_layouts = []
    for layout in master_info.layouts:
        analyzed_layout = analyze_layout(layout)
        analyzed_layouts.append(analyzed_layout)

    master_info.layouts = analyzed_layouts

    # Generate code for imports
    imports = [
        "import datetime",
        "from typing import Literal",
        "",
        "import tppt",
        "",
    ]

    # Generate code for layout classes
    layout_classes = []
    for layout in master_info.layouts:
        layout_class = generate_layout_class(layout)
        layout_classes.append(layout_class)

    # Generate master class
    master_class = generate_master_class(master_info)

    # Combine everything
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
