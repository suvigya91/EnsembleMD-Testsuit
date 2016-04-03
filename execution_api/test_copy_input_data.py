
#---------------------------------------------------------------------------
#
#This testcase tests:
# 1. upload_input_data api from Kernal
# 2. download_output_data api from Kernel
#---------------------------------------------------------------------------


import os
import sys
import glob
import json
import pytest
import time
import radical.ensemblemd


from radical.ensemblemd import SingleClusterEnvironment
from radical.ensemblemd.exceptions import TypeError
from radical.ensemblemd.tests.helpers import _exception_test_helper

#export RADICAL_PILOT_AGENT_CONFIG="$HOME/radical.pilot-devel/src/radical/pilot/configs/agent_default.json"

class _TestMyApp(radical.ensemblemd.Pipeline):

      def __init__(self, steps, instances):#, copy_directives, checksum_inputfile, download_output):
             radical.ensemblemd.Pipeline.__init__(self,steps,instances)
##             self._copy_directives = copy_directives
##             self._checksum_inputfile = checksum_inputfile
##             self._download_output = download_output


      def step_1(self, instance):
##            k = radical.ensemblemd.Kernel(name="misc.chksum")
##            k.arguments            = ["--inputfile={0}".format(self._checksum_inputfile), "--outputfile={0}".format(self._download_output)]
##            k.copy_input_data      = self._copy_directives
##            k.download_output_data = self._download_output

            k = radical.ensemblemd.Kernel(name="misc.hello")
            k.upload_input_data = ['./input_file.txt > temp.txt']
            k.arguments = ["--file=temp.txt"]
            k.download_output_data = ['./temp.txt > ./output_file.txt']
            return k

class TestCopyInputData():
      def test_copy_input_data_single(self):
#if __name__ == '__main__':

          #resource = 'local.localhost'
          try:

              with open('%s/config.json'%os.path.dirname(os.path.abspath(__file__))) as data_file:    
                    config = json.load(data_file)

                  # Create a new static execution context with one resource and a fixed
                  # number of cores and runtime.
              
              cluster = SingleClusterEnvironment(
                              resource='xsede.stampede',
                              cores=1,
                              walltime=15,
                              #username=None,
	    		      username='tg831932',
	    		      project='TG-MCB090174',
	    		      access_schema='ssh',
	    		      queue='development',

                              #project=config[resource]['project'],
                              #access_schema = config[resource]['schema'],
                              #queue = config[resource]['queue'],

                              database_url='mongodb://suvigya:temp123@ds051585.mlab.com:51585/rutgers_thesis'
                        )

              os.system('/bin/echo passwd > input_file.txt')

                  # Allocate the resources.
              cluster.allocate(wait=True)

                  # Set the 'instances' of the pipeline to 1. This means that 1 instance
                  # of each pipeline step is executed.
      ##        app = _TestMyApp(instances=1,
      ##                         copy_directives="/etc/passwd",
      ##                         checksum_inputfile="passwd",
      ##                         download_output="CHKSUM_1"
      ##                         )
              app = _TestMyApp(steps=1,instances=1)
              cluster.run(app)
              f = open("./output_file.txt")
              print "Name of file: ", f.name
              print "file closed or not: ", f.closed
              fname = f.readline().split()
              print "fname: ", fname
              cluster.deallocate()
              assert fname == ['passwd']
              f.close()
              os.remove("./output_file.txt")

          except Exception as er:
              print "Ensemble MD Toolkit Error: {0}".format(str(er))
              raise # Just raise the execption again to get the backtrace
