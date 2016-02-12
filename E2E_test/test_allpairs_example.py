#!/usr/bin/env python
#---------------------------------------------------------------------------
#
#This testcase tests AllPairs pattern end to end.
#
#---------------------------------------------------------------------------

import math
import sys
import os
import json
import pytest

from radical.ensemblemd import Kernel
from radical.ensemblemd import AllPairs
from radical.ensemblemd import EnsemblemdError
from radical.ensemblemd import SingleClusterEnvironment


# ------------------------------------------------------------------------------
#
class _TestRandomAP(AllPairs):
    def __init__(self,set1elements, windowsize1, set2elements=None, windowsize2=None):
        AllPairs.__init__(self, set1elements=set1elements,windowsize1=windowsize1,
            set2elements=set2elements,windowsize2=windowsize2)


    def set1element_initialization(self,element):
        # Creating an ASCII file by using the misc.mkfile kernel. Each file represents
        # a element of the set.
        print "Creating Element {0}".format(element)
        k = Kernel(name = "misc.mkfile")
        k.arguments = ["--size=10000", "--filename=asciifile_{0}.dat".format(element)]
        return k

    def set2element_initialization(self,element):
        # Creating an ASCII file by using the misc.mkfile kernel. Each file represents
        # a element of the set.
        print "Creating Element {0}".format(element)
        k = Kernel(name = "misc.mkfile")
        k.arguments = ["--size=10000", "--filename=newfile_{0}.dat".format(element)]
        return k

    def element_comparison(self, elements1, elements2):
        input_filename1 = "asciifile_{0}.dat".format(elements1[0])
        input_filename2 = "newfile_{0}.dat".format(elements2[0])
        output_filename = "comparison_{0}_{1}.log".format(elements1[0], elements2[0])
        print "\nComparing {0} with {1}. Saving result in {2}".format(input_filename1,input_filename2,output_filename)

        # Compare the previously generated files with the misc.diff kernel and
        # write the result of each comparison to a specific output file.

        k = Kernel(name="misc.diff")
        k.arguments            = ["--inputfile1={0}".format(input_filename1),
                                  "--inputfile2={0}".format(input_filename2),
                                  "--outputfile={0}".format(output_filename)]

        # Download the result files.
        k.download_output_data = output_filename
        return k

# ------------------------------------------------------------------------------
#
class TestAllPairs():
    def test_all_pairs_remote(self,cmdopt):
#if __name__ == "__main__":


    # use the resource specified as argument, fall back to localhost
        resource = cmdopt
        try:

            with open('/home/suvigya/radical.ensemblemd-master/tests/tests/config.json') as data_file:    
                config = json.load(data_file)
            print 'project: ', config[resource]['project']
            print 'username: ',config[resource]['username']
            # Create a new static execution context with one resource and a fixed
            # number of cores and runtime.
            cluster = SingleClusterEnvironment(
                            resource=resource,
                            cores=1,
                            walltime=15,
                            username=config[resource]['username'],

                            project=config[resource]['project'],
                            access_schema = config[resource]['schema'],
                            queue = config[resource]['queue'],

                            database_url='mongodb://suvigya:temp123@ds051585.mongolab.com:51585',
                            database_name='rutgers_thesis',
            )

            # Allocate the resources.
            cluster.allocate()

            # For example the set has 5 elements.
            ElementsSet1 = range(1,2)
            randAP = _TestRandomAP(set1elements=ElementsSet1,windowsize1=1)

            cluster.run(randAP)

            cluster.deallocate()
            print "Pattern Execution Completed Successfully! Result files are downloaded!"
            assert os.path.isfile("./comparison_1_1.log")
            os.remove("./comparison_1_1.log")
            
        except EnsemblemdError, er:

            print "Ensemble MD Toolkit Error: {0}".format(str(er))
            raise # Just raise the execption again to get the backtrace
