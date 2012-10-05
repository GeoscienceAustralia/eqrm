import os

from eqrm_code import parse_in_parameters
from eqrm_code import analysis

def create_demo_data():
    """
    Create the demo data if it is not already there.
    """
    
    # Make the current dir the dir this file is in.
    known_dir, tail = os.path.split(__file__)
    if known_dir == '':
        known_dir = '.'
    known_dir = os.path.abspath(known_dir)
    os.chdir(known_dir)
    files = os.listdir(known_dir)
    plot_files = [x for x in files if x[-2:] == 'py']
    #plot_files = [x for x in plot_files if x[:12] == 'little_plot_']
    plot_files = [x for x in plot_files if x[:5] == 'plot_']
    print "plot_files", plot_files
    for plot_file in plot_files:
        THE_PARAM_T = parse_in_parameters.create_parameter_data(plot_file)
        plot_output_dir = os.path.join(THE_PARAM_T['output_dir'])
        files = os.listdir(plot_output_dir)
        demo_files = [x for x in files if x[-3:] == 'txt']
        print "len(demo_files)", len(demo_files)
        if len(demo_files) <= 4: # 4 is the magic number
            # Assume the plot data has not been created.
            # Run the plot scenario
            analysis.main(os.path.join(plot_file))


#-------------------------------------------------------------
        
if __name__ == "__main__":
    create_demo_data()
    
