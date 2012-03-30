function Convert_Mat2Py_PARAM_T(filein, fileout)
% Converts a Matlab eqrm_param_T structure (in filein) into 
% THE_PARAM_T.txt (fileout) file that is required by the 
% Python version of the EQRM. 
%
% Notes: 
% This function will most likely be used in preprocessing. However,
% it is stored in the postprocessing directory so that it is stored
% with its counterpart Convert_Py2Mat_PARAM_T.m
%
% INPUTS: 
% filein        [string] full path to Matlab *.mat file 
%               containing the structure eqrm_param_T
% fileout       [string] full path and filename of 
%               output file. Note that file has the correct format to be
%               used with the Python version of the EQRM.
%
% OUTPUTS: 
% There are no outputs returned to the matalab workspace. Output is 
% a saved file (filout)
%
% David Robinson
% 3 April 2007. 

load(filein) % loads THE_PARAM_T structure

fid = fopen(fileout, 'w'); % open the file
fprintf(fid,'%s\n','[Operation_Mode]');
fprintf(fid, '%s\n',['run_type=[',num2str(eqrm_param_T.run_type),']']);
fprintf(fid, '%s\n',['    ']);
fprintf(fid, '%s\n',['[General]']);
fprintf(fid, '%s\n',['destring=',eqrm_param_T.destring]);
fprintf(fid, '%s\n',['small_site_flag=[', num2str(eqrm_param_T.small_site_flag),']']);
fprintf(fid, '%s\n',['site_loc=',eqrm_param_T.site_loc]);
fprintf(fid, '%s\n',['SiteInd=', str_from_vector(eqrm_param_T.SiteInd,'row')]);
fprintf(fid, '%s\n',['inputdir=', eqrm_param_T.inputdir]);
fprintf(fid, '%s\n',['savedir=', eqrm_param_T.savedir]);
fprintf(fid, '%s\n',['rtrn_per=', str_from_vector(eqrm_param_T.rtrn_per,'col')]);
fprintf(fid, '%s\n',['grid_flag=[',num2str(eqrm_param_T.grid_flag),']']);
fprintf(fid, '%s\n',['    ']);
fprintf(fid, '%s\n',['[Source]']);
fprintf(fid, '%s\n',['azi=[',num2str(eqrm_param_T.azi),']']);
fprintf(fid, '%s\n',['min_mag_cutoff=[',num2str(eqrm_param_T.min_mag_cutoff),']']);
fprintf(fid, '%s\n',['nbins=[',num2str(eqrm_param_T.nbins),']']);
fprintf(fid, '%s\n',['wdth=[',num2str(eqrm_param_T.wdth),']']);
fprintf(fid, '%s\n',['ftype=[',num2str(eqrm_param_T.ftype),']']);
fprintf(fid, '%s\n',['ntrgvector=',str_from_vector(eqrm_param_T.ntrgvector,'row')]);
fprintf(fid, '%s\n',['d_azi=[',num2str(eqrm_param_T.d_azi),']']);
fprintf(fid, '%s\n',['dip=[',num2str(eqrm_param_T.dip),']']);

fprintf(fid, '%s\n',['[Event_Spawn]    ']);
fprintf(fid, '%s\n',['src_eps_switch=[',num2str(eqrm_param_T.src_eps_switch),']']);
fprintf(fid, '%s\n',['mbnd=[',num2str(eqrm_param_T.mbnd),']']);
fprintf(fid, '%s\n',['nsigma=[',num2str(eqrm_param_T.nsigma),']']);
fprintf(fid, '%s\n',['nsamples=[',num2str(eqrm_param_T.nsamples),']']);
fprintf(fid, '%s\n',['    ']);
fprintf(fid, '%s\n',['[Scenario]    ']);
fprintf(fid, '%s\n',['determ_azi=[',num2str(eqrm_param_T.determ_azi),']']);
fprintf(fid, '%s\n',['determ_r_z=[',num2str(eqrm_param_T.determ_r_z),']']);
fprintf(fid, '%s\n',['determ_lat=[',num2str(eqrm_param_T.determ_lat),']']);
fprintf(fid, '%s\n',['determ_mag=[',num2str(eqrm_param_T.determ_mag),']']);
fprintf(fid, '%s\n',['determ_ntrg=[',num2str(eqrm_param_T.determ_ntrg),']']);
fprintf(fid, '%s\n',['determ_lon=[',num2str(eqrm_param_T.determ_lon),']']);
fprintf(fid, '%s\n',['determ_flag=[',num2str(eqrm_param_T.determ_flag),']']);
fprintf(fid, '%s\n',['    ']);
fprintf(fid, '%s\n',['[Attenuation]    ']);
try; fprintf(fid, '%s\n',['smoothed_response_flag=[',num2str(eqrm_param_T.smoothed_response_flag),']']);
catch; fprintf(fid, '%s\n',['smoothed_response_flag=[',num2str(-9999),']']); end % probably a Matlab hazard inmput file
fprintf(fid, '%s\n',['pgacutoff=[',num2str(eqrm_param_T.pgacutoff),']']);
fprintf(fid, '%s\n',['attenuation_flag=', str_from_matrix(eqrm_param_T.attenuation_flag)]);
fprintf(fid, '%s\n',['attn_region=', str_from_vector(eqrm_param_T.attn_region,'row')]);
fprintf(fid, '%s\n',['var_attn_flag=[',num2str(eqrm_param_T.var_attn_flag),']']);
fprintf(fid, '%s\n',['var_attn_method=[',num2str(eqrm_param_T.var_attn_method),']']);
fprintf(fid, '%s\n',['periods=', str_from_vector(eqrm_param_T.periods,'row')]);
try; fprintf(fid, '%s\n',['resp_crv_flag=[',num2str(eqrm_param_T.resp_crv_flag),']']);
catch; fprintf(fid, '%s\n',['resp_crv_flag=[',num2str(-9999),']']); end  % probably a Matlab hazard inmput file 
fprintf(fid, '%s\n',['Rthrsh=[',num2str(eqrm_param_T.Rthrsh),']']);
fprintf(fid, '%s\n',['    ']);
fprintf(fid, '%s\n',['[Amplification]    ']);
fprintf(fid, '%s\n',['MinAmpFactor=[',num2str(eqrm_param_T.MinAmpFactor),']']);
fprintf(fid, '%s\n',['var_amp_method=[',num2str(eqrm_param_T.var_amp_method),']']);
fprintf(fid, '%s\n',['amp_switch=[',num2str(eqrm_param_T.amp_switch),']']);
fprintf(fid, '%s\n',['var_amp_flag=[',num2str(eqrm_param_T.var_amp_flag),']']);
fprintf(fid, '%s\n',['MaxAmpFactor=[',num2str(eqrm_param_T.MaxAmpFactor),']']);
fprintf(fid, '%s\n',['    ']);
fprintf(fid, '%s\n',['[Bclasses]    ']);
try; fprintf(fid, '%s\n',['hazus_dampingis5_flag=[',num2str(eqrm_param_T.hazus_dampingis5_flag),']']);
catch; fprintf(fid, '%s\n',['hazus_dampingis5_flag=[',num2str(-9999),']']); end % probably a Matlab hazard inmput file 
try; fprintf(fid, '%s\n',['buildpars_flag=[',num2str(eqrm_param_T.buildpars_flag),']']);
catch; fprintf(fid, '%s\n',['buildpars_flag=[',num2str(-9999),']']); end% probably a Matlab hazard inmput file 
try; fprintf(fid, '%s\n',['hazus_btypes_flag=[',num2str(eqrm_param_T.hazus_btypes_flag),']']);
catch; fprintf(fid, '%s\n',['hazus_btypes_flag=[',num2str(-9999),']']); end % probably a Matlab hazard inmput file 
try; fprintf(fid, '%s\n',['b_usage_type_flag=[',num2str(eqrm_param_T.b_usage_type_flag),']']);
catch; fprintf(fid, '%s\n',['b_usage_type_flag=[',num2str(-9999),']']); end % probably a Matlab hazard inmput file 
fprintf(fid, '%s\n',['    ']);
fprintf(fid, '%s\n',['[Bclasses2]    ']);
try; fprintf(fid, '%s\n',['determ_buse=[',num2str(eqrm_param_T.determ_buse),']']);
catch; fprintf(fid, '%s\n',['determ_buse=[',num2str(-9999),']']); end % probably a Matlab hazard inmput file 
fprintf(fid, '%s\n',['force_btype_flag=[',num2str(eqrm_param_T.force_btype_flag),']']);
try; fprintf(fid, '%s\n',['determ_btype=[',num2str(eqrm_param_T.determ_btype),']']);
catch; fprintf(fid, '%s\n',['determ_btype=[',num2str(-9999),']']); end % probably a Matlab hazard inmput file
%fprintf(fid, '%s\n',['ignore_post89_flag=[',num2str(eqrm_param_T.ignore_post89_flag),']']);
fprintf(fid, '%s\n',['    ']);
fprintf(fid, '%s\n',['[CSM]']);
try; fprintf(fid, '%s\n',['var_bcap_flag=[',num2str(eqrm_param_T.var_bcap_flag),']']);
catch; fprintf(fid, '%s\n',['var_bcap_flag=[',num2str(-9999),']']); end % probably a Matlab hazard inmput file
try; fprintf(fid, '%s\n',['stdcap=[',num2str(eqrm_param_T.stdcap),']']);
catch; fprintf(fid, '%s\n',['stdcap=[',num2str(-9999),']']); end % probably a Matlab hazard inmput file
try; fprintf(fid, '%s\n',['bcap_var_method=[',num2str(eqrm_param_T.bcap_var_method),']']);
catch; fprintf(fid, '%s\n',['bcap_var_method=[',num2str(-9999),']']); end % probably a Matlab hazard inmput file
try; fprintf(fid, '%s\n',['damp_flags=', str_from_vector(eqrm_param_T.damp_flags,'row')]);
catch; fprintf(fid, '%s\n',['damp_flags=', str_from_vector([-9999 -9999 -9999],'row')]); end % probably a Matlab hazard inmput file
try; fprintf(fid, '%s\n',['Harea_flag=[',num2str(eqrm_param_T.Harea_flag),']']);
catch; fprintf(fid, '%s\n',['Harea_flag=[',num2str(-9999),']']); end % probably a Matlab hazard input file
try; fprintf(fid, '%s\n',['max_iterations=[',num2str(eqrm_param_T.max_iterations),']']);
catch; fprintf(fid, '%s\n',['max_iterations=[',num2str(-9999),']']); end % probably a Matlab hazard input file
try; fprintf(fid, '%s\n',['SDRelTol=[',num2str(eqrm_param_T.SDRelTol),']']);
catch; fprintf(fid, '%s\n',['SDRelTol=[',num2str(-9999),']']); end % probably a Matlab hazard input file
fprintf(fid, '%s\n',['    ']);
fprintf(fid, '%s\n',['[Diagnostics]']);
fprintf(fid, '%s\n',['qa_switch_map=[',num2str(eqrm_param_T.qa_switch_map),']']);
fprintf(fid, '%s\n',['qa_switch_attn=[',num2str(eqrm_param_T.qa_switch_attn),']']);
fprintf(fid, '%s\n',['qa_switch_ampfactors=[',num2str(eqrm_param_T.qa_switch_ampfacors),']']);
try; fprintf(fid, '%s\n',['qa_switch_vun=[',num2str(eqrm_param_T.qa_switch_vun),']']);
catch; fprintf(fid, '%s\n',['qa_switch_vun=[',num2str(-9999),']']); end  % probably a Matlab hazard input file
try; fprintf(fid, '%s\n',['qa_switch_soc=[',num2str(eqrm_param_T.qa_switch_soc),']']);
catch; fprintf(fid, '%s\n',['qa_switch_soc=[',num2str(-9999),']']); end  % probably a Matlab hazard input file
fprintf(fid, '%s\n',['qa_switch_mke_evnts=[',num2str(eqrm_param_T.qa_switch_mke_evnts),']']);
fprintf(fid, '%s\n',['qa_switch_watercheck=[',num2str(eqrm_param_T.qa_switch_watercheck),']']);
fprintf(fid, '%s\n',['qa_switch_fuse=[',num2str(eqrm_param_T.qa_switch_fuse),']']);
fprintf(fid, '%s\n',['    ']);
fprintf(fid, '%s\n',['[Loss]']);
try; fprintf(fid, '%s\n',['ci=[',num2str(eqrm_param_T.ci),']']);
catch; fprintf(fid, '%s\n',['ci=[',num2str(-9999),']']); end % probably a Matlab hazard input file
try; fprintf(fid, '%s\n',['pga_mindamage=[',num2str(eqrm_param_T.pga_mindamage),']']);
catch; fprintf(fid, '%s\n',['pga_mindamage=[',num2str(-9999),']']); end % probably a Matlab hazard input file
try; fprintf(fid, '%s\n',['aus_contents_flag=[',num2str(eqrm_param_T.aus_contents_flag),']']);
catch; fprintf(fid, '%s\n',['aus_contents_flag=[',num2str(-9999),']']); end % probably a Matlab hazard input file
fprintf(fid, '%s\n',['    ']);
fprintf(fid, '%s\n',['[Save]']);
try; fprintf(fid, '%s\n',['save_deagecloss_flag=[',num2str(eqrm_param_T.save_deagecloss_flag),']']);
catch; fprintf(fid, '%s\n',['save_deagecloss_flag=[',num2str(-9999),']']); end % probably a Matlab hazard input file
try; fprintf(fid, '%s\n',['save_probdam_flag=[',num2str(eqrm_param_T.save_probdam_flag),']']);
catch; fprintf(fid, '%s\n',['save_probdam_flag=[',num2str(-9999),']']); end % probably a Matlab hazard input file
fprintf(fid, '%s\n',['hazard_map_flag=[',num2str(eqrm_param_T.hazard_map_flag),']']);
try, % do it if it exists - this one may not exist in many of the matalb files
    fprintf(fid, '%s\n',['save_motion_flag=[',num2str(eqrm_param_T.save_motion_flag),']']);
catch, % otherwise creat it
    fprintf(fid, '%s\n',['save_motion_flag=[',num2str(0),']']);
end
try; fprintf(fid, '%s\n',['save_ecloss_flag=[',num2str(eqrm_param_T.save_ecloss_flag),']']);
catch; fprintf(fid, '%s\n',['save_ecloss_flag=[',num2str(-9999),']']); end % probably a Matlab hazard input file
try; fprintf(fid, '%s\n',['save_socloss_flag=[',num2str(eqrm_param_T.save_socloss_flag),']']);
catch; fprintf(fid, '%s\n',['save_socloss_flag=[',num2str(-9999),']']); end % probably a Matlab hazard input file


fclose(fid);  % close the file


function strout = str_from_matrix(A) 

[n m] = size(A);
strout = '[';
for i = 1:n % loop over the rows
    tmp = str_from_vector(A(i,:),'row');
    if i~=n
        strout = [strout, tmp(2:end-1), ';'];
    elseif i ==n
        strout = [strout, tmp(2:end-1)];
    end
end  
strout = [strout, ']'];

function strout = str_from_vector(A,vectype)
%converts a vector into a string for the Python output. 
% Inputs: 
% A             vector to be converted
% vectype       vector type
%                   col => column vector
%                   row => row vector
n = length(A);
strout = '[';
for i = 1:n
    if i~=n & strcmp(vectype,'row')
        strout = [strout, num2str(A(i)), ','];
    elseif i~=n & strcmp(vectype,'col')
        strout = [strout, num2str(A(i)), ';'];
    elseif i ==n
        strout = [strout, num2str(A(i))];
    end
end
strout = [strout, ']'];