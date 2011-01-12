
import os

from eqrm_code import eqrm_filesystem
from eqrm_code import analysis

def demo_run(verbose=True):
    if verbose:
        print 'STARTING'  

    # list of input parameter files to use in the batch run
    run_names = ['plot_ProbRisk.py', 'plot_ProbHaz.py', 'plot_ScenGM.py']
    #run_names = ['plot_ScenGM.py']
    plot_dir = os.path.join(eqrm_filesystem.demo_plot_path)
    current_dir = os.getcwd()
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

if __name__ == '__main__':
    demo_run()
