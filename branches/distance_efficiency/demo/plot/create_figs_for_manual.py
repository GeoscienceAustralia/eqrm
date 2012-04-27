import os
import shutil
import execute_all_demos
from eqrm_code import eqrm_filesystem

FIG_EXTEN = '.pdf'
MANUAL_FIGS = ['demo_hazard_exceedance','demo_loss_exceedance',
               'demo_annloss_deagg_distmag', 
               'demo_scenario_building_loss_percent',
               'demo_hazard']
               
def move_figs_to_manual_dir(fig_list):
    for fig in fig_list:
        file_name = fig + FIG_EXTEN
        file_path = os.path.join(eqrm_filesystem.manual_diagrams, 
                                 file_name)  
        print "moving to ", file_path     
        shutil.copyfile(file_name, file_path)
        try:
            shutil.copyfile(file_name, file_path)
        except:
            print "Could not copy ", file_name
    
        
        
#-------------------------------------------------------------
        
if __name__ == "__main__":
    # This will check that many plot demo simulations have been run,
    # Not just the ones needed for MANUAL_FIGS.
    execute_all_demos.create_demo_data()
    execute_all_demos.execute_demos([x+'.py' for x in MANUAL_FIGS])
    move_figs_to_manual_dir(MANUAL_FIGS)
    
