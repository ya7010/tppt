# API Reference

## Presentation

### Constructor

```python
Presentation(template: Optional[str] = None)
```

Creates a new presentation, optionally using a template.

### Methods

#### add_slide

```python
def add_slide(self, layout: Optional[str] = None) -> Slide
```

Adds a new slide to the presentation.

#### save

```python
def save(self, filename: str, format: Optional[str] = None)
```

Saves the presentation to a file.

## Slide

### Methods

#### add_title

```python
def add_title(self, text: str) -> Shape
```

Adds a title to the slide.

#### add_text

```python
def add_text(self, text: str, x: Optional[float] = None, y: Optional[float] = None) -> Shape
```

Adds text to the slide at the specified position.

#### add_image

```python
def add_image(
    self,
    image_path: str,
    x: Optional[float] = None,
    y: Optional[float] = None,
    width: Optional[float] = None,
    height: Optional[float] = None
) -> Shape
```

Adds an image to the slide.

#### add_table

```python
def add_table(
    self,
    data: List[List[Any]],
    x: Optional[float] = None,
    y: Optional[float] = None,
    width: Optional[float] = None,
    height: Optional[float] = None
) -> Shape
```

Adds a table to the slide.

#### add_shape

```python
def add_shape(
    self,
    shape_type: str,
    x: float,
    y: float,
    width: float,
    height: float
) -> Shape
```

Adds a shape to the slide.

## Shape

### Properties

- `fill_color: str` - The fill color of the shape
- `line_color: str` - The line color of the shape
- `line_width: float` - The line width of the shape
- `text: str` - The text content of the shape
- `font_name: str` - The font name for text
- `font_size: float` - The font size for text
- `font_bold: bool` - Whether the text is bold
- `font_italic: bool` - Whether the text is italic

### Methods

#### set_position

```python
def set_position(self, x: float, y: float)
```

Sets the position of the shape.

#### set_size

```python
def set_size(self, width: float, height: float)
```

Sets the size of the shape.

## DataFrameSupport

When using the pandas or polars support:

### Methods

#### add_dataframe

```python
def add_dataframe(
    self,
    df: Union[pd.DataFrame, pl.DataFrame],
    x: Optional[float] = None,
    y: Optional[float] = None,
    width: Optional[float] = None,
    height: Optional[float] = None
) -> Shape
```

Adds a data frame as a table to the slide. 