
Questions and comments are welcomed. Please please join the list
    eqrm-user (https://sourceforge.net/mail/?group_id=198293).

---------------------------------------------------------------------
Summary:

The module, "demo_risk.py" demonstrates the ability of EQRM to
calculate earthquake risk for a given input ground motions.  This
module requires several key inputs in order for it to function, and
outputs a summary of the fractional damage and dollar loss to a given
structure.  These inputs and outputs are described below.

---------------------------------------------------------------------

Inputs:

1) The first requirement to run "demo_risk.py" is the input ground
   motions (or spectral accelerations) at the sites of interest (e.g.,
   see "example_soil_SA.txt" in the "input" directory).  At present,
   this ground motion file is automatically generated when the main
   EQRM analysis module, "eqrm_analysis.py", is run for a scenario
   risk event.  Ground motions are calculated at the location of
   structures, (see below).  In the future, we plan EQRM to have the ability
   to parse gridded shaking information (e.g., from the USGS ShakeMap
   program), and interpolate these ground shaking values to the
   locations specified in the structure file.

2) Information regarding the structures if interest is needed (e.g.,
   see "structure_example.csv").  Detailed information on the content
   of this file is given in the EQRM technical manual (p. 45-53) and
   the Site_file_specification.doc document, but in summary, this file
   includes the location of each structure, the stucture type,
   stucture usage (residential or commercial), suburb/town, postcode,
   building and contents cost density, and the floor area.
   
For further information about the inputs to risk_main read the
comments for risk_main in eqrm_code/risk.py.

---------------------------------------------------------------------

Outputs:

Running "demo_risk.py" will output four files detailed below.  Note
file names will change on modifying input and output file name
information in "demo_risk.py" (see notes on usage below).

demo_risk_structural_damage.txt: Delivers the cumulative probability of each
structure being in each of the following damage states; slight,
moderate, extensive, and complete

demo_risk_building_loss.txt: For each building, delivers the dollar
loss value due to structural and non-structural damage, excluding contents.

demo_risk_contents_loss.txt: For each building, delivers the dollar
loss value owing to contents damage.

demo_risk_total_building_loss.txt: For each building, delivers the
total dollar loss value due to buidling and contents damage

---------------------------------------------------------------------

Usage:

1) Save "demo_risk.py" as another file (e.g., "scenario1_risk.py"),

2) Modify input and output directory names as necessary.

3) Modify input and output file names as necessary.

4) Type "python scenario1_risk.py" into command window.