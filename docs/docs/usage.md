# Usage Guide

This guide will walk you through the basic usage of TPPT.

## Creating a Presentation

```python
from tppt import Presentation

# Create a new presentation
presentation = Presentation()

# Or open an existing presentation
presentation = Presentation.open("template.pptx")
```

## Working with Slides

### Adding Slides

```python
# Add a blank slide
slide = presentation.add_slide()

# Add a slide with a specific layout
slide = presentation.add_slide(layout="title_and_content")
```

### Adding Content to Slides

```python
# Add title and content
slide.add_title("My Presentation")
slide.add_text("This is some content")

# Add an image
slide.add_image("path/to/image.png")

# Add a table
data = [
    ["Header 1", "Header 2"],
    ["Row 1", "Value 1"],
    ["Row 2", "Value 2"],
]
slide.add_table(data)
```

## Working with Data Frames

If you have installed the pandas or polars support:

```python
import pandas as pd

# Create a data frame
df = pd.DataFrame({
    "Column 1": [1, 2, 3],
    "Column 2": ["A", "B", "C"]
})

# Add data frame as a table
slide.add_dataframe(df)
```

## Saving the Presentation

```python
# Save to a file
presentation.save("output.pptx")

# Save to a specific format
presentation.save("output.pdf", format="pdf")
```

## Advanced Features

### Using Templates

```python
# Create a presentation from a template
presentation = Presentation.from_template("template.pptx")

# Apply a template to specific slides
presentation.apply_template("template.pptx", slide_indices=[0, 1])
```

### Working with Shapes

```python
# Add shapes
slide.add_shape("rectangle", x=100, y=100, width=200, height=100)
slide.add_shape("oval", x=300, y=300, width=100, height=100)

# Style shapes
shape = slide.shapes[-1]  # Get the last added shape
shape.fill_color = "#FF0000"
shape.line_color = "#000000"
shape.line_width = 2
```

For more detailed information about specific features, please refer to the [API Reference](api.md). 