
#---------------------------------------------------------------------------
#
#This testcase tests Pipeline pattern end to end.
#
#---------------------------------------------------------------------------


import sys
import os
import json

from radical.ensemblemd import Kernel
from radical.ensemblemd import Pipeline
from radical.ensemblemd import EnsemblemdError
from radical.ensemblemd import SingleClusterEnvironment


class _TestPipeline(Pipeline):

      def __init__(self, steps,instances):
             Pipeline.__init__(self, steps,instances)

      def step_1(self, instance):
            k = Kernel(name="misc.hello")
            k.upload_input_data = ['./input_file.txt > temp.txt']
            k.arguments = ["--file=temp.txt"]
            k.download_output_data = ['./temp.txt > /home/suvigya/radical.ensemblemd-master/tests/tests/temp_results/remote_file.txt']
            return k

class TestPipelinePattern():
    def test_pipeline_remote(self,cmdopt):
#if __name__ == "__main__":
        resource = cmdopt
        try:

            with open('/home/suvigya/radical.ensemblemd-master/tests/tests/config.json') as data_file:    
                  config = json.load(data_file)
            #resource='xsede.stampede'
            print "project: ",config[resource]['project']
            print "username: ", config[resource]['username'] 
            # Create a new static execution context with one resource and a fixed
            # number of cores and runtime.
            cluster = SingleClusterEnvironment(
                        resource=resource,
                        cores=1,
                        walltime=15,
                        #username='tg831932',
                        username=config[resource]['username'],
                        #project="TG-MCB090174",
                        #access_schema="ssh",
                        #queue="development",
                        project=config[resource]['project'],
                        access_schema = config[resource]['schema'],
                        queue = config[resource]['queue'],

                        database_url='mongodb://suvigya:temp123@ds051585.mongolab.com:51585',
                        database_name='rutgers_thesis',
                  )

            os.system('/bin/echo remote > input_file.txt')

            # Allocate the resources.
            cluster.allocate()

            # Set the 'instances' of the pipeline to 1. This means that 1 instance
            # of each pipeline step is executed.
            app = _TestPipeline(steps=1,instances=1)

            cluster.run(app)

            # Deallocate the resources. 
            cluster.deallocate()
            f = open("/home/suvigya/radical.ensemblemd-master/tests/tests/temp_results/remote_file.txt")
            print "Name of file: ", f.name
            print "file closed or not: ", f.closed
            fname = f.readline().split()
            print "fname: ", fname
            assert fname == ['remote']
            f.close()
            os.remove("/home/suvigya/radical.ensemblemd-master/tests/tests/temp_results/remote_file.txt")

        except EnsemblemdError, er:

            print "Ensemble MD Toolkit Error: {0}".format(str(er))
            raise # Just raise the execption again to get the backtrace


    #------------------------------------------------------------------------
    #def test_pipeline
        
