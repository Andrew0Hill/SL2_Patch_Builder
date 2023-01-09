# SL2 Patch Builder
This project provides the ability to create and edit patterns for the Boss SL-2 Slicer effect pedal. You can run the tool from your browser at http://sl2-patch-editor.xyz

Using this tool, you can upload any of the existing SL-2 preset patterns, and modify their parameters. You can also create your own SL-2 patches from scratch, and load them onto your SL-2.

Thanks to /u/CompetitionSuper7287 on reddit for figuring out all of the parameter array mappings for .tsl files!

# How to use this tool
A web-hosted version of this dashboard is available using the link at the top of the README. You will also need to download BOSS Tone Studio for SL-2 in order to import or export pattern files from your SL-2.

## Creating a pattern from scratch
1. Navigate to http://sl2-patch-editor.xyz 
    - The tool contains a default set of parameters that will generate a (pretty boring) SL-2 pattern. 
2. Change the parameters as desired, then click 'Download .tsl' to download your new pattern.
3. Using Tone Studio, import your `.tsl` file. A new Liveset will be created.
4. Drag the pattern you created to a slot on your SL-2.
5. Done!

## Modifying an existing pattern
1. From BOSS Tone Studio, create a new Liveset containing the patttern you'd like to modify. Export this pattern using Boss Tone Studio, the output filetype should be `.tsl`.
2. Navigate to http://sl2-patch-editor.xyz in your browser and upload your .tsl file.
3. Edit the parameters using the interface, then click the 'Download .tsl' button to download your created pattern.
    - I recommend changing the 'Patch Name' before downloading your new pattern, so that it is easy to distinguish from the original preset pattern.
4. Import the new `.tsl` file back into Tone Studio, and drag the pattern to a slot on your SL-2.
5. Done! 


## Running locally
To run the dashboard locally, clone this repository or download the .ZIP file. You will need Python 3 (Preferably Python 3.9 or 3.10) installed to run it.

Once downloaded, run 
```
pip install -r sl2_dashboard/requirements.txt
```
to install all required dependencies, then run move into the `sl2_dashboard` directory and run
```
python3 main.py
```
and navigate to the link presented in the console (likely `http://localhost:8050`)


# What works
- Plotly Dash-based dashboard provides a web interface for reading and writing .tsl files. 
- Basic library for reading, validating, and writing .tsl files using the `sl2` module

# What's in progress (in order of most-to-least priority)
- Implement the rest of the parameters (beyond just `PATCH%SLICER(1)` and `PATCH%SLICER(2)`):
  - Continue development of `sl2` to support validation for other parameters.
  - Update dashboard to enable modification of these parameters.
- Finalize structure and clean implementation of `sl2` module.
- Generate documentation for `sl2` module.

If you have any questions, issues, bugs or suggestions, please open a GitHub issue!