#!/usr/bin/env python


import eqrm_code.output_manager as om


def make_hazard_filename(site_tag, soil_amp, return_period):
    """Make a hazard filename given:

    site_tag      event descriptor string
    soil_amp      type of geology (boolean). True='soil_SA', False='bedrock_SA'
    return_period event return period
    """

    geo_type = 'bedrock_SA'
    if geo:
        geo_type = 'soil_SA'

    return '%s_%s_rp%d.txt' % (site_tag, soil_amp, return_period)


def obsolete_plot_hazard(input_dir, site_tag, soil_amp, return_period, period, output_dir,
                plot_file=None, save_file=None, title=None, np_posn=None,
                s_posn=None, cb_steps=None, colourmap=None,
                annotate=[]):
    """Plot an earthquake hazard map.

    input_dir     directory containing input data files
    site_tag      event descriptor string
    soil_amp      type of geology (boolean). True='soil_SA', False='bedrock_SA'
    return_period event return period
    period        period of the event
    output_dir    directory for output file(s)
    plot_file     full filename for generated plot file (*.png, *.eps, etc)
    save_file     full filename for saved plot data

    All other parameters are plot parameters as described elsewhere.

    Outputs are:
        plot_file  if specified, a plot file (*.png, *.eps, etc)
        save_file  if specified, a file containing data as plotted,
                   after any 'calc' manipulations.
    """

    # get raw data, all periods
    data = om.load_lat_long_haz_SA(input_dir, site_tag, soil_amp,
                                   return_period, period)

    # would do extra calc functions here, if required

    # if user wants to save actual plotted data
    if save_file:
        save(data, save_file)                                   ####################### needs change

    # plot the data
    if plot_file:
        # use default contour values if user didn't supply any
        if cb_steps is None:
            cb_steps = [0.1,0.15,0.20,0.30,0.40,0.50]

        if title is None:
            title = '%s hazard, RP=%s, period=%s' % (soil_amp, rp, p)

        pgxc.plot_gmt_xyz_contour(data, plot_file,
                                  title=title, np_posn=np_posn,
                                  s_posn=s_posn, cb_label=cb_label,
                                  cb_steps=cb_steps, annotate=annotate)


import eqrm_code.eqrm_filesystem as ef

#input_dir = ef.Demo_Output_ProbRisk_Path
input_dir = '.'

obsolete_plot_hazard(input_dir, 'newc', True, 100, 0.1, '.',
            plot_file='test.png', save_file=None, title=None, np_posn=None,
            s_posn=None, cb_steps=None, colourmap=None, annotate=[])
