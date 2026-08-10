\# GeoReality Architecture



Version: 1.0

Status: Draft



Author: Jonas Bermin - WSP



\---



\# Vision



GeoReality is a modular visualization platform for Swedish

subsurface data.



The platform is designed to support environmental,

hydrogeological, geological and geophysical information

in interactive 3D environments and future augmented

reality workflows.



\---



\# Design Principles



1\. All source code shall be written in English.



2\. All comments shall be written in English.



3\. All technical documentation shall be written in English.



4\. User interface text shall be localizable.



5\. Sweden-first approach.



6\. Modular architecture.



7\. Coordinate-system agnostic design.



8\. Full metadata traceability.



9\. Sandbox visualization before augmented reality.



10\. Open and documented file formats whenever possible.



\---



\# Primary Data Sources



\- SGU

\- Lantmäteriet

\- Surfer

\- ArcGIS

\- CSV

\- XYZ



\---



\# Coordinate Systems



Default:



\- SWEREF99 TM (EPSG:3006)



Preferred vertical reference:



\- RH2000



The platform shall support any EPSG-based coordinate

reference system through pyproj.



\---



\# Project Metadata



Default project author:



Jonas Bermin - WSP



Required metadata:



\- Project name

\- Author

\- Date created

\- Coordinate system

\- Source files

\- Data type

\- Processing method



\---



\# Architecture



Core:



\- Data IO

\- Coordinates

\- Geometry

\- Metadata

\- Export



Modules:



\- Sweden

\- PFAS

\- Hydrogeology

\- Geophysics



Frontend:



\- Web Viewer

\- Localization



\---



\# MVP Objectives



Version 0.1



\- Read Surfer GRD

\- Generate surface mesh

\- Export GLB

\- Display model in browser

\- Display metadata

\- Support mobile devices



AR functionality is not included in Version 0.1.

# Prototype Progress

Completed Components

- Project Metadata
- CRS Manager
- Coordinate Transformation Engine
- Surfer 7 Binary GRD Reader
- Mesh Builder
- glTF Exporter

Validated Workflows

GRD
↓
GeoReality Reader
↓
Mesh Builder
↓
PyVista Rendering
↓
glTF Export

\---



\# Long-Term Goals



\- Sandbox visualization

\- SGU integration

\- Lantmäteriet integration

\- Groundwater surfaces

\- Virtual boreholes

\- Geophysical models

\- Augmented reality

