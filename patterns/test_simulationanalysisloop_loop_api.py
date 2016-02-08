import os
import sys
import pytest
import math
import radical.ensemblemd

from radical.ensemblemd.exceptions import NotImplementedError


class _TestSAL(radical.ensemblemd.SimulationAnalysisLoop):
    def __init__(self, maxiterations, simulation_instances=1, analysis_instances=1):
        radical.ensemblemd.SimulationAnalysisLoop.__init__(self, maxiterations, simulation_instances, analysis_instances)

    def pre_loop(self):
        k = radical.ensemblemd.Kernel(name="misc.mkfile")
        k.arguments = ["--size=1000", "--filename=reference.dat"]
	k.upload_input_data = ['levenshtein.py']
        return k

    def simulation_step(self, iteration, instance):
        k = radical.ensemblemd.Kernel(name="misc.mkfile")
        k.arguments = ["--size=1000", "--filename=simulation-{0}-{1}.dat".format(iteration, instance)]
        return k

    def analysis_step(self, iteration, instance):
        input_filename  = "simulation-{0}-{1}.dat".format(iteration, instance)
        output_filename = "analysis-{0}-{1}.dat".format(iteration, instance)

        k = radical.ensemblemd.Kernel(name="misc.levenshtein")
        k.link_input_data      = ["$PRE_LOOP/reference.dat", "$SIMULATION_ITERATION_{1}_INSTANCE_{2}/{0}".format(input_filename,iteration,instance),"$PRE_LOOP/levenshtein.py"]
        k.arguments            = ["--inputfile1=reference.dat",
                                  "--inputfile2={0}".format(input_filename),
                                  "--outputfile={0}".format(output_filename)]
        k.download_output_data = output_filename
        return k

    def post_loop(self):
        # post_loop is executed after the main simulation-analysis loop has
        # finished. In this example we don't do anything here.
        pass


class TestBasicApi(object):
#----------------------------------------
#testing import
    def test_import(self):
        from radical.ensemblemd import SimulationAnalysisLoop

#-----------------------------------------
#Test pattern name
    def test_pattern_name(self):
        from radical.ensemblemd import SimulationAnalysisLoop

        pattern = SimulationAnalysisLoop(1,1,1)
        assert pattern.name == 'SimulationAnalysisLoop'


#-----------------------------------------
#Test max number of iteration loops
    def test_iterations(self):
        from radical.ensemblemd import SimulationAnalysisLoop

        pattern = SimulationAnalysisLoop(5,1,1)
        assert pattern.iterations == 5


#-----------------------------------------
#Test number of simulations instances
#TODO: Incorrect simulation spelling
    def test_simulation_instances(self):
        from radical.ensemblemd import SimulationAnalysisLoop

        pattern = SimulationAnalysisLoop(5,5,1)
        assert pattern.simlation_instances == 5


#-----------------------------------------
#Test number of simulations instances
    def test_analysis_instances(self):
        from radical.ensemblemd import SimulationAnalysisLoop

        pattern = SimulationAnalysisLoop(5,5,5)
        assert pattern.analysis_instances == 5

#-----------------------------------------
#Test simulations adaptivity
    def test_simulation_adaptivity(self):
        from radical.ensemblemd import SimulationAnalysisLoop

        pattern = SimulationAnalysisLoop(5,5,5)
        assert pattern.simulation_adaptivity == False


class TestNotImplemented(object):
#-----------------------------------------
#Test pre_loop not implemented
    def test_pre_loop_not_implemented(self):
        from radical.ensemblemd import SimulationAnalysisLoop

        pattern = SimulationAnalysisLoop(5,5,5)
        with pytest.raises(NotImplementedError):
            pattern.pre_loop()


#-----------------------------------------
#Test simulation_step not implemented
    def test_simulation_step_not_implemented(self):
        from radical.ensemblemd import SimulationAnalysisLoop

        pattern = SimulationAnalysisLoop(1,1,1)
        with pytest.raises(NotImplementedError):
            pattern.simulation_step(1,1)

#-----------------------------------------
#Test analysis_step not implemented
    def test_analysis_step_not_implemented(self):
        from radical.ensemblemd import SimulationAnalysisLoop

        pattern = SimulationAnalysisLoop(1,1,1)
        with pytest.raises(NotImplementedError):
            pattern.analysis_step(1,1)


#-----------------------------------------
#Test post_loop not implemented
    def test_post_loop_not_implemented(self):
        from radical.ensemblemd import SimulationAnalysisLoop

        pattern = SimulationAnalysisLoop(5,5,5)
        with pytest.raises(NotImplementedError):
            pattern.post_loop()


class TestImplemented():
#--------------------------------------------
#
    def test_pre_loop(self):
        pattern = _TestSAL(5,5,5)
        assert type(pattern.pre_loop()) == radical.ensemblemd.Kernel
    #------------------------------------------

    def test_simulation_step(self):
        pattern = _TestSAL(5,5,5)
        assert type(pattern.simulation_step(5,5))  == radical.ensemblemd.Kernel

    #--------------------------------------------
    def test_analysis_step(self):
        pattern = _TestSAL(5,5,5)
        assert type(pattern.analysis_step(5,5)) == radical.ensemblemd.Kernel

    #--------------------------------------------
    #TODO: Implement this
    def test_post_loop(self):
        pass
        

    
        
