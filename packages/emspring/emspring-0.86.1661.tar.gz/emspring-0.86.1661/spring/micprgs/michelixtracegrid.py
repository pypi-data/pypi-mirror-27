# Author: Carsten Sachse 19-Aug-2017
# Copyright: EMBL (2010 - 2018)
# License: see license.txt for details
"""
Program to optimize michelixtrace by varying michelixtrace parameters systematically on a grid
"""

from collections import OrderedDict
from spring.csinfrastr.csdatabase import SpringDataBase, grid_base, GridTable, GridRefineTable
from spring.csinfrastr.csfeatures import Features
from spring.csinfrastr.cslogger import Logger
from spring.csinfrastr.csproductivity import OpenMpi
from spring.csinfrastr.csreadinput import OptHandler
from spring.micprgs.michelixtrace import MicHelixTracePar, MicHelixTrace
from spring.segment3d.segclassreconstruct import SegClassReconstruct
from spring.segment3d.segrefine3dgrid import SegRefine3dGrid

from sqlalchemy.sql.expression import desc
from tabulate import tabulate

import numpy as np
import os


class MicHelixTraceGridPar(MicHelixTracePar):
    """
    Class to initiate default dictionary with input parameters including help and range values and status dictionary
    """
    def __init__(self):
        # package/program identity
        self.package = 'emspring'       
        self.progname = 'michelixtracegrid'
        self.proginfo = __doc__
        self.code_files = [self.progname]

        self.mictrace_features = Features()
        self.feature_set = self.mictrace_features.setup(self)
        
        self.define_parameters_and_their_properties()
        self.define_program_states()


    def define_parameters_and_their_properties(self):
        super(MicHelixTraceGridPar, self).define_input_and_output_michelixtrace()
        parameters_to_be_varied = self.get_parameters_to_be_varied()

        self.feature_set = self.mictrace_features.set_first_parameter_choice(self.feature_set, parameters_to_be_varied,
        'alpha_threshold')
        
        self.feature_set = self.mictrace_features.set_second_parameter_choice(self.feature_set, parameters_to_be_varied,
        'min_helix_length' )
        
        self.feature_set = self.mictrace_features.set_lower_and_upper_limit_first_parameter(self.feature_set)
        self.feature_set = self.mictrace_features.set_lower_and_upper_limit_second_parameter(self.feature_set)
        self.feature_set = self.mictrace_features.set_first_and_second_parameter_increment(self.feature_set)
        self.feature_set = self.mictrace_features.set_subgrid_option(self.feature_set)
        self.feature_set = self.mictrace_features.set_subgrid_details(self.feature_set)
        self.feature_set = self.mictrace_features.set_continue_grid_option(self.feature_set)
        self.feature_set = self.mictrace_features.set_grid_database_cont(self.feature_set)
        
        super(MicHelixTraceGridPar, self).define_michelixtrace_parameters()
        
    def define_program_states(self):
        super(MicHelixTraceGridPar, self).define_program_states()

    def get_parameters_to_be_varied(self):
        parameter_to_be_varied = [
        'tile_size_power', 'tile_overlap', 'binning_factor', 'alpha_threshold',
        'min_helix_length', 'max_helix_length', 'order_fit'
                                  ]
        return parameter_to_be_varied


class MicHelixTraceGridSetup(MicHelixTrace):
    def __init__(self, parset = None):
        self.log = Logger()
        if parset is not None:
            self.feature_set = parset
            p = self.feature_set.parameters
            self.define_all_michelixtrace_parameters(p)
            
            self.primary_variable = p['First parameter']
            self.secondary_variable = p['Second parameter']
            self.primary_range = p['Lower and upper limit first parameter']
            self.primary_inc, self.second_inc = p['First and second parameter increment']
            self.secondary_range = p['Lower and upper limit second parameter']
            self.subgrid_option = p['Subgrid option']
            self.subgrid = p['Part and number of subgrids']
            self.continue_grid = p['Grid continue option']
            self.grid_database = p['Grid database']
            
        
    def generate_michelixtrace_parameters_while_removing_grid_parameters(self, parameters):
        
        michelixtrace_params = OrderedDict()
        for each_param in parameters:
            if each_param not in ['First parameter', 'Second parameter', 'Lower and upper limit first parameter',
                                  'Lower and upper limit second parameter', 'First and second parameter increment',
                                  'Subgrid option', 'Part and number of subgrids', 'Grid continue option', 
                                  'Grid database']:
                michelixtrace_params[each_param] = parameters[each_param]
        
        return michelixtrace_params
    

    def setup_grid_parameters(self, each_grid_point, parameters, index, one_of_both_parameters):
        if one_of_both_parameters == 'tile_size_power':
            parameters['Tile size power spectrum in Angstrom'] = each_grid_point[index]
        elif one_of_both_parameters == 'tile_overlap':
            parameters['Tile overlap in percent'] = each_grid_point[index]
        elif one_of_both_parameters == 'binning_factor':
            parameters['Binning factor'] = each_grid_point[index]
        elif one_of_both_parameters == 'alpha_threshold':
            parameters['Alpha threshold cc-map'] = each_grid_point[index]
        elif one_of_both_parameters == 'order_fit':
            parameters['Order fit'] = each_grid_point[index]
            
        elif one_of_both_parameters == 'min_helix_length':
            parameters['Minimum and maximum helix length'] = \
            (each_grid_point[index], parameters['Minimum and maximum helix length'][1])
        elif one_of_both_parameters == 'max_helix_length':
            parameters['Minimum and maximum helix length'] = \
            (parameters['Minimum and maximum helix length'][0], each_grid_point[index])
        return parameters
    

    def add_grid_point_to_parameter_dictionary(self, first_param, second_param, each_grid_point, parameters):
        """
        >>> from spring.micprgs.michelixtracegrid import MicHelixTraceGrid
        >>> min_hl = 'min_helix_length'
        >>> params = MicHelixTraceGridPar().parameters
        >>> s = MicHelixTraceGrid()
        >>> s.add_grid_point_to_parameter_dictionary('alpha_threshold', min_hl, [-111, 1.111], params) #doctest: +NORMALIZE_WHITESPACE
        OrderedDict([('Micrographs', 'cs_scan034.tif'), ('Diagnostic plot pattern', 'michelixtracegrid_diag.pdf'), 
        ('First parameter', 'alpha_threshold'), ('Second parameter', 'min_helix_length'), 
        ('Lower and upper limit first parameter', (1.4, 1.9)), ('Lower and upper limit second parameter', (22.0, 24.0)), 
        ('First and second parameter increment', (0.1, 0.3)), ('Subgrid option', False), 
        ('Part and number of subgrids', (1, 3)), ('Grid continue option', False), ('Grid database', 'grid.db'), 
        ('Helix reference', 'helix_reference.hdf'), ('Invert option', False), ('Estimated helix width in Angstrom', 200), 
        ('Pixel size in Angstrom', 1.163), ('Binning option', True), ('Binning factor', 4), 
        ('Tile size power spectrum in Angstrom', 500), ('Tile overlap in percent', 80), ('Alpha threshold cc-map', -111), 
        ('Absolute threshold option cc-map', False), ('Absolute threshold cc-map', 0.2), ('Order fit', 2), 
        ('Minimum and maximum helix length', (1.111, 1500)), ('Pruning cutoff bending', 2.0), 
        ('Box file coordinate step', 70.0), ('Compute performance score', False), ('Parameter search option', False), 
        ('Manually traced helix file', 'mic.box'), ('MPI option', True), ('Number of CPUs', 2), 
        ('Temporary directory', '/tmp')])
        """
        for index, one_of_both_parameters in enumerate([first_param, second_param]):
            if one_of_both_parameters is not None:
                parameters = self.setup_grid_parameters(each_grid_point, parameters, index,
                one_of_both_parameters)
        
        return parameters


    def setup_parameters_for_each_grid_point(self, first_param, second_param, each_grid_point, parameters):
        parameters = self.add_grid_point_to_parameter_dictionary(first_param, second_param, each_grid_point, parameters)
        run_name = SegRefine3dGrid().generate_file_name_for_grid_search(first_param, second_param, each_grid_point)
                
        parameter_file = Features().write_parfile(parameters, run_name, tag=False)
        
        return parameter_file, run_name
    
    
class MicHelixTraceGrid(MicHelixTraceGridSetup):
    
    def get_variables_ranges_and_increments(self, grid_name):
        if self.continue_grid:
            last_grid_cycle_id, ref_grid = \
            SegRefine3dGrid().get_grid_parameters_and_final_grid_entry(self.grid_database, grid_name)
            
            primary_variable = ref_grid.primary_variable
            secondary_variable = ref_grid.secondary_variable
            primary_range = ref_grid.primary_min, ref_grid.primary_max
            primary_inc = ref_grid.primary_inc
            secondary_range = ref_grid.second_min, ref_grid.second_max
            second_inc = ref_grid.second_inc
        else:
            last_grid_cycle_id = 0
            primary_variable = self.primary_variable
            primary_range = self.primary_range
            primary_inc = self.primary_inc
            secondary_variable = self.secondary_variable
            secondary_range = self.secondary_range
            second_inc = self.second_inc
 
            if primary_variable == secondary_variable or secondary_variable == 'none':
                secondary_variable = None
                secondary_range = (None, None)
                second_inc = None
                secondary_range = self.iteration_count, self.iteration_count
                second_inc = 0
 
        return primary_range, primary_inc, secondary_range, second_inc, last_grid_cycle_id, primary_variable, \
        secondary_variable
 
 
    def setup_grid_sequence(self):
        grid_name = SegRefine3dGrid().get_grid_database_name(self.subgrid_option)
             
        primary_range, primary_inc, secondary_range, second_inc, last_grid_cycle_id, primary_variable, \
        secondary_variable = self.get_variables_ranges_and_increments(grid_name)
             
        if not 'alpha_threshold' in [primary_variable, secondary_variable]:
            grid_sequence = \
            SegClassReconstruct().generate_rise_rotation_or_pitch_unitnumber_pairs_for_symmetry_grid(primary_range,
            primary_inc, secondary_range, second_inc)
            
        else:
            primary_series, second_series = SegClassReconstruct().generate_unique_rise_rotation_or_pitch_unitnumber_arrays(primary_range,
            primary_inc, secondary_range, second_inc)
        
            if primary_variable == 'alpha_threshold':
                primary_series = \
                np.logspace(np.log10(min(primary_series)), np.log10(max(primary_series)), len(primary_series)).tolist()
            elif secondary_variable == 'alpha_threshold':
                second_series = \
                np.logspace(np.log10(min(second_series)), np.log10(max(second_series)), len(second_series)).tolist()

            grid_sequence =\
            SegClassReconstruct().convert_rise_rotation_or_pitch_unitnumber_series_to_grid_of_tuples(primary_series,
            second_series)
             
        grid_sequence = grid_sequence.ravel()
        grid_sequence = SegRefine3dGrid().split_grid_if_demanded(self.subgrid_option, self.subgrid, grid_sequence)
         
        grid_str = [(each_id, each_first, each_second) for each_id, (each_first, each_second) in enumerate(grid_sequence)]
        msg = tabulate(grid_str, ['local_grid_id', primary_variable, secondary_variable])
        self.log.ilog('The following grid combinations will be run:\n{0}'.format(msg))
             
        return grid_sequence, last_grid_cycle_id, primary_variable, secondary_variable, grid_name


    def generate_cmdline_for_each_grid_point(self, parameter_file):
        """
        >>> from spring.micprgs.michelixtracegrid import MicHelixTraceGrid
        >>> s = MicHelixTraceGrid()
        >>> s.generate_cmdline_for_each_grid_point('alpha_threshold_1e-10_min_helix_length_500.par')
        'michelixtrace --d alpha_threshold_1e-10_min_helix_length_500 --f alpha_threshold_1e-10_min_helix_length_500.par'
        """
        cmdline = 'michelixtrace --d {0} --f {1}'.format(os.path.splitext(parameter_file)[0],
        parameter_file)
        
        return cmdline
    

    def make_database_entries(self, run_name, each_grid_point, grid_session, comparison_measures):
        grid_cycle = GridRefineTable()
        rundir_name = os.path.abspath(run_name)
        grid_cycle.dirname = rundir_name
        grid_cycle.primary_value = each_grid_point[0]
        grid_cycle.secondary_value = each_grid_point[1]

        grid_cycle.precision = comparison_measures.precision
        grid_cycle.recall = comparison_measures.recall
        grid_cycle.f1_measure = comparison_measures.f1_measure
        grid_cycle.f05_measure = comparison_measures.f05_measure

        grid_session.add(grid_cycle)
        
        last_grid_entry = grid_session.query(GridTable).order_by(desc(GridTable.id)).first()
        last_grid_entry.completed_grid_id = grid_cycle.id
        
        grid_session.merge(last_grid_entry)
        grid_session.commit()
        
        return grid_cycle
        

    def enter_parameters_in_grid_database(self, primary_variable, secondary_variable, run_name, each_grid_point,
    grid_name, comp_measures):
        grid_session = SpringDataBase().setup_sqlite_db(grid_base, grid_name)
                
        this_cycle = self.make_database_entries(run_name, each_grid_point, grid_session, comp_measures)
        
        columns = SpringDataBase().get_columns_from_table(GridRefineTable)
        log_entries = [str(getattr(this_cycle, each_col)) for each_col in columns]
                                                         
        msg = tabulate(zip(columns, log_entries))

        self.log.ilog('The following parameters have been determined and entered into the database:\n{0}'.format(msg))
        
    
    def enter_variables_into_grid_database(self, primary_variable, secondary_variable, primary_range, secondary_range,
    primary_inc, second_inc, rise_rot_or_pitch_unit_choice=None):
        """
        common?
        """
        if rise_rot_or_pitch_unit_choice is None:
            primary_db_variable, secondary_db_variable = primary_variable, secondary_variable
        else:
            primary_db_variable, secondary_db_variable = \
            SegClassReconstruct().get_correct_primary_and_secondary_variables_for_database(rise_rot_or_pitch_unit_choice, 
            secondary_variable)
            
        this_grid_run = SegClassReconstruct().enter_starting_parameters_of_grid_search(primary_db_variable, 
            secondary_db_variable, primary_range, primary_inc, secondary_range, second_inc)
        
        return this_grid_run, primary_db_variable, secondary_db_variable
    

    def prepare_grid_database(self, primary_variable, secondary_variable, primary_range, secondary_range, primary_inc,
    second_inc, grid_name):
        grid_session = SpringDataBase().setup_sqlite_db(grid_base, grid_name)
        this_grid_run, primary_db_variable, secondary_db_variable = self.enter_variables_into_grid_database(primary_variable, 
            secondary_variable, primary_range, secondary_range, primary_inc, second_inc)
        
        grid_session.add(this_grid_run)
        grid_session.commit()

        return primary_db_variable, secondary_db_variable


    def retrieve_performance_score_from_run(self, trace_db):
        print trace_db
        grid_session = SpringDataBase().setup_sqlite_db(grid_base, trace_db)
        tracing_results = grid_session.query(GridRefineTable).order_by(desc(GridRefineTable.id)).first()
        
        return tracing_results


    def launch_michelixtrace_jobs(self):
        grid_sequence, last_grid_cycle_id, primary_variable, secondary_variable, grid_name = self.setup_grid_sequence()
        
        michelixtrace_parameters = \
        self.generate_michelixtrace_parameters_while_removing_grid_parameters(self.feature_set.parameters)
        
        primary_db_variable, secondary_db_variable = self.prepare_grid_database(primary_variable,
        secondary_variable, self.primary_range, self.secondary_range, self.primary_inc, self.second_inc, grid_name)
            
        for each_grid_id, each_grid_point in enumerate(grid_sequence):
            if each_grid_id >= last_grid_cycle_id:
                parameter_file, run_name = self.setup_parameters_for_each_grid_point(primary_variable, secondary_variable,
                each_grid_point, michelixtrace_parameters)
                
                cmdline = self.generate_cmdline_for_each_grid_point(parameter_file)
                self.log.in_progress_log()
                OpenMpi().launch_command(cmdline)
                
                comp_measures = self.retrieve_performance_score_from_run(os.path.join(run_name, 'trace_grid.db'))
    
                self.enter_parameters_in_grid_database(primary_db_variable, secondary_db_variable, run_name, 
                each_grid_point, grid_name, comp_measures)
            
            self.log.plog(100 * (each_grid_id + 1) / len(grid_sequence))
        
        self.log.endlog(self.feature_set)
            
            
def main():
    # Option handling
    parset = MicHelixTraceGridPar()
    mergeparset = OptHandler(parset)

    ######## Program
    stack = MicHelixTraceGrid(mergeparset)
    stack.launch_michelixtrace_jobs()

if __name__ == '__main__':
    main()