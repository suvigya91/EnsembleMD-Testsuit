#---------------------------------------------------------------------------
#
#This testcase tests Replica Exchange pattern end to end.
#
#---------------------------------------------------------------------------


import os
import sys
import json
import math
import time
import random
import pprint
import optparse
import datetime
import pytest
import radical.pilot
from os.path import expanduser

from radical.ensemblemd import Kernel
from radical.ensemblemd import EnsemblemdError
from radical.ensemblemd import SingleClusterEnvironment
from radical.ensemblemd.patterns.replica_exchange import Replica
from radical.ensemblemd.patterns.replica_exchange import ReplicaExchange

#-------------------------------------------------------------------------------
#

class _TestReplicaP(Replica):
    def __init__(self, my_id, cores=1):
        self.id = int(my_id)
        self.cores = int(cores)
        self.parameter = random.randint(300, 600)
        self.cycle = 0

        super(_TestReplicaP, self).__init__(my_id)

class _TestRePattern(ReplicaExchange):
    def __init__(self, workdir_local=None):
        # hardcoded name of the input file base
        self.inp_basename = "md_input"
        # number of replicas to be launched during the simulation
        self.replicas = None
        # number of cycles the simulaiton will perform
        self.nr_cycles = None

        self.workdir_local = workdir_local

        super(_TestRePattern, self).__init__()

    # --------------------------------------------------------------------------
    #
    def initialize_replicas(self):
        try:
            self.replicas+1
        except:
            print "Ensemble MD Toolkit Error: Number of replicas must be \
            defined for pattern ReplicaExchange!"
            raise


        replicas = []
        N = self.replicas
        for k in range(N):
            r = _TestReplicaP(k)
            replicas.append(r)

        return replicas

    # --------------------------------------------------------------------------
    #
    def build_input_file(self, replica):
        file_name = self.inp_basename + "_" + \
                    str(replica.id) + "_" + \
                    str(replica.cycle) + ".md"

        fo = open(file_name, "wb")
        for i in range(1,500):
            fo.write(str(random.randint(i, 500) + i*2.5) + " ");
            if i % 10 == 0:
                fo.write(str("\n"));
        fo.close()

    # --------------------------------------------------------------------------
    #
    def prepare_replica_for_md(self, replica):
        input_name = self.inp_basename + "_" + \
                     str(replica.id) + "_" + \
                     str(replica.cycle) + ".md"
        output_name = self.inp_basename + "_" + \
                      str(replica.id) + "_" + \
                      str(replica.cycle) + ".out"

        k = Kernel(name="misc.ccount")
        k.arguments            = ["--inputfile=" + input_name, 
                                  "--outputfile=" + output_name]
        k.upload_input_data      = input_name
        k.download_output_data = output_name
        k.cores = 1

        replica.cycle = replica.cycle + 1
        return k

    # --------------------------------------------------------------------------
    #
    def prepare_replica_for_exchange(self, replica):
        pass

    #---------------------------------------------------------------------------
    #
    def exchange(self, r_i, replicas, swap_matrix):
        return random.choice(replicas)

    #---------------------------------------------------------------------------
    #
    def get_swap_matrix(self, replicas):
        # init matrix
        swap_matrix = [[ 0. for j in range(len(replicas))]
            for i in range(len(replicas))]

        return swap_matrix

    #---------------------------------------------------------------------------
    #
    def perform_swap(self, replica_i, replica_j):
        param_i = replica_i.parameter
        replica_i.parameter = replica_j.parameter
        replica_j.parameter = param_i

# ------------------------------------------------------------------------------
#


class TestReplicaExchangePattern():
    def test_replica_exchange(self,cmdopt):
#if __name__ == "__main__":
        resource = cmdopt
        home = expanduser("~")
        try:

            with open('%s/workspace/EnsembleMDTesting/config.json'%home) as data_file:    
                config = json.load(data_file)

            print 'Project: ',config[resource]['project']
            print 'Username: ',config[resource]['username']
            # Create a new static execution context with one resource and a fixed
            # number of cores and runtime.

            workdir_local = os.getcwd()
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

            # creating RE pattern object
            re_pattern = _TestRePattern(workdir_local)

            # set number of replicas
            re_pattern.replicas = 2
     
            # set number of cycles
            re_pattern.nr_cycles = 1

            # initializing replica objects
            replicas = re_pattern.initialize_replicas()

            re_pattern.add_replicas( replicas )

            # run RE simulation
            cluster.run(re_pattern, force_plugin="replica_exchange.static_pattern_1")

            cluster.deallocate()
            
            print "RE simulation finished!"
            print "Simulation performed {0} cycles for {1} replicas. In your working directory you should".format(re_pattern.nr_cycles, re_pattern.replicas)
            print "have {0} md_input_x_y.md files and {0} md_input_x_y.out files where x in {{0,1,2,...{1}}} and y in {{0,1,...{2}}}.".format( (re_pattern.nr_cycles*re_pattern.replicas), (re_pattern.replicas-1), (re_pattern.nr_cycles-1) )
            print ".md file is replica input file and .out is output file providing number of occurrences of each character."

            assert os.path.isfile("./md_input_0_0.out") and os.path.isfile("./md_input_1_0.out")
            os.remove("./md_input_0_0.out")
            os.remove("./md_input_0_0.md")
            os.remove("./md_input_1_0.out")
            os.remove("./md_input_1_0.md")

        except EnsemblemdError, er:

            print "Ensemble MD Toolkit Error: {0}".format(str(er))
            raise # Just raise the execption again to get the backtrace
