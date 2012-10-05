#!/usr/bin/env python

"""
This script demonstrates how to compare the hazard curves from two different EQRM simulations
"""


import os
import numpy
import matplotlib.pyplot as plt
import filecmp

teststr1 = 'test6'
teststr2 = 'test26'

compare_dir1 = '../'+teststr1+'/outputs/haz_curves'
compare_dir2 = '../'+teststr2+'/outputs/haz_curves'
title = 'Hazard Exceedance: '+teststr1+'(solid) - '+teststr2+'(dashed)'
savefile = 'comparison_'+teststr1+'_'+teststr2+'.png'


# Confirm that the site files are identical
file1 = compare_dir1+'/sites.npy'
file2 = compare_dir2+'/sites.npy'
if not filecmp.cmp(file1,file2):
    raise("site files must be identical")

# lets load the sites
sites1 = numpy.load(file1)
sites2 = numpy.load(file2)
[numsites,numattri] = numpy.shape(sites1)
#print numsites

# let's load the probabilities of exceedance
poe1 = numpy.load(compare_dir1+'/prob_of_exceed.npy')
poe2 = numpy.load(compare_dir2+'/prob_of_exceed.npy')

plot_str1 = ['b','g','y','r','k']
plot_str2 = ['b--','g--','y--','r--','k--']

#setup figure and axes
fig = plt.figure()
ax = fig.add_subplot(111)
legend_titles=[]

xlabel = 'Hazard (g)'
ylabel = 'Probability of Exceedance in One Year'
legend_placement = 'upper right'
hand = []
# Add the lines for the first test first
for i in range(0,numsites):
    # load the hazard data (i.e. for one site at a time)
    haz1 = numpy.load(compare_dir1+'/site'+str(i)+'_hazard_curves.npy')
    # setup the legend
    legend = ('Location: (%.1f,%.1f)    RSA Period: %.1f'
                  %  (float(sites1[i,0]), float(sites1[i,1]), float(sites1[i,2])))
    legend_titles.append(legend)
    #plot one hazard curve at a time
    tmp_pltstr = plot_str1[i]
    hand1 = plt.plot(haz1,poe1,tmp_pltstr)          
     
# Add the lines for the second test (note we do not remake the legend here)
for i in range(0,numsites): 
    tmp_pltstr = plot_str2[i]
    haz2 = numpy.load(compare_dir2+'/site'+str(i)+'_hazard_curves.npy')
    hand2 = plt.plot(haz2,poe2,tmp_pltstr)

ax.set_xlabel(xlabel)
ax.set_ylabel(ylabel)
ax.set_title(title)
ax.set_yscale('log')
ax.grid(True)
leg = ax.legend(legend_titles,'upper right')
#ax.set_xlim = 
plt.savefig(savefile)
plt.show()
