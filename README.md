# SL2 Patch Builder
This repository contains a work-in-progress patch builder/customizer for the Boss SL-2 Slicer effect pedal. Thanks to /u/CompetitionSuper7287 on reddit for figuring out all of the parameter array mappings for .tsl files!

## What works
- Plotly Dash-based dashboard provides a web interface for reading and writing .tsl files. 
- Basic library for reading, validating, and writing .tsl files using the `sl2` module

## What's in progress (in order of most-to-least priority)
- Implement the rest of the parameters (beyond just `PATCH%SLICER(1)` and `PATCH%SLICER(2)`):
  - Continue development of `sl2` to support validation for other parameters.
  - Update dashboard to enable modification of these parameters.
- Finalize structure and clean implementation of `sl2` module.
- Generate documentation for `sl2` module.
