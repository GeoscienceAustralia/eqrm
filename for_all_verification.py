"""
This automatically does all the tests, checks and demos EQRM has.

"""
from os import chdir
from os.path import join

from eqrm_code.util import determine_eqrm_path, run_call
from eqrm_code.eqrm_audit_wrapper import eqrm_audit_wrapper


def do_tests_checks_demos_audits(eqrm_root_dir,
                                 ip_audit=False,
                                 test_all=True,
                                 check_scenarios=True,
                                 mini_check_scenarios=True,
                                 demo_batchrun=True,
                                 verbose=False,
                                 python_command='python'):
    """
    Automatically do all of the quick tests, checks demos and audits EQRM has.

    precondition: The current directory is eqrm_root_dir.
    args:
      eqrm_root_dir - The directory eqrm_code is in.
      python_command: String used to control the python version.
        e.g.'python2.4'

    return:
      False if any of these actions fail, otherwise True.
    """
    # chdir(eqrm_root_dir)
    # FIXME If any more tests are added loop this!

    def stop_message():
        print 'Stopping the distribution process.'
        print 'No zip file produced.'

    if ip_audit is True:
        if verbose:
            print "Start IP Audit"
        eqrm_audit_wrapper_results = eqrm_audit_wrapper(eqrm_root_dir)
        if eqrm_audit_wrapper_results is False:
            print 'ERROR: Unlicensed files in the distribution package.'
            stop_message()
            return False

    if test_all is True:
        if verbose:
            print "Start test_all.py"
        Retcode = run_call(join('eqrm_code', 'test_all.py'), eqrm_root_dir,
                           python_command=python_command)
        if not Retcode == 0:
            print 'ERROR: test_all.py failed.'
            stop_message()
            return False
        if verbose:
            print "Finish test_all.py"

    if check_scenarios is True:
        if verbose:
            print "Start check_scenarios.py"
        chdir(join(eqrm_root_dir, 'eqrm_code'))
        Retcode = run_call(join('eqrm_code', 'check_scenarios.py'),
                           eqrm_root_dir,
                           python_command=python_command)
        if not Retcode == 0:
            print 'ERROR: check_scenarios.py failed.'
            stop_message()
            return False

    if mini_check_scenarios is True:
        # mini_check_scenarios is not packaged up with the distribution
        if verbose:
            print "Start mini_check_scenarios.py"
        chdir(eqrm_root_dir)
        Retcode = run_call('mini_check_scenarios.py', eqrm_root_dir,
                           python_command=python_command)
        if not Retcode == 0:
            print 'ERROR: mini_check_scenarios.py failed.'
            stop_message()
            return False

    if demo_batchrun is True:
        if verbose:
            print "Start demo_batchrun.py"
        chdir(join(eqrm_root_dir, 'demo'))
        run_call(join('demo', 'demo_batchrun.py'), eqrm_root_dir,
                 python_command=python_command)
        # No return code, since no comparisions are made

    return True

if __name__ == '__main__':
    do_tests_checks_demos_audits(determine_eqrm_path(),
                                 check_scenarios=False,
                                 ip_audit=True,
                                 test_all=False,
                                 mini_check_scenarios=False,
                                 demo_batchrun=False,
                                 python_command='python')
