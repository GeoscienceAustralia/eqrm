# This is the main program of the EQRM
# See README-getting-started.txt for information on how to use it

# this will run if eqrm_analysis.py is called from DOS prompt or double clicked
if __name__ == '__main__':
    from sys import argv
    from eqrm_code.analysis import main
    from os import path

    # Let's work-out the eqrm dir
    eqrm_dir, tail = path.split(__file__)
    if eqrm_dir == '':
        eqrm_dir = '.'

    if len(argv) > 2:
        f = argv[1]  # note argv[0] will be 'main.py'
        use_determ_seed = argv[2]
        if use_determ_seed is 'y':
            print 'RESETTING RANDOM SEED'
            use_determ_seed = True
        elif use_determ_seed is 'n':
            print 'NOT RESETTING RANDOM SEED'
            use_determ_seed = False
        else:
            raise ValueError('Input seed parameter must be y or n')
        compress_output = False
        if len(argv) > 3:
            compress_output = argv[3]
            if compress_output is 'y':
                print 'Compressing output'
                compress_output = True
            elif compress_output is 'n':
                print 'Not compressing output'
                compress_output = False
        main(f, use_determ_seed, compress_output=compress_output)
    else:
        assert len(argv) == 1
        import profile
        profile.run("main('setdata.txt',True)", 'fooprof')
        import pstats
        p = pstats.Stats('fooprof')
        p.sort_stats('cumulative').print_stats(10)
        p.sort_stats('cumulative').strip_dirs().print_callees(
            'distribution_function')
