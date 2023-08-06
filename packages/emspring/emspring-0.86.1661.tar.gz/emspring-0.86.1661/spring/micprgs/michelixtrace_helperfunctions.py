# Author: Carsten Sachse 
# with Stefan Huber (2017) 
# Copyright: EMBL (2010 - 2018)
# License: see license.txt for details
from EMAN2 import EMNumPy
import matplotlib
from matplotlib.mlab import griddata
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np

from spring.csinfrastr.csproductivity import DiagnosticPlot
from scipy import interpolate, ndimage, optimize, stats
from collections import namedtuple


class MicHelixTraceSupport(object):
    def roundint(self, arr):
            return np.rint(arr).astype(np.int)
            
            
    def interpolate_chain(self, chain, step_A=1):
        lenx, leny = np.abs(chain[-1] - chain[0])
        x, y = chain[:, 0], chain[:, 1]
        if lenx >= leny:
            f = interpolate.interp1d(x, y)
            x_new = np.arange(x.min()+step_A, x.max(), step_A)
            return np.vstack((x_new, f(x_new))).T
        else:
            f = interpolate.interp1d(y, x)
            y_new = np.arange(y.min()+step_A, y.max(), step_A)
            return np.vstack((f(y_new), y_new)).T
    
    
    def setup_boolean_grid(self, bundle, sizex_A, sizey_A, gridsize_A, chain_interpolation_A=1):
        gridsizex, gridsizey = sizex_A // gridsize_A + 1, sizey_A // gridsize_A + 1
        grid = np.zeros((gridsizey, gridsizex))
        for chain in bundle:
            chain = self.roundint(self.interpolate_chain(chain, chain_interpolation_A) / float(gridsize_A))
            chain = chain[chain[:, 1] < gridsizex]
            chain = chain[chain[:, 0] < gridsizey]
            grid[chain[:, 1], chain[:, 0]] = 1

        return grid
    
    
    def clean_boolean_grid(self, boolean_grid, gridsize_A, edge_clean=400, helix_ends_clean=True,
    helix_ends_clean_radius=100, helix_bundle=None, minimum_distance_helixends=150):
        """
        :param boolean_grid:
        :param gridsize_A:
        :param edge_clean: Are edges of the micrograph cleaned.
        :param helix_ends_clean: Clean helix ends out of boolean grid
        :param helix_ends_clean_radius: What radius to use for cleaning
        :param helix_bundle: Bundle of ground truth helices from helixboxer, used to find helix ends
        :param minimum_distance_helixends: Helix ends are just removed if above a minimum distance.
        Prevents discontinous helices from being removed.
        :return: copy of boolean_grid
        """
    
        boolean_grid = np.copy(boolean_grid)
    
        edge_clean_pixel = edge_clean // gridsize_A
    
    
        boolean_grid[0:edge_clean_pixel] = False
        boolean_grid[-edge_clean_pixel:] = False
        boolean_grid[:, 0:edge_clean_pixel] = False
        boolean_grid[:, -edge_clean_pixel:] = False
    
        if helix_ends_clean:
            helix_ends = np.vstack(([[i[0], i[-1]] for i in helix_bundle]))
            from scipy.spatial.distance import pdist, squareform
            helix_ends_distant = helix_ends[(squareform(pdist(helix_ends)) < minimum_distance_helixends).sum(0) == 1]
            for cx,cy in helix_ends_distant:
                cx, cy = self.roundint(cx/float(gridsize_A)), self.roundint(cy/float(gridsize_A))
                radius = self.roundint(helix_ends_clean_radius/float(gridsize_A))
                index = self.prepare_circular_mask(radius)
                clean_area = boolean_grid[cy - radius:cy + radius + 1, cx - radius:cx + radius + 1]
                if clean_area.shape == index.shape:
                    boolean_grid[cy - radius:cy + radius + 1, cx - radius:cx + radius + 1][index] = False
    
        return boolean_grid
    
    
    def prepare_circular_mask(self, size):
        X, Y = [np.arange(-size, size + 1)] * 2
        disk_mask = X[:, None] ** 2 + Y ** 2 <= size ** 2

        return disk_mask
    
    
    def inflate_binary(self, binary, size):
        disk_mask = self.prepare_circular_mask(size)
        binary_inflated = ndimage.binary_dilation(binary, structure=disk_mask).astype(binary.dtype)

        return binary_inflated
    

    def compute_precision_and_recall(self, grid_truth, grid_truth_inflate, grid_test, grid_test_inflate):
        """
        Recall is also called TPR or Sensitivity. Likelihood that a true helix is really found as a positive test outcome
        Precision is also called positive predictive value, Likelihood that positive test outcome is correct
        """
        P = grid_truth.sum()
        Test_Outcome_Positive = grid_test.sum()
    
        TP_recall = (grid_test_inflate * grid_truth).sum()  # Number of squares found when inflating result
        TP_precision = (grid_test * grid_truth_inflate).sum()  # Number of correctly found squares when inflating truth
    
        return [TP_recall, TP_precision, P, Test_Outcome_Positive]
        
    
    def compare_interactively_traced_with_ground_truth(self, helices_ground_truth, helices_traced, size_y, size_x,
    ori_pixelsize, helixwidth_A):
        sizex_A, sizey_A = self.roundint(np.array([size_x, size_y]) * ori_pixelsize)
        gridsize_A = 25
        radius_A = helixwidth_A / 2.0
        
        michelix = self.setup_boolean_grid(helices_traced, sizex_A, sizey_A, gridsize_A)
        michelix_inflate = self.inflate_binary(michelix, radius_A / gridsize_A)
    
        michelix_inflate_clean = self.clean_boolean_grid(michelix_inflate, gridsize_A, edge_clean=400, helix_ends_clean=True,
                                      helix_ends_clean_radius=radius_A*2,
                                      helix_bundle=helices_ground_truth)
    
        michelix_clean = self.clean_boolean_grid(michelix, gridsize_A, edge_clean=400, helix_ends_clean=True,
                                          helix_ends_clean_radius=radius_A*2,
                                          helix_bundle=helices_ground_truth)
    
        helixboxer = self.setup_boolean_grid(helices_ground_truth, sizex_A, sizey_A, gridsize_A)
        helixboxer_inflate = self.inflate_binary(helixboxer, radius_A / gridsize_A)
    
        helixboxer_inflate_clean = self.clean_boolean_grid(helixboxer_inflate, gridsize_A, edge_clean=400, helix_ends_clean=True,
                                        helix_ends_clean_radius=radius_A*2,
                                        helix_bundle=helices_ground_truth)
    
        helixboxer_clean = self.clean_boolean_grid(helixboxer, gridsize_A, edge_clean=400, helix_ends_clean=True,
                                        helix_ends_clean_radius=radius_A*2,
                                        helix_bundle=helices_ground_truth)
                #[TP_recall, TP_precision, P, Test_Outcome_Positive]
        P_R = self.compute_precision_and_recall(helixboxer_clean, helixboxer_inflate_clean, michelix_clean,
        michelix_inflate_clean)
    
        return P_R
                                        
    
    def summarize_parameter_info_over_micrographs_old(self, tracing_results_mic):
        """
        >>> from spring.micprgs.michelixtrace_helperfunctions import MicHelixTraceSupport
        >>> params = [['test_mic.hdf', 200, 0.5, 0.0, 0.0, 37.0, 157.0], ['test_mic.hdf', 400, 0.5, 0.0, 0.0, 37.0, 71.0], ['test_mic.hdf', 600, 0.5, 0.0, 0.0, 37.0, 71.0], ['test_mic.hdf', 900, 0.5, 0.0, 0.0, 37.0, 0.0], ['test_mic.hdf', 200, 0.01, 0.0, 0.0, 37.0, 317.0], ['test_mic.hdf', 400, 0.01, 0.0, 0.0, 37.0, 334.0], ['test_mic.hdf', 600, 0.01, 0.0, 0.0, 37.0, 281.0], ['test_mic.hdf', 900, 0.01, 0.0, 0.0, 37.0, 196.0], ['test_mic.hdf', 200, 0.001, 0.0, 0.0, 37.0, 293.0], ['test_mic.hdf', 400, 0.001, 0.0, 0.0, 37.0, 313.0], ['test_mic.hdf', 600, 0.001, 0.0, 0.0, 37.0, 290.0], ['test_mic.hdf', 900, 0.001, 0.0, 0.0, 37.0, 227.0], ['test_mic.hdf', 200, 1e-05, 0.0, 0.0, 37.0, 212.0], ['test_mic.hdf', 400, 1e-05, 0.0, 0.0, 37.0, 226.0], ['test_mic.hdf', 600, 1e-05, 0.0, 0.0, 37.0, 174.0], ['test_mic.hdf', 900, 1e-05, 0.0, 0.0, 37.0, 38.0]]
        >>> MicHelixTraceSupport().summarize_parameter_info_over_micrographs_old(params)
        array([[  2.00000000e+02,   1.00000000e-05,   0.00000000e+00,
                  0.00000000e+00],
               [  2.00000000e+02,   1.00000000e-03,   0.00000000e+00,
                  0.00000000e+00],
               [  2.00000000e+02,   1.00000000e-02,   0.00000000e+00,
                  0.00000000e+00],
               [  2.00000000e+02,   5.00000000e-01,   0.00000000e+00,
                  0.00000000e+00],
               [  4.00000000e+02,   1.00000000e-05,   0.00000000e+00,
                  0.00000000e+00],
               [  4.00000000e+02,   1.00000000e-03,   0.00000000e+00,
                  0.00000000e+00],
               [  4.00000000e+02,   1.00000000e-02,   0.00000000e+00,
                  0.00000000e+00],
               [  4.00000000e+02,   5.00000000e-01,   0.00000000e+00,
                  0.00000000e+00],
               [  6.00000000e+02,   1.00000000e-05,   0.00000000e+00,
                  0.00000000e+00],
               [  6.00000000e+02,   1.00000000e-03,   0.00000000e+00,
                  0.00000000e+00],
               [  6.00000000e+02,   1.00000000e-02,   0.00000000e+00,
                  0.00000000e+00],
               [  6.00000000e+02,   5.00000000e-01,   0.00000000e+00,
                  0.00000000e+00],
               [  9.00000000e+02,   1.00000000e-05,   0.00000000e+00,
                  0.00000000e+00],
               [  9.00000000e+02,   1.00000000e-03,   0.00000000e+00,
                  0.00000000e+00],
               [  9.00000000e+02,   1.00000000e-02,   0.00000000e+00,
                  0.00000000e+00],
               [  9.00000000e+02,   5.00000000e-01,   0.00000000e+00,
                             nan]])
    
        """
        # Content is: [micrograph_name, each_min_helix_length, alpha each_threshold, TP_recall, TP_precision, P, Test_outcome_positive]
        tracing_results_mic = np.stack(tracing_results_mic)
    
        tracing_results_mic[:,0] = 0
        tracing_results_mic = tracing_results_mic.astype(np.float)
        min_helix_lengths = np.unique(tracing_results_mic[:,1])
        thresholds = np.unique(tracing_results_mic[:,2])
        tracing_criteria_comb = []
        for each_min_helix_length in min_helix_lengths:
            for each_threshold in thresholds:
                summary_all_micrographs = tracing_results_mic[
                    (tracing_results_mic[:,1]==each_min_helix_length) & 
                    (tracing_results_mic[:,2]==each_threshold)].sum(0)
                    
                summary_recall = summary_all_micrographs[3] / summary_all_micrographs[5]
                summary_precision = summary_all_micrographs[4] / summary_all_micrographs[6]
                tracing_criteria_comb.append([each_min_helix_length, each_threshold, summary_recall, summary_precision])
    
        return np.array(tracing_criteria_comb) #[each_min_helix_length, each_threshold, summary_recall, summary_precision]
        
        
    def summarize_parameter_info_over_micrographs(self, tracing_results_mic):
        """
        >>> from spring.micprgs.michelixtrace_helperfunctions import MicHelixTraceSupport
        >>> params = [['test_mic.hdf', 200, 0.5, 0.0, 0.0, 37.0, 157.0], ['test_mic.hdf', 400, 0.5, 0.0, 0.0, 37.0, 71.0], ['test_mic.hdf', 600, 0.5, 0.0, 0.0, 37.0, 71.0], ['test_mic.hdf', 900, 0.5, 0.0, 0.0, 37.0, 0.0], ['test_mic.hdf', 200, 0.01, 0.0, 0.0, 37.0, 317.0], ['test_mic.hdf', 400, 0.01, 0.0, 0.0, 37.0, 334.0], ['test_mic.hdf', 600, 0.01, 0.0, 0.0, 37.0, 281.0], ['test_mic.hdf', 900, 0.01, 0.0, 0.0, 37.0, 196.0], ['test_mic.hdf', 200, 0.001, 0.0, 0.0, 37.0, 293.0], ['test_mic.hdf', 400, 0.001, 0.0, 0.0, 37.0, 313.0], ['test_mic.hdf', 600, 0.001, 0.0, 0.0, 37.0, 290.0], ['test_mic.hdf', 900, 0.001, 0.0, 0.0, 37.0, 227.0], ['test_mic.hdf', 200, 1e-05, 0.0, 0.0, 37.0, 212.0], ['test_mic.hdf', 400, 1e-05, 0.0, 0.0, 37.0, 226.0], ['test_mic.hdf', 600, 1e-05, 0.0, 0.0, 37.0, 174.0], ['test_mic.hdf', 900, 1e-05, 0.0, 0.0, 37.0, 38.0]]
        >>> crit = MicHelixTraceSupport().summarize_parameter_info_over_micrographs(params)
        >>> np.array(crit)
        array([[  2.00000000e+02,   1.00000000e-05,   0.00000000e+00,
                  0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
               [  2.00000000e+02,   1.00000000e-03,   0.00000000e+00,
                  0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
               [  2.00000000e+02,   1.00000000e-02,   0.00000000e+00,
                  0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
               [  2.00000000e+02,   5.00000000e-01,   0.00000000e+00,
                  0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
               [  4.00000000e+02,   1.00000000e-05,   0.00000000e+00,
                  0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
               [  4.00000000e+02,   1.00000000e-03,   0.00000000e+00,
                  0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
               [  4.00000000e+02,   1.00000000e-02,   0.00000000e+00,
                  0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
               [  4.00000000e+02,   5.00000000e-01,   0.00000000e+00,
                  0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
               [  6.00000000e+02,   1.00000000e-05,   0.00000000e+00,
                  0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
               [  6.00000000e+02,   1.00000000e-03,   0.00000000e+00,
                  0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
               [  6.00000000e+02,   1.00000000e-02,   0.00000000e+00,
                  0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
               [  6.00000000e+02,   5.00000000e-01,   0.00000000e+00,
                  0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
               [  9.00000000e+02,   1.00000000e-05,   0.00000000e+00,
                  0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
               [  9.00000000e+02,   1.00000000e-03,   0.00000000e+00,
                  0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
               [  9.00000000e+02,   1.00000000e-02,   0.00000000e+00,
                  0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
               [  9.00000000e+02,   5.00000000e-01,   0.00000000e+00,
                  0.00000000e+00,   0.00000000e+00,   0.00000000e+00]])

        """
        # Content is: 
        #[micrograph_name, each_min_helix_length, alpha each_threshold, TP_recall, TP_precision, P, Test_outcome_positive]
        tracing_results_mic = np.stack(tracing_results_mic)
    
        tracing_results_mic[:,0] = 0
        tracing_results_mic = tracing_results_mic.astype(np.float)
        min_helix_lengths = np.unique(tracing_results_mic[:,1])
        thresholds = np.unique(tracing_results_mic[:,2])
        tracing_criteria_comb = []
        criteria_tuple = namedtuple('criteria', 'min_length threshold recall precision f1_measure f05_measure')
        for each_min_helix_length in min_helix_lengths:
            for each_threshold in thresholds:
                summary_all_micrographs = tracing_results_mic[
                    (tracing_results_mic[:,1]==each_min_helix_length) & 
                    (tracing_results_mic[:,2]==each_threshold)].sum(0)
                    
                if summary_all_micrographs[5] > 0:
                    recall = summary_all_micrographs[3] / summary_all_micrographs[5]
                else:
                    recall = 0.0

                if summary_all_micrographs[6] > 0:
                    precision = summary_all_micrographs[4] / summary_all_micrographs[6]
                else:
                    precision = 0.0

                f1_score = self.compute_fscore_b(1 / 1.0, precision, recall)
                f05_score = self.compute_fscore_b(1 / 2.0, precision, recall)
                tracing_criteria_comb.append(
                    criteria_tuple(each_min_helix_length, each_threshold, recall, precision, f1_score, f05_score))
    
        return tracing_criteria_comb
        
        
    def interpolate_parameter_space(self, trcng_crit_comb):
        alphas = np.array([each_trcng_result.threshold for each_trcng_result in trcng_crit_comb])
        mincut = np.array([each_trcng_result.min_length for each_trcng_result in trcng_crit_comb])

        x = np.unique(alphas)
        y = np.unique(mincut)
    
        recalls = np.array([each_trcng_result.recall for each_trcng_result in trcng_crit_comb])
        precisions = np.array([each_trcng_result.precision for each_trcng_result in trcng_crit_comb])
        
        xi = np.logspace(np.log10(x.min()), np.log10(x.max()), 70)
        yi = np.linspace(y.min(), y.max(), 70)
        zi_precisions = griddata(alphas, mincut, precisions, xi, yi, interp='linear')
        zi_recalls = griddata(alphas, mincut, recalls, xi, yi, interp='linear')
    
        return xi, yi, zi_precisions, zi_recalls
    
        
    def compute_fscore_b_old(self, beta, prec, recall):
        fscore = (1+beta**2) * prec * recall / (beta**2*prec+recall)
        fscore[np.isinf(fscore)] = 0
    
        return np.nan_to_num(fscore)


    def compute_fscore_b(self, beta, prec, recall):
        """
        >>> from spring.micprgs.michelixtrace_helperfunctions import MicHelixTraceSupport
        >>> MicHelixTraceSupport().compute_fscore_b(1/2.0, 1, 0)
        0.0
        >>> MicHelixTraceSupport().compute_fscore_b(1/2.0, 0, 1)
        0.0
        >>> MicHelixTraceSupport().compute_fscore_b(1/2.0, 1, 1)
        1.0
        >>> MicHelixTraceSupport().compute_fscore_b(1/2.0, 0.25, 0.75)
        0.28846153846153844
        >>> MicHelixTraceSupport().compute_fscore_b(1/2.0, 0, 0)
        0.0
        >>> a = np.zeros(10)
        >>> a[0] = 1.0
        >>> MicHelixTraceSupport().compute_fscore_b(1/2.0, a, a)
        array([ 1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.])
        """
        if np.isscalar(prec) and prec + recall == 0:
            fscore = 0.0
        else:
            fscore = (1  + beta**2) * prec * recall / (beta**2 * prec + recall)

        if not np.isscalar(fscore):
            fscore = np.nan_to_num(fscore)
    
        return fscore

    
    def plot_parameter_search_summary(self, xi, yi, zi_precisions, zi_recalls, absolutethresholdoption):
        matplotlib.rcParams.update({'font.size': 10})
        contour_fontsize = 8
    
        fig, [[ax1,ax2],[ax3,ax4]] = plt.subplots(2,2, figsize=(7,7))
    
        def plot_parameter_contour(ax, xi, yi, zi, cont_font, title):
            ax.pcolormesh(xi, yi, zi, cmap = plt.get_cmap('rainbow'))
            CS = ax.contour(xi, yi, zi, colors = 'k')
            ax.clabel(CS, inline=1, fontsize=cont_font)
            ax.set_title(title)
            ax.set_xscale("log") 
            if absolutethresholdoption:
                ax.set_xlabel('Absolute CC threshold')
            else:
                ax.set_xlabel('Alpha threshold (Adaptive)')
            ax.set_ylabel('Minimum Helix Cutoff')
    
        plot_parameter_contour(ax1, xi, yi, zi_precisions, contour_fontsize, 'Precision')
        plot_parameter_contour(ax2, xi, yi, zi_recalls, contour_fontsize, 'Recall')        
    
        beta = 1/2.0
        fscore = self.compute_fscore_b(beta, zi_precisions, zi_recalls)
        plot_parameter_contour(ax3, xi, yi, fscore.data, contour_fontsize, 'F%.2f Measure'%(beta)) 
        maxidx = np.unravel_index(fscore.argmax(), fscore.shape)
        max_x, max_y = xi[maxidx[1]], yi[maxidx[0]]
        prec, rec = zi_precisions[maxidx[0], maxidx[1]], zi_recalls[maxidx[0], maxidx[1]]
        ax3.scatter(max_x, max_y, color='white', edgecolor='k', s=50, 
                    label='%.3g, %.0f\nPrecision %.2g\nRecall %.2g'%(max_x, max_y, prec, rec))
        ax3.legend(fontsize=7)
    
        beta = 1/1.0
        fscore = self.compute_fscore_b(beta, zi_precisions, zi_recalls)
        plot_parameter_contour(ax4, xi, yi, fscore.data, contour_fontsize, 'F%.2f Measure'%(beta)) 
        maxidx = np.unravel_index(fscore.argmax(), fscore.shape)
        max_x, max_y = xi[maxidx[1]], yi[maxidx[0]]
        prec, rec = zi_precisions[maxidx[0], maxidx[1]], zi_recalls[maxidx[0], maxidx[1]]
        ax4.scatter(max_x, max_y, color='white', edgecolor='k', s=50, 
                    label='%.3g, %.0f\nPrecision %.2g\nRecall %.2g'%(max_x, max_y, prec, rec))
        ax4.legend()
        ax4.legend(fontsize=7)
        
        for ax in [ax1,ax2,ax3,ax4]:
            ax.set_xlim(xi.min(), xi.max())
            ax.set_ylim(yi.min(), yi.max())
        
        fig.tight_layout()
        fig.savefig('ParameterSpace.pdf')
        
        return max_x, max_y #pair of (best threshold, best min_helix_length) is returned
    
    
    def compute_persistence_length_from_tangent_vector_correlation(self, bundle):
        """Bundle is a list of 'chains' - shape (n,2) arrays, where n can differ between the arrays.
           Length of segments is allowed to be different within a chain and between chains"""
        correlations = []
        distances = []
        for chain in bundle:
            tangent_vecs = chain[1:] - chain[:-1]
            unit_tangent_vecs = tangent_vecs / np.sqrt(np.sum(tangent_vecs ** 2, 1))[:, None]
            segment_dist_matrix = self.compute_segment_dist_matrix(chain)
            correlation = np.inner(unit_tangent_vecs, unit_tangent_vecs)
            correlations.extend(correlation.flatten().tolist())
            distances.extend(segment_dist_matrix.flatten().tolist())
    
        correlations = np.array(correlations)
        distances = np.array(distances)
    
        bins = np.linspace(distances[distances!=0].min()*2.0, np.percentile(distances, 70), 20)
    
        bin_means, bin_edges, binnumber = stats.binned_statistic(distances, correlations, statistic = 'mean',
                                                                 bins = bins)
        bin_stds,  bin_edges, binnumber = stats.binned_statistic(distances, correlations, statistic = 'std',
                                                                 bins = bins)
        bin_stds /= np.sqrt(np.bincount(binnumber)[0:len(bin_stds)])
        bin_width = (bin_edges[1] - bin_edges[0])
        bin_centers = bin_edges[1:] - bin_width / 2
    
        def expon(reclamb, x):
            return np.exp(-reclamb*x) #reclamb symbolises 1/lamb
    
        # Interpolate possible nan values
        nan_values = np.isnan(bin_means)
        bin_means[nan_values] = np.interp(np.flatnonzero(nan_values), np.flatnonzero(~nan_values), bin_means[~nan_values])

        # Curve fit
        reclamb, dreclamb = optimize.curve_fit(expon, bin_centers, bin_means, p0=0.001, sigma=None, absolute_sigma=False)
        lamb = 1/reclamb[0]
    
        # Error propagation, relative error of reclam is also relative error of lamb
        dlamb = np.sqrt(dreclamb[0,0])/reclamb[0]*lamb
    
        return distances, correlations, bin_centers, bin_means, bin_stds, lamb, dlamb
    
    
    def compute_segment_dist_matrix(self, chain):
        n_segments = len(chain) - 1
    
        segment_mids = (chain[1:] + chain[:-1]) / 2.0
        segment_mids_vectors = segment_mids[1:] - segment_mids[:-1]
        segment_distances = np.sqrt(np.sum(segment_mids_vectors ** 2, 1))
        segment_distances_cumulated = np.hstack((0, np.cumsum(segment_distances)))
    
        segment_dist_matrix = np.zeros((n_segments, n_segments))
        for i in range(n_segments):
            jump_distances = (segment_distances_cumulated[i + 1:] - segment_distances_cumulated[0:-i - 1])
            rgn = np.arange(len(jump_distances))
            segment_dist_matrix[rgn, rgn + 1 + i] = jump_distances
    
        segment_dist_matrix += segment_dist_matrix.T
    
        return segment_dist_matrix
    
    
    def compute_mad(self, data):
        return 1.4826 * np.mean(np.absolute(data - np.mean(data)))
    
    def plot_pers_length_summary(self, bundle, pl_exact, dpl_exact, pl_list, distances, correlations, bin_centers,
                                 bin_means, bin_stds, pruning_cutoff, plotfile):
        pl_list = pl_list[~np.isnan(pl_list)]
        fig, axarr = plt.subplots(2, 2, figsize=(11.69, 8.27))
    
        ex = [0, np.percentile(distances, 95), np.percentile(correlations, 3),  1]
        hexplot = axarr[1, 0].hexbin(distances, correlations, gridsize=20, cmap='gist_heat_r', extent=ex,
            norm=matplotlib.colors.LogNorm()) #, bins='log'
        axarr[1, 0].scatter(bin_centers, bin_means, s=5, color='green', label='Binned mean')
        axarr[1, 0].legend(fontsize=12)
        axarr[1, 0].set_xlabel('Polymer Length [Angstrom]')
        axarr[1, 0].set_ylabel('dot product of tangent vectors')
        axarr[1, 0].set_xlim(ex[0:2])
        axarr[1, 0].set_ylim(ex[2:])
        plt.colorbar(hexplot,ax=axarr[1, 0], label='Histogram Count')
        axarr[1, 0].get_yaxis().get_major_formatter().set_useOffset(False)
    
        bins = 10 ** np.linspace(np.log10(pl_list.min() / 10000.0), np.log10(pl_list.max() / 10000.0), 50)
        n, bins, patches = axarr[0, 1].hist(pl_list / 10000.0, color='darkolivegreen', bins=bins)
        axarr[0, 1].set_xlabel('Persistence Length [um]')
        axarr[0, 1].set_ylabel('# of helices')
    
        median = np.median(pl_list)
        axarr[0, 1].axvline(median/10000.0, color='blue', label='Distribution median = %.3g um' % (median/10000.0))
        axarr[0, 1].axvline(np.exp(np.log(median) + self.compute_mad(np.log(pl_list)))/10000.0, color='blue', linestyle='dotted',
                            label='Median Absolute Deviation ~ 1 StdDev')
        axarr[0, 1].axvline(np.exp(np.log(median) - self.compute_mad(np.log(pl_list)))/10000.0, color='blue', linestyle='dotted')
        pruning_cutoff_absolute = np.exp(np.log(median) - float(pruning_cutoff)*self.compute_mad(np.log(pl_list)))/ 10000.0
        axarr[0, 1].axvline(pruning_cutoff_absolute, color='orangered',
                            linestyle='-.', label='Persistence Length Cutoff %.3g um'%pruning_cutoff_absolute)
        axarr[0, 1].legend(fontsize=9)
        axarr[0, 1].set_title('Persistence Length Measure per Helix')
        axarr[0, 1].set_xscale("log")
        for b, p in zip(bins, patches):
            if b < pruning_cutoff_absolute:
                plt.setp(p, 'facecolor', 'red')
    
    #     bin_width = bin_centers[1] - bin_centers[0]
    #     bin_left = bin_centers - bin_width/2.0
        bin_centers_zero = np.hstack(([0], bin_centers))
        bin_means_zero = np.hstack(([1], bin_means))
        bin_stds_zero = np.hstack(([0], bin_stds))
        np.savetxt('TangentVectorDotProduct.txt', np.column_stack((bin_centers_zero, bin_means_zero, bin_stds_zero)),
                   header = 'Polymer Length\tCorrelation\tCorr Std\tPL=%.5f'%pl_exact, delimiter='\t')
        axarr[1, 1].errorbar(bin_centers_zero, bin_means_zero, label='Real Data\nbinned mean and se', color='darkolivegreen', yerr=bin_stds_zero)
        axarr[1, 1].plot(bin_centers_zero, np.exp(-1 / pl_exact * bin_centers_zero),
                         label='Exponential Fit\nLambda = \n(%.3g +- %.2g) um' % (pl_exact / 10000.0, dpl_exact / 10000.0),
                         color='black', linestyle='dotted')
        axarr[1, 1].set_ylim(ex[2:])
        axarr[1, 1].set_xlabel('Polymer Length [Angstrom]')
        axarr[1, 1].set_ylabel('dot product of tangent vectors')
        axarr[1, 1].legend(fontsize=12, loc=3)
        axarr[1, 1].get_yaxis().get_major_formatter().set_useOffset(False)
    
        colormap = plt.get_cmap('autumn')
        colormap.set_under(color='black')
        vmax, vmin = pl_list.max()/10000.0, pruning_cutoff_absolute
        norm = matplotlib.colors.LogNorm(vmin, vmax)
        sm = plt.cm.ScalarMappable(cmap=colormap, norm=norm)
        sm._A = []
        if len(bundle) > 300:
            for i in np.random.choice(len(bundle), 300):
                lineplot = axarr[0, 0].plot(*bundle[i].T, color=colormap(norm(pl_list[i]/10000)))
        else:
            for i, chain in enumerate(bundle):
                lineplot = axarr[0, 0].plot(*chain.T, color=colormap(norm(pl_list[i]/10000)))
        axarr[0, 0].set_xlabel('x [Angstrom]')
        axarr[0, 0].set_ylabel('y [Angstrom]')
        axarr[0, 0].set_title('300 random helix traces (black: too curved)')
        axarr[0, 0].set_aspect('equal', adjustable='box')
        axarr[0, 0].tick_params(axis='both', which='major', labelsize=8)
        if vmax>vmin:
            plt.colorbar(sm, ax=axarr[0, 0], label='Persistence Length Measure [um]')
    
        fig.tight_layout()
        fig.savefig(plotfile)
    
        return pruning_cutoff_absolute
    
    
    def remove_ticks_and_scale_correctly(self, ax, mic_np):
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim([0, mic_np.shape[1]])
        ax.set_ylim([0, mic_np.shape[0]])
    
        return ax
    
    
    def visualize_traces_in_diagnostic_plot_verbose(self, infile, outfile, overlap_cc, binary, helices, mic, ref,
                                                    cross_corr, rho, angles, peaks, xy_center_grid, fitfunct,
                                                    fitparams, skel, pers_lengths, feature_set, a_threshold):
        mic.read_image(infile)
        mic_np = np.copy(EMNumPy.em2numpy(mic))
    
        michelixtrace_plot = DiagnosticPlot()
        fig = michelixtrace_plot.add_header_and_footer(feature_set, infile, outfile)
    
        ax1 = michelixtrace_plot.plt.subplot2grid((2, 5), (0, 0), colspan=1, rowspan=1)  # Overl_CC
        ax2 = michelixtrace_plot.plt.subplot2grid((2, 5), (1, 0), colspan=1, rowspan=1)  # Binary CC
        ax2_hist = michelixtrace_plot.plt.subplot2grid((2, 5), (0, 1), colspan=1, rowspan=1)  # Overl_CC Hist
        ax2_hist_trans = michelixtrace_plot.plt.subplot2grid((2, 5), (1, 1), colspan=1, rowspan=1)  # Overl_CC Hist
        ax3 = michelixtrace_plot.plt.subplot2grid((2, 5), (0, 2), colspan=1, rowspan=1)  # Micrograph with helices
        ax4 = michelixtrace_plot.plt.subplot2grid((2, 5), (1, 2), colspan=1, rowspan=1)  # Reference Helix
        ax5 = michelixtrace_plot.plt.subplot2grid((2, 5), (0, 3), colspan=1, rowspan=1)  # 2DCC
        ax6 = michelixtrace_plot.plt.subplot2grid((2, 5), (1, 3), colspan=1, rowspan=1)  # Reconstruction Vectors
        ax7 = michelixtrace_plot.plt.subplot2grid((2, 5), (0, 4), colspan=1, rowspan=1)  # Helix Angles + AngleCC
        ax8 = michelixtrace_plot.plt.subplot2grid((2, 5), (1, 4), colspan=1, rowspan=1)  # 2DCC
    
        cc_im = ax1.imshow(overlap_cc, cmap='jet', origin='lower', interpolation='nearest')
        ax1 = self.remove_ticks_and_scale_correctly(ax1, mic_np)
        ax1.set_title('Overlapping Cross Correlation %sx%s' % overlap_cc.shape, fontsize=4)
        cax = fig.add_axes([0.005, 0.65, 0.01, 0.20])
        cbar = fig.colorbar(cc_im, cax)
        for t in cbar.ax.get_yticklabels():
            t.set_fontsize(4)
    
        ax2.set_title('Thresholded at alpha-value of {0}'.format(a_threshold), fontsize=4)
        bin_mask = np.ma.masked_where(binary < 0.5, -1 * binary)
        ax2.imshow(bin_mask, cmap='gray', origin='lower', interpolation='nearest')
        ax2 = self.remove_ticks_and_scale_correctly(ax2, mic_np)
        skel_mask = np.ma.masked_where(skel < 0.5, -1 * skel)
        ax2.imshow(skel_mask, cmap='autumn', origin='lower', interpolation='nearest')
    
        ax2_hist.set_title('Overlapping Cross Correlation Histogram', fontsize=4)
        ax2_hist.set_yscale('log', basey=10)
        n, bins, patches = ax2_hist.hist(overlap_cc[overlap_cc > cutoff].flatten(), 100, facecolor='green',
                                         linewidth=0.5, normed=True, log=True)
        ax2_hist.tick_params(axis='both', which='major', labelsize=4)
        x = np.linspace(overlap_cc.min(), overlap_cc.max(), 500)
        ax2_hist.plot(x, fitfunct.pdf(x, *fitparams), color='red')  # 1/float(bins[1]-bins[0]) *
        ax2_hist.set_ylim((10e-4, 1 / float(bins[1] - bins[0])))
    
        ax2_hist_trans.set_title('Overlapping Cross Correlation Histogram', fontsize=4)
        n, bins, patches = ax2_hist_trans.hist(overlap_cc[overlap_cc > cutoff].flatten(), 100, facecolor='green',
                                               linewidth=0.5, normed=True)
        ax2_hist_trans.tick_params(axis='both', which='major', labelsize=4)
        x = np.linspace(overlap_cc.min(), overlap_cc.max(), 500)
        ax2_hist_trans.plot(x, fitfunct.pdf(x, *fitparams), color='red')  # 1/float(bins[1]-bins[0]) *
        ax2_hist_trans.set_ylim((0, 1 / float(bins[1] - bins[0]) / 40.))
    
        ax3.imshow(mic_np, cmap='gray', origin='lower', interpolation='nearest')
        ax3.set_title('Micrograph with detected helices %sx%s' % mic_np.shape, fontsize=4)
        colors = plt.cm.rainbow(np.linspace(0, 1, len(helices)))[:, 0:3] / 2.0
        font = {'weight': 'bold', 'size': 3}
        for pers, c, (each_xcoord, each_ycoord) in zip(pers_lengths, colors, helices):
            ax3.plot(each_xcoord, each_ycoord, 'o', markersize=0.6, alpha=1, markeredgewidth=0.0, color=c)
            c_dark = c / 1.5
            xmean, ymean = each_xcoord.mean(), each_ycoord.mean()
            ax3.text(xmean, (ymean + each_ycoord.max()) / 2.0, "%.1f" % pers, color=c_dark, fontdict=font)
    
        ax3 = self.remove_ticks_and_scale_correctly(ax3, mic_np)
    
        ax4.imshow(ref, cmap='gray', origin='lower', interpolation='nearest')
        ax4.set_aspect('equal')
        ax4.set_title('Reference Helix', fontsize=4)
        ax4 = self.remove_ticks_and_scale_correctly(ax4, ref)
    
        cc_vals = ax5.imshow(cross_corr.T, origin='lower', interpolation='nearest')
        ax5.set_title('2D Cross-Corr %sx%s' % cross_corr.shape, fontsize=4)
        ax5.set_xticks([])
        ax5.set_yticks([])
        cax = fig.add_axes([0.77, 0.65, 0.01, 0.20])
        cbar = fig.colorbar(cc_vals, cax)
        for t in cbar.ax.get_yticklabels():
            t.set_fontsize(4)
    
        reconst = ax6.imshow(overlap_cc, cmap='jet', origin='lower',
                             interpolation='nearest')  # extent=[-0.5, n-0.5, -0.5, m-0.5]
        X = np.array([i[0] for i in xy_center_grid.ravel()]).reshape(xy_center_grid.shape)
        Y = np.array([i[1] for i in xy_center_grid.ravel()]).reshape(xy_center_grid.shape)
        transparency = cross_corr - cross_corr.min()
        transparency = transparency / transparency.max()
        rgba_colors = [(1, 1, 1, a) for a in transparency.flatten()]
        ax6.scatter(X.flatten(), Y.flatten(), color=rgba_colors, s=0.5, linewidth=0)
        a1 = np.cos(np.deg2rad(angles)) * rho - X  # Vector AB from line-defining-point to all matrix points
        a2 = np.sin(np.deg2rad(angles)) * rho - Y  # Vector AB from line-defining-point to all matrix points
        AB = np.dstack([a1, a2])
        line_direction = np.dstack([np.cos(np.deg2rad(angles)), np.sin(np.deg2rad(angles))])
        length = np.einsum('ijk,ijk->ij', line_direction, AB)  # Dot product along last axis
        u = np.cos(np.deg2rad(angles)) * length / float(overlap_cc.shape[1])
        v = np.sin(np.deg2rad(angles)) * length / float(overlap_cc.shape[0])
        angles_plt = ax6.quiver(X, Y, u, v, linewidths=0.1, scale=1.0, alpha=0.5, color='white')
        ax6.set_title('Projection by Rho and Theta %sx%s' % angles.shape, fontsize=4)
        ax6.set_aspect(1.)
        ax6 = self.remove_ticks_and_scale_correctly(ax6, overlap_cc)
        ax6.set_xlim([-1, overlap_cc.shape[1] + 1])
        ax6.set_ylim([-1, overlap_cc.shape[0] + 1])
        cax = fig.add_axes([0.77, 0.25, 0.01, 0.20])
        cbar = fig.colorbar(reconst, cax)
        for t in cbar.ax.get_yticklabels():
            t.set_fontsize(4)
    
        x, y = np.arange(peaks.shape[0]), np.arange(peaks.shape[1])
        X, Y = np.meshgrid(x, y)
        peaks_plt = ax7.imshow(peaks.T, origin='lower', interpolation='nearest')
        u, v = np.cos(np.deg2rad(angles.T - 90)), np.sin(np.deg2rad(angles.T - 90))
        angles_plt = ax7.quiver(X, Y, u, v, linewidths=0.2, pivot='mid')
        ax7.set_title('Helix Angles and AngleCC-Scores %sx%s' % peaks.shape, fontsize=4)
        ax7.set_xticks([])
        ax7.set_yticks([])
        ax7.set_xlim(-0.5, peaks.shape[0] - 0.5)
        ax7.set_ylim(-0.5, peaks.shape[1] - 0.5)
        cax = fig.add_axes([0.971, 0.65, 0.01, 0.20])
        cbar = fig.colorbar(peaks_plt, cax)
        for t in cbar.ax.get_yticklabels():
            t.set_fontsize(4)
    
        rho_plot = ax8.imshow(cross_corr.T, origin='lower', interpolation='nearest')
        ax8.set_title('2D Cross-Corr %sx%s' % rho.shape, fontsize=4)
        ax8.set_xticks([])
        ax8.set_yticks([])
        cax = fig.add_axes([0.971, 0.25, 0.01, 0.20])
        cbar = fig.colorbar(rho_plot, cax)
        for t in cbar.ax.get_yticklabels():
            t.set_fontsize(4)
    
        plt.subplots_adjust(left=0.04, right=0.96, bottom=0.18, top=0.92)
    
        fig.savefig(outfile[:-4] + '_verbose.pdf', dpi=600)
    
        return outfile
    
    

    def add_ccmap(self, overlap_cc, cross_corr, rho, angles, xy_center_grid, fig, ax1):
        ax1.set_title('Projection by Rho and Theta %sx%s' % angles.shape, fontsize=5)

        reconst = ax1.imshow(overlap_cc, cmap='jet', origin='lower', interpolation='nearest') # extent=[-0.5, n-0.5, -0.5, m-0.5]
        X = np.array([i[0] for i in xy_center_grid.ravel()]).reshape(xy_center_grid.shape)
        Y = np.array([i[1] for i in xy_center_grid.ravel()]).reshape(xy_center_grid.shape)
        transparency = cross_corr - cross_corr.min()
        transparency = transparency / transparency.max()
        rgba_colors = [(1, 1, 1, a) for a in transparency.flatten()]
        ax1.scatter(X.flatten(), Y.flatten(), color=rgba_colors, s=0.5, linewidth=0)
        a1 = np.cos(np.deg2rad(angles)) * rho - X # Vector AB from line-defining-point to all matrix points
        a2 = np.sin(np.deg2rad(angles)) * rho - Y # Vector AB from line-defining-point to all matrix points
        AB = np.dstack([a1, a2])
        line_direction = np.dstack([np.cos(np.deg2rad(angles)), np.sin(np.deg2rad(angles))])
        length = np.einsum('ijk,ijk->ij', line_direction, AB) # Dot product along last axis
        u = np.cos(np.deg2rad(angles)) * length / float(overlap_cc.shape[1])
        v = np.sin(np.deg2rad(angles)) * length / float(overlap_cc.shape[0])
        angles_plt = ax1.quiver(X, Y, u, v, linewidths=0.1, scale=1.0, alpha=0.5, color='white')
        ax1.set_aspect(1.)
        ax1 = self.remove_ticks_and_scale_correctly(ax1, overlap_cc)
        ax1.set_xlim([-1, overlap_cc.shape[1] + 1])
        ax1.set_ylim([-1, overlap_cc.shape[0] + 1])
        cax = fig.add_axes([0.003, 0.695, 0.01, 0.22])
        cbar = fig.colorbar(reconst, cax)
        for t in cbar.ax.get_yticklabels():
            t.set_fontsize(4)
        
        return ax1


    def add_referene_image(self, ref, ax2):
        ax2.set_title('Reference Helix', fontsize=5)
        
        ax2.imshow(ref, cmap='gray', origin='lower', interpolation='nearest')
        ax2.set_aspect('equal')
        ax2 = self.remove_ticks_and_scale_correctly(ax2, ref)

        return ax2


    def add_thresholded_ccmap(self, binary, skel, a_threshold, absolute_threshold, mic_np, ax3):
        if absolute_threshold is None:
            title = 'Thresholded at alpha-value of {0}'.format(a_threshold)
        else:
            title = 'Thresholded at cc-threshold of {0}'.format(absolute_threshold)

        ax3.set_title(title, fontsize=5)

        bin_mask = np.ma.masked_where(binary < 0.5, -1 * binary)
        ax3.imshow(bin_mask, cmap='gray', origin='lower', interpolation='nearest')
        ax3.plot(None, label='thresholded', color='black')
        ax3 = self.remove_ticks_and_scale_correctly(ax3, mic_np)

        skel_mask = np.ma.masked_where(skel < 0.5, -1 * skel)
        ax3.imshow(skel_mask, cmap='autumn', origin='lower', interpolation='nearest')
        ax3.plot(None, label='cleaned up', color='red')
        ax3.legend(fontsize=4)

        return ax3


    def add_cc_histogram(self, overlap_cc, lamb, absolute_threshold, background_cutoff,  a_threshold, ax4):
        ax4.set_title('Projection Map Histogram & Thresholding', fontsize=5)
        
        n, bins, patches = ax4.hist(overlap_cc[overlap_cc>background_cutoff].flatten(), 80, facecolor='grey',
                                    linewidth=0.0, normed=True)
        ax4.tick_params(axis='both', which='major', labelsize=4)
        x = np.linspace(overlap_cc.min(), overlap_cc.max(), 500)

        if absolute_threshold is None:
            fitfunct = stats.expon
            fitparams = [0, lamb]

            ax4.plot(x, fitfunct.pdf(x, *fitparams), color='red', linewidth=1,
                     label='Exp. Fit\nlambda=%.3f'%lamb)  # 1/float(bins[1]-bins[0]) *

            absolute_threshold = fitfunct.ppf(1 - a_threshold, *fitparams)
            ax4.axvline(absolute_threshold, color='green', linewidth=1, label="alpha=%.2e" % a_threshold)

            colors_choice = {}
            colors_choice[-1.] = 'blue'
            colors_choice[1.] = 'orange'
            for each_d in colors_choice:
                alt_alpha = a_threshold * (10.0 ** each_d)
                alt_absolute_threshold = fitfunct.ppf(1 - (alt_alpha), *fitparams)
                ax4.axvline(alt_absolute_threshold, color=colors_choice[each_d], linewidth=0.5, linestyle=':', label="alpha=%.2e" % alt_alpha)

            ax4.text(1.1 * absolute_threshold, 1 / float(bins[1] - bins[0]) / 20 * 0.9,
                     "cc_threshold=%.3e\nalpha=%.2e" % (absolute_threshold, a_threshold),
                     color='green', fontsize=5)

        else:
            ax4.axvline(absolute_threshold, color='green', linewidth=1)
            ax4.text(1.1 * absolute_threshold, 1 / float(bins[1] - bins[0]) / 20 * 0.9,
                     "cc threshold=%.3e" % (absolute_threshold),
                     color='green', fontsize=5)

        ax4.set_ylim((0, 1 / float(bins[1] - bins[0]) / 20.))
        for b, p in zip(bins, patches):
            if b > absolute_threshold:
                plt.setp(p, 'facecolor', 'green')
        
        legend = ax4.legend(fontsize=5, labelspacing=0.2, loc=7)
        
        return ax4


    def add_micrograph(self, ax5, mic_np, helices, pers_lengths):
        ax5.set_title('Micrograph with detected helices %sx%s. Numbers denote persistence length in um' % mic_np.shape,
                      fontsize=5)

        ax5.imshow(mic_np, cmap='gray', origin='lower', interpolation='nearest')
        colors = plt.cm.hsv(np.linspace(0, 1, len(helices)))[:, 0:3]  # / 1.0
        font = {'weight': 'bold', 'size': 5}
        for pers, c, (each_xcoord, each_ycoord) in zip(pers_lengths, colors, helices):
            ax5.plot(each_xcoord, each_ycoord, 'o', markersize=2, alpha=1, markeredgewidth=0.0, color=c)
            c_dark = c / 5.0
            xmean, ymean = each_xcoord.mean(), each_ycoord.mean()
            ax5.text(xmean, ymean, "%.1f" % pers, color=c_dark, fontdict=font)
        ax5 = self.remove_ticks_and_scale_correctly(ax5, mic_np)
        
        return ax5 

    
    def visualize_traces_in_diagnostic_plot(self, infile, outfile, overlap_cc, binary, helices, mic, ref, cross_corr,
                                            rho, angles, xy_center_grid, lamb, absolute_threshold, background_cutoff,
                                            skel, pers_lengths, feature_set, a_threshold):
        mic.read_image(infile)
        mic_np = np.copy(EMNumPy.em2numpy(mic))
        michelixtrace_plot = DiagnosticPlot()
        fig = michelixtrace_plot.add_header_and_footer(feature_set, infile, outfile)
    
        gs = gridspec.GridSpec(2, 4, width_ratios=[1, 1, 1.25, 1.25], height_ratios=[1, 1.7])
    
        ax1 = fig.add_subplot(gs[0, 0])  # Reconstruction
        ax2 = fig.add_subplot(gs[1, 1])  # Reference
        ax3 = fig.add_subplot(gs[0, 1])  # Thresholded
        ax4 = fig.add_subplot(gs[1, 0])  # Histogram
        ax5 = fig.add_subplot(gs[:, 2:])  # Micrograph
    
        ax1 = self.add_ccmap(overlap_cc, cross_corr, rho, angles, xy_center_grid, fig, ax1)
        ax2 = self.add_referene_image(ref, ax2)
        ax3 = self.add_thresholded_ccmap(binary, skel, a_threshold, absolute_threshold, mic_np, ax3)
        ax4 = self.add_cc_histogram(overlap_cc, lamb, absolute_threshold, background_cutoff, a_threshold, ax4)
        ax5 = self.add_micrograph(ax5, mic_np, helices, pers_lengths)
    
        fig.tight_layout()
        fig.subplots_adjust(left=0.045, right=0.99, bottom=0.21, top=0.93)
        fig.savefig(outfile, dpi=600)
    
        return outfile
