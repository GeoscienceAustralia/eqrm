"""

Benchmark EQRM.

Do the benchmark on a hazard and a risk scenario.

Be able to generate profile info as well.

To run in parallel:
mpirun -np XX -hostfile ~/.machines.cyclone python benchmark_eqrm

profile info will not be written over if run in parallel
"""

import time
import os

import sys
import tempfile
import profile
import pstats
import csv
import platform
import string


#import eqrm_code.compile
from eqrm_code.analysis import main
from eqrm_code.get_version import get_version
from eqrm_code.parallel import Parallel

# Code not checked in is lost!
#from clean_profile_output import clean_profile_output



def time_trial_runs(run_profile=False,
                    trials=['./benchmark_input/TS_haz08.py',
                            './benchmark_input/TS_risk56.py'],
                    ofile="timing_results.csv"):
    """
    A controlling function.
    Given a list of trials, run them and write the time and memory info
    to file.

    """
    con = EQRM_controller()
     
    try:
        import eqrm_code.polygon_ext
        is_compiled = True
    except ImportError:
        is_compiled = False
        
    # The csv file out header
    output = [["system", "is_compiled", "trial","eqrm_version", "mem",
               "time_sec"]]
    
    for trial in trials:
        con.scenario_name = trial 
        time_taken_sec, memory_used, version = con.run_trial(
            run_profile= run_profile)
        output.append([con.host,
                       is_compiled,
                       trial,
                       version,
                       memory_used,
                       time_taken_sec])
        
    if not run_profile:
        # Only write overall times to a file when not profiling.
        writer = csv.writer(open(ofile, "ab"))
        writer.writerows(output)
    
    
def mem_usage():
    """
    returns the rss.

  RSS  The total amount of physical memory used by  the  task,  in  kilo-
            bytes,  is  shown  here.  For ELF processes used library pages are
            counted here, for a.out processes not.
            
    Only works on nix systems.
    """
    
    import string
    p=os.popen('ps uwp %s'%os.getpid()) 
    lines=p.readlines()
    #print "lines", lines
    status=p.close() 
    if status or len(lines)!=2 or sys.platform == 'win32': 
        return None 
    return int(string.split(lines[1])[4]) 


class EQRM_controller:
    """
    This class will be in control of running EQRM scenarios for benchmarking.

    It's interface could end up changing alot.  We'll see.
    """
    def __init__(self):

        # This is a hack to get the version based on the eqrm_code dir        
        current_dir = os.getcwd()
        os.chdir('..')
        #os.chdir('eqrm_code')            
        self.version, date, modified = get_version()
        os.chdir(current_dir)
        self.host = platform.uname()[1]
        
        parallel = Parallel()
        self.node_number = str(parallel.rank)

    def run_trial(self, run_profile=False, use_determ_seed=True):
        """

        """

        if run_profile:          
            self.run_trial_profile(run_profile=run_profile,
                              use_determ_seed=use_determ_seed)
            memory_used = None
            time_taken_sec = None
        else:
            #Initial time and memory
            t0 = time.time()
            
            #m0 = None on windows
            m0 = mem_usage()

            # The main call
            main(self.scenario_name,use_determ_seed)
            
            time_taken_sec = (time.time()-t0)
            m1 = mem_usage()
            if m0 is None or m1 is None:
                memory_used = None
            else:
                memory_used = (m1 - m0)
        return time_taken_sec, memory_used, self.version


    def run_trial_profile(self, run_profile=False, use_determ_seed=True):
        version = string.split(string.split(sys.version)[0], ".")
        if map(int, version) < [2, 4, 9]:
            print "Profiling needs python2.5"
            sys.exit() 
            
        try:
            import eqrm_code.polygon_ext
            is_compiled = True
        except ImportError:
            is_compiled = False
                
        this_dir, tail = os.path.split(self.scenario_name)
        name = tail.split('.')
        profile_base = 'pro_' + name[0] + '_v' + str(self.version) + \
                       '_n' + self.node_number
        #profile_file = profile_base + ".txt"
        raw_prof_file = profile_base + ".prof"
        
        s="""main(self.scenario_name,use_determ_seed)"""
        pobject = profile.Profile()
        presult = pobject.runctx(s, vars(sys.modules[__name__]),
                                 vars())
        #raw_prof_file = tempfile.mktemp(".prof")
        presult.dump_stats(profile_base + ".prof")
        
        # Process the results
        file_name = profile_base + "_cum.txt"
        xfile = open(file_name, "w")
        self.pstats_file_header(is_compiled, xfile, profile_base)
        S = pstats.Stats(raw_prof_file, stream=xfile)
        s = S.sort_stats('cumulative').print_stats(50)
        xfile.close()
        #clean_profile_output(file_name)
        
        file_name = profile_base + "_time.txt"
        xfile = open(file_name, "w")
        self.pstats_file_header(is_compiled, xfile, profile_base)
        S = pstats.Stats(raw_prof_file, stream=xfile)
        s = S.strip_dirs().sort_stats('time').print_stats(50)
        xfile.close()
        #clean_profile_output(file_name)

    def pstats_file_header(self, is_compiled, fhandle, profile_base):
        fhandle.write('Descriptor: ' + profile_base + \
                      '     Host:' + self.host + '\n')
        if not is_compiled:
            fhandle.write('Code not compiled.\n')
        
        
  
#-------------------------------------------------------------
if __name__ == "__main__": # run_profile=True,

    time_trial_runs()
    if False:
        time_trial_runs(
            run_profile=True,
            trials=['../../case_studies/test_national/event_gen_opt_A.py'],
            ofile="dump_results.csv")
            
  #  time_trial_runs(trials=['./benchmark_input/ProbNatHaz.py'])
  #   time_trial_runs(trials=['./benchmark_input/TS_haz08.par',
#                             './benchmark_input/TS_risk56.par',
#                             './benchmark_input/TS_risk59.par'])
                    #run_profile=True)
    #trial = ['./benchmark_input/TS_risk56.par']
    #time_trial_runs(trials=trial) #, run_profile=True)
    #,trials=['./benchmark_input/TS_small.par'])
    
        
    
