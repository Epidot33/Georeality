# GeoReality Roadmap

Author: Jonas Bermin - WSP

---

# Vision

GeoReality is a modular platform for visualization and interpretation of subsurface data.

The platform is designed to support:

- Hydrogeology
- Environmental investigations
- PFAS investigations
- Geophysics
- Geological modelling
- Swedish geospatial datasets

The system is built Sweden-first while maintaining a generic architecture that can be expanded internationally.

---

# Design Principles

- Build for Sweden
- Keep the core generic
- Separate visualization from data handling
- Maintain full traceability
- Keep modules independent
- Prioritize simplicity over complexity

---

# Current Status

GeoReality has moved beyond the planning stage and is now a working prototype.

Implemented and verified functionality exists for:

- Surfer grid import
- Coordinate system management
- Mesh generation
- glTF export
- Browser visualization
- Layer handling
- Project handling

---

# Version 0.1 – Core Foundation

Status: In Progress

## Objectives

Create the first complete GeoReality workflow.

## Completed

### Documentation

- README
- ARCHITECTURE
- ROADMAP
- AI_USAGE
- Development Log

### Core Infrastructure

- Project metadata
- Layer model
- Project model
- CRS manager
- Coordinate transformations

### Data Import

- Surfer 7 Binary Grid (DSRB) reader

### Geometry

- Structured mesh generation
- NoData handling

### Export

- glTF export

### Viewer

- Three.js viewer
- Orbit navigation
- Auto centering
- Auto zoom
- Local server workflow
- Drag-and-drop interface
- Browser visualization

### Workflows

Implemented:

GRD
→ Reader
→ Mesh
→ Layer
→ Project
→ glTF
→ Browser Viewer

### Validation

Successfully tested using a real-world magnetic susceptibility dataset.

Verified:

- Coordinate transformations
- Mesh generation
- glTF export
- Browser visualization
- Viewer navigation
- Drag-and-drop loading

## Remaining

- Package installation
- Improved project persistence
- Layer serialization
- Automated testing
- Viewer polish

## Deliverable

First working GeoReality prototype.

---

# Version 0.2 – Project Management

Status: Planned

## Objectives

Support complete GeoReality projects.

## Features

- Project save/load
- Project file format
- Layer collections
- Layer visibility
- Layer groups
- Scene persistence

## Deliverables

A project containing multiple layers can be saved and reopened.

Example:

- Topography
- Groundwater
- PFAS
- Geophysics

within the same project.

---

# Version 0.3 – Multi-Layer Visualization

Status: Planned

## Objectives

Support simultaneous visualization of multiple datasets.

## Features

- Multi-layer scenes
- Layer manager
- Layer visibility controls
- Layer ordering
- Opacity control

## Deliverables

Interactive management of multiple datasets in the same scene.

---

# Version 0.4 – Sweden Integration

Status: Planned

## Objectives

Native support for Swedish data sources.

## Features

- SGU integration
- Lantmäteriet integration
- Swedish CRS presets
- Swedish terrain support

## Deliverables

Direct import of common Swedish geospatial datasets.

---

# Version 0.5 – Hydrogeology Module

Status: Planned

## Objectives

Support hydrogeological investigations.

## Features

- Groundwater surfaces
- Hydraulic gradients
- Flow vectors
- Virtual observation wells

## Deliverables

Interactive groundwater visualization.

---

# Version 0.6 – PFAS Module

Status: Planned

## Objectives

Support environmental contamination projects.

## Features

- PFAS concentration surfaces
- PFAS plume visualization
- Time-series support
- Source area visualization
- Contaminant layer management

## Deliverables

Interactive PFAS investigation support.

---

# Version 0.7 – Geophysics Module

Status: Planned

## Objectives

Support geophysical datasets.

## Features

- Magnetic susceptibility
- Resistivity
- Conductivity
- CVES sections
- Geophysical volumes

## Deliverables

Interactive geophysical interpretation environment.

---

# Version 0.8 – Sandbox Environment

Status: Planned

## Objectives

Provide immersive model exploration.

## Features

- Tabletop mode
- Adjustable scale
- Scene presets
- Presentation mode

## Deliverables

Interactive sandbox visualization.

---

# Version 0.9 – Augmented Reality Foundations

Status: Planned

## Objectives

Prepare for field-based visualization.

## Features

- AR-ready scene export
- Real-world scaling
- GPS integration groundwork

## Deliverables

First AR-compatible GeoReality projects.

---

# Version 1.0 – GeoReality Release

Status: Vision

## Objectives

Release the first production-ready version.

## Features

- Stable architecture
- Multi-layer projects
- Hydrogeology module
- PFAS module
- Geophysics module
- Swedish geodata integration
- Browser viewer
- Sandbox mode

## Deliverables

Production-ready GeoReality platform.

---

# Development Milestones

## Milestone 01

First successful import of a real-world Surfer grid.

Completed.

---

## Milestone 02

First successful mesh generation.

Completed.

---

## Milestone 03

First successful glTF export.

Completed.

---

## Milestone 04

First successful browser visualization.

Completed.

---

## Milestone 05

First complete GeoReality workflow.

Completed.

Workflow:

GRD
→ Reader
→ Mesh
→ Layer
→ Project
→ glTF
→ Browser Viewer

---

# Current Priority

1. Project persistence
2. Layer management
3. Multi-layer visualization
4. Viewer improvements
5. Swedish data integration

---

# GeoReality Principle

"It is just a matter of throwing it in."

The user should be able to import data, visualize it and begin interpretation with as little friction as possible.