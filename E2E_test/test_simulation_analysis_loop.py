import sys
import os
import json
import pytest

from radical.ensemblemd import Kernel
from radical.ensemblemd import SimulationAnalysisLoop
from radical.ensemblemd import EnsemblemdError
from radical.ensemblemd import SimulationAnalysisLoop
from radical.ensemblemd import SingleClusterEnvironment

# ------------------------------------------------------------------------------
#
class RandomSA(SimulationAnalysisLoop):
    def __init__(self, maxiterations, simulation_instances=1, analysis_instances=1):
        SimulationAnalysisLoop.__init__(self, maxiterations, simulation_instances, analysis_instances)

    def pre_loop(self):
        k = Kernel(name="misc.mkfile")
        k.arguments = ["--size=1000", "--filename=reference.dat"]
	k.upload_input_data = ['levenshtein.py']
        return k

    def simulation_step(self, iteration, instance):
        k = Kernel(name="misc.mkfile")
        k.arguments = ["--size=1000", "--filename=simulation-{0}-{1}.dat".format(iteration, instance)]
        return k

    def analysis_step(self, iteration, instance):
        input_filename  = "simulation-{0}-{1}.dat".format(iteration, instance)
        output_filename = "analysis-{0}-{1}.dat".format(iteration, instance)

        k = Kernel(name="misc.levenshtein")
        k.link_input_data      = ["$PRE_LOOP/reference.dat", "$SIMULATION_ITERATION_{1}_INSTANCE_{2}/{0}".format(input_filename,iteration,instance),"$PRE_LOOP/levenshtein.py"]
        k.arguments            = ["--inputfile1=reference.dat",
                                  "--inputfile2={0}".format(input_filename),
                                  "--outputfile={0}".format(output_filename)]
        k.download_output_data = output_filename
        return k

    def post_loop(self):
        pass


# ------------------------------------------------------------------------------
#
class TestSAL():
    def test_sal(self,cmdopt):
#if __name__ == "__main__":

        resource = cmdopt
        try:

            with open('/home/suvigya/radical.ensemblemd-master/tests/tests/config.json') as data_file:    
                config = json.load(data_file)

            print 'Project: ',config[resource]['project']
            print 'Username: ',config[resource]['username']
     
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

                            database_url='mongodb://suvigya:temp123@ds051585.mongolab.com:51585/rutgers_thesis',
                            #database_name='myexps',
            )

            # Allocate the resources.
            cluster.allocate()
            randomsa = RandomSA(maxiterations=1, simulation_instances=1, analysis_instances=1)
            cluster.run(randomsa)
            cluster.deallocate()


            # After execution has finished, we print some statistical information
            # extracted from the analysis results that were transferred back.
            for it in range(1, randomsa.iterations+1):
                print "\nIteration {0}".format(it)
                ldists = []
                for an in range(1, randomsa.analysis_instances+1):
                    ldists.append(int(open("analysis-{0}-{1}.dat".format(it, an), "r").readline()))
                print "   * Levenshtein Distances: {0}".format(ldists)
                print "   * Mean Levenshtein Distance: {0}".format(sum(ldists) / len(ldists))
            assert os.path.isfile("./analysis-1-1.dat")
            os.remove("./analysis-1-1.dat")
        except EnsemblemdError, er:

            print "Ensemble MD Toolkit Error: {0}".format(str(er))
            raise # Just raise the execption again to get the backtrace
