function test_calc_annloss(root_eqrm_dir)
    saved_ecloss = [2000.0, 5.0;10.0, 2001.0]
    saved_ecbval2 = [2020.0, 2030.0]
    nu =  [0.01; 0.001]
    outputdir = ''
    varargin = 'd'
calc_annloss(saved_ecloss, saved_ecbval2, nu, outputdir, varargin)

end