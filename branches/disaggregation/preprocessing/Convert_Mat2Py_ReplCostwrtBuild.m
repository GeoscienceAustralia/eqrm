function Convert_Mat2Py_ReplCostwrtBuild(datadirin, datadirout)
% This function converts the MATLAB ReplCostwrtBuild dat files into text
% files for use in Python. 
%
% INPUTS: 
% datadirin     [string] full path to source of data (directory)
% datadirout    [string] full path to directory where output files are to
%               be saved
%
% OUTPUTS: 
% outputs are saved into datadirout
%
% David Robinson
% 16 April 2007

if nargin ==0
    datadirin = 'Z:\1\cit\natural_hazard_impacts\earthquake\sandpits\drobinson\eqrm\eqrm_app\resources\data';
    datadirout = 'Z:\1\cit\natural_hazard_impacts\earthquake\sandpits\drobinson\ExternalRepos\python_eqrm\resources\data';
end

disp('Now doing ReplCostwrtBuildCEdwardsFCBusage')
load([datadirin, '\rc_perReplCostwrtBuildCEdwardsFCBusage.mat'])   
save([datadirout, '\rc_perReplCostwrtBuildCEdwardsFCBusage_rc_nsd_a.txt'],'rc_nsd_a','-ascii')
save([datadirout, '\rc_perReplCostwrtBuildCEdwardsFCBusage_rc_nsd_d.txt'],'rc_nsd_d','-ascii')
save([datadirout, '\rc_perReplCostwrtBuildCEdwardsFCBusage_rc_perReplCostwrtbuildUsage_nsd_a.txt'],'rc_perReplCostwrtbuildUsage_nsd_a','-ascii')
save([datadirout, '\rc_perReplCostwrtBuildCEdwardsFCBusage_rc_perReplCostwrtbuildUsage_nsd_d.txt'],'rc_perReplCostwrtbuildUsage_nsd_d','-ascii')
save([datadirout, '\rc_perReplCostwrtBuildCEdwardsFCBusage_rc_perReplCostwrtbuildUsage_struct.txt'],'rc_perReplCostwrtbuildUsage_struct','-ascii')
save([datadirout, '\rc_perReplCostwrtBuildCEdwardsFCBusage_rc_sd.txt'],'rc_sd','-ascii')

disp('Now doing ReplCostwrtBuildCHazusage')
load([datadirin, '\rc_perReplCostwrtBuildCHazusage.mat'])          
save([datadirout,'\rc_perReplCostwrtBuildCHazusage_rc_nsd_a.txt'],'rc_nsd_a','-ascii') 
save([datadirout,'\rc_perReplCostwrtBuildCHazusage_rc_nsd_d.txt'],'rc_nsd_d','-ascii') 
save([datadirout,'\rc_perReplCostwrtBuildCHazusage_rc_perReplCostwrtbuildUsage_nsd_a.txt'],'rc_perReplCostwrtbuildUsage_nsd_a','-ascii') 
save([datadirout,'\rc_perReplCostwrtBuildCHazusage_rc_perReplCostwrtbuildUsage_nsd_d.txt'],'rc_perReplCostwrtbuildUsage_nsd_d','-ascii') 
save([datadirout,'\rc_perReplCostwrtBuildCHazusage_rc_perReplCostwrtbuildUsage_struct.txt'],'rc_perReplCostwrtbuildUsage_struct','-ascii') 
save([datadirout,'\rc_perReplCostwrtBuildCHazusage_rc_perReplCostwrtbuilding.txt'],'rc_perReplCostwrtbuilding','-ascii') 
save([datadirout,'\rc_perReplCostwrtBuildCHazusage_rc_sd.txt'],'rc_sd','-ascii')       

disp('Now doing ReplCostwrtBuildCEdwardsHazususage')
load([datadirin, '\rc_perReplCostwrtBuildCEdwardsHazususage.mat']) 
save([datadirout,'\rc_perReplCostwrtBuildCEdwardsHazususage_rc_nsd_a.txt'],'rc_nsd_a','-ascii')                             
save([datadirout,'\rc_perReplCostwrtBuildCEdwardsHazususage_rc_nsd_d.txt'],'rc_nsd_d','-ascii')                              
save([datadirout,'\rc_perReplCostwrtBuildCEdwardsHazususage_rc_perReplCostwrtbuildUsage_nsd_a.txt'],'rc_perReplCostwrtbuildUsage_nsd_a','-ascii')  
save([datadirout,'\rc_perReplCostwrtBuildCEdwardsHazususage_rc_perReplCostwrtbuildUsage_nsd_d.txt'],'rc_perReplCostwrtbuildUsage_nsd_d','-ascii')  
save([datadirout,'\rc_perReplCostwrtBuildCEdwardsHazususage_rc_perReplCostwrtbuildUsage_struct.txt'],'rc_perReplCostwrtbuildUsage_struct','-ascii')  
save([datadirout,'\rc_perReplCostwrtBuildCEdwardsHazususage_rc_perReplCostwrtbuilding.txt'],'rc_perReplCostwrtbuilding','-ascii')  
save([datadirout,'\rc_perReplCostwrtBuildCEdwardsHazususage_rc_sd.txt'],'rc_perReplCostwrtbuilding','-ascii')  