
import os
import string

from eqrm_code import eqrm_filesystem
from eqrm_code import analysis
from eqrm_code import parse_in_parameters


plot_demo_run_names = [
    'plot_probhaz2.py', 'plot_probhaz.py', 'plot_prob_risk.py',
                 'plot_scen_gm.py', 'plot_scen_risk.py']
                 
def demo_run(verbose=True, plot_dir=eqrm_filesystem.demo_plot_path,
             run_names=plot_demo_run_names):
    if verbose:
        print 'STARTING'  

    plot_dir = os.path.join(plot_dir) # Why do this?
    current_dir = os.path.abspath(os.getcwd())
    print "current_dir", current_dir
    os.chdir(plot_dir)
    if verbose:
        print 'Parameter file names = ',run_names

    for run in run_names:
        run = os.path.join(plot_dir, run)
        # loop over all the input parameter files
        #(i.e. loop over different simulations)
        
        if verbose:
            print '============================\n============================'
            print 'Doing ', run
            
        # run the EQRM with the next input parameter file
        analysis.main(run)
        
        if verbose:
            print 'FINISH'
    os.chdir(current_dir)

    
def run_scenarios(dir, file_start='plot_', extension='.py'):
    """
    Run all of the python files starting with [file_start] in a directory,.
    """
    
    # Make the current dir the dir this file is in.
    #known_dir, tail = os.path.split(__file__)
    #if known_dir == '':
      #  known_dir = '.'
    known_dir = os.path.abspath(dir)
    current_dir = os.getcwd()
    os.chdir(known_dir)
    plot_files = os.listdir(known_dir)
    plot_files = [x for x in plot_files if x.endswith(extension)]
    plot_files = [x for x in plot_files if 0 == string.find(x,file_start)]
    for plot_file in plot_files:
        eqrm_flags = parse_in_parameters.create_parameter_data(plot_file)
        plot_output_dir = os.path.join(eqrm_flags['output_dir'])
        files = os.listdir(plot_output_dir)
        demo_files = [x for x in files if x[-3:] == 'txt']
        #print "len(demo_files)", len(demo_files)
        if len(demo_files) <= 4: # 4 is the magic number
            # Assume the plot data has not been created.
            # Run the plot scenario
            analysis.main(os.path.join(plot_file))
    os.chdir(current_dir)

if __name__ == '__main__':
    demo_run()
