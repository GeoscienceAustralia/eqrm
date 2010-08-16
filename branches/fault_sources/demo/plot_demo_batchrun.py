
def demo_run():
    print 'STARTING'     
    try:
        # import main (i.e. this is basically eqrm_analysis.py)
        from eqrm_code import analysis
    except:
        raise ImportError(
            'Please edit the PYTHONPATH ' + \
            'environmental variable to point to the python_eqrm directory.')


    # list of input parameter files to use in the batch run
    run_names = ['plot_ProbRisk.py', 'plot_ProbHaz.py']

    print 'Parameter file names = ',run_names

    for run in run_names:
        # loop over all the input parameter files
        #(i.e. loop over different simulations)
        print '============================\n============================'
        print 'Doing ', run
        # run the EQRM with the next input parameter file
        analysis.main(run)
        print 'FINISH'

if __name__ == '__main__':
    demo_run()
