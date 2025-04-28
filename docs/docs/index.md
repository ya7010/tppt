# Welcome to TPPT Documentation

TPPT (Typed Python PowerPoint Tool) is a Python library for creating and manipulating PowerPoint presentations with type safety.

## Features

- Type-safe PowerPoint presentation creation
- Support for various Python versions (3.11+)
- Rich set of features for slide manipulation
- Extensible architecture

## Quick Start

```python
from tppt import Presentation

# Create a new presentation
presentation = Presentation()

# Add a slide
slide = presentation.add_slide()

# Add content to the slide
slide.add_title("Hello, World!")
slide.add_text("This is a sample slide.")

# Save the presentation
presentation.save("example.pptx")
```

## Getting Started

To get started with TPPT, check out the [Installation](installation.md) guide and [Usage](usage.md) documentation.

## License

TPPT is licensed under the MIT License.
