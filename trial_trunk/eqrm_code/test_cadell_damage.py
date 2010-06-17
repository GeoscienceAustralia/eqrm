


import os
import sys
import csv
import unittest
from os.path import join

from scipy import array, newaxis, where, allclose

from eqrm_code.damage_model import Damage_model
from eqrm_code.capacity_spectrum_model import Capacity_spectrum_model
from eqrm_code.structures import Structures
from eqrm_code.util import determine_eqrm_path

CADELL_TEST_DIR = '../test_cadell/Cadell/'
class Test_cadell(unittest.TestCase):    
    def test_cadel_ground_motion(self):   
        
        eqrm_dir = determine_eqrm_path()
        cadel_dir = join(eqrm_dir, 'test_cadell', 'Cadell')
        natcadell_loc = join(cadel_dir, 'natcadell.csv')
        default_input_dir = join(eqrm_dir,'resources',
                                 'data', '')
        sites=Structures.from_csv(natcadell_loc,
                                  'building_parameters_workshop_3',
                                  default_input_dir,
                                  eqrm_dir=eqrm_dir,
                                  buildings_usage_classification='FCB')

        magnitudes=array([7.2])                     

        cadell_periods_loc = join(cadel_dir, 'Cadell_periods.csv')
        periods=csv.reader(open(cadell_periods_loc)).next()
        periods=array([float(v) for v in periods])
        num_periods=len(periods)
        num_sites=len(sites.latitude)

        assert allclose(periods,[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,
                                 0.9,1,1.5,2,2.5,3,3.5,4,4.5,5])
        
        cadell_gm_loc = join(cadel_dir, 'Cadell_ground_motions_precision.csv')
        SA=self.ground_motions_from_csv(cadell_gm_loc,
            num_periods,num_sites)

        # set up damage model
        csm_use_variability = None
        csm_standard_deviation = None
        damage_model=Damage_model(sites,SA,periods,magnitudes,
                 csm_use_variability, csm_standard_deviation)
        damage_model.csm_use_variability=False
        damage_model.csm_standard_deviation=0.3
        
        point=damage_model.get_building_displacement()
        # point is SA,SD 
        
        # SA should by of shape
        # (number of buildings,number of events,number of samples).
        # print point[0].shape

        # check that SA is the right shape
        assert point[0].shape==(num_sites,1)
        
        # check that SD is the same shape as SA
        assert point[1].shape== point[0].shape 

        point = (point[0][...,0],point[1][...,0])
        #collapse out sample dimension so it matches the shape of matlab
     
        cadell_bd_loc = join(cadel_dir, 'Cadell_building_displacements.csv')
        matlab_point=open(cadell_bd_loc)
        matlab_point=array([[float(p) for p in mpoint.split(',')]
                            for mpoint in matlab_point])        
        matlab_point=(matlab_point[:,1],matlab_point[:,0])
        assert allclose(point,matlab_point,5e-3)
        assert allclose(point,matlab_point,1e-2)
        # check that we are 1% of matlabs SA and SD
        assert allclose(point,matlab_point,5e-3)
        # check that we are 0.5% of matlabs SA and SD

        # If fails if we go any futher, especially on SD.
        # I guess the convergance is different, or something.

        # But note that it is all still within 1%.
        # SD is the worst, and only 100 points out of >4000 are
        # not within 0.1%. So it is basically in accord with matlabs results.
        
        
    def ground_motions_from_csv(self,filename,num_periods,num_sites):
        matlab_ground_motions=[]
        for line in csv.reader(open(filename)):
            a=array([float(v) for v in line])
            assert len(a)==num_periods*num_sites
            a=a.reshape(num_periods,num_sites)
            matlab_ground_motions.append(a)
        matlab_ground_motions=array(matlab_ground_motions)
        matlab_ground_motions=matlab_ground_motions.transpose()
        matlab_ground_motions=[a.transpose() for a in matlab_ground_motions]
        matlab_ground_motions=array(matlab_ground_motions)
        #matlab_ground_motions=matlab_ground_motions[...,newaxis]
        # add a dim for sample
        return matlab_ground_motions

#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_cadell,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
