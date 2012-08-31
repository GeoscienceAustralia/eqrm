#!/usr/bin/env python

import os
import time

def main():

  jiffy = os.sysconf(os.sysconf_names['SC_CLK_TCK'])
  num_cpu = 8

  stat_fd = open('/proc/stat')
  stat_buf = stat_fd.readlines()[0].split()
  user, nice, sys, idle, iowait, irq, sirq = ( float(stat_buf[1]), float(stat_buf[2]), 
                                               float(stat_buf[3]), float(stat_buf[4]),
                                               float(stat_buf[5]), float(stat_buf[6]),
                                               float(stat_buf[7]) )

  stat_fd.close()                                               

  time.sleep(1)                                            

  stat_fd = open('/proc/stat')
  stat_buf = stat_fd.readlines()[0].split()
  user_n, nice_n, sys_n, idle_n, iowait_n, irq_n, sirq_n = ( float(stat_buf[1]), float(stat_buf[2]), 
                                                             float(stat_buf[3]), float(stat_buf[4]),
                                                             float(stat_buf[5]), float(stat_buf[6]),
                                                             float(stat_buf[7]) )

  stat_fd.close()                                               

  print ((user_n - user) * 100 / jiffy) / num_cpu

if __name__ == '__main__':
  main()
