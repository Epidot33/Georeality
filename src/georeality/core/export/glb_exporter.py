"""
GeoReality GLTF Exporter

Author:
    Jonas Bermin - WSP
"""

from pathlib import Path

import pyvista as pv


def export_gltf(
    mesh: pv.DataSet,
    output_file: str,
    source_file: str = "Unknown",
    author: str = "Jonas Bermin - WSP",
    epsg_code: int = 3006,
) -> Path:
    """
    Export a mesh to glTF format.
    """

    output_path = Path(output_file)

    plotter = pv.Plotter(off_screen=True)

    plotter.add_mesh(
        mesh,
        cmap="terrain",
    )

    plotter.export_gltf(str(output_path))

    print("")
    print("GeoReality Export Summary")
    print("-------------------------")
    print(f"File: {output_path.name}")
    print(f"Source: {source_file}")
    print(f"Author: {author}")
    print(f"CRS: EPSG:{epsg_code}")
    print(f"Vertices: {mesh.n_points}")
    print(f"Cells: {mesh.n_cells}")

    return output_path