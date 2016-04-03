
#---------------------------------------------------------------------------
#
#This testcase tests Execution context Apis:
# 1. test import
# 2. test name
# 3. allocate() - resource allocations
# 4. run() - execute job on resource
# 5. deallocate()- deallocation of job
#
#---------------------------------------------------------------------------

import os
import sys
import glob
import pytest
import time
import radical.ensemblemd

from radical.ensemblemd.exceptions import TypeError
from radical.ensemblemd.tests.helpers import _exception_test_helper


class _TestRun(radical.ensemblemd.Pipeline):

      def __init__(self, steps,instances):
             radical.ensemblemd.Pipeline.__init__(self, steps,instances)

      def step_1(self, instance):
            k = radical.ensemblemd.Kernel(name="misc.hello")
            k.arguments = ["--file=output.txt"]
            return k


@pytest.fixture(scope="class")
def enmd_setup():
    from radical.ensemblemd import SingleClusterEnvironment
    try:
        sec = SingleClusterEnvironment(
            resource="local.localhost",
            cores=1,
            walltime=1,
            database_url='mongodb://suvigya:temp123@ds051585.mongolab.com:51585',
            database_name='rutgers_thesis'
            )
        ret_allocate = sec.allocate(wait=True)
        ret_deallocate = False
        ret_deallocate= sec.deallocate()

    except Exception as e:
        print 'test failed'
        raise

    return ret_allocate,ret_deallocate

@pytest.fixture(scope="class")
def enmd_setup_run(request):
    from radical.ensemblemd import SingleClusterEnvironment
    try:
        sec = SingleClusterEnvironment(
            resource="local.localhost",
            cores=1,
            walltime=1,
            database_url='mongodb://suvigya:temp123@ds051585.mongolab.com:51585',
            database_name='rutgers_thesis'
            )
        test = _TestRun(steps=1,instances=1)
        ret_allocate = sec.allocate()
        ret_run = sec.run(test)
        ret_deallocate = sec.deallocate()
    except Exception as e:
        print ret_run
        raise
    return ret_allocate,ret_run,ret_deallocate
    

#--------------------------------------------------------
class TestSingleClusterEnvironmentApi(object):
    #----------------------------------------------------
    #Test import
    def test_import(self):
        from radical.ensemblemd import SingleClusterEnvironment
        from radical.ensemblemd.exceptions import TypeError

    #------------------------------------------------------
    #Test Name
    def test_name(self):
        from radical.ensemblemd import SingleClusterEnvironment
        sec = SingleClusterEnvironment(
            resource="local.localhost",
            cores=1,
            walltime=1,
            database_url='mongodb://localhost:27017',
            database_name='dbname'
            )
        assert sec.name == 'Static'

    #-----------------------------------------------------
    #Test allocate()
    def test_allocate(self,enmd_setup):
        ret_allocate,ret_deallocate = enmd_setup
        assert (ret_allocate == True)

    #-----------------------------------------------------
    #Test deallocate()
    def test_deallocate(self,enmd_setup):
        ret_allocate,ret_deallocate = enmd_setup
        assert (ret_deallocate == True)
        
    #-----------------------------------------------------
    #Test run()
    #TODO: What does run() return?
    def test_run(self,enmd_setup_run):
        ret_allocate,ret_run,ret_deallocate = enmd_setup_run
        #pass
        assert ret_run == True
       
 

        
##def func(x):
##        return x + 1
##
##def test_answer():
##        assert func(3) == 5
##                #pass
