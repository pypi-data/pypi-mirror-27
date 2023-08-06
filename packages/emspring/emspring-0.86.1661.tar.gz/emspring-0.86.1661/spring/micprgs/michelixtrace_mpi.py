# Author: Carsten Sachse 03-Nov-2013
# with Stefan Huber (2017) 
# Copyright: EMBL (2010 - 2018)
# License: see license.txt for details

from spring.csinfrastr.csproductivity import OpenMpi
from spring.micprgs.micctfdetermine_mpi import ScanMpi
from spring.micprgs.michelixtrace import MicHelixTrace, MicHelixTracePar
from spring.micprgs.michelixtrace_helperfunctions import MicHelixTraceSupport
from spring.segment2d.segment_mpi import SegmentMpi


class MicHelixTraceMpi(MicHelixTrace, ScanMpi):

    def trace_helices(self):
        self.startup_scan_mpi_programs()
        
        if self.micrograph_files != []:
            if self.parametersearch_option:
                tracing_results_mic = self.trace_helices_in_micrographs(self.micrograph_files, self.outfiles)
                self.comm.barrier()

                tracing_results_mic = self.comm.gather(tracing_results_mic, root=0)
                if self.rank == 0:
                    tracing_results_mic = OpenMpi().merge_sequence_of_sequences(tracing_results_mic)
                    trcng_crit_comb = MicHelixTraceSupport().summarize_parameter_info_over_micrographs(tracing_results_mic)
                    
                    self.write_out_determined_tracing_criteria_in_database(trcng_crit_comb)
                    self.generate_and_plot_parameter_search_summary(trcng_crit_comb, self.absolutethresholdoption)
                
                self.end_scan_mpi_programs()
            else:
                if self.compute_stat:
                    tracing_results_mic, helix_info, plot_info = \
                    self.trace_helices_in_micrographs(self.micrograph_files, self.outfiles)
                    self.comm.barrier()

                    tracing_results_mic = self.comm.gather(tracing_results_mic, root=0)
                    if self.rank == 0:
                        tracing_results_mic = OpenMpi().merge_sequence_of_sequences(tracing_results_mic)
                        trcng_crit_comb = MicHelixTraceSupport().summarize_parameter_info_over_micrographs(tracing_results_mic)
                        self.write_out_determined_tracing_criteria_in_database(trcng_crit_comb)
                else:
                    helix_info, plot_info = self.trace_helices_in_micrographs(self.micrograph_files, self.outfiles)

                helix_info = SegmentMpi().gather_distributed_helices_to_root(self.comm, helix_info)

                if self.rank == 0:
                    if len(helix_info) > 100: #at least 100 helices necessary
                        helix_info = self.prune_helices_and_plot_persistence_length_summary(helix_info)
                    self.write_boxfiles_from_helix_info(helix_info)
                    self.enter_helixinfo_into_springdb(helix_info)
                    coordinates = [[i.micrograph, i.coordinates] for i in helix_info]
                else:
                    coordinates = None
        
                coordinates = self.comm.bcast(coordinates, root=0)
        
                self.correct_coordinates_and_visualize_traces(plot_info, coordinates)
                self.end_scan_mpi_programs()

def main():
    parset = MicHelixTracePar()
    reduced_parset = OpenMpi().start_main_mpi(parset)
    
    ####### Program
    micrograph = MicHelixTraceMpi(reduced_parset)
    micrograph.trace_helices()


if __name__ == '__main__':
    main()
