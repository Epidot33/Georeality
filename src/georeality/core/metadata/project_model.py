"""
GeoReality Project Model

Author:
    Jonas Bermin - WSP

Description:
    Defines the GeoReality project object.
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[4]
src_directory = project_root / "src"

sys.path.insert(0, str(src_directory))

from dataclasses import dataclass, field
from typing import List

from georeality.core.metadata.layer_model import Layer


@dataclass
class Project:
    """
    GeoReality project.
    """

    name: str
    epsg_code: int
    author: str = "Jonas Bermin - WSP"

    layers: List[Layer] = field(default_factory=list)

    def add_layer(self, layer: Layer) -> None:
        """
        Add a layer to the project.
        """

        self.layers.append(layer)

    def layer_count(self) -> int:
        """
        Return number of layers in the project.
        """

        return len(self.layers)

    def summary(self) -> str:
        """
        Return project summary.
        """

        text = (
            f"Project: {self.name}\n"
            f"Author: {self.author}\n"
            f"EPSG: {self.epsg_code}\n"
            f"Layers: {self.layer_count()}\n"
        )

        if self.layers:

            text += "\nLayer List\n"
            text += "----------\n"

            for layer in self.layers:

                text += (
                    f"{layer.name} "
                    f"({layer.layer_type})\n"
                )

        return text



if __name__ == "__main__":

    from georeality.core.io.grd_reader import read_grd
    from georeality.core.geometry.mesh_builder import create_surface_mesh


    grid = read_grd(
        r"C:\Users\jonas\OneDrive\georeality\examples\grids\test.grd"
    )

    mesh = create_surface_mesh(grid)

    magnetic_layer = Layer(
        name="Magnetic Susceptibility",
        layer_type="geophysics",
        source_file="test.grd",
        epsg_code=3006,
        mesh=mesh,
    )

    project = Project(
        name="GeoReality Test Project",
        epsg_code=3006,
    )

    project.add_layer(magnetic_layer)
    
    for layer in project.layers:

        print("")
        print(layer.summary())

    print("GeoReality Project Model")
    print("------------------------")
    print(project.summary())
