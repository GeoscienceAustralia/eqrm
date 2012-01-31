import os

from eqrm_code.create_demo_plot_data import demo_run
from eqrm_code import eqrm_filesystem

def create_demo_data():
    """
    Create the demo data if it is not already there.
    Only checks one directory to see if the plot demo files have been executed.
    """
    files = os.listdir(eqrm_filesystem.Demo_Output_PlotScenGM_Path)
    demo_files = [x for x in files if x[-3:] == 'txt']
    if len(demo_files) <= 20:
        # Assume the plot data has not been created.
        demo_run()
    # run the plot demo batch program

def execute_demos():
    files = os.listdir('.')
    extension = 'py'
    demo_files = [x for x in files if x[-2:] == 'py']
    demo_files = [x for x in demo_files if x[:5] == 'demo_']
    #demo_files = ['demo_histogram.py']
    #demo_files.remove()

    for file in demo_files:
        command = 'python ' + file
        print "Doing ", command
        os.system(command)

#-------------------------------------------------------------
        
if __name__ == "__main__":
    print "This is broken.  Try \eqrm_core\demo\plot\execute_all_demos.py"
    #create_demo_data()
    #execute_demos()
    
