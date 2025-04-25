"""Tests for table module."""

import pathlib

import pytest

import tppt
from tppt._features import USE_PANDAS, USE_POLARS


def test_create_table_with_list_data(output: pathlib.Path) -> None:
    """Test creating a table with list data."""
    table_data = [
        ["Header 1", "Header 2", "Header 3"],
        ["Cell 1,1", "Cell 1,2", "Cell 1,3"],
        ["Cell 2,1", "Cell 2,2", "Cell 2,3"],
    ]

    presentation = (
        tppt.Presentation.builder()
        .slide(
            tppt.SlideBuilder().table(
                table_data,
                left=(100, "pt"),
                top=(100, "pt"),
                width=(400, "pt"),
                height=(200, "pt"),
            )
        )
        .build()
    )
    presentation.save(output / "table_list_data.pptx")


@pytest.mark.skipif(not USE_PANDAS, reason="Pandas not installed")
def test_create_table_with_pandas_dataframe(output: pathlib.Path) -> None:
    """Test creating a table with pandas DataFrame."""
    # Type checking is done at runtime when pandas is available
    import pandas as pd  # type: ignore[import]

    # Create pandas DataFrame with simple data using dictionary
    data = {
        "名前": ["田中", "佐藤", "鈴木"],
        "年齢": [25, 30, 22],
        "都市": ["東京", "大阪", "名古屋"],
    }
    df = pd.DataFrame(data)

    # Convert DataFrame to a list of lists for table creation
    table_data = [df.columns.tolist()] + df.values.tolist()

    presentation = (
        tppt.Presentation.builder()
        .slide(
            tppt.SlideBuilder().table(
                table_data,  # 変換したリストを使用
                left=(100, "pt"),
                top=(100, "pt"),
                width=(400, "pt"),
                height=(200, "pt"),
                first_row_header=True,
            )
        )
        .build()
    )
    presentation.save(output / "table_pandas_data.pptx")


@pytest.mark.skipif(not USE_POLARS, reason="Polars not installed")
def test_create_table_with_polars_dataframe(output: pathlib.Path) -> None:
    """Test creating a table with polars DataFrame."""
    # Type checking is done at runtime when polars is available
    import polars as pl  # type: ignore[import]

    # Create polars DataFrame with simple data using dictionary
    data = {
        "製品": ["A製品", "B製品", "C製品"],
        "価格": [1000, 2000, 3000],
        "在庫": [50, 30, 10],
    }
    df = pl.DataFrame(data)

    # Convert DataFrame to a list of lists for table creation
    table_data = [df.columns] + df.to_numpy().tolist()

    presentation = (
        tppt.Presentation.builder()
        .slide(
            tppt.SlideBuilder().table(
                table_data,  # 変換したリストを使用
                left=(100, "pt"),
                top=(100, "pt"),
                width=(400, "pt"),
                height=(200, "pt"),
                first_row_header=True,
            )
        )
        .build()
    )
    presentation.save(output / "table_polars_data.pptx")


@pytest.mark.skipif(not USE_POLARS, reason="Polars not installed")
def test_create_table_with_polars_lazyframe(output: pathlib.Path) -> None:
    """Test creating a table with polars LazyFrame."""
    # Type checking is done at runtime when polars is available
    import polars as pl  # type: ignore[import]

    # Create polars LazyFrame with simple data using dictionary
    data = {
        "カテゴリ": ["食品", "電化製品", "衣類"],
        "売上": [5000, 12000, 8000],
        "利益率": [0.2, 0.15, 0.25],
    }
    lazy_df = pl.LazyFrame(data)

    # Collect LazyFrame to DataFrame
    df = lazy_df.collect()

    # Convert DataFrame to a list of lists for table creation
    table_data = [df.columns] + df.to_numpy().tolist()

    presentation = (
        tppt.Presentation.builder()
        .slide(
            tppt.SlideBuilder().table(
                table_data,
                left=(100, "pt"),
                top=(100, "pt"),
                width=(400, "pt"),
                height=(200, "pt"),
                first_row_header=True,
            )
        )
        .build()
    )
    presentation.save(output / "table_polars_lazyframe_data.pptx")
