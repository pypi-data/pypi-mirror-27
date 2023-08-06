# Author: Carsten Sachse 27-Oct-2013
# with Stefan Huber (2017) 
# Copyright: EMBL (2010 - 2018)
# License: see license.txt for details
""" 
Program to trace helices from micrographs
"""

from EMAN2 import EMUtil, EMData, EMNumPy, Util, periodogram
from filter import filt_gaussh
from fundamentals import window2d, rot_shift2D
import os
from spring.csinfrastr.csdatabase import SpringDataBase, base, grid_base, GridRefineTable
from spring.csinfrastr.csfeatures import Features, FeaturesSupport
from spring.csinfrastr.cslogger import Logger
from spring.csinfrastr.csproductivity import Temporary, OpenMpi
from spring.csinfrastr.csreadinput import OptHandler
from spring.micprgs.micexam import MicrographExam
from spring.micprgs.michelixtrace_helperfunctions import MicHelixTraceSupport
from spring.segment2d.segment import Segment
from spring.segment2d.segmentalign2d import SegmentAlign2d
from spring.segment3d.segclassreconstruct import SegClassReconstruct
from utilities import model_blank, image_decimate, model_circle

from scipy import ndimage, stats, signal
from tabulate import tabulate

import numpy as np


class MicHelixTracePar(object):
    """
    Class to initiate default dictionary with input parameters including help and range values and 
    status dictionary
    """

    def __init__(self):
        # package/program identity
        self.package = 'emspring'
        self.progname = 'michelixtrace'
        self.proginfo = __doc__
        self.code_files = [self.progname]
        self.tilesize_pix = None

        self.mictrace_features = Features()
        self.feature_set = self.mictrace_features.setup(self)

        self.define_parameters_and_their_properties()
        self.define_program_states()


    def define_input_and_output_michelixtrace(self):
        self.feature_set = self.mictrace_features.set_inp_multiple_micrographs(self.feature_set)
        self.feature_set = self.mictrace_features.set_output_plot_pattern(self.feature_set, self.progname + '_diag.pdf')


    def define_michelixtrace_parameters(self):
        self.feature_set = self.set_helix_reference(self.feature_set)
        self.feature_set = self.set_invert_option(self.feature_set)
        self.feature_set = self.mictrace_features.set_helix_width(self.feature_set)
        self.feature_set = self.mictrace_features.set_pixelsize(self.feature_set)
        self.feature_set = self.mictrace_features.set_binning_option(self.feature_set, default=True)
        self.feature_set = self.mictrace_features.set_binning_factor(self.feature_set, binfactor=4)
        self.feature_set = self.mictrace_features.set_power_tile_size(self.feature_set, size=500)
        self.feature_set = self.mictrace_features.set_tile_overlap(self.feature_set, percent=80)
        self.feature_set = self.set_a_threshold(self.feature_set)
        self.feature_set = self.set_absolute_threshold_option(self.feature_set)
        self.feature_set = self.set_absolute_threshold(self.feature_set)
        self.feature_set = self.set_order_fit(self.feature_set)
        self.feature_set = self.set_helix_length(self.feature_set)
        self.feature_set = self.set_pruning_cutoff(self.feature_set)
        self.feature_set = self.set_box_file_step(self.feature_set)
        # parameter search option
        self.feature_set = self.set_compute_recall_precision(self.feature_set)
        self.feature_set = self.set_parameter_search_option(self.feature_set)
        # specify box files
        self.feature_set = self.set_ground_truth_coord_file(self.feature_set)
        self.feature_set = self.mictrace_features.set_mpi(self.feature_set)
        self.feature_set = self.mictrace_features.set_ncpus_scan(self.feature_set)
        self.feature_set = self.mictrace_features.set_temppath(self.feature_set)


    def define_parameters_and_their_properties(self):
        self.define_input_and_output_michelixtrace()
        self.define_michelixtrace_parameters()


    def define_program_states(self):
        self.feature_set.program_states['orient_reference_power_with_overlapping_powers'] = 'Find orientations of ' + \
                                                                                            'by matching power spectra.'
        self.feature_set.program_states['find_translations_by_cc'] = 'Find translations by cross-correlation '
        self.feature_set.program_states['perform_connected_component_analysis'] = 'Extract individual helices by ' + \
                                                                                   'connected component analysis.'
        self.feature_set.program_states['build_cc_image_of_helices'] = 'Compute fine map of helix localisation'
        self.feature_set.program_states['visualize_traces_in_diagnostic_plot'] = 'Generate diagnostic plot'

    def set_helix_reference(self, feature_set):
        inp1 = 'Helix reference'
        feature_set.parameters[inp1] = 'helix_reference.hdf'
        feature_set.properties[inp1] = feature_set.file_properties(1, ['spi', 'hdf', 'img', 'hed'], 'getFile')
        feature_set.hints[inp1] = 'Helix reference: long rectangular straight box of helix to be traced. ' + \
                                  FeaturesSupport().add_accepted_file_formats_to_hint(feature_set, inp1)
        feature_set.level[inp1] = 'beginner'
        return feature_set


    ### PARAMETER SEARCH OPTIONS
    def set_compute_recall_precision(self, feature_set):
        inp6 = 'Compute performance score'
        feature_set.parameters[inp6] = bool(False)
        feature_set.hints[inp6] = 'Option to compute measures of tracing performance based on recall, precision ' + \
        'F1-measure, F05-measure by comparison of traced with provided ground truth helices.'
        feature_set.level[inp6] = 'expert'
        return feature_set    

    def set_parameter_search_option(self, feature_set):
        inp6 = 'Parameter search option'
        feature_set.parameters[inp6] = bool(False)
        feature_set.hints[inp6] = 'If True, tracing is run with multiple parameter pairs of Alpha threshold and ' + \
                                  'Minimum helix length cutoff to determine optimum parameter set. The grid search ' + \
                                  'will output a ParameterSpace.pdf file.'
        feature_set.level[inp6] = 'expert'
        feature_set.relatives[inp6]='Compute performance score'
        return feature_set    
        
    def set_ground_truth_coord_file(self, feature_set):
        inp8 = 'Manually traced helix file'
        feature_set.parameters[inp8] = 'mic.box'
        feature_set.properties[inp8] = feature_set.file_properties(1000, ['box', 'txt'], 'getFiles')
        feature_set.hints[inp8] = 'Interactively traced helix file considered to be the ground truth in for parameter search. ' + \
        'Input: file with identical name of corresponding micrograph (accepted file ' + \
        'formats EMAN\'s Helixboxer/Boxer, EMAN2\'s E2helixboxer and Bsoft filament parameters coordinates: {0}{1}). '.\
        format(os.extsep, FeaturesSupport().add_file_extensions_in_comma_separated_string(feature_set, inp8)) + \
        'Make sure that helix paths are continuous. A helix path can follow a C- or S-path but must NOT form a U-turn.'
        feature_set.level[inp8]='expert'
        feature_set.relatives[inp8]='Compute performance score'
        return feature_set
    #########

    def set_box_file_step(self, feature_set):
        inp9 = 'Box file coordinate step'
        feature_set.parameters[inp9] = float(70)
        feature_set.hints[inp9] = 'If resulting box files are to be used in another software, step size in Anstrom' +\
                                  'between coordinates can be set here. Leave unchanged for subjequent usage within'+\
                                  'SPRING, since this can be adjusted in the SPRING program #segment seperately.'
        feature_set.properties[inp9] = feature_set.Range(1, 500, 0.1)
        feature_set.level[inp9] = 'expert'
        return feature_set

    def set_helix_length(self, feature_set):
        inp9 = 'Minimum and maximum helix length'
        feature_set.parameters[inp9] = tuple((500, 1500))
        feature_set.hints[inp9] = 'Sets the minimum and maximum allowed helix length in Angstrom. ' + \
                                  'Too short values can lead to contaminations being recognized as helices ' + \
                                  'Too large values can be too stringent, especially for overlapping or ' + \
                                  'highly bent helices. Longer helices will be split in half. ' + \
                                  'Maximum helix length is recommended to be at least double of minimum helix length. '
        feature_set.properties[inp9] = feature_set.Range(100, 7000, 1)
        feature_set.level[inp9] = 'expert'

        return feature_set

    def set_a_threshold(self, feature_set):
        inp9 = 'Alpha threshold cc-map'
        feature_set.parameters[inp9] = float(0.001)
        feature_set.hints[inp9] = 'Parameter for adaptive thresholding of CC-map:' +\
                                  'The significance of cross correlation values in the micrograph will be judged ' + \
                                  'by how extreme values compare to an exponential null hypothesis.' + \
                                  'The corresponding p-values are considered significant if below significance level ' + \
                                  'alpha. Lower this value in orders of magnitude if helix tracing too promiscuous.'
        feature_set.properties[inp9] = feature_set.Range(0, 1, 0.0000000001)
        feature_set.level[inp9] = 'expert'
        return feature_set

    def set_absolute_threshold_option(self, feature_set):
        inp6 = 'Absolute threshold option cc-map'
        feature_set.parameters[inp6] = bool(False)
        feature_set.hints[inp6] = 'If True, then adaptive thresholding using Alpha threhold will not be used. ' + \
                                  'Instead, absolute CC-value can be defined using Absolute threshold parameter.'
        feature_set.level[inp6] = 'expert'
        return feature_set

    def set_absolute_threshold(self, feature_set):
        inp9 = 'Absolute threshold cc-map'
        feature_set.parameters[inp9] = float(0.2)
        feature_set.hints[inp9] = 'Absolute CC threshold to regard pixel in CC-map as helix. Can only be used if ' \
                                  'Absolute threshold option is on.'
        feature_set.properties[inp9] = feature_set.Range(0, 10., 0.001)
        feature_set.level[inp9] = 'expert'
        feature_set.relatives[inp9]='Absolute threshold option cc-map'
        return feature_set

    def set_pruning_cutoff(self, feature_set):
        inp9 = 'Pruning cutoff bending'
        feature_set.parameters[inp9] = float(2)
        feature_set.hints[inp9] = 'Outlier helices that are too bent or kinked are removed in this pruning step. '+ \
                                  'The distribution of persistence length measures is analyzed once a population of ' + \
                                  'more than 100 helices have been detected. The pruning cutoff ' + \
                                  'determines how many standard deviations (estimated by MAD) the persistence length ' +\
                                  'is allowed to be below the median of the distribution. Diagnostic output file ' + \
                                  '\"PersistenceLength.pdf\" is generated. Values between 1 and 3 are recommended.'
        feature_set.properties[inp9] = feature_set.Range(0, 10, 0.01)
        feature_set.level[inp9] = 'expert'
        return feature_set

    def set_invert_option(self, feature_set):
        inp6 = 'Invert option'
        feature_set.parameters[inp6] = bool(False)
        feature_set.hints[inp6] = 'Inversion of contrast of reference, e.g. when using inverted class-average' + \
                                  'Reference must have same contrast than the micrograph, e.g. protein requires to be ' + \
                                  'black in micrograph as well as reference.'
        feature_set.level[inp6] = 'expert'
        return feature_set

    def set_order_fit(self, feature_set):
        inp9 = 'Order fit'
        feature_set.parameters[inp9] = int(2)
        feature_set.hints[inp9] = 'Order of polynomial fit the coordinates of detected helix (1=linear, ' + \
                                  '2=quadratic, 3=cubic ...). Can be used as a further restraint.'
        feature_set.properties[inp9] = feature_set.Range(1, 19, 1)
        feature_set.level[inp9] = 'expert'

        return feature_set


class MicHelixTrace(object):
    """
    * Class that holds functions for examining micrograph quality

    * __init__ Function to read in the entered parameter dictionary and load micrograph

    #. Usage: MicrographExam(pardict)
    #. Input: pardict = OrderedDict of program parameters
    """

    def define_all_michelixtrace_parameters(self, p):
        self.infile = p['Micrographs']
        self.outfile = p['Diagnostic plot pattern']
        self.micrograph_files = Features().convert_list_of_files_from_entry_string(self.infile)
        self.reference_file = p['Helix reference']
        self.invertoption = p['Invert option']
        self.helixwidth = p['Estimated helix width in Angstrom']

        self.ori_pixelsize = p['Pixel size in Angstrom']
        self.binoption = p['Binning option']
        self.binfactor = p['Binning factor']
        if self.binfactor == 1 and self.binoption is True:
            self.binoption = False
        self.tile_size_A = p['Tile size power spectrum in Angstrom']
        self.tile_overlap = p['Tile overlap in percent']

        self.a_threshold = p['Alpha threshold cc-map']
        self.absolutethresholdoption = p['Absolute threshold option cc-map']
        self.absolute_threshold = p['Absolute threshold cc-map']
        self.order_fit = p['Order fit']
        self.min_helix_length, self.max_helix_length = p['Minimum and maximum helix length']
        self.boxfile_coordinatestep = p['Box file coordinate step']
        self.pruning_cutoff = p['Pruning cutoff bending']
        self.compute_stat = p['Compute performance score']
        self.parametersearch_option = p['Parameter search option']
        self.ground_truth_files = p['Manually traced helix file']
        if self.compute_stat:
            self.ground_truth_files = Features().convert_list_of_files_from_entry_string(self.ground_truth_files)

        self.temppath = p['Temporary directory']
        self.mpi_option = p['MPI option']
        self.cpu_count = p['Number of CPUs']

    def __init__(self, parset=None):
        self.log = Logger()
        if parset is not None:
            self.feature_set = parset
            p = self.feature_set.parameters

            self.define_all_michelixtrace_parameters(p)

    def gold_particles_mask(self, mic_1d, thr=0.001):
        '''
        :param mic_1d: Ravelled (1D) micrograph
        :param thr: Threshold when to treat pixel value as gold particle. Corresponds to alpha value in hypothesis
                    testing when we test for every pixel value if it deviates (left-sided) from the null hypothesis
        :return: 1D mask that is 1 where the micrograph contains a gold particle, otherwise 0.
        '''
        norm_distribution = stats.norm

        med = np.median(mic_1d)
        mad = np.median(np.absolute(mic_1d - med)) * 1.4826

        p_values = norm_distribution.cdf(mic_1d, med, mad)

        mic_trunc = np.ones(mic_1d.size)
        mic_trunc[p_values < thr] = 0

        return mic_trunc

    def preprocess_micrograph(self, mic, pixelsize):

        # High Pass Filter
        mic = filt_gaussh(mic, 0.02, pad=True)
        mic_np = np.copy(EMNumPy.em2numpy(mic))
        size_y, size_x = mic_np.shape

        # Gold particles
        mic_1d = mic_np.ravel()
        maskk = self.gold_particles_mask(mic_1d)
        mask = maskk.reshape(mic_np.shape)
        mic_masked = mic_np * mask

        # Mask Edges
        mic_trunc = self.mask_micrograph_edges(mic_masked, pixelsize * 2.0)
        mic_preprocessed = EMNumPy.numpy2em(np.copy(mic_trunc))

        return mic_preprocessed, size_y, size_x

    def smooth_mask_helix(self, pixelsize, reference):
        '''
        :return: boxfunction with smooth edges for masking the reference helix
        '''
        n = reference.shape[1]
        helix_pixel = self.helixwidth / pixelsize * 1.2
        background_pixel = n-helix_pixel
        boxfunction = np.zeros(n)
        boxfunction[background_pixel//2:-background_pixel//2] = 1
        boxfunction_smooth = signal.fftconvolve(boxfunction, signal.gaussian(helix_pixel/5.0, helix_pixel/10.0),
                                                mode='same')
        return boxfunction_smooth


    def prepare_power_from_reference(self, reference_file):
        reference = EMData()
        reference.read_image(reference_file)
        reference.process_inplace('normalize')

        if self.binoption:
            reference = image_decimate(reference, self.binfactor, fit_to_fft=False)
            pixelsize = self.ori_pixelsize * float(self.binfactor)
        else:
            pixelsize = self.ori_pixelsize

        reference = np.copy(EMNumPy.em2numpy(reference))
        # Smooth masking of helix within reference
        reference *= self.smooth_mask_helix(pixelsize, reference)
        # Invert reference if needed
        if self.invertoption:
            reference *= (-1)
        reference = EMNumPy.numpy2em(np.copy(reference))

        overlap_percent = 90.0
        step_size = int(reference.get_ysize() * (100.0 - overlap_percent) / 100.0)
        tile_size_pix = int(self.tile_size_A / pixelsize)
        tile_size_pix = Segment().determine_boxsize_closest_to_fast_values(tile_size_pix)
        ref_size = reference.get_ysize()

        if ref_size < tile_size_pix:
            msg = 'Chosen reference size ({0} Angstrom) is smaller than specified '.format(int(ref_size * pixelsize)) + \
                  'tile size of {0} Angstrom. Please increase reference or decrease tile size.'.format(self.tile_size_A)
            raise ValueError(msg)

        y_positions = np.arange(0, reference.get_ysize() - tile_size_pix, step_size)

        if reference.get_xsize() < tile_size_pix:
            reference = Util.pad(reference, tile_size_pix, ref_size, 1, 0, 0, 0, 'zero')
        if reference.get_xsize() > tile_size_pix:
            reference = Util.window(reference, tile_size_pix, ref_size, 1, 0, 0, 0)

        reference.process_inplace('normalize')

        if len(y_positions) > 0:
            reference_pw = model_blank(tile_size_pix, tile_size_pix)
            for each_y in y_positions:
                wi_ref = window2d(reference, tile_size_pix, tile_size_pix, 'l', 0, int(each_y))
                reference_pw += periodogram(wi_ref)
        else:
            wi_ref = Util.window(reference, tile_size_pix, tile_size_pix, 1, 0, 0, 0)
            reference_pw = periodogram(wi_ref)

        circle_mask = -1 * model_circle(3, tile_size_pix, tile_size_pix) + 1
        reference_pw *= circle_mask

        reference = np.copy(EMNumPy.em2numpy(reference))

        return reference_pw, tile_size_pix, reference

    def compute_step_size(self, tile_size, overlap):
        step = int(tile_size - tile_size * overlap / 100.0)
        return step

    def determine_xy_center_grid(self, tile_size, overlap, x_size, y_size):
        """
        >>> from spring.micprgs.michelixtrace import MicHelixTrace
        >>> MicHelixTrace().determine_xy_center_grid(15, 50, 50, 100)
        array([[(7.0, 7.0), (7.0, 14.0), (7.0, 21.0), (7.0, 28.0), (7.0, 35.0),
                (7.0, 42.0), (7.0, 49.0), (7.0, 56.0), (7.0, 63.0), (7.0, 70.0),
                (7.0, 77.0), (7.0, 84.0), (7.0, 91.0)],
               [(14.0, 7.0), (14.0, 14.0), (14.0, 21.0), (14.0, 28.0),
                (14.0, 35.0), (14.0, 42.0), (14.0, 49.0), (14.0, 56.0),
                (14.0, 63.0), (14.0, 70.0), (14.0, 77.0), (14.0, 84.0),
                (14.0, 91.0)],
               [(21.0, 7.0), (21.0, 14.0), (21.0, 21.0), (21.0, 28.0),
                (21.0, 35.0), (21.0, 42.0), (21.0, 49.0), (21.0, 56.0),
                (21.0, 63.0), (21.0, 70.0), (21.0, 77.0), (21.0, 84.0),
                (21.0, 91.0)],
               [(28.0, 7.0), (28.0, 14.0), (28.0, 21.0), (28.0, 28.0),
                (28.0, 35.0), (28.0, 42.0), (28.0, 49.0), (28.0, 56.0),
                (28.0, 63.0), (28.0, 70.0), (28.0, 77.0), (28.0, 84.0),
                (28.0, 91.0)],
               [(35.0, 7.0), (35.0, 14.0), (35.0, 21.0), (35.0, 28.0),
                (35.0, 35.0), (35.0, 42.0), (35.0, 49.0), (35.0, 56.0),
                (35.0, 63.0), (35.0, 70.0), (35.0, 77.0), (35.0, 84.0),
                (35.0, 91.0)],
               [(42.0, 7.0), (42.0, 14.0), (42.0, 21.0), (42.0, 28.0),
                (42.0, 35.0), (42.0, 42.0), (42.0, 49.0), (42.0, 56.0),
                (42.0, 63.0), (42.0, 70.0), (42.0, 77.0), (42.0, 84.0),
                (42.0, 91.0)]], dtype=object)

        """
        edge_x0 = edge_y0 = tile_size / 2
        edge_x1 = x_size - edge_x0
        edge_y1 = y_size - edge_y0

        step = self.compute_step_size(tile_size, overlap)

        x_array = np.arange(edge_x0, edge_x1, step)
        y_array = np.arange(edge_y0, edge_y1, step)

        xy_center_grid = np.zeros((x_array.size, y_array.size), dtype=tuple)
        for each_x_id, each_x in enumerate(x_array):
            for each_y_id, each_y in enumerate(y_array):
                xy_center_grid[each_x_id][each_y_id] = (np.ceil(each_x), np.ceil(each_y))

        return xy_center_grid

    def generate_stack_of_overlapping_images_powers(self, mic, tile_size, overlap, gaussian_kernel_2d):

        x_size = mic.get_xsize()
        y_size = mic.get_ysize()

        xy_center_grid = self.determine_xy_center_grid(tile_size, overlap, x_size, y_size)

        # xy_table = tabulate(xy_center_grid.ravel(), ['x_coordinate', 'y_coordinate'])
        # self.log.ilog('The following x, y coordinates are the centers of the tiles of ' + \
        # 'the binned micrograph:\n{0}'.format(xy_table))

        pw_stack = os.path.join(self.tempdir, 'pw_stack.hdf')
        img_stack = os.path.join(self.tempdir, 'img_stack.hdf')
        circle = -1 * model_circle(3, tile_size, tile_size) + 1

        for each_id, (each_x, each_y) in enumerate(xy_center_grid.ravel()):
            upper_x = each_x - tile_size / 2
            upper_y = each_y - tile_size / 2
            img = window2d(mic, tile_size, tile_size, "l", upper_x, upper_y)
            img = np.copy(EMNumPy.em2numpy(img))
            img *= gaussian_kernel_2d
            img = EMNumPy.numpy2em(np.copy(img))
            pw = periodogram(img) * circle
            img.write_image(img_stack, each_id)
            pw.write_image(pw_stack, each_id)

        return img_stack, pw_stack, xy_center_grid

    def orient_reference_power_with_overlapping_powers(self, pw_stack, ref_power, xy_center_grid):
        self.log.fcttolog()

        image_dimension = ref_power.get_xsize()
        polar_interpolation_parameters, ring_weights = SegmentAlign2d().prepare_empty_rings(1, image_dimension / 2 - 2,
                                                                                            1)

        cimage = SegmentAlign2d().make_rings_and_prepare_cimage_header(image_dimension, polar_interpolation_parameters,
                                                                       ring_weights, ref_power)

        x_range = y_range = 0.0
        translation_step = 1.0
        shift_x = shift_y = 0
        center_x = center_y = image_dimension / 2 + 1
        full_circle_mode = 'F'
        pw_img_count = EMUtil.get_image_count(pw_stack)

        pw_img = EMData()
        angles = []
        peaks = []
        for each_pw_id in list(range(pw_img_count)):
            pw_img.read_image(pw_stack, each_pw_id)

            [angt, _, _, _, _, peakt] = Util.multiref_polar_ali_2d(pw_img, [cimage], x_range,
                                                                                  y_range, translation_step,
                                                                                  full_circle_mode,
                                                                                  polar_interpolation_parameters,
                                                                                  center_x + shift_x,
                                                                                  center_y + shift_y)

            angles.append(angt)
            peaks.append(peakt)

        angles = np.array(angles).reshape(xy_center_grid.shape)
        peaks = np.array(peaks).reshape(xy_center_grid.shape)

        # angle_table = tabulate(angles)
        # peaks_table = tabulate(peaks)
        #
        # self.log.ilog('The following angles were assigned to the tiles:\n{0}'.format(angle_table))
        # self.log.ilog('The following peaks were found for the tiles:\n{0}'.format(peaks_table))

        return angles, peaks

    def find_translations_by_cc(self, angles, xy_centers, img_stack, ref):
        self.log.fcttolog()

        image_dimension = ref.shape[1]

        fl_centers = xy_centers.ravel()
        rhos = np.zeros(fl_centers.shape)
        thetas = np.zeros(fl_centers.shape)
        circle = model_circle(image_dimension / 2, image_dimension, image_dimension)
        cross_corr = []
        for each_id, each_angle in enumerate(angles.ravel()):
            img = EMData()
            img.read_image(img_stack, each_id)
            img = rot_shift2D(circle * img, each_angle)
            img = np.copy(EMNumPy.em2numpy(img))
            cc_prof_2d = signal.fftconvolve(img, ref, mode='same') / img.size

            max_shift = np.argmax(cc_prof_2d)
            max_shift_y, max_shift_x = np.unravel_index(max_shift, cc_prof_2d.shape)
            cross_corr.append(cc_prof_2d[max_shift_y, max_shift_x])
            max_shift_y -= img.shape[0] // 2
            max_shift_x -= img.shape[1] // 2

            x_coord = fl_centers[each_id][0]
            y_coord = fl_centers[each_id][1]
            rhos[each_id] = x_coord * np.cos(np.deg2rad(each_angle)) + \
                            y_coord * np.sin(np.deg2rad(each_angle)) + max_shift_x
            thetas[each_id] = each_angle

        rhos = rhos.reshape(angles.shape)
        thetas = thetas.reshape(angles.shape)
        cross_corr = np.array(cross_corr).reshape(angles.shape)

        return rhos, thetas, cross_corr


    def perform_absolute_thresholding_of_ccmap(self, overlap_cc, absolute_threshold):
        absolute_threshold = absolute_threshold
        thres_map = (overlap_cc>absolute_threshold)
        lamb = None
        background_cutoff = 0.0

        return thres_map, lamb, absolute_threshold, background_cutoff


    def perform_thresholding_of_ccmap(self, overlap_cc, a_threshold):
        y_size, x_size = overlap_cc.shape
        fitfunction = stats.expon

        lamb = 0
        # Iterative check for background cutoff ~0 that is not used for fitting
        for i in range(10):
            # Preparation of z-values (CC_values)
            cc_values = overlap_cc.ravel()
            background_cutoff = lamb / 100.0
            cc_values_fitting = overlap_cc[overlap_cc > background_cutoff] # do not include ~zero values in fitting

            # Median to estimate lambda of exponential
            lamb = np.median(cc_values_fitting) / np.log(2)
            params = [0, lamb]

        # Convert cc-values to p-values according to fitted exponential distribution with parameter lambda
        p_values = 1 - fitfunction.cdf(cc_values, *params)

        # Thresholding
        pixel_count = len(p_values)
        thres_map = np.zeros(pixel_count)
        thres_map[p_values <= a_threshold] = 1
        thres_map = thres_map.reshape((y_size, x_size))

        absolute_threshold = None

        return thres_map, lamb, absolute_threshold, background_cutoff


    def build_cc_image_of_helices(self, rhos, thetas, cross_corr, xy_center_grid, x_size, y_size, tilesize,
    overlap_percent):

        overlap_cc = np.zeros((y_size, x_size))

        fl_rhos = rhos.ravel()
        fl_thetas = thetas.ravel()
        fl_cc = cross_corr.ravel()

        step = self.compute_step_size(tilesize, overlap_percent)

        thick = max(1, int(np.around(y_size / 1000.)))
        for each_id, (each_x, each_y) in enumerate(xy_center_grid.ravel()):
            each_fl_cc = fl_cc[each_id]

            lower_x = each_x - tilesize / 2
            upper_x = min(x_size, each_x + tilesize / 2)

            lower_y = each_y - tilesize / 2
            upper_y = min(y_size, each_y + tilesize / 2)

            each_angle = fl_thetas[each_id]

            point_count = tilesize
            if 45 <= each_angle < 135 or 225 <= each_angle < 315:
                xx = np.linspace(lower_x, upper_x, point_count)
                yy = (fl_rhos[each_id] - xx * np.cos(np.deg2rad(each_angle))) / np.sin(np.deg2rad(each_angle))

                yyy = yy[(lower_y <= yy) & (yy < upper_y)]
                xxx = xx[(lower_y <= yy) & (yy < upper_y)]
            else:
                yy = np.linspace(lower_y, upper_y, point_count)
                xx = (fl_rhos[each_id] - yy * np.sin(np.deg2rad(each_angle))) / np.cos(np.deg2rad(each_angle))

                yyy = yy[(lower_x <= xx) & (xx < upper_x)]
                xxx = xx[(lower_x <= xx) & (xx < upper_x)]

            yyy = np.round(yyy).astype(dtype=np.int16)
            xxx = np.round(xxx).astype(dtype=np.int16)
            each_fl_cc_blur = each_fl_cc * signal.gaussian(len(yyy), 2*step)
            for i, (each_xx, each_yy) in enumerate(zip(xxx, yyy)):
#                 if 45 <= each_angle < 135 or 225 <= each_angle < 315:
#                     overlap_cc[each_yy - thick:each_yy + thick + 1, each_xx - thick:each_xx + thick + 1] += each_fl_cc_blur[i]
#                 else:
#                     overlap_cc[each_yy - thick - 1:each_yy + thick, each_xx - thick - 1:each_xx + thick] += each_fl_cc_blur[i]
                overlap_cc[each_yy - thick:each_yy + thick, each_xx - thick:each_xx + thick] += each_fl_cc_blur[i]

        overlap_count = tilesize / float(self.compute_step_size(tilesize, overlap_percent))
        overlap_cc /= overlap_count

        histogram_bin = np.histogram(overlap_cc)
        table_cc = tabulate([np.append('cc_bin', histogram_bin[1]), np.append('pixel_count', histogram_bin[0])])

        cc_summary = tabulate([[np.min(overlap_cc), np.max(overlap_cc), np.average(overlap_cc), np.std(overlap_cc)]],
                              ['min', 'max', 'average', 'stdev'])

        self.log.ilog('The following weighted cross correlations were determined:\n{0}'.format(table_cc))
        self.log.ilog('Cross correlation summary:\n{0}'.format(cc_summary))

        return overlap_cc

    def get_lookup_table_for_bwmorph_thin(self):
        G123_LUT = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1,
                             0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0,
                             1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                             0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1,
                             0, 0, 0], dtype=np.bool)

        G123P_LUT = np.array([0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0,
                              1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0,
                              0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0,
                              1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1,
                              0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0], dtype=np.bool)

        return G123_LUT, G123P_LUT

    def bwmorph_thin(self, image, n_iter=None):
        """
        Perform morphological thinning of a binary image
        
        Parameters
        ----------
        image : binary (M, N) ndarray
            The image to be thinned.
        
        n_iter : int, number of iterations, optional
            Regardless of the value of this parameter, the thinned image
            is returned immediately if an iteration produces no change.
            If this parameter is specified it thus sets an upper bound on
            the number of iterations performed.
        
        Returns
        -------
        out : ndarray of bools
            Thinned image.
        
        See also
        --------
        skeletonize
        
        Notes
        -----
        This algorithm [1]_ works by making multiple passes over the image,
        removing pixels matching a set of criteria designed to thin
        connected regions while preserving eight-connected components and
        2 x 2 squares [2]_. In each of the two sub-iterations the algorithm
        correlates the intermediate skeleton image with a neighborhood mask,
        then looks up each neighborhood in a lookup table indicating whether
        the central pixel should be deleted in that sub-iteration.
        
        References
        ----------
        .. [1] Z. Guo and R. W. Hall, "Parallel thinning with
               two-subiteration algorithms," Comm. ACM, vol. 32, no. 3,
               pp. 359-373, 1989.
        .. [2] Lam, L., Seong-Whan Lee, and Ching Y. Suen, "Thinning
               Methodologies-A Comprehensive Survey," IEEE Transactions on
               Pattern Analysis and Machine Intelligence, Vol 14, No. 9,
               September 1992, p. 879
        
        Examples
        --------
        >>> from spring.micprgs.michelixtrace import MicHelixTrace
        >>> m = MicHelixTrace()
        >>> square = np.zeros((7, 7), dtype=np.uint8)
        >>> square[1:-1, 2:-2] = 1
        >>> square[0,1] =  1
        >>> square
        array([[0, 1, 0, 0, 0, 0, 0],
               [0, 0, 1, 1, 1, 0, 0],
               [0, 0, 1, 1, 1, 0, 0],
               [0, 0, 1, 1, 1, 0, 0],
               [0, 0, 1, 1, 1, 0, 0],
               [0, 0, 1, 1, 1, 0, 0],
               [0, 0, 0, 0, 0, 0, 0]], dtype=uint8)
        >>> skel = m.bwmorph_thin(square)
        >>> skel.astype(np.uint8)
        array([[0, 1, 0, 0, 0, 0, 0],
               [0, 0, 1, 0, 0, 0, 0],
               [0, 0, 0, 1, 0, 0, 0],
               [0, 0, 0, 1, 0, 0, 0],
               [0, 0, 0, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0]], dtype=uint8)
        """
        # check parameters
        if n_iter is None:
            n = -1
        elif n_iter <= 0:
            raise ValueError('n_iter must be > 0')
        else:
            n = n_iter

        # check that we have a 2d binary image, and convert it
        # to uint8
        skel = np.array(image).astype(np.uint8)

        if skel.ndim != 2:
            raise ValueError('2D array required')
        if not np.all(np.in1d(image.flat, (0, 1))):
            raise ValueError('Image contains values other than 0 and 1')

        # neighborhood mask
        mask = np.array([[8, 4, 2],
                         [16, 0, 1],
                         [32, 64, 128]], dtype=np.uint8)

        # iterate either 1) indefinitely or 2) up to iteration limit
        G123_LUT, G123P_LUT = self.get_lookup_table_for_bwmorph_thin()
        while n != 0:
            before = np.sum(skel)  # count points before thinning

            # for each subiteration
            for lut in [G123_LUT, G123P_LUT]:
                # correlate image with neighborhood mask
                N = ndimage.correlate(skel, mask, mode='constant')
                # take deletion decision from this subiteration's LUT
                D = np.take(lut, N)
                # perform deletion
                skel[D] = 0

            after = np.sum(skel)  # coint points after thinning

            if before == after:
                # iteration had no effect: finish
                break

            # count down to iteration limit (or endlessly negative)
            n -= 1

        return skel.astype(np.bool)

    """
    # here's how to make the LUTs
    def nabe(n):
        return np.array([n>>i&1 for i in range(0,9)]).astype(np.bool)
    def hood(n):
        return np.take(nabe(n), np.array([[3, 2, 1],
                                          [4, 8, 0],
                                          [5, 6, 7]]))
    def G1(n):
        s = 0
        bits = nabe(n)
        for i in (0,2,4,6):
            if not(bits[i]) and (bits[i+1] or bits[(i+2) % 8]):
                s += 1
        return s==1
                
    g1_lut = np.array([G1(n) for n in range(256)])
    def G2(n):
        n1, n2 = 0, 0
        bits = nabe(n)
        for k in (1,3,5,7):
            if bits[k] or bits[k-1]:
                n1 += 1
            if bits[k] or bits[(k+1) % 8]:
                n2 += 1
        return min(n1,n2) in [2,3]
    g2_lut = np.array([G2(n) for n in range(256)])
    g12_lut = g1_lut & g2_lut
    def G3(n):
        bits = nabe(n)
        return not((bits[1] or bits[2] or not(bits[7])) and bits[0])
    def G3p(n):
        bits = nabe(n)
        return not((bits[5] or bits[6] or not(bits[3])) and bits[4])
    g3_lut = np.array([G3(n) for n in range(256)])
    g3p_lut = np.array([G3p(n) for n in range(256)])
    g123_lut  = g12_lut & g3_lut
    g123p_lut = g12_lut & g3p_lut
    """

    def set_up_branch_point_response(self):
        """
        >>> from spring.micprgs.michelixtrace import MicHelixTrace
        >>> m = MicHelixTrace()
        >>> b = m.set_up_branch_point_response() #doctest: +NORMALIZE_WHITESPACE
        >>> assert b == m.get_branch_point_response()
        """
        features = [np.array([[0, 1, 0],
                              [1, 1, 1],
                              [0, 0, 0]]),
                    np.array([[0, 1, 0],
                              [1, 1, 0],
                              [0, 0, 1]]),
                    np.array([[0, 0, 1],
                              [0, 1, 0],
                              [1, 0, 1]]),
                    np.array([[1, 0, 1],
                              [0, 1, 0],
                              [0, 1, 0]]),
                    np.array([[0, 0, 1],
                              [1, 1, 0],
                              [1, 1, 0]]),
                    np.array([[0, 1, 0],
                              [1, 1, 1],
                              [0, 0, 1]]),
                    np.array([[0, 1, 0],
                              [1, 1, 1],
                              [0, 1, 0]])
                    ]

        features = [np.rot90(each_feature, each_rot) for each_feature in features for each_rot in list(range(4))]

        mask = self.get_mask()

        feature_values = list(set([ndimage.correlate(each_feature, mask)[1, 1] for each_feature in features]))
        feature_values.sort()

        return feature_values

    def get_branch_point_response(self):
        return [277, 293, 297, 298, 313, 325, 329, 330, 334, 337, 338, 340, 362, 394, 402, 403, 404, 410, 418, 420, 422,
        424, 425, 426, 484]

    def get_mask(self):
        mask = np.array([[1, 2, 4],
                         [128, 256, 8],
                         [64, 32, 16]])
        return mask

    def get_rid_of_branchpoints_and_crossings(self, skel, helix_width):
        branch_point_response = self.get_branch_point_response()
        mask = self.get_mask()

        N = ndimage.correlate(skel.astype(np.uint16), mask, mode='constant')

        branch_points = np.in1d(N.ravel(), branch_point_response)
        helix_radius = np.ceil(helix_width / 2.0) // 2 * 2 + 1
        dilate_kernel = self.model_circle(helix_radius, helix_radius, 2 * helix_radius, 2 * helix_radius)
        if np.sum(branch_points) > 0:
            branch_points_img = branch_points.reshape((skel.shape))

            branch_points_img = ndimage.binary_dilation(branch_points_img, structure=dilate_kernel)
            skel *= np.invert(branch_points_img)
        return skel

    def model_circle(self, radius_y, radius_x, ydim, xdim, center_y=None, center_x=None):
        """
        >>> from spring.micprgs.michelixtrace import MicHelixTrace
        >>> m = MicHelixTrace()
        >>> m.model_circle(3, 5, 10, 12)
        array([[ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  0.,  0.],
               [ 0.,  0.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  0.],
               [ 0.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.],
               [ 0.,  0.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  0.],
               [ 0.,  0.,  0.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]])

        >>> m.model_circle(3, 3, 10, 12, -1, 1)
        array([[ 1.,  1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 1.,  1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]])
        """
        if center_y is None:
            center_y = ydim / 2
        if center_x is None:
            center_x = xdim / 2

        y, x = np.ogrid[-center_y:ydim - center_y, -center_x:xdim - center_x]
        mask = (x / float(radius_x)) ** 2 + (y / float(radius_y)) ** 2 <= 1

        circle = np.zeros((ydim, xdim))
        circle[mask] = 1

        return circle

    def model_square(self, length_y, length_x, ydim, xdim, center_y=None, center_x=None):
        """
        >>> from spring.micprgs.michelixtrace import MicHelixTrace
        >>> m = MicHelixTrace()
        >>> m.model_square(6, 3, 10, 12)
        array([[ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]])

        >>> m.model_square(6, 6, 10, 12, -1, 1)
        array([[ 1.,  1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 1.,  1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]])
        """
        if center_y is None:
            center_y = ydim / 2
        if center_x is None:
            center_x = xdim / 2

        h_length_y = length_y / 2.0
        h_length_x = length_x / 2.0

        square = np.zeros((ydim, xdim))
        square[max(0, center_y - h_length_y):min(ydim, center_y + h_length_y),
        max(0, center_x - h_length_x):min(xdim, center_x + h_length_x)] = 1

        return square

    def mask_micrograph_edges(self, mic, pixelsize):
        ydim, xdim = mic.shape
        circle = self.model_circle(1.2 * ydim / 2, 1.2 * xdim / 2, ydim, xdim)
        min_dist_to_edge = np.ceil(0.5 * 25000 * 0.02 / pixelsize)
        circle *= self.model_square(ydim - 2 * min_dist_to_edge, xdim - 2 * min_dist_to_edge, ydim, xdim)
        mic *= circle.astype(mic.dtype)
        return mic

    def fit_and_create_coordinates_according_to_order(self, x, y, order_fit, step_coord):
        x_arg = np.argsort(x)
        x = x[x_arg]
        y = y[x_arg]
        _, uniqidx = np.unique(x, return_index=True)
        x = x[uniqidx]
        y = y[uniqidx]
        fine_x_coord = np.linspace(x[0], x[-1], int((x[-1] - x[0]) / step_coord))
        fitt = np.polyfit(x, y, order_fit)
        fine_y_coord = np.polyval(fitt, fine_x_coord)
        return fine_x_coord, fine_y_coord

    def compute_length_of_fit(self, fine_x_coord, fine_y_coord):
        if len(fine_x_coord) >= 2:
            lengths = np.sqrt((fine_x_coord[:-1] - fine_x_coord[1:]) ** 2 \
                              + (fine_y_coord[:-1] - fine_y_coord[1:]) ** 2)
            cum_length = np.concatenate(([0], np.cumsum(lengths)))
            length = cum_length[-1]
        else:
            cum_length, length = None, 0
        return cum_length, length

    def perform_connected_component_analysis(self, binary, pixelsize, order_fit, min_length, max_length):
        label_im, label_count = ndimage.label(binary, structure=np.ones((3,3)))

        feature_list = list(range(1, label_count + 1))

        step_coord_A = self.boxfile_coordinatestep
        single_helices = []
        while len(feature_list) > 0:
            each_feature = feature_list[0]
            slice_y, slice_x = ndimage.find_objects(label_im == each_feature)[0]
            height = int(slice_y.stop - slice_y.start)
            width = int(slice_x.stop - slice_x.start)

            roi = (label_im == each_feature)
            roi_thin = self.bwmorph_thin(roi)
            y, x = np.where(roi_thin == 1)
            y = y.astype(dtype=np.float64)
            x = x.astype(dtype=np.float64)

            # For very small particles (e.g.) dirt, fitting below will fail
            if len(x) < 5:
                feature_list.remove(each_feature)
                continue

            # Fit polynomial
            if height >= width:
                fine_y_coord, fine_x_coord = self.fit_and_create_coordinates_according_to_order(y, x, order_fit,
                                                                                                step_coord_A / pixelsize)
            else:
                fine_x_coord, fine_y_coord = self.fit_and_create_coordinates_according_to_order(x, y, order_fit,
                                                                                                step_coord_A / pixelsize)

            # Accurately determine length of fitted polynomial
            cum_length, length = self.compute_length_of_fit(fine_x_coord, fine_y_coord)

            # Too short helices will be thrown away
            if length <= (min_length / pixelsize):
                feature_list.remove(each_feature)
                continue

            # Too long helices will be split into 2 by determining midpoint and writing two new regions in label_im
            if length > (max_length / pixelsize):
                label_count_roi = 1
                deleter = np.zeros_like(roi)
                midpoint = int((np.abs(cum_length - length / 2.0)).argmin())
                mid_x = fine_x_coord[midpoint]
                mid_y = fine_y_coord[midpoint]
                deleter[mid_y, mid_x] = 1
                counter = 0  # For safety to avoid endless loops
                while label_count_roi < 2 and counter <= 12:
                    roi *= np.invert(deleter)
                    label_im_roi, label_count_roi = ndimage.label(roi)
                    deleter = ndimage.binary_dilation(deleter)
                if counter < 12:
                    # If by cutting, more than 2 parts are produced, look which are the biggest two pieces
                    labels, counts = np.unique(label_im_roi, return_counts=True)
                    biggest_labels = labels[1:][np.argsort(counts[1:])[::-1][0:2]]
                    for label in biggest_labels:
                        new_label = label_im.max() + 1
                        feature_list.append(new_label)
                        label_im[label_im_roi == label] = new_label  # Add cutted helix to label_im
                    feature_list.remove(each_feature)
                    continue

            # Appending helix to list
            single_helices.append((fine_x_coord, fine_y_coord))

            feature_list.remove(each_feature)

        return single_helices


    def compute_persistence_length(self, helices, pixelsize):
        if self.order_fit == 1:
            pers_lengths = [1.0 for x_coord, y_coord in helices]
        elif self.order_fit > 1:
            s = Segment()
            pers_lengths = [1e+6 * s.compute_persistence_length_m_from_coordinates_A(x_coord * pixelsize,
                                                                                     y_coord * pixelsize)
                            for x_coord, y_coord in helices]
            helix_ids = list(range(len(pers_lengths)))
            msg = tabulate(zip(helix_ids, pers_lengths), ['helix', 'persistence length in micrometers'])
            self.log.ilog(msg)

        return np.array(pers_lengths)


    def prune_helices_and_plot_persistence_length_summary(self, helix_info):
        len_before = len(helix_info)
        bundle = [np.array(each_helix.coordinates)*self.ori_pixelsize for each_helix in helix_info]

        distances, correlations, bin_centers, bin_means, bin_stds, pl_exact, dpl_exact = \
        MicHelixTraceSupport().compute_persistence_length_from_tangent_vector_correlation(bundle)

        pl_list = np.array([each_helix.curvature[0] for each_helix in helix_info]) * 1e10
        pl_list = pl_list[pl_list>0] # avoid trouble with log(0)
        
        pruning_cutoff_absolute = MicHelixTraceSupport().plot_pers_length_summary(bundle, pl_exact, dpl_exact, pl_list,
        distances, correlations,bin_centers, bin_means, bin_stds, self.pruning_cutoff, 'PersistenceLength.pdf')

        helix_info = [h for h in helix_info if h.curvature[0]*1e+6>pruning_cutoff_absolute]

        if len(helix_info)<len_before:
            msg = 'A total of {0} helices were excluded '.format(len_before-len(helix_info)) + \
                  'persistence length cutoff {0} micrometers.'.format(pruning_cutoff_absolute)
            self.log.ilog(msg)

        return helix_info
        

    def generate_and_plot_parameter_search_summary(self, trcng_crit_comb, absolutethresholdoption):
        xi, yi, zi_precisions, zi_recalls = MicHelixTraceSupport().interpolate_parameter_space(trcng_crit_comb)
        # xi=threshold, yi=min_helix_cutoff, zi=interpolated parameter spaces
        best_x, best_y = MicHelixTraceSupport().plot_parameter_search_summary(xi, yi, zi_precisions, zi_recalls,
        absolutethresholdoption)


    def write_helixinfo(self, helix_info, single_helices, each_mic, tilesize, pixelsize, helixwidth):

        overlap_name = os.path.splitext(os.path.basename(each_mic))[0]
        overlap_dir = os.path.join(os.path.abspath(os.curdir), overlap_name)

        if not self.binoption:
            self.binfactor = 1
        s = Segment()
        s.segsizepix = tilesize
        for each_id, (each_xcoord, each_ycoord) in enumerate(single_helices):
            xcoord = (each_xcoord + 0.5) * self.binfactor
            ycoord = (each_ycoord + 0.5) * self.binfactor
            each_box = os.path.join(overlap_dir, overlap_name) + '_{0:03}'.format(each_id) + os.extsep + 'box'
            int_xcoord, int_ycoord, ipangle, curvature = \
                s.interpolate_coordinates(xcoord, ycoord, pixelsize, self.boxfile_coordinatestep, helixwidth,
                                          '', new_stepsize=False)
            helix_info = s.enter_helixinfo_into_helices(helix_info, each_mic, overlap_dir, each_box,
                                                                           ipangle, curvature,
                                                                           list(zip(xcoord, ycoord)),
                                                                           list(zip(int_xcoord, int_ycoord)))
        return helix_info


    def write_boxfiles_from_helix_info(self, helix_info):
        
        segsizepix = int(self.tile_size_A / self.ori_pixelsize)
        for each_helix in helix_info:
            interpolated_xcoord, interpolated_ycoord = zip(*each_helix.coordinates)
            helixfile = os.path.splitext(os.path.basename(each_helix.micrograph))[0] + '.box'
        
            Segment().write_boxfile(np.array(interpolated_xcoord), np.array(interpolated_ycoord), segsizepix,
            filename=helixfile)


    def get_interactively_traced_helices_to_compare(self):
        
        s = Segment()
        s.helixwidth = self.helixwidth
        s.frame_option = False
        s.remove_ends = False
        s.perturb_step = False
        s.segsizepix = int(self.tile_size_A / self.ori_pixelsize)

        pair = s.assign_reorganize(self.micrograph_files, self.ground_truth_files)
        _, _, dirs = zip(*pair)
        
        [os.rename(each_dir, each_dir + '_groundtruth') for each_dir in dirs]
        pair = [(each_p[0], each_p[1], each_p[2] + '_groundtruth') for each_p in pair]

        stepsize_A = 70.0
        truth_helices, _, _ = s.single_out(pair, stepsize_A, self.ori_pixelsize, assigned_mics=None)

        return truth_helices


    def define_thresholds_and_minimum_helix_lengths(self, parametersearch_option, a_threshold, min_helix_length,
    max_helix_length, absolutethresholdoption, absolute_threshold):
        """
        >>> from spring.micprgs.michelixtrace import MicHelixTrace
        >>> m = MicHelixTrace()
        >>> m.define_thresholds_and_minimum_helix_lengths(False, 0.01, 500, 1000, False, 0)
        ([0.01], [(500, 1000)])
        >>> m.define_thresholds_and_minimum_helix_lengths(True, 0.01, 500, 1000, False, 0)
        ([0.0001, 0.001, 0.01, 0.1, 1.0], [(200, 500), (350, 875), (500, 1250), (650, 1625), (800, 2000)])
        >>> m.define_thresholds_and_minimum_helix_lengths(True, 0.01, 500, 1000, True, 0.5)
        ([0.09999999999999998, 0.3, 0.5, 0.7, 0.9], [(200, 500), (350, 875), (500, 1250), (650, 1625), (800, 2000)])
        """
        if parametersearch_option:
            step_length = 150
            min_helix_lengths = [min_helix_length + i * step_length for i in range(-2,3)]
            max_helix_lengths = [int(2.5 * each_min_helix_length) for each_min_helix_length in min_helix_lengths]
            helix_lengths = zip(min_helix_lengths, max_helix_lengths)

            if absolutethresholdoption:
                step_cc = 0.2
                thresholds = [absolute_threshold + i * step_cc for i in range(-2,3)]
            else:
                base = 10.0
                thresholds = [a_threshold * base**i for i in range(-2,3)]
        else:
            helix_lengths = [(min_helix_length, max_helix_length) ]
            if absolutethresholdoption:
                thresholds = [absolute_threshold]
            else:
                thresholds = [a_threshold]
        
        return thresholds, helix_lengths
        

    def prepare_compute_rho_theta_cc_based_on_overlapping_tiles(self, micrograph_files, ref_power, ref, each_id, each_mic):
        each_mic, pixelsize, tilesize_bin = MicrographExam().bin_micrograph(each_mic, self.binoption, self.binfactor,
        self.ori_pixelsize, self.tile_size_A, self.tempdir)
        each_mic_name = micrograph_files[each_id]
        # Load and preprocess micrograph
        mic = EMData()
        mic.read_image(each_mic)
        mic.process_inplace('normalize')
        mic, size_y, size_x = self.preprocess_micrograph(mic, pixelsize)
        mic.process_inplace('normalize')
        # Define Gaussian Kernel to decrease information in tiles from center to corners
        gaussian_kernel = signal.gaussian(self.tilesize_pix, 1.41 * self.compute_step_size(self.tilesize_pix, self.tile_overlap))
        gaussian_kernel_2d = np.outer(gaussian_kernel, gaussian_kernel)
        # Generate overlapping image tiles
        img_stack, pw_stack, xy_center_grid = self.generate_stack_of_overlapping_images_powers(mic, self.tilesize_pix,
        self.tile_overlap, gaussian_kernel_2d)
        # Angle determination in Fourier space
        angles, peaks = self.orient_reference_power_with_overlapping_powers(pw_stack, ref_power, xy_center_grid)
        os.remove(pw_stack)
        # Shift determination in Real Space
        rhos, thetas, cross_corr = self.find_translations_by_cc(angles, xy_center_grid, img_stack, ref)
        os.remove(img_stack)

        return each_mic, rhos, thetas, cross_corr, xy_center_grid, pixelsize, each_mic_name, size_y, size_x, angles


    def treshold_and_clean_up_binary_map(self, pixelsize, overlap_cc, each_threshold):
        if self.absolutethresholdoption:
            binary, lamb, absolute_threshold, background_cutoff = self.perform_absolute_thresholding_of_ccmap(overlap_cc,
                                                                                              each_threshold)
        else:
            binary, lamb, absolute_threshold, background_cutoff = self.perform_thresholding_of_ccmap(overlap_cc,
                                                                                                     each_threshold)

        # Some tweaking of the resulting binary 
        if binary.mean()>0.4: # if thresholding is very promiscous, whole map will be ones.
            binary=np.zeros_like(binary, dtype=bool) # this would lead to problems
        helix_radius = np.ceil(self.helixwidth / pixelsize / 2.0) // 2 * 2 + 1
        smoothing_radius = max(1,int(np.around((helix_radius / 4.0))))
        X, Y = [np.arange(-smoothing_radius, smoothing_radius + 1)] * 2
        disk_mask = X[:, None] ** 2 + Y ** 2 <= smoothing_radius ** 2

        binary_smoothed = ndimage.binary_dilation(binary, structure=disk_mask).astype(binary.dtype)

        # Skeletonize
        skel = self.bwmorph_thin(binary_smoothed)

        # Remove branch points
        skel_thick = self.get_rid_of_branchpoints_and_crossings(skel, self.helixwidth / pixelsize)
        skel_thick = self.mask_micrograph_edges(skel_thick, pixelsize)
        skel_thick = ndimage.binary_dilation(skel_thick)

        return skel_thick, binary, lamb, absolute_threshold, background_cutoff


    def compute_precision_and_recall_of_traces_with_respect_ground_truth(self, parameter_info, ground_truth_info,
    each_mic_name, size_y, size_x, each_threshold, each_min_helix_length, helices):
        helices_ground_truth = [i.coordinates for i in ground_truth_info \
                                if os.path.splitext(i.micrograph)[0] == os.path.splitext(each_mic_name)[0]]

        helices_ground_truth = [np.array(i) * self.ori_pixelsize for i in helices_ground_truth]
        helices_traced = [(np.array(i).T + 0.5) * self.binfactor * self.ori_pixelsize for i in helices]

        statistics = MicHelixTraceSupport().compare_interactively_traced_with_ground_truth(helices_ground_truth, 
            helices_traced, size_y * self.binfactor, size_x * self.binfactor, self.ori_pixelsize, self.helixwidth)

        parameter_info.append([each_mic_name, each_min_helix_length, each_threshold] + statistics)
    
        return parameter_info


    def update_plot_info_and_helix_info_for_each_micrograph(self, ref, helix_info, plot_info, each_mic, each_outfile,
    rhos, cross_corr, xy_center_grid, pixelsize, each_mic_name, angles, overlap_cc, skel_thick, binary, lamb,
                                                            absolute_threshold, background_cutoff, helices):
        pers_lengths = self.compute_persistence_length(helices, pixelsize)
        mic = EMData()

        plot_info.append([each_mic, each_outfile, overlap_cc, binary, helices, mic, ref, cross_corr, rhos, angles,
                            xy_center_grid, lamb, absolute_threshold, background_cutoff, skel_thick,
                            pers_lengths, self.feature_set,   self.a_threshold])

        helix_info = self.write_helixinfo(helix_info, helices, each_mic_name, self.tilesize_pix, self.ori_pixelsize,
        self.helixwidth)

        return helix_info, plot_info


    def trace_helices_in_micrographs(self, micrograph_files, outfiles):
        ref_power, self.tilesize_pix, ref = self.prepare_power_from_reference(self.reference_file)

        thresholds, helix_lengths = self.define_thresholds_and_minimum_helix_lengths(self.parametersearch_option,
        self.a_threshold, self.min_helix_length, self.max_helix_length, self.absolutethresholdoption,
        self.absolute_threshold)

        if self.parametersearch_option or self.compute_stat:
            tracing_results_mic = []
            ground_truth_info = self.get_interactively_traced_helices_to_compare()
        if not self.parametersearch_option:
            helix_info = []
            plot_info = []

        for each_id, (each_mic, each_outfile) in enumerate(zip(micrograph_files, outfiles)):
            each_mic, rhos, thetas, cross_corr, xy_center_grid, pixelsize, each_mic_name, size_y, size_x, angles = \
            self.prepare_compute_rho_theta_cc_based_on_overlapping_tiles(micrograph_files, ref_power, ref, each_id,
            each_mic)
            
            if self.parametersearch_option:
                os.remove(each_mic)

            # Construct CC Image by projecting lines into an image using rho and theta
            overlap_cc = self.build_cc_image_of_helices(rhos, thetas, cross_corr, xy_center_grid,
                                                        size_x, size_y, self.tilesize_pix, self.tile_overlap)
            
            # Looping over parameter 1
            for each_threshold in thresholds:
                # Threshold overlap_cc image
                skel_thick, binary, lamb, absolute_threshold, background_cutoff = \
                    self.treshold_and_clean_up_binary_map(pixelsize, overlap_cc, each_threshold)
                # Looping over Parameter 2
                for each_min_helix_length, each_max_helix_length in helix_lengths:
#                     print(each_threshold, each_min_helix_length)
                    # Find helices in binary image
                    helices = self.perform_connected_component_analysis(skel_thick, pixelsize,
                                                                    self.order_fit, each_min_helix_length,
                                                                    each_max_helix_length)
                    
                    if self.parametersearch_option or self.compute_stat:
                        tracing_results_mic = self.compute_precision_and_recall_of_traces_with_respect_ground_truth(tracing_results_mic,
                        ground_truth_info, each_mic_name, size_y, size_x, each_threshold, each_min_helix_length, helices)
                        
            if not self.parametersearch_option:
                helix_info, plot_info = self.update_plot_info_and_helix_info_for_each_micrograph(ref, helix_info,
                plot_info, each_mic, each_outfile, rhos, cross_corr, xy_center_grid, pixelsize, each_mic_name, angles,
                overlap_cc, skel_thick, binary, lamb, absolute_threshold, background_cutoff, helices)

        if self.parametersearch_option:
            return tracing_results_mic
        else:
            if self.compute_stat:
                return tracing_results_mic, helix_info, plot_info
            elif not self.compute_stat:
                return helix_info, plot_info


    def write_out_determined_tracing_criteria_in_database(self, trcng_results_comb):
        grid_session = SpringDataBase().setup_sqlite_db(grid_base, 'trace_grid.db')

        lengths = [each_result.min_length for each_result in trcng_results_comb]
        thresholds = [each_result.threshold for each_result in trcng_results_comb]
        if len(lengths) > 1:
            primary_range = (float(min(lengths)), float(max(lengths)))
            primary_inc = np.max(np.unique(np.diff(np.sort(np.unique(lengths)))))
    
            secondary_range = (float(min(thresholds)), float(max(thresholds)))
            second_inc = np.max(np.unique(np.diff(np.sort(np.unique(thresholds)))))
            
            grid_run = SegClassReconstruct().enter_starting_parameters_of_grid_search('min_helix_length', 'threshold', 
            primary_range, primary_inc, secondary_range, second_inc)
            
            grid_run.completed_grid_id = len(trcng_results_comb)
            grid_session.add(grid_run)

        for each_trcng_result in trcng_results_comb:
            grid_cycle = GridRefineTable()
            rundir_name = os.path.abspath(os.curdir)
            grid_cycle.dirname = rundir_name
            grid_cycle.primary_value = each_trcng_result.min_length
            grid_cycle.secondary_value = each_trcng_result.threshold
            grid_cycle.precision = each_trcng_result.precision
            grid_cycle.recall = each_trcng_result.recall
            grid_cycle.f1_measure = each_trcng_result.f1_measure
            grid_cycle.f05_measure = each_trcng_result.f05_measure
            grid_session.add(grid_cycle)

        grid_session.commit()


    def enter_helixinfo_into_springdb(self, helix_info):
        s = Segment()
        s.pixelsize = self.ori_pixelsize
        s.stepsize = self.boxfile_coordinatestep
        s.averaging_option = False
        s.ctfcorrect_option = False
        s.segsizepix = int(self.tile_size_A / self.ori_pixelsize)

        session = SpringDataBase().setup_sqlite_db(base)
        session = s.enter_helix_info_into_segments_and_helix_tables(helix_info, session)


    def correct_coordinates_and_visualize_traces(self, plot_info, coordinates):
        mhts = MicHelixTraceSupport()
        for i, each_pi in enumerate(plot_info):
            each_coordinates = [np.array(each_h[1]).T / float(self.binfactor) for each_h in coordinates \
                                if each_h[0] == self.micrograph_files[i]]

            each_pi_corrected = each_pi[0:4] + [each_coordinates] + each_pi[5:]
            mhts.visualize_traces_in_diagnostic_plot(*each_pi_corrected)

            if self.binoption:
                os.remove(each_pi[0]) #delete micrograph after plotting


    def trace_helices(self):
        if len(self.micrograph_files) < self.cpu_count:
            self.cpu_count = len(self.micrograph_files)
            self.feature_set.parameters['Number of CPUs'] = self.cpu_count
        OpenMpi().setup_and_start_mpi_version_if_demanded(self.mpi_option, self.feature_set, self.cpu_count)
        self.tempdir = Temporary().mktmpdir(self.temppath)

        outfiles = Features().rename_series_of_output_files(self.micrograph_files, self.outfile)

        if self.parametersearch_option:
            tracing_results_mic = self.trace_helices_in_micrographs(self.micrograph_files, outfiles)
            trcng_crit_comb = MicHelixTraceSupport().summarize_parameter_info_over_micrographs(tracing_results_mic)

            self.write_out_determined_tracing_criteria_in_database(trcng_crit_comb)
            self.generate_and_plot_parameter_search_summary(trcng_crit_comb, self.absolutethresholdoption)
        else:
            if self.compute_stat:
                tracing_results_mic, helix_info, plot_info = self.trace_helices_in_micrographs(self.micrograph_files, outfiles)
                trcng_crit_comb = MicHelixTraceSupport().summarize_parameter_info_over_micrographs(tracing_results_mic)

                self.write_out_determined_tracing_criteria_in_database(trcng_crit_comb)
            elif not self.compute_stat:
                helix_info, plot_info = self.trace_helices_in_micrographs(self.micrograph_files, outfiles)

            if len(helix_info) > 100: #at least 100 helices necessary
                helix_info = self.prune_helices_and_plot_persistence_length_summary(helix_info)
            self.write_boxfiles_from_helix_info(helix_info)
            self.enter_helixinfo_into_springdb(helix_info)
            coordinates = [[each_i.micrograph, each_i.coordinates] for each_i in helix_info]

            self.correct_coordinates_and_visualize_traces(plot_info, coordinates)

        os.rmdir(self.tempdir)
        self.log.endlog(self.feature_set)


def main():
    # Option handling
    parset = MicHelixTracePar()
    mergeparset = OptHandler(parset)

    ######## Program
    micrograph = MicHelixTrace(mergeparset)
    micrograph.trace_helices()


if __name__ == '__main__':
    main()
