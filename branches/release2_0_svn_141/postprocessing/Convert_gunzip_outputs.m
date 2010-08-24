function Convert_gunzip_outputs(ConvertCommand,datadir, tmpdir, param_fname, varargin)
% This function is a wrapper for the individual Convert routines.
% It makes a directory tmpdir, gunzips all files ending in *.gz 
% which are located in dirin into tmpdir, converts them to a 
% MATLAB binary *.mat file using one of the EQRMs convert routines, 
% saves it in dirin and then deletes the contents of tmpdir.
%
% INPUTS: 
% ConvertCommand    [string] defining the original Convert command 
%                   to use, e.g. Convert_Py2Mat_Hazard or
%                   Convert_Py2Mat_Risk    
% datadir           [string] full path to directory containing *.gz 
%                   files of interest 
% tmpdir            [string] full path to A temporary directory where
%                   most of the work is conducted. 
% param_fname       [string] name of THE_PARAM_T file
% varargin          extra inputs if required by ConvertCommand
%                     1) NOT APPLICABLE if 
%                          ConvertCommand ='Convert_Py2Mat_Hazard'
%                     2) default_data (see Convert_Py2Mat_Risk) if 
%                          ConvertCommand ='Convert_Py2Mat_Risk'
%
% OUTPUTS
% the output is a *.mat file (nature defined by ConvertCommand) saved
% in dirin 
%
% DEMO
% Convert_gunzip_outputs('Convert_Py2Mat_Hazard','c:/temp','c:/temp/temp2' , 'setdata.txt')
% Convert_gunzip_outputs('Convert_Py2Mat_Risk','c:/temp','c:/temp/temp2','setdata.txt','c:\python_eqrm\resources\data')
%
% David Robinson
% 30 May 2007

mkdir(tmpdir)
gunzip_EQRMoutputs(datadir, tmpdir)
copyfile([datadir, '\',param_fname], tmpdir) 

switch ConvertCommand
    case  'Convert_Py2Mat_Hazard'
        [THE_PARAM_T] = Convert_Py2Mat_Hazard(tmpdir,param_fname)
        copyfile([tmpdir, '\',THE_PARAM_T.site_loc, '_db_hzd.mat' ], datadir) 
        

    case 'Convert_Py2Mat_Risk'
        Convert_Py2Mat_Risk(tmpdir,param_fname, varargin{1})
        a = dir(tmpdir)
        for i = 1:n
            ind = strfind(a(i).name, '.mat')
            if ~isempty(ind)
                copyfile([tmpdir,'\',a(i).name],datadir)
            end
        end
end

rmdir(tmpdir, 's')