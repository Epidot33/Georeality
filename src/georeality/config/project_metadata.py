"""
GeoReality Project Metadata

Author:
    Jonas Bermin - WSP

Project:
    GeoReality

Description:
    Central metadata definitions for the GeoReality platform.

Development Note:
    This file may include AI-assisted drafting.
    All generated code must be reviewed,
    understood and tested before use.
"""

# =============================================================================
# PROJECT INFORMATION
# =============================================================================

PROJECT_NAME: str = "GeoReality"

PROJECT_VERSION: str = "0.1.0"

PROJECT_AUTHOR: str = "Jonas Bermin - WSP"

PROJECT_ORGANISATION: str = "WSP"

PROJECT_DESCRIPTION: str = (
    "Visualization platform for Swedish subsurface data."
)

# =============================================================================
# LANGUAGE SETTINGS
# =============================================================================

DEFAULT_LANGUAGE: str = "sv"

SUPPORTED_LANGUAGES = [
    "sv",
    "en",
]

# =============================================================================
# DEFAULT COUNTRY PROFILE
# =============================================================================

DEFAULT_COUNTRY_PROFILE: str = "Sweden"

# =============================================================================
# COORDINATE REFERENCE SYSTEMS
# =============================================================================

DEFAULT_PROJECT_EPSG: int = 3006

DEFAULT_PROJECT_CRS_NAME: str = "SWEREF99 TM"

DEFAULT_VERTICAL_REFERENCE_SYSTEM: str = "RH2000"

# =============================================================================
# DATA SOURCES
# =============================================================================

SUPPORTED_DATA_SOURCES = [
    "SGU",
    "Lantmäteriet",
    "Surfer",
    "ArcGIS",
    "CSV",
    "XYZ",
    "GeoTIFF",
]

# =============================================================================
# SIMPLE TEST
# =============================================================================

if __name__ == "__main__":

    print("GeoReality Metadata")
    print("-------------------")
    print(f"Project: {PROJECT_NAME}")
    print(f"Version: {PROJECT_VERSION}")
    print(f"Author: {PROJECT_AUTHOR}")
    print(f"Default CRS: {DEFAULT_PROJECT_CRS_NAME}")
    print(f"EPSG: {DEFAULT_PROJECT_EPSG}")