#!/usr/bin/env python
"""
Test module to check michelixtrace module
"""
from EMAN2 import EMData
from fundamentals import window2d, rot_shift2D, shift2d
from glob import glob
from multiprocessing import cpu_count
import os
from spring.csinfrastr.csproductivity import TestingDirectory
from spring.micprgs.michelixtrace import MicHelixTrace, MicHelixTracePar
from spring.tests.csinfrastr.test_csreadinput import EndToEndTest
from spring.tests.segment2d.test_segment import MicrographHelixPreparation
from utilities import model_circle


class TestMicHelixTracePrepare(object):
    def prepare_micrograph_and_reference(self):
        MicrographHelixPreparation().prepare_ctf_micrograph(self.micrograph_test_file, self.avg_defocus, self.cs,
        self.voltage, self.pixelsize, self.ampcont, self.astigmatism, self.astigmatism_angle)

        left_x, left_y = 88, 80
        img = EMData()
        img.read_image(self.micrograph_test_file)
        shifted_img_zero = shift2d(img, img.get_xsize() / 4.0, img.get_ysize() / 4.0)
        shifted_img_one = shift2d(img, img.get_xsize() / 2, img.get_ysize() / 3)
        shifted_img_two = rot_shift2D(shifted_img_one, 103, 220, 300)
        shifted_img_three = rot_shift2D(shifted_img_one, -45, -350, 100)
        shifted_img_four = rot_shift2D(shifted_img_one, 103, 150, 300)
        shifted_img_five = rot_shift2D(shifted_img_one, 90, -40, -40)

        new_mic = img + shifted_img_zero + shifted_img_one + shifted_img_two + shifted_img_three + shifted_img_four + \
        shifted_img_five

        new_mic.write_image(self.micrograph_test_file)
        
        wimg = window2d(img, 150, 150, 'l', left_x, left_y)
        wimg = rot_shift2D(wimg, -45)
        wimg *= model_circle(75, 150, 150)
        wimg.write_image(self.ref_test_image)

    def write_groud_truth_coord_file(self):
        coord_txt = \
        "630     577     100     100     -1\n" + \
        "523     748     100     100     -2\n" + \
        "616     442     100     100     -1\n" + \
        "482     309     100     100     -2\n" + \
        "453     754     100     100     -1\n" + \
        "563     582     100     100     -2\n" + \
        "262     388     100     100     -1\n" + \
        "310     342     100     100     -2\n" + \
        "238     229     100     100     -1\n" + \
        "314     308     100     100     -2\n" + \
        "403     245     100     100     -1\n" + \
        "336     309     100     100     -2\n" + \
        "-18     -24     100     100     -1\n" + \
        "115     112     100     100     -2\n" + \
        "223     668     100     100     -1\n" + \
        "221     463     100     100     -2"

        coord_f = open(self.helix_box_file, 'w')
        coord_f.write(coord_txt)
        coord_f.close()


    def check_detected_helix_count(self, expected_count=4):
        f = open(os.path.basename(self.helix_box_file), 'r')
        helix_count = 0
        for each_line in f.readlines():
            if '-2' in each_line:
                helix_count += 1
        
        print helix_count
        assert expected_count - 1 <= helix_count 


class TestMicHelixTrace(TestMicHelixTracePrepare, MicHelixTrace):
    def setup_of_common_non_mpi_parameters(self):
        self.feature_set = MicHelixTracePar()
        self.setup_main_michelixtrace_parameters()
        
    def setup_main_michelixtrace_parameters(self):
        self.micrograph_test_file = 'test_mic.hdf'
        self.test_diagnostic = 'test_diagnostic.pdf'
        self.helix_box_file = os.path.join(os.pardir, os.path.splitext(self.micrograph_test_file)[0] + os.extsep + 'box')
        self.avg_defocus = 20000
        self.cs = 2.0
        self.voltage = 200.0
        self.pixelsize = 5.0
        self.ampcont = 0.10
        self.astigmatism = 1000
        self.astigmatism_angle = 35.0
        self.ref_test_image = 'test_reference.hdf'

        self.prepare_micrograph_and_reference()
        
        self.feature_set.parameters['Micrographs']=self.micrograph_test_file
        self.feature_set.parameters['Diagnostic plot pattern']=self.test_diagnostic
        self.feature_set.parameters['Helix reference']=self.ref_test_image
        self.feature_set.parameters['Invert option']=False
        self.feature_set.parameters['Estimated helix width in Angstrom']=300
            
        self.feature_set.parameters['Pixel size in Angstrom'] = self.pixelsize
        self.feature_set.parameters['Binning option'] = True
        self.feature_set.parameters['Binning factor'] = 4
        self.feature_set.parameters['Tile size power spectrum in Angstrom'] = 640
        self.feature_set.parameters['Tile overlap in percent']= 80

        self.feature_set.parameters['Alpha threshold cc-map']=0.0001
        self.feature_set.parameters['Absolute threshold option cc-map']=False
        self.feature_set.parameters['Absolute threshold cc-map']=0.2
        self.feature_set.parameters['Order fit']= 2
        self.feature_set.parameters['Minimum and maximum helix length']=((500, 1500))
        self.feature_set.parameters['Box file coordinate step']=70.0
        self.feature_set.parameters['Pruning cutoff bending']=2.0
        self.feature_set.parameters['Compute performance score']=False
        self.feature_set.parameters['Parameter search option']=False
        self.feature_set.parameters['Manually traced helix file']=self.helix_box_file

        self.feature_set.parameters['MPI option']=False
        self.feature_set.parameters['Number of CPUs']=min(8, cpu_count())
            
        self.feature_set.parameters['Temporary directory']=os.path.abspath(os.curdir)

    def setup(self):
        self.testingdir = TestingDirectory(os.path.splitext(os.path.basename(__file__))[0])
        self.testingdir.create()
        
        self.setup_of_common_non_mpi_parameters()
        super(TestMicHelixTrace, self).__init__(self.feature_set)


    def remove_mic_dir_including_box_files(self):
        [os.remove(each_file) for each_file in glob('test_mic_groundtruth/*'.format(sep=os.extsep))]
        test_mic_dir = os.path.splitext(self.micrograph_test_file)[0] + '_groundtruth'
        if os.path.exists(test_mic_dir):
            os.rmdir(test_mic_dir)

    def teardown(self):
        pass
        os.remove(self.micrograph_test_file)
        os.remove(self.test_diagnostic)
        if os.path.exists(self.helix_box_file):
            os.remove(self.helix_box_file)
            os.remove('spring.db')
        os.remove(self.ref_test_image)
               
        self.remove_mic_dir_including_box_files()
                    
        self.testingdir.remove()


class TestMicHelixTraceMain(TestMicHelixTrace):
    def do_test_case_mt1(self):
        """
        Mictrace test to trace filaments using a reference
        """
        self.trace_helices()
        self.check_detected_helix_count(5)


class TestMicHelixTraceMore(TestMicHelixTrace):
    def do_test_case_mt2(self):
        """
        Mictrace test empty micrograph
        """
        super(TestMicHelixTrace, self).__init__(self.feature_set)
      
        MicrographHelixPreparation().prepare_ctf_micrograph(self.micrograph_test_file, self.avg_defocus, self.cs,
        self.voltage, self.pixelsize, self.ampcont, self.astigmatism, self.astigmatism_angle, helix=False)
              
        self.trace_helices()
        assert not os.path.exists(os.path.basename(self.helix_box_file))
  
  
    def do_test_case_mt3(self):
        """
        Mictrace test parameter search including parameter search
        """
        self.feature_set.parameters['Compute performance score']=True
        self.feature_set.parameters['Parameter search option']=True
        super(TestMicHelixTrace, self).__init__(self.feature_set)
     
        self.write_groud_truth_coord_file()
        self.trace_helices()
        os.rename(self.helix_box_file, self.test_diagnostic)
        assert os.path.exists('trace_grid.db')
        os.remove('trace_grid.db')
 
 
    def do_test_case_mt4(self):
        """
        Mictrace test recall/precision computation but no parameter search
        """
        self.feature_set.parameters['Compute performance score']=True
        self.feature_set.parameters['Parameter search option']=False
        super(TestMicHelixTrace, self).__init__(self.feature_set)
     
        self.write_groud_truth_coord_file()
        self.trace_helices()
        os.remove(self.helix_box_file)


    def do_test_case_mt5(self):
        """
        Mictrace test absolute threshold option
        """
        self.feature_set.parameters['Absolute threshold option cc-map']=True
        super(TestMicHelixTrace, self).__init__(self.feature_set)
     
        self.trace_helices()
        self.check_detected_helix_count(5)


class TestMicHelixTraceEndToEnd(TestMicHelixTrace):
    def do_end_to_end_test_mt_inputfile(self):
        EndToEndTest().do_end_to_end_inputfile(self.feature_set)

    def do_end_to_end_test_mt_prompt(self):
        EndToEndTest().do_end_to_end_prompt(self.feature_set)


class TestMicHelixTraceMpi(TestMicHelixTrace):
    def do_end_to_end_test_mt_inputfile_with_MPI(self):
        self.feature_set.parameters['MPI option'] = True
        self.feature_set.parameters['Number of CPUs']=2
        
        EndToEndTest().do_end_to_end_inputfile(self.feature_set)


class TestMicHelixTraceMpiMore(TestMicHelixTrace):
    def do_end_to_end_test_mt_inputfile_with_MPI_param(self):
        self.feature_set.parameters['Compute performance score']=True
        self.feature_set.parameters['Parameter search option']=True
        self.feature_set.parameters['MPI option'] = True
        self.feature_set.parameters['Number of CPUs']=2
        
        self.write_groud_truth_coord_file()
        EndToEndTest().do_end_to_end_inputfile(self.feature_set)
        os.rename(self.helix_box_file, self.test_diagnostic)
        assert os.path.exists('trace_grid.db')
        os.remove('trace_grid.db')

    def do_end_to_end_test_mt_inputfile_with_MPI_comp(self):
        self.feature_set.parameters['Compute performance score']=True
        self.feature_set.parameters['Parameter search option']=False
        self.feature_set.parameters['MPI option'] = True
        self.feature_set.parameters['Number of CPUs']=2
        
        self.write_groud_truth_coord_file()
        EndToEndTest().do_end_to_end_inputfile(self.feature_set)
        os.rename(self.helix_box_file, self.test_diagnostic)
        assert os.path.exists('trace_grid.db')
        os.remove('trace_grid.db')

def main():
    tseg = TestMicHelixTraceMain()
    tseg.setup()
    tseg.do_test_case_mt1()
        
if __name__ == '__main__':
    main()
