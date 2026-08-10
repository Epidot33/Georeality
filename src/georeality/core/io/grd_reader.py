"""
GeoReality GRD Reader

Author:
    Jonas Bermin - WSP

Project:
    GeoReality

Description:
    Reader for Surfer grid files.

    The first supported production format is Surfer 7 binary
    grid format, identified by the DSRB header tag.

Development note:
    This file may include AI-assisted drafting.
    All code must be reviewed, understood and tested before use.

Created:
    2026
"""

from __future__ import annotations

import argparse
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


try:
    import numpy as np
except ImportError as import_error:
    np = None
    _NUMPY_IMPORT_ERROR = import_error
else:
    _NUMPY_IMPORT_ERROR = None


# =============================================================================
# SURFER CONSTANTS
# =============================================================================

SURFER_7_HEADER_TAG = b"DSRB"
SURFER_7_GRID_TAG = b"GRID"
SURFER_7_DATA_TAG = b"DATA"

SURFER_NODATA_VALUE = 1.70141e38


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class SurferGrid:
    """
    Store a Surfer grid and associated metadata.

    Parameters
    ----------
    file_path : Path
        Path to the source GRD file.

    format_name : str
        Name of the detected Surfer grid format.

    version : int
        Surfer grid format version.

    n_rows : int
        Number of rows in the grid.

    n_columns : int
        Number of columns in the grid.

    x_lower_left : float
        X coordinate of the lower-left grid node.

    y_lower_left : float
        Y coordinate of the lower-left grid node.

    x_spacing : float
        Grid spacing in the X direction.

    y_spacing : float
        Grid spacing in the Y direction.

    z_min : float
        Minimum Z value reported by the grid file.

    z_max : float
        Maximum Z value reported by the grid file.

    blank_value : float
        Surfer blanking value.

    rotation : Optional[float]
        Grid rotation value, if present in the file.

    x_coordinates : np.ndarray
        One-dimensional array of X coordinates.

    y_coordinates : np.ndarray
        One-dimensional array of Y coordinates.

    z_values : np.ndarray
        Two-dimensional array of Z values with shape
        (n_rows, n_columns).
    """

    file_path: Path
    format_name: str
    version: int
    n_rows: int
    n_columns: int
    x_lower_left: float
    y_lower_left: float
    x_spacing: float
    y_spacing: float
    z_min: float
    z_max: float
    blank_value: float
    rotation: Optional[float]
    x_coordinates: object
    y_coordinates: object
    z_values: object


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _ensure_numpy_is_available() -> None:
    """
    Ensure that NumPy is available.

    Raises
    ------
    ImportError
        Raised if NumPy is not installed.
    """

    if np is None:
        raise ImportError(
            "NumPy is required for GRD reading. "
            "Install it with: pip install numpy"
        ) from _NUMPY_IMPORT_ERROR


def _read_exact_bytes(file_object, number_of_bytes: int) -> bytes:
    """
    Read an exact number of bytes from a binary file.

    Parameters
    ----------
    file_object
        Open binary file object.

    number_of_bytes : int
        Number of bytes to read.

    Returns
    -------
    bytes
        Bytes read from the file.

    Raises
    ------
    EOFError
        Raised if the file ends before the requested number
        of bytes has been read.
    """

    binary_data = file_object.read(number_of_bytes)

    if len(binary_data) != number_of_bytes:
        raise EOFError(
            f"Unexpected end of file. "
            f"Expected {number_of_bytes} bytes, got {len(binary_data)} bytes."
        )

    return binary_data


def _read_tag(file_object) -> tuple[bytes, int]:
    """
    Read a Surfer 7 tag.

    Parameters
    ----------
    file_object
        Open binary file object.

    Returns
    -------
    tuple[bytes, int]
        Tag identifier and section size in bytes.
    """

    tag_identifier = _read_exact_bytes(file_object, 4)
    section_size = struct.unpack("<i", _read_exact_bytes(file_object, 4))[0]

    return tag_identifier, section_size


def _replace_surfer_nodata_values(
    z_values,
    blank_value: float,
    version: int,
):
    """
    Replace Surfer NoData values with NaN.

    Parameters
    ----------
    z_values : np.ndarray
        Grid values.

    blank_value : float
        Surfer blanking value.

    version : int
        Surfer 7 grid version.

    Returns
    -------
    np.ndarray
        Grid values where NoData has been replaced by NaN.

    Notes
    -----
    For Surfer 7 version 1, values greater than or equal
    to BlankValue are treated as NoData.

    For Surfer 7 version 2, values equal to BlankValue
    are treated as NoData.

    Very large Surfer NoData values are also treated as NoData.
    """

    _ensure_numpy_is_available()

    cleaned_z_values = z_values.astype(float, copy=True)

    if version == 1:
        nodata_mask = cleaned_z_values >= blank_value
    else:
        nodata_mask = np.isclose(cleaned_z_values, blank_value)

    very_large_value_mask = cleaned_z_values >= SURFER_NODATA_VALUE * 0.99

    combined_nodata_mask = nodata_mask | very_large_value_mask

    cleaned_z_values[combined_nodata_mask] = np.nan

    return cleaned_z_values


# =============================================================================
# SURFER 7 BINARY READER
# =============================================================================

def read_surfer_7_binary_grid(file_path: str | Path) -> SurferGrid:
    """
    Read a Surfer 7 binary GRD file.

    Parameters
    ----------
    file_path : str or Path
        Path to the Surfer 7 binary GRD file.

    Returns
    -------
    SurferGrid
        Parsed grid data and metadata.

    Raises
    ------
    ValueError
        Raised if the file is not a supported Surfer 7 binary grid.
    """

    _ensure_numpy_is_available()

    grid_file_path = Path(file_path)

    with grid_file_path.open("rb") as grid_file:

        # ---------------------------------------------------------------------
        # Header section
        # ---------------------------------------------------------------------

        header_tag, header_size = _read_tag(grid_file)

        if header_tag != SURFER_7_HEADER_TAG:
            raise ValueError(
                f"Unsupported GRD format. "
                f"Expected DSRB header, got {header_tag!r}."
            )

        header_data = _read_exact_bytes(grid_file, header_size)

        if header_size < 4:
            raise ValueError(
                "Invalid Surfer 7 header section. "
                "Header section is too small."
            )

        version = struct.unpack("<i", header_data[:4])[0]

        # ---------------------------------------------------------------------
        # Read following sections until GRID and DATA have both been found.
        # ---------------------------------------------------------------------

        grid_metadata = None
        z_values = None

        while True:
            try:
                section_tag, section_size = _read_tag(grid_file)
            except EOFError:
                break

            section_data = _read_exact_bytes(grid_file, section_size)

            if section_tag == SURFER_7_GRID_TAG:

                grid_metadata = _parse_surfer_7_grid_section(section_data)

            elif section_tag == SURFER_7_DATA_TAG:

                if grid_metadata is None:
                    raise ValueError(
                        "DATA section found before GRID section. "
                        "This is not supported by the current reader."
                    )

                n_rows = grid_metadata["n_rows"]
                n_columns = grid_metadata["n_columns"]

                expected_value_count = n_rows * n_columns
                expected_byte_count = expected_value_count * 8

                if section_size < expected_byte_count:
                    raise ValueError(
                        "DATA section is smaller than expected. "
                        f"Expected at least {expected_byte_count} bytes, "
                        f"got {section_size} bytes."
                    )

                flat_z_values = np.frombuffer(
                    section_data[:expected_byte_count],
                    dtype="<f8",
                )

                z_values = flat_z_values.reshape((n_rows, n_columns))

        if grid_metadata is None:
            raise ValueError("No GRID section found in Surfer 7 file.")

        if z_values is None:
            raise ValueError("No DATA section found in Surfer 7 file.")

    cleaned_z_values = _replace_surfer_nodata_values(
        z_values=z_values,
        blank_value=grid_metadata["blank_value"],
        version=version,
    )

    x_coordinates = (
        grid_metadata["x_lower_left"]
        + np.arange(grid_metadata["n_columns"]) * grid_metadata["x_spacing"]
    )

    y_coordinates = (
        grid_metadata["y_lower_left"]
        + np.arange(grid_metadata["n_rows"]) * grid_metadata["y_spacing"]
    )

    return SurferGrid(
        file_path=grid_file_path,
        format_name="Surfer 7 Binary Grid",
        version=version,
        n_rows=grid_metadata["n_rows"],
        n_columns=grid_metadata["n_columns"],
        x_lower_left=grid_metadata["x_lower_left"],
        y_lower_left=grid_metadata["y_lower_left"],
        x_spacing=grid_metadata["x_spacing"],
        y_spacing=grid_metadata["y_spacing"],
        z_min=grid_metadata["z_min"],
        z_max=grid_metadata["z_max"],
        blank_value=grid_metadata["blank_value"],
        rotation=grid_metadata["rotation"],
        x_coordinates=x_coordinates,
        y_coordinates=y_coordinates,
        z_values=cleaned_z_values,
    )


def _parse_surfer_7_grid_section(section_data: bytes) -> dict:
    """
    Parse a Surfer 7 GRID section.

    Parameters
    ----------
    section_data : bytes
        Raw binary data from the GRID section.

    Returns
    -------
    dict
        Parsed grid metadata.

    Notes
    -----
    Some Surfer 7 grids include a rotation value in the GRID section.
    This reader supports both 64-byte and 72-byte GRID sections.
    """

    section_size = len(section_data)

    if section_size == 72:
        unpacked_values = struct.unpack("<ii8d", section_data)

        n_rows = unpacked_values[0]
        n_columns = unpacked_values[1]
        x_lower_left = unpacked_values[2]
        y_lower_left = unpacked_values[3]
        x_spacing = unpacked_values[4]
        y_spacing = unpacked_values[5]
        z_min = unpacked_values[6]
        z_max = unpacked_values[7]
        rotation = unpacked_values[8]
        blank_value = unpacked_values[9]

    elif section_size == 64:
        unpacked_values = struct.unpack("<ii7d", section_data)

        n_rows = unpacked_values[0]
        n_columns = unpacked_values[1]
        x_lower_left = unpacked_values[2]
        y_lower_left = unpacked_values[3]
        x_spacing = unpacked_values[4]
        y_spacing = unpacked_values[5]
        z_min = unpacked_values[6]
        z_max = unpacked_values[7]
        rotation = None
        blank_value = unpacked_values[8]

    else:
        raise ValueError(
            "Unsupported GRID section size. "
            f"Expected 64 or 72 bytes, got {section_size} bytes."
        )

    return {
        "n_rows": n_rows,
        "n_columns": n_columns,
        "x_lower_left": x_lower_left,
        "y_lower_left": y_lower_left,
        "x_spacing": x_spacing,
        "y_spacing": y_spacing,
        "z_min": z_min,
        "z_max": z_max,
        "rotation": rotation,
        "blank_value": blank_value,
    }


# =============================================================================
# PUBLIC READER
# =============================================================================

def read_grd(file_path: str | Path) -> SurferGrid:
    """
    Read a supported Surfer GRD file.

    Parameters
    ----------
    file_path : str or Path
        Path to the GRD file.

    Returns
    -------
    SurferGrid
        Parsed grid data and metadata.

    Raises
    ------
    ValueError
        Raised if the GRD file format is not supported.
    """

    grid_file_path = Path(file_path)

    with grid_file_path.open("rb") as grid_file:
        first_four_bytes = grid_file.read(4)

    if first_four_bytes == SURFER_7_HEADER_TAG:
        return read_surfer_7_binary_grid(grid_file_path)

    raise ValueError(
        "Unsupported GRD format. "
        f"First four bytes were {first_four_bytes!r}. "
        "Currently supported format: Surfer 7 binary DSRB."
    )


# =============================================================================
# COMMAND LINE TEST
# =============================================================================

def _print_grid_summary(grid: SurferGrid) -> None:
    """
    Print a summary of a parsed Surfer grid.

    Parameters
    ----------
    grid : SurferGrid
        Parsed grid object.
    """

    valid_z_values = grid.z_values[~np.isnan(grid.z_values)]

    print("GeoReality GRD Reader")
    print("---------------------")
    print(f"File: {grid.file_path}")
    print(f"Format: {grid.format_name}")
    print(f"Version: {grid.version}")
    print(f"Rows: {grid.n_rows}")
    print(f"Columns: {grid.n_columns}")
    print(f"X lower left: {grid.x_lower_left}")
    print(f"Y lower left: {grid.y_lower_left}")
    print(f"X spacing: {grid.x_spacing}")
    print(f"Y spacing: {grid.y_spacing}")
    print(f"File Z min: {grid.z_min}")
    print(f"File Z max: {grid.z_max}")
    print(f"Computed Z min: {float(np.nanmin(grid.z_values))}")
    print(f"Computed Z max: {float(np.nanmax(grid.z_values))}")
    print(f"NoData count: {int(np.isnan(grid.z_values).sum())}")
    print(f"Valid value count: {int(valid_z_values.size)}")

    if grid.rotation is not None:
        print(f"Rotation: {grid.rotation}")


if __name__ == "__main__":

    argument_parser = argparse.ArgumentParser(
        description="Read a Surfer GRD file and print metadata."
    )

    argument_parser.add_argument(
        "grd_file",
        help="Path to the Surfer GRD file.",
    )

    parsed_arguments = argument_parser.parse_args()

    parsed_grid = read_grd(parsed_arguments.grd_file)

    _print_grid_summary(parsed_grid)