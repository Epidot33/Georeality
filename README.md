\# GeoReality



Author: Jonas Bermin - WSP



\## Overview



GeoReality is a modular visualization platform for Swedish subsurface data.



The platform is designed to support:



\- Environmental data

\- Hydrogeological data

\- Geological data

\- Geophysical data



GeoReality focuses on interactive 3D visualization and future augmented reality workflows.



\---



\## Vision



To make subsurface data easier to understand, communicate and explore through modern visualization technology.



\---



\## Primary Data Sources



\- SGU

\- Lantmäteriet

\- Surfer

\- ArcGIS

\- CSV

\- XYZ

\- GeoTIFF



\---



\## Design Principles



\- Code language: English

\- Comments: English

\- Documentation: English

\- User interface: Localizable

\- Sweden-first strategy

\- Modular architecture

\- Coordinate-system agnostic

\- Metadata-driven design

\- Full traceability



\---



\## Project Structure



src/

docs/

tests/

examples/



\---



\## MVP Goals



Version 0.1



\- Read Surfer GRD files

\- Generate 3D surface meshes

\- Export GLB models

\- Display models in a web browser

\- Support mobile devices

\- Support metadata and coordinate systems



\---



\## Long-Term Goals



\- SGU data integration

\- Lantmäteriet integration

\- Groundwater visualization

\- Virtual boreholes

\- Geophysical models

\- Sandbox visualization

\- Augmented reality



\---


## Current Status

The GeoReality prototype can currently:

- Read Surfer 7 binary GRD files
- Handle NoData values
- Generate structured 3D meshes
- Display models using PyVista
- Export models to glTF format
- Manage coordinate reference systems using EPSG codes
- Support SWEREF99 TM as the default Swedish project CRS

The prototype has been successfully tested using real geophysical data.

Current Capabilities

GeoReality can currently:

- Import Surfer 7 Binary GRD files
- Generate 3D meshes
- Create GeoReality projects and layers
- Export glTF models
- Visualize models in a web browser
- Load models through drag-and-drop

Validated using multiple real-world geophysical datasets.


\## Author



Jonas Bermin - WSP

