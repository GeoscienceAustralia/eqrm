name='Atkinson_Boore'
model_flags=[2;1]
region=1
spawning=0 % don't spawn
% first row = names
% 2nd row = weights

% first row: 0=gaull,1=toro,2=Atkinson_Boore, 3 = Sadigh, 4 = somerville

% For some reason (probably setdata.mat, I am using a name 'gaull' for some
% internal stuff. It doesn't affect the outputs (which may be ie toro, 
% and will be named appropriatly).

cd R:\earthquake\sandpits\tdhu\eqrm\eqrm_app\m_code\startup
eqrm_startup('R:\earthquake\sandpits\tdhu\eqrm\eqrm_app')
cd G:\earthquake\eqrm_refactor\test_data


copyfile('newc_par_ampfactors.mat','R:\earthquake\sandpits\tdhu\eqrm\eqrm_app\resources\data\gaull_par_ampfactors.mat')

cd(strcat('hazard_test_perth_',name,'\'))

add_field2setdata('replace','setdata.mat','setdata.mat','inputdir',pwd)
add_field2setdata('replace','setdata.mat','setdata.mat','savedir',pwd)
load setdata
add_field2setdata('replace','setdata.mat','setdata.mat','attn_region',region)



add_field2setdata('replace','setdata','setdata','savedir',pwd)
add_field2setdata('replace','setdata','setdata','inputdir',pwd)


add_field2setdata('replace','setdata','setdata','var_attn_flag',0)
add_field2setdata('replace','setdata','setdata','var_amp_flag',0)
add_field2setdata('replace','setdata','setdata','amp_switch',1)

add_field2setdata('replace','setdata','setdata','Rthrsh',5000)
add_field2setdata('replace','setdata','setdata','pgacutoff',5)


if spawning==1
    add_field2setdata('replace','setdata','setdata','src_eps_switch',1)
    add_field2setdata('replace','setdata','setdata','var_attn_flag',1)
    add_field2setdata('replace','setdata','setdata','var_attn_method',1)
    add_field2setdata('replace','setdata','setdata','determ_flag',1)
    add_field2setdata('replace','setdata','setdata','determ_ntrg',1)
    add_field2setdata('replace','setdata','setdata','nsamples',5)
    add_field2setdata('replace','setdata','setdata','nsigma',2.5)
end



load setdata
% eqrm_param_gui
add_field2setdata('replace','setdata.mat','setdata.mat','attenuation_flag',model_flags)
load setdata
eqrm_analysis -r -f setdata.mat % r=reset random seed, f=filename

load(strcat('gaull','_db_mot'))
load(strcat('gaull','_db_hzd'))

% Note that gaull needs it own special flag (as it has a different shape)
if model_flags[1,1]==0
    evntdb_to_xml(strcat('gaull','_db_evntdb.mat'),'hazard_test_event.xml',0)
end
if model_flags[1,1]>=1
    evntdb_to_xml(strcat('gaull','_db_evntdb.mat'),'hazard_test_event.xml',1)
end
    
load(strcat('gaull','_par_site_uniform')) %slow

sites_to_csv(SiteLocations,site_classes,'hazard_test_sites.csv')
csvwrite(strcat('hazard_test_',name,'_rock_motions.csv'),rock_motions)
csvwrite(strcat('hazard_test_',name,'_soil_motions.csv'),soil_motions)
csvwrite('hazard_test_periods.csv',periods)
csvwrite('hazard_test_jb_dist.csv',dist_jb)
csvwrite('hazard_test_rup_dist.csv',dist_rup)

csvwrite(strcat('hazard_test_',name,'_bedrock_hazard.csv'),hzd_rock)
csvwrite(strcat('hazard_test_',name,'_regolith_hazard.csv'),hzd_regolith)

csvwrite('hazard_test_return_periods.csv',rtrn_per)

delete('R:\earthquake\sandpits\tdhu\eqrm\eqrm_app\resources\data\gaull_par_ampfactors.mat')
% Don't leave it in the main sandpit.
