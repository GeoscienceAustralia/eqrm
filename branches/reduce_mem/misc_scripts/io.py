#!/usr/bin/env python

import os
import time

def main():

  jiffy = os.sysconf(os.sysconf_names['SC_CLK_TCK'])
  num_cpu = 8

  stat_fd = open('/proc/stat')
  stat_buf = stat_fd.readlines()[0].split()
  user, nice, syst, idle, wait, irq, sirq = \
      ( float(stat_buf[1]), float(stat_buf[2]), 
        float(stat_buf[3]), float(stat_buf[4]),
        float(stat_buf[5]), float(stat_buf[6]),
        float(stat_buf[7]) )

  stat_fd.close()                                               
  
  while True:
    time.sleep(3)                                            

    stat_fd = open('/proc/stat')
    stat_buf = stat_fd.readlines()[0].split()
    user_n, nice_n, syst_n, idle_n, wait_n, irq_n, sirq_n = \
        ( float(stat_buf[1]), float(stat_buf[2]), 
          float(stat_buf[3]), float(stat_buf[4]),
          float(stat_buf[5]), float(stat_buf[6]),
          float(stat_buf[7]) )

    stat_fd.close()
        
    user_d = user_n - user
    nice_d = nice_n - nice
    syst_d = syst_n - syst
    idle_d = idle_n - idle
    wait_d = wait_n - wait
    irq_d = irq_n - irq
    sirq_d = sirq_n - sirq
    
    cact = user_d + syst_d + nice_d 
    ctot = user_d + nice_d + syst_d + idle_d + wait_d + irq_d + sirq_d 
    
    tcpu = cact/ctot*100;                         # total  % cpu utilization
    ucpu = user_d/ctot*100;                         # user   % cpu utilization
    scpu = syst_d/ctot*100;                         # system % cpu utilization
    ncpu = nice_d/ctot*100;                         # nice   % cpu utilization
    wcpu = wait_d/ctot*100;                         # wait   % cpu utilization
    
    print "total:%3.1f%% user:%3.1f%% system:%3.1f%% nice:%3.1f%% wait:%3.1f%%\n" %(tcpu,ucpu,scpu,ncpu,wcpu)
    
    user = user_n
    nice = nice_n
    syst = syst_n
    idle = idle_n
    wait = wait_n
    irq = irq_n
    sirq = sirq_n
    

if __name__ == '__main__':
  main()
