# SL2 Patch Builder
This repository contains a work-in-progress patch builder/customizer for the Boss SL-2 Slicer effect pedal. Thanks to /u/CompetitionSuper7287 on reddit for figuring out all of the parameter array mappings!

## What works
- Skeleton functionality for reading a `.tsl` live set file, converting to Python objects, and writing back to `.tsl`.

## What's in progress (in order of most-to-least priority)
- Verify that a `.tsl` file written from program can be read correctly by the SL-2
- Complete the Jupyter notebook to demonstrate reading/modifying/writing a patch.
  - Extend the basic audio "simulation" of the slicer pattern, so that users can get an idea of what their custom pattern sounds like without having to export and upload to the SL-2 every time they change something. *Note: The audio simulation will only include the slicer effect, I do not anticipate trying to simulate the SL-2's EQ, Compression, Noise Supression, etc. *
  - Create visualizations/simple GUI to help in designing patches (i.e. drag parameters up/down).
- Generate a packaged GUI application or web dashboard that allows users to generate, modify, preview, and download their own patches.
