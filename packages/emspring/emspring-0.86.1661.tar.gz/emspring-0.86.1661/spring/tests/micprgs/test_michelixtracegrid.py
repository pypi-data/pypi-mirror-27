#!/usr/bin/env python
"""
Test module to check michelixtracegrid
"""
from glob import glob
from multiprocessing import cpu_count
import os
import shutil
from spring.csinfrastr.csproductivity import TestingDirectory
from spring.tests.csinfrastr.test_csreadinput import EndToEndTest
from spring.tests.micprgs.test_michelixtrace import TestMicHelixTrace
from spring.micprgs.michelixtracegrid import MicHelixTraceGrid, MicHelixTraceGridPar


class TestMicHelixTraceGridSetup(TestMicHelixTrace):
    def setup_of_common_mhtg_non_mpi_parameters(self):
        self.feature_set = MicHelixTraceGridPar()
#         self.input_stack = 'test_mic.hdf'
        self.prim_var = 'alpha_threshold'
        self.sec_var = 'min_helix_length'
        self.grid_db = os.path.join(os.pardir, 'grid.db')
        self.prim_range = ((1e-7, 1e-3))
        self.sec_range = ((300.0, 700.0))
        self.prim_inc = 0.0001998
        self.sec_inc = 100.0
        
        self.feature_set.parameters['First parameter']=self.prim_var
        self.feature_set.parameters['Second parameter']=self.sec_var
        self.feature_set.parameters['Lower and upper limit first parameter']=self.prim_range
        self.feature_set.parameters['Lower and upper limit second parameter']=self.sec_range
        self.feature_set.parameters['First and second parameter increment']=((self.prim_inc, self.sec_inc))
        self.feature_set.parameters['Subgrid option']=False
        self.feature_set.parameters['Part and number of subgrids']=(3, 3)
        self.feature_set.parameters['Grid continue option']=False
        self.feature_set.parameters['Grid database']=self.grid_db
        self.setup_main_michelixtrace_parameters()
        

class TestMicHelixTraceGrid(TestMicHelixTraceGridSetup, MicHelixTraceGrid):
    def setup_mhtg(self):
        self.setup_of_common_mhtg_non_mpi_parameters()
        
        self.feature_set.parameters['Compute performance score']=True
        self.feature_set.parameters['MPI option']=False
        self.feature_set.parameters['Number of CPUs']=min(3, cpu_count())
        self.feature_set.parameters['Temporary directory']=os.path.abspath(os.curdir)
        
        super(TestMicHelixTraceGridSetup, self).__init__(self.feature_set)
        self.write_groud_truth_coord_file()
        
    def setup(self):
        self.testingdir = TestingDirectory(os.path.splitext(os.path.basename(__file__))[0])
        self.testingdir.create()
        
        self.setup_mhtg()

    def teardown(self):
        pass
        os.remove(self.helix_box_file)
         
        parfiles = glob('*par')
        logfiles = glob('*log')
        directory = 'alpha_threshold'
        dirfiles = glob('{dir}*{sep}*'.format(dir=directory, sep=os.sep))
        for each_dir in dirfiles:
            os.chdir(os.path.dirname(each_dir))
            self.remove_mic_dir_including_box_files() 
            os.chdir(os.pardir)
         
        for each_file in logfiles + parfiles + dirfiles:
            if os.path.isfile(each_file):
                os.remove(each_file)
            elif os.path.isdir(each_file):
                os.rmdir(each_file)
 
        for each_dir in glob('{0}*'.format(directory)):
            shutil.rmtree(each_dir)
            
        for each_file in glob('gri*.db'):
            os.remove(each_file)
          
        self.remove_mic_dir_including_box_files()
 
        self.testingdir.remove()
            
        
class TestMicHelixTraceGridMain(TestMicHelixTraceGrid):
    def do_test_case_mhtg1(self):
        """
        Test standard Michelixtracegrid
        """
        self.launch_michelixtrace_jobs()


class TestMicHelixTraceGridMpi(TestMicHelixTraceGrid):
    def do_end_to_end_test_mhtg_inputfile(self):
        """
        Test standard Michelixtracegrid MPI option
        """
        self.feature_set.parameters['MPI option']=True
        self.feature_set.parameters['Number of CPUs']=min(3, cpu_count())

        EndToEndTest().do_end_to_end_inputfile(self.feature_set)

 
class TestMicHelixTraceGridEndToEnd(TestMicHelixTraceGrid):
    def do_end_to_end_test_mhtg_inputfile(self):
        EndToEndTest().do_end_to_end_inputfile(self.feature_set)
 

    def do_end_to_end_test_mhtg_prompt(self):
        EndToEndTest().do_end_to_end_prompt(self.feature_set)
        
        
def main():
    tmhtg = TestMicHelixTraceGridMain()
    tmhtg.setup()
    tmhtg.do_test_case_mhtg1()
        
if __name__ == '__main__':
    main()
