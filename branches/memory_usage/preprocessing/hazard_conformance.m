name='torro'
model_flags=[1;1]
region=1
% first row = names
% 2nd row = weights

% first row: 0=gaull,1=torro,2=ab, 3 = sadigh, 4 = somerville

cd R:\earthquake\sandpits\tdhu\eqrm\eqrm_app\m_code\startup
eqrm_startup('R:\earthquake\sandpits\tdhu\eqrm\eqrm_app')
cd G:\earthquake\eqrm_refactor\test_data

cd(strcat('hazard_test_perth_',name,'\'))

add_field2setdata('replace','setdata.mat','setdata.mat','inputdir',pwd)
add_field2setdata('replace','setdata.mat','setdata.mat','savedir',pwd)
load setdata
add_field2setdata('replace','setdata.mat','setdata.mat','attn_region',region)
load setdata
% eqrm_param_gui
add_field2setdata('replace','setdata.mat','setdata.mat','attenuation_flag',model_flags)
load setdata
eqrm_analysis -r -f setdata.mat % r=reset random seed, f=filename

load(strcat('gaull','_db_mot'))
load(strcat('gaull','_db_hzd'))

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