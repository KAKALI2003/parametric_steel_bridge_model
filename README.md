# Parametric Steel Girder Bridge (pythonOCC)

This project generates a parametric 3D CAD model of a steel girder bridge using **PythonOCC (OpenCASCADE)**.

The bridge model includes:

- Steel I-girders
- Reinforced concrete deck
- Kerb (edge support)
- Parapet walls
- STEP export for CAD interoperability

## Features

- Parametric bridge geometry
- Adjustable span length
- Adjustable girder spacing
- Adjustable section dimensions
- Automatic 3D visualization
- STEP file export

## Bridge Components

- Steel I-section girders
- Concrete deck slab
- Edge kerb support
- Parapet walls

## Default Parameters

| Parameter | Value |
|-----------|------|
Span Length | 12000 mm|
Number of Girders | 3|
Girder Spacing | 3000 mm|
Deck Thickness | 200 mm|
Deck Overhang | 500 mm|

## Installation

```bash
pip install pythonocc-core