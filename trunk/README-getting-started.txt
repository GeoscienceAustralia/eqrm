
Questions and comments are welcomed. Please please join the list
    eqrm-user (https://sourceforge.net/mail/?group_id=198293).

---------------------------------------------------------------------

1. DIFFERENT RUN MODES

*** Five DEMOS are provided in *\eqrm_core\demo. This section demonstrates
 how to use them. Note that * refers to a path - it will vary depending where
 you have installed the EQRM. 

*** All of the demos are deliberately working on a subset of data. To undertake
 the full simulation toggle small_site_flag in the parameter file.
    

1) Ground Motion Scenario 

    Run at DOS command line:
    cd *\eqrm_core\demo
    python setdata_ScenGM.py


2) Damage Scenario with a single attenuation model 
   file: setdata_ScenRisk.txt)

    Run at DOS command line:
    cd *\eqrm_core\demo
    python setdata_ScenRisk.py

3) Damage Scenario with multiple attenuation models 
  

    Run at DOS command line:
    cd *\eqrm_core\demo
    python setdata_ScenRisk.py


4) Probabilistic Hazard Simulation 

    Run at DOS command line:
    cd *\eqrm_core\demo
    python setdata_ProbHaz.py

5) Probabilistic Risk Simulation

    Run at DOS command line:
    cd *\eqrm_core\demo
    python setdata_ProbRisk.py


INPUT:
1) The first input *\demo\setdata_ProbRisk.py is a parameter file
   containing flags and other input parameters to control the type/nature
   of the simulation. Further information of individual parameters is
   given in *\eqrm_core\Documentation\new_param_list.pdf
2) The second input controls the random number seed (see below for further
   information.
3) A third (optional) input can be used to force the EQRM to zip output
   files for reduced storage (see below for further information). Otherwise
   outputs are saved as ascii files. 
   
The parameter file gives the location of the site file.  The format of
the site file is described in documentation/site_file_specification.

---------------------------------------------------------------------

2. RESETTING THE RANDOM NUMBER SEED

The EQRM relies on random numbers - you must explicitly choose
between using a hardwired seed value, or using time as a random
seed.

Run at DOS command line:
    cd *\eqrm_core\demo
    python setdata_ScenGM.py y
        ** to deterministicaly seed the random number generator
           (the run is repeatable)

        or

    python setdata_ScenGM.py n
        ** to seed the random number generated based on time (the run
           is not repeatable)

NOTE - We recommend that you deterministically set the seed. Having
	 repeatable runs is very useful (or even essential) for many
	 projects. 
	 
	 Generally, the only exception to this is if you wish to
	 conduct a sensitivity analysis to the random number sequence.

---------------------------------------------------------------------

3. SAVING OPTIONS

The EQRM saves outputs as text files. An optionally input can be supplied
when calling the EQRM if the user desires these files to be zipped. 

This is worth doing if you have a large number of site-event pairs;
particularly if doing a scenario loss of probabilistic risk
simulation.

To implement the zip save mode run the following at the DOS command line
(note use of second y):
    	cd *\eqrm_core\demo
	python setdata_ProbHaz.py y y


---------------------------------------------------------------------

4. INPUTS:

*** All simulations require an input parameter file. Examples of these
    include setdata_ProbRisk.txt, setdata_ScenRisk2.txt, etc. An
    explanation of all parameters in the input file is provided in
    
              *\eqrm_core\Documentation\new_param_list.pdf

There are three variables that warrant special mention here.
1) site_loc = 	string prefix used for all input and output files. 
		The EQRM user must select a prefix to suite the project.
		For example we use newc for the Newcastle projects. 
		
2) inputdir =  string full path to directory containin input files such as
		source zone files, grid files etc. (see below for more 
		information). Local that the EQRM will search for all input
		files in inputdir - if it can not find it there it will 
		then search in *\eqrm_core\resources\data.
		
3) savedir  =  string full path for location to save output files. 

*** The following lists the input files required for each of the major
    simulation types and it points to examples that ship with the eqrm
    in the *\eqrm_core\resources\data directory:

1) Ground Motion Scenario (example parameter file: setdata_ScenGM.py)
		
	a) A grid of sites at which to compute motion (longitude,
	latitude and site class)
	e.g. *\eqrm_core\demo\input\newc_par_site.csv (if grid_flag
	== 1) 
	*** use a dummy variable for site class (e.g. A) if not
	using amplification

	b) OPTIONAL: Amplification Factors are needed if using amplification
		e.g. *\eqrm_core\demo\input\newc_par_ampfactors.xml   

2) Damage Scenario (example parameter file: setdata_ScenRisk.py)

	a) Building database (contains building locations, properties etc.)
	e.g. *\eqrm_core\demo\input\sitedb_newc.csv
	*** use a dummy variable for site class (e.g. A) if not using
	 amplification

	b) OPTIONAL: Amplification Factors are needed if using amplification
	e.g. *\eqrm_core\demo\input\newc_par_ampfactors.xml   


3) Probabilistic Hazard Simulation (e.g. parameter file: setdata_ProbHaz.txt)
		
	a) Source zone file (boundary, G-R parameters (Lambda_Min,b),
	Mag_min, Mag_max, area etc.
	e.g. *\eqrm_core\demo\input\newc_source_polygon.xml *** note
	that Lambda_Min is the actual number of earthquakes of Mag >=
	Mag_min expected per year (i.e. it is related to the G-R a
	parameter but it is different)
		
	b) A grid of sites at which to compute hazard (longitude,
	latitude and site class)
	e.g. *\eqrm_core\demo\input\newc_par_site.csv (if grid_flag
	== 1) 
	*** use a dummy variable for site class (e.g. A) if not
	using amplification

	c) OPTIONAL: Amplification Factors are needed if using amplification
		e.g. *\eqrm_core\demo\input\newc_par_ampfactors.xml   


4) Probabilistic Risk Simulation (example parameter file: setdata_ProbRisk.txt)

	a) Source zone file (boundary, G-R parameters (Lambda_Min,b),
	Mag_min, Mag_max, area etc.
	e.g. *\eqrm_core\demo\input\newc_source_polygon.xml 
	
	*** note that Lambda_Min is the actual number of earthquakes
	of Mag >= Mag_min expected per year (i.e. it is related to the
	G-R a parameter but it is different)
		
	b) Building database (contains building locations, properties etc.)
	e.g. *\eqrm_core\demo\input\sitedb_newc.csv
	*** use a dummy variable for site class (e.g. A) if not using
	 amplification

	c) OPTIONAL: Amplification Factors are needed if using amplification
	e.g. *\eqrm_core\demo\input\newc_par_ampfactors.xml   


COMMENT ON RESOURCE AND LOCAL DATA FILES: When eqrm tries to open an
input file (such as site locations, soil amplification files, etc), it
first checks in the local input directory (specified as inputdir in
the parameter file), then it looks in the EQRM resource directory
(*\eqrm_core\resources\data).


GENERATING THE INPUT FILES: for the most part you are on your own in
this department. Just look at the examples for the desired file format
and generate the required files for your own study.

*** However, there is one utility to help with the geration of a grid
for ground motion or probabilistic hazard calculations. You will need
to supply a polygon file containing the site class polygons in the
correct format (e.g. perth_par_site_class_polys.xml). You can then
generate your grid at the DOS prompt as follows.

	cd  *\eqrm_core\preprocessing
	python grid_generator.py newc ..\implementation_tests\input c:\temp\eqrmdemos 50 50

	Where the inputs (in order) are:
		1) site_loc (e.g. newc)
		2) directory containing *_par_site_class_polys.xml 
		(e.g. ..\implementation_tests\input)
		3) directory to save output grid file (e.g. c:/temp/eqrmdemos)
		4) nlats: number of latitude grid points along line of
		 equal longitude (e.g. 50)
		5) nlons: number of longitude grid points along line
		 of equal latitude (e.g. 50)


---------------------------------------------------------------------
5. SETTING UP A BATCH SIMULATION

If you are doing multiple simulations you will probably want to use a
batch file to process all your simulations. An example of how to do
this is provided in the demo area. To run at the DOS command prompt:

    cd *\eqrm_core\demo
    python demo_batchrun.py 


---------------------------------------------------------------------

6. POSTPROCESSING

Note that all outputs from the EQRM are text files (or gzip compressed
text files).  You are free to analyse this data as you
please. However, a number of MATLAB processing routines are supplied
for your convenience. You will need a MATLAB license to use these.
They all follow the same basic process (from within MATLAB): 1)
Convert the EQRM output files to a Matlab binary file (*.MAT) with
pre-specified format 2) Run a Matlab function (or functions) to
process and/or plot the data

It is useful to note that there is a fundamental difference between
the data saved in a probabilistic hazard (PSHA) and a probablistic
risk simulation (PSRA).In the case of PSHA the output are hazard
values (i.e. we do not save the ground motion at each site due to
memory problems encountered if you need ground motion across multiple
RSA periods), whereas the outputs for PSRA are estimated loss values
at each building for every synthetic event. In the later case you must
consider this loss data as well as the event activities (something
like a 'probability') to get a loss exceedance curve. The examples
below demonstrate how to process/plot the data for each of the demo
types above.

Please also note that some of these have not been used extensively and
may contain bugs - USE WITH CAUTION.

EXAMPLES Follow
	- Commands must be implemented at the MATLAB prompt 
	- text following % is a comment 
	- all the MATLAB routines have extensive comments and help files
	- you must modify the MATLABPATH environment variable to
	include the following directories.  (This is done within
	Matlab using file>Set Path):
		1) *\eqrm_core\Matlab_utils
		2) *\eqrm_core\preprocessing
		3) *\eqrm_core\postprocessing
		
	- the following instructions assume that you have not asked
        the EQRM to compress the output files. If you do have
        compressed output files use the wrapper Convert_gunzip_outputs
        in place of the routines Convert_Py2Mat_Risk or
        Convert_Py2Mat_Hazard.


1) Ground Motion Scenario (example parameter file: setdata_ScenGM.txt)

	>> demodir = 'C:\eqrm\demo\output\scen_gm' 
	>> cd(demodir) 
	>> Convert_Py2Mat_ScenGroundMot(demodir,'THE_PARAM_T.txt')  % convert EQRM outputs to MATLAB binary file 
	
	*** Now the data are conveniently in MATLAB but there are no
	 Matlab plotting tools for this ***


2) Damage Scenario with a single attenuation model (example parameter
   file: setdata_ScenRisk.txt)
	
	>> demodir = 'C:\temp\demo\output\scen_risk';
	>> cd(demodir) 
	>> Convert_Py2Mat_Risk(demodir,'THE_PARAM_T.txt','C:\workstuff\sandpit\eqrm_core\resources\data') % convert EQRM outputs to MATLAB binary files (x2) 
	
	*** Now the data are conveniently in MATLAB - it's time to 
	have a look at it ***
	
	*** The following will draw two histograms and compute 
	some basic data ***
	>> [eqrm_param_T, ecloss_data,scen_loss_stats,hf] = wrap_risk_plots(1,'calc_scen_loss_stats',demodir, [demodir,'/matlab_setdata.mat'],[demodir,'/newc_db_savedecloss.mat'],{1,1,1,1,[1,50]});

	*** The following will compute the loss observed in different suburbs ***
	*** CAUTION - this has not been thouroughly tested! ***
	>> [eqrm_param_T, ecloss_data,scenloss_sub_T] = wrap_risk_plots(1, 'calc_scenloss_sub',demodir, [demodir,'/matlab_setdata.mat'],[demodir,'/newc_db_savedecloss.mat'],{0,0,0,10});
	
	*** Note that that for large data sets it is possible to
          re-use wrap_risk_plots multiple times without re-loading the
          MATLAB binary file that is produced by Convert_Py2Mat_Risk
          (see in-built help for wrap_risk_plots for further
          information). ***

3) Damage Scenario with multiple attenuation models (example parameter
   file: setdata_ScenRisk2.txt)

	>> demodir = 'C:\temp\demo\output\scen_risk2';
	>> cd(demodir) 

		*** as in Example 2 ***

4) Probabilistic Hazard Simulation (example parameter file:
   setdata_ProbHaz.txt)

	>> demodir = 'C:\temp\demo\output\prob_haz';
	>> cd(demodir)
	>> Convert_Py2Mat_Hazard(demodir ,'THE_PARAM_T.txt')

	*** The following computes and plot the uniform hazard spectra
	at two points ***
	
	>> [tmp]=plot_singlesite_hzd([demodir,'\newc_db_hzd.mat'],'UniformHzd',[151.65,-33.15;151.5,-32.9; 151.6,-33],[500 2500],'lin','rock','single');

	*** The following plots a hazard exceedance curves for two sites at the three periods [0 0.30303 1]
	>> [tmp]=plot_singlesite_hzd([demodir,'\newc_db_hzd.mat'],'HazPML',[151.65,-33.15;151.5,-32.9; 151.6,-33],[0 0.30303 1],'lin','rock','single');


5) Probabilistic Risk Simulation (example parameter file:
   setdata_ProbRisk.txt)

	>> demodir = 'C:\temp\demo\output\prob_risk'; % use scen_gm?
	>> cd(demodir)
	>> Convert_Py2Mat_Risk(demodir,'THE_PARAM_T.txt','C:\workstuff\sandpit\eqrm_core\resources\data') % convert EQRM outputs to MATLAB binary files (x2) 
	
	*** Now the data are conveniently in MATLAB - it's time to have a look at it ***

	*** The following will draw a loss exceedance curve
	>> [eqrm_param_T, ecloss_data, pml_curve, hf] = wrap_risk_plots(1, 'calc_pml', demodir, [demodir,'/matlab_setdata.mat'],[demodir,'/newc_db_savedecloss.mat'],{'p','d'});
	
	*** The following computes the annualised loss and draws a
            picture of the cummulative annualised loss
	>> [eqrm_param_T, ecloss_data, ann_loss, hf] = wrap_risk_plots(1, 'calc_annloss', demodir, [demodir,'/matlab_setdata.mat'],[demodir,'/newc_db_savedecloss.mat'],{'p','d'});

	*** The following plots the dis-aggregated annualised loss in distance-magnitude bins
	>> [eqrm_param_T, ecloss_data,NormDeAggLoss, hf] = wrap_risk_plots(1,'calc_annloss_deagg_distmag',demodir, [demodir,'/matlab_setdata.mat'],[demodir,'/newc_db_savedecloss.mat'],{[4.5:0.5:6.5],[4.5:0.5:6.5],0:5:100, 1,1,[0,8]});
	
	*** The following will compute the dis-aggregated annualised
            loss for different suburbs.
	*** This is broken.  It requires sitedb_newc.mat
	>> [eqrm_param_T, ecloss_data,annloss_deagg_sub_T] = wrap_risk_plots(1, 'calc_annloss_deagg_sub',demodir, [demodir,'/matlab_setdata.mat'],[demodir,'/newc_db_savedecloss.mat']);

	*** The following will compute the dis-aggregated annualised loss by structural type categories: Steel Frame, Timber frame, Concrete, Un-reinforced Masonry and plot a figure
	>> [eqrm_param_T, ecloss_data,annloss_deagg_structural_T,hf] = wrap_risk_plots(1,'calc_annloss_deagg_structural',demodir,[demodir,'/matlab_setdata.mat'],[demodir,'/newc_db_savedecloss.mat'],{1,[0,0.08]});

	***** The following will compute the dis-aggregated annualised
              by structural type (not categories as with
              'calc_annloss_deagg_structural') and save outputs to
              file
	*** This is broken.  It requires sitedb_newc.mat
	>> [eqrm_param_T, ecloss_data,annloss_deagg_btype_T] = wrap_risk_plots(1, 'calc_annloss_deagg_btype',demodir,[demodir,'/matlab_setdata.mat'],[demodir,'/newc_db_savedecloss.mat']);


	*** Note that that for large data sets it is possible to
	re-use wrap_risk_plots multiple times without re-loading the
	MATLAB binary file that is produced by Convert_Py2Mat_Risk
	(see in-built help for wrap_risk_plots for further
	information).

---------------------------------------------------------------------

RUNNING EQRM IN PARALLEL

EQRM can run in parallel using mpi. Run mpirun and an EQRM script to
run a scenario in parallel.  Here is an example of running
check_scenarios in parallel, on 4 processes;
 
 mpirun -np 4 -hostfile ~/.machines_tornado -x PYTHONPATH python2.5
 check_scenarios.py
 
 Check the web for more information on mpirun to run EQRM in parallel.
