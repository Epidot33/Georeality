"""
GeoReality Layer Model

Author:
    Jonas Bermin - WSP

Description:
    Defines the GeoReality layer object used throughout
    the platform.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class Layer:
    """
    GeoReality data layer.
    """

    name: str
    layer_type: str
    source_file: str
    epsg_code: int

    visible: bool = True

    mesh: Optional[object] = None

    def summary(self) -> str:
        """
        Return a formatted layer summary.
        """

        if self.mesh is not None:
            mesh_status = (
                f"Loaded "
                f"({self.mesh.n_points} points, "
                f"{self.mesh.n_cells} cells)"
            )
        else:
            mesh_status = "Not Loaded"

        return (
            f"Layer: {self.name}\n"
            f"Type: {self.layer_type}\n"
            f"Source: {self.source_file}\n"
            f"EPSG: {self.epsg_code}\n"
            f"Visible: {self.visible}\n"
            f"Mesh: {mesh_status}"
        )


if __name__ == "__main__":

    test_layer = Layer(
        name="Magnetic Susceptibility",
        layer_type="geophysics",
        source_file="test.grd",
        epsg_code=3006,
    )

    print("GeoReality Layer Model")
    print("----------------------")
    print(test_layer.summary())