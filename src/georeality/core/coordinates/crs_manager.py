"""
GeoReality CRS Manager

Author:
    Jonas Bermin - WSP

Project:
    GeoReality

Description:
    Coordinate reference system management for GeoReality.

    This module provides functions and classes for defining,
    validating and transforming coordinate reference systems.

Development note:
    This file may include AI-assisted drafting.
    All code must be reviewed, understood and tested before use.

Created:
    2026
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


try:
    from pyproj import CRS, Transformer
except ImportError as import_error:
    CRS = None
    Transformer = None
    _PYPROJ_IMPORT_ERROR = import_error
else:
    _PYPROJ_IMPORT_ERROR = None


# =============================================================================
# DEFAULT COORDINATE SETTINGS
# =============================================================================

DEFAULT_PROJECT_EPSG: int = 3006
DEFAULT_PROJECT_CRS_NAME: str = "SWEREF99 TM"
DEFAULT_VERTICAL_REFERENCE_SYSTEM: str = "RH2000"


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass(frozen=True)
class CRSDefinition:
    """
    Store basic information about a coordinate reference system.

    Parameters
    ----------
    epsg_code : int
        EPSG code for the coordinate reference system.

    name : str
        Human-readable name of the coordinate reference system.

    authority : str
        CRS authority name. Usually "EPSG".

    is_projected : bool
        True if the CRS is projected.

    is_geographic : bool
        True if the CRS is geographic.

    axis_info : str
        Text description of CRS axis information.
    """

    epsg_code: int
    name: str
    authority: str
    is_projected: bool
    is_geographic: bool
    axis_info: str


# =============================================================================
# CRS MANAGER
# =============================================================================

class CRSManager:
    """
    Manage coordinate reference systems for GeoReality.

    The CRSManager is responsible for:

    - Creating CRS objects from EPSG codes
    - Validating EPSG codes
    - Describing coordinate reference systems
    - Comparing coordinate reference systems
    - Transforming coordinates between systems

    Notes
    -----
    GeoReality uses SWEREF99 TM, EPSG:3006, as the default project CRS
    for Swedish projects, but the system is designed to support any
    EPSG-based coordinate reference system supported by pyproj.
    """

    def __init__(self, default_epsg: int = DEFAULT_PROJECT_EPSG) -> None:
        """
        Initialize the CRS manager.

        Parameters
        ----------
        default_epsg : int, optional
            Default EPSG code for the project coordinate reference system.
            The default value is 3006, corresponding to SWEREF99 TM.
        """

        self._ensure_pyproj_is_available()

        self.default_epsg: int = default_epsg
        self.default_crs = self.create_crs_from_epsg(default_epsg)

    @staticmethod
    def _ensure_pyproj_is_available() -> None:
        """
        Ensure that pyproj is available.

        Raises
        ------
        ImportError
            Raised if pyproj is not installed.
        """

        if CRS is None or Transformer is None:
            raise ImportError(
                "pyproj is required for coordinate reference system handling. "
                "Install it with: pip install pyproj"
            ) from _PYPROJ_IMPORT_ERROR

    @staticmethod
    def create_crs_from_epsg(epsg_code: int):
        """
        Create a pyproj CRS object from an EPSG code.

        Parameters
        ----------
        epsg_code : int
            EPSG code.

        Returns
        -------
        pyproj.CRS
            Coordinate reference system object.

        Raises
        ------
        ValueError
            Raised if the EPSG code is invalid.
        """

        CRSManager._ensure_pyproj_is_available()

        try:
            coordinate_reference_system = CRS.from_epsg(epsg_code)
        except Exception as error:
            raise ValueError(
                f"Invalid or unsupported EPSG code: {epsg_code}"
            ) from error

        return coordinate_reference_system

    @staticmethod
    def validate_epsg(epsg_code: int) -> bool:
        """
        Validate an EPSG code.

        Parameters
        ----------
        epsg_code : int
            EPSG code to validate.

        Returns
        -------
        bool
            True if the EPSG code can be resolved by pyproj.
            False otherwise.
        """

        try:
            CRSManager.create_crs_from_epsg(epsg_code)
        except ValueError:
            return False

        return True

    @staticmethod
    def describe_crs(epsg_code: int) -> CRSDefinition:
        """
        Create a CRSDefinition object from an EPSG code.

        Parameters
        ----------
        epsg_code : int
            EPSG code.

        Returns
        -------
        CRSDefinition
            Structured description of the coordinate reference system.
        """

        coordinate_reference_system = CRSManager.create_crs_from_epsg(epsg_code)

        authority = coordinate_reference_system.to_authority()
        authority_name = authority[0] if authority else "Unknown"

        axis_info_text = "; ".join(
            str(axis) for axis in coordinate_reference_system.axis_info
        )

        return CRSDefinition(
            epsg_code=epsg_code,
            name=coordinate_reference_system.name,
            authority=authority_name,
            is_projected=coordinate_reference_system.is_projected,
            is_geographic=coordinate_reference_system.is_geographic,
            axis_info=axis_info_text,
        )

    def get_default_project_crs(self):
        """
        Get the default project coordinate reference system.

        Returns
        -------
        pyproj.CRS
            Default project CRS.
        """

        return self.default_crs

    def get_default_project_definition(self) -> CRSDefinition:
        """
        Get a structured description of the default project CRS.

        Returns
        -------
        CRSDefinition
            Description of the default project CRS.
        """

        return self.describe_crs(self.default_epsg)

    @staticmethod
    def are_same_crs(source_epsg: int, target_epsg: int) -> bool:
        """
        Check whether two EPSG codes describe the same CRS.

        Parameters
        ----------
        source_epsg : int
            First EPSG code.

        target_epsg : int
            Second EPSG code.

        Returns
        -------
        bool
            True if both EPSG codes describe equivalent CRS definitions.
            False otherwise.
        """

        source_crs = CRSManager.create_crs_from_epsg(source_epsg)
        target_crs = CRSManager.create_crs_from_epsg(target_epsg)

        return source_crs == target_crs

    @staticmethod
    def transform_xy(
        x_coordinate: float,
        y_coordinate: float,
        source_epsg: int,
        target_epsg: int,
    ) -> Tuple[float, float]:
        """
        Transform a single XY coordinate pair between two CRS definitions.

        Parameters
        ----------
        x_coordinate : float
            X coordinate in the source CRS.

        y_coordinate : float
            Y coordinate in the source CRS.

        source_epsg : int
            EPSG code for the source CRS.

        target_epsg : int
            EPSG code for the target CRS.

        Returns
        -------
        tuple[float, float]
            Transformed X and Y coordinates in the target CRS.

        Notes
        -----
        The transformer uses always_xy=True to keep coordinate order
        consistent as X, Y. This is important for geospatial workflows
        where longitude/easting should be handled before latitude/northing.
        """

        source_crs = CRSManager.create_crs_from_epsg(source_epsg)
        target_crs = CRSManager.create_crs_from_epsg(target_epsg)

        transformer = Transformer.from_crs(
            source_crs,
            target_crs,
            always_xy=True,
        )

        transformed_x, transformed_y = transformer.transform(
            x_coordinate,
            y_coordinate,
        )

        return transformed_x, transformed_y

    @staticmethod
    def transform_xyz(
        x_coordinate: float,
        y_coordinate: float,
        z_coordinate: Optional[float],
        source_epsg: int,
        target_epsg: int,
    ) -> Tuple[float, float, Optional[float]]:
        """
        Transform an XYZ coordinate between two CRS definitions.

        Parameters
        ----------
        x_coordinate : float
            X coordinate in the source CRS.

        y_coordinate : float
            Y coordinate in the source CRS.

        z_coordinate : float or None
            Z coordinate. GeoReality currently preserves this value without
            applying vertical datum transformation.

        source_epsg : int
            EPSG code for the source CRS.

        target_epsg : int
            EPSG code for the target CRS.

        Returns
        -------
        tuple[float, float, float or None]
            Transformed X and Y coordinates, with the original Z value.

        Notes
        -----
        This function does not perform vertical datum transformation.
        Vertical reference systems, such as RH2000, must be handled
        explicitly in later development.
        """

        transformed_x, transformed_y = CRSManager.transform_xy(
            x_coordinate=x_coordinate,
            y_coordinate=y_coordinate,
            source_epsg=source_epsg,
            target_epsg=target_epsg,
        )

        return transformed_x, transformed_y, z_coordinate


# =============================================================================
# SIMPLE MANUAL TEST
# =============================================================================

if __name__ == "__main__":
    crs_manager = CRSManager()

    default_definition = crs_manager.get_default_project_definition()

    print("GeoReality CRS Manager")
    print("----------------------")
    print(f"Default EPSG: {default_definition.epsg_code}")
    print(f"Default CRS name: {default_definition.name}")
    print(f"Projected: {default_definition.is_projected}")
    print(f"Geographic: {default_definition.is_geographic}")

    # Example transformation:
    # Malmö approximate coordinate in WGS84.
    longitude = 13.0038
    latitude = 55.6050

    sweref_x, sweref_y = CRSManager.transform_xy(
        x_coordinate=longitude,
        y_coordinate=latitude,
        source_epsg=4326,
        target_epsg=3006,
    )

    print("")
    print("Example transformation")
    print("----------------------")
    print(f"WGS84 longitude: {longitude}")
    print(f"WGS84 latitude: {latitude}")
    print(f"SWEREF99 TM X: {sweref_x:.3f}")
    print(f"SWEREF99 TM Y: {sweref_y:.3f}")