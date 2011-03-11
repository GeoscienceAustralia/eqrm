import os
import string

from eqrm_code.create_demo_plot_data import run_scenarios
from eqrm_code import eqrm_filesystem

def create_demo_data():
    """
    Create the demo data if it is not already there.
    Only checks one directory to see if the plot demo files have been executed.
    """
    run_scenarios(eqrm_filesystem.demo_plot_scenarios)

def execute_demos():
    files = os.listdir('.')
    extension = 'py'
    demo_files = [x for x in files if x.endswith('py')]
    demo_files = [x for x in demo_files if 0 == string.find(x,'demo_')]
    #demo_files = ['demo_histogram.py']
    #demo_files.remove()

    for file in demo_files:
        command = 'python ' + file
        print "Doing ", command
        os.system(command)

#-------------------------------------------------------------
        
if __name__ == "__main__":
    create_demo_data()
    execute_demos()
    
