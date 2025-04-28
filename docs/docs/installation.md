# Installation

TPPT can be installed using pip or your favorite Python package manager.

## Requirements

- Python 3.11 or higher
- pip or uv package manager

## Using pip

```bash
pip install tppt
```

## Using uv

```bash
uv pip install tppt
```

## Optional Dependencies

TPPT provides optional dependencies for additional features:

### Data Frame Support

For working with data frames:

```bash
# For pandas support
uv pip install "tppt[pandas]"

# For polars support
uv pip install "tppt[polars]"
```

### Pydantic Support

For Pydantic integration:

```bash
uv pip install "tppt[pydantic]"
```

### Development Tools

For development purposes:

```bash
uv pip install "tppt[dev]"
```

## Verifying Installation

You can verify the installation by running:

```python
import tppt
print(tppt.__version__)
``` 