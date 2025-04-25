# tppt

tppt is a type-safe PowerPoint presentation builder. This library allows you to easily generate PowerPoint presentations from Python code.

## Installation

```bash
pip install tppt
```

## Usage Example

```python
from pathlib import Path
import tppt
from tppt.types import Color

# Create a presentation using the builder pattern
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
            "Image Example",
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
            "Table Example",
            left=(50, "pt"),
            top=(50, "pt"),
            width=(300, "pt"),
            height=(40, "pt"),
        )
        .table(
            [
                ["Product", "Price", "Stock"],
                ["Product A", "$10.00", "10 units"],
                ["Product B", "$25.00", "5 units"],
            ],
            left=(50, "pt"),
            top=(100, "pt"),
            width=(400, "pt"),
            height=(200, "pt"),
        )
    )
    .build()
)

# Save the presentation
presentation.save("output.pptx")
```

## Features

- Type-safe interface
- Intuitive API with builder pattern
- Easy placement of text, images, and tables
- Fine-tuned control over position and size
- Customization of text styles (size, bold, italic, color)

## Architecture

This library consists of the following modules:

- `types`: Type-safe basic types for length, color, etc.
- `_data`: Data classes
- `_builders`: Implementation of the builder pattern
- `_presentation`: Presentation class
- `_slide_master`: Slide master class
- `_tppt`: Interface with python-pptx

## License

MIT
