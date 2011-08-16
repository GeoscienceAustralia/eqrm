This folder contacins scripts for preparing input data to EQRM. 

Scripts include:

catalogue_reader.py
Module for reading a variety of earthquake catalogues. Please update this if there are other format that you use.

earthquake_event.py
Contains classes for earthquake events and event sets. Method exists to create subsets of event sets based on min/max values of location, time, magnitude and/or depth.

plot_catalogue_xsection.py
Plot a cross-section of a catalogue or catalogue subset by projecting all earthquakes within the subset onto a defined plane.

recurrence_from_catalogue.py
This is used to calculate a and b values from an earthquake catalogue.

recurrence_from_catalogue_subset.py
This is used to calculate a and b values from a subset of an earthquake catalogue. Subsets are defined as in plot_catalogue_xsection.py