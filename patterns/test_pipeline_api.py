import os
import sys
import glob
import pytest
import radical.ensemblemd

from radical.ensemblemd.exceptions import NotImplementedError
#from radical.ensemblemd import Pipeline
#from radical.ensemblemd import Kernel

class _TestPipeline(radical.ensemblemd.Pipeline):
    
    def __init__(self,steps,instances):
        radical.ensemblemd.Pipeline.__init__(self,steps,instances)

    def step_1(self,instance):
        k= radical.ensemblemd.Kernel(name="misc.mkfile")
        k.arguments = ["--size=1000000", "--filename=asciifile-{0}.dat".format(instance)]
        #assert k is None
        return k

#--------------------------------------------------    
class TestBasicApi(object):
#----------------------------------------
#testing import
    def test_import(self):
        from radical.ensemblemd import Pipeline
    

#-----------------------------------------
#Test pattern name
    
    def test_pattern_name(self):
        from radical.ensemblemd import Pipeline

        pattern = Pipeline()
        assert pattern.name == 'Pipeline'

#-----------------------------------------
#Test instance
    def test_pattern_instance(self):
        from radical.ensemblemd import Pipeline

        pattern = Pipeline(steps=2,instances=2)
        assert pattern.instances == 2


#-----------------------------------------
#Test number of steps
    def test_pattern_number_steps(self):
        from radical.ensemblemd import Pipeline

        pattern = Pipeline(steps=2,instances=1)
        assert pattern.steps == 2


class TestNotImplemented(object):
#-----------------------------------------
#Test number of steps not_implemented
    def test_pattern_steps_1_not_implemented(self):
        from radical.ensemblemd import Pipeline

        pattern = Pipeline(steps=1,instances=1)
        with pytest.raises(NotImplementedError) as er:
            pattern.step_1(1)
        
#---------------------------------------------        


class TestImplemented(object):
    def test_pattern_step_1(self):
        try:
            test = _TestPipeline(steps=2,instances=2)
            #step_1() returns object of Kernel type
            assert type(test.step_1(2)) == radical.ensemblemd.Kernel

        except Exception:
            print 'Step_1() Test Failed'
            raise
