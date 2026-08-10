"""
GeoReality Import GRD Workflow

Author:
    Jonas Bermin - WSP

Description:
    Complete workflow:

    GRD
      -> Layer
      -> Mesh
      -> Project
      -> glTF Export
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[3]
src_directory = project_root / "src"

sys.path.insert(0, str(src_directory))

from georeality.core.io.grd_reader import read_grd
from georeality.core.geometry.mesh_builder import create_surface_mesh
from georeality.core.metadata.layer_model import Layer
from georeality.core.metadata.project_model import Project
from georeality.core.export.glb_exporter import export_gltf


def run_workflow():

    grd_file = (
        r"C:\Users\jonas\OneDrive\georeality"
        r"\examples\grids\test2.grd"
    )

    output_file = (
        r"C:\Users\jonas\OneDrive\georeality"
        r"\examples\output\EC.gltf"
    )

    # -----------------------------------------------------------------
    # Read grid
    # -----------------------------------------------------------------

    grid = read_grd(grd_file)

    # -----------------------------------------------------------------
    # Generate mesh
    # -----------------------------------------------------------------

    mesh = create_surface_mesh(grid)

    # -----------------------------------------------------------------
    # Create layer
    # -----------------------------------------------------------------

    layer = Layer(
        name="Magnetic Susceptibility",
        layer_type="geophysics",
        source_file="test.grd",
        epsg_code=3006,
        mesh=mesh,
    )

    # -----------------------------------------------------------------
    # Create project
    # -----------------------------------------------------------------

    project = Project(
        name="GeoReality Demo Project",
        epsg_code=3006,
    )

    project.add_layer(layer)

    # -----------------------------------------------------------------
    # Export
    # -----------------------------------------------------------------

    export_gltf(
        mesh,
        output_file,
        source_file="test.grd",
    )

    print("")
    print("Workflow Summary")
    print("----------------")
    print(project.summary())


if __name__ == "__main__":

    run_workflow()