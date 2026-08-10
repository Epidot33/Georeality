"""
GeoReality Mesh Builder

Author:
    Jonas Bermin - WSP

Description:
    Create 3D meshes from GeoReality grid objects.
"""

from pathlib import Path
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[4]
src_directory = project_root / "src"

sys.path.insert(0, str(src_directory))
import numpy as np
import pyvista as pv

from georeality.core.io.grd_reader import read_grd
from georeality.core.export.glb_exporter import export_gltf

def create_surface_mesh(grid):
    """
    Create a PyVista StructuredGrid from a Surfer grid.
    """

    x_grid, y_grid = np.meshgrid(
        grid.x_coordinates,
        grid.y_coordinates
    )

    z_grid = np.nan_to_num(
        grid.z_values,
        nan=np.nanmin(grid.z_values)
    )

    surface_mesh = pv.StructuredGrid(
        x_grid,
        y_grid,
        z_grid
    )

    return surface_mesh


if __name__ == "__main__":

    grid = read_grd(
        r"C:\Users\jonas\OneDrive\georeality\examples\grids\test.grd"
    )

    mesh = create_surface_mesh(grid)
    
    export_path = export_gltf(
        mesh,
        r"C:\Users\jonas\OneDrive\georeality\examples\output\test.gltf",
        source_file="test.grd",
        author="Jonas Bermin - WSP",
        epsg_code=3006,
    )

    print("")
    print("GLB Export")
    print("----------")
    print(export_path)

    print("GeoReality Mesh Builder")
    print("-----------------------")
    print(mesh)

    mesh.plot(
        show_edges=False,
        cmap="terrain"
    )
    
