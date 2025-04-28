# Installation

TPPT can be installed using your favorite Python package manager.

## Requirements

- Python 3.11 or higher
- One of the following package managers:
    * [uv](https://docs.astral.sh/uv/)
    * [poetry](https://python-poetry.org/)
    * [hatch](https://hatch.pypa.io/)
    * [pip](https://pip.pypa.io/)

=== "uv"
    ```bash
    uv add tppt
    ```

=== "pip"
    ```bash
    pip install tppt
    ```

=== "poetry"
    ```bash
    poetry add tppt
    ```

=== "hatch"
    ```bash
    hatch add tppt
    ```

## Optional Dependencies

TPPT provides optional dependencies for additional features:

### Data Frame Support

For working with data frames:

=== "uv"
    ```bash
    # For pandas support
    uv add "tppt[pandas]"

    # For polars support
    uv add "tppt[polars]"
    ```

=== "pip"
    ```bash
    # For pandas support
    pip install "tppt[pandas]"

    # For polars support
    pip install "tppt[polars]"
    ```

=== "poetry"
    ```bash
    # For pandas support
    poetry add "tppt[pandas]"

    # For polars support
    poetry add "tppt[polars]"
    ```

=== "hatch"
    ```bash
    # For pandas support
    hatch add "tppt[pandas]"

    # For polars support
    hatch add "tppt[polars]"
    ```

### Pydantic Support

For Pydantic integration:

=== "uv"
    ```bash
    uv add "tppt[pydantic]"
    ```

=== "pip"
    ```bash
    pip install "tppt[pydantic]"
    ```

=== "poetry"
    ```bash
    poetry add "tppt[pydantic]"
    ```

=== "hatch"
    ```bash
    hatch add "tppt[pydantic]"
    ```

### Development Tools

For development purposes:

=== "uv"
    ```bash
    uv add "tppt[dev]"
    ```

=== "pip"
    ```bash
    pip install "tppt[dev]"
    ```

=== "poetry"
    ```bash
    poetry add "tppt[dev]"
    ```

=== "hatch"
    ```bash
    hatch add "tppt[dev]"
    ```

## Verifying Installation

You can verify the installation by running:

```python
--8<-- "examples/check_version.py"
``` 