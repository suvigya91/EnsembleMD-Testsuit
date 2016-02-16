#---------------------------------------------------------------------------
#
#This testcase tests AllPair Pattern APIs
#1. import
#2. name
#3. add_replicas()
#4. initialize_replica()
#5. build_input_file()
#6. get_swap_matrix()
#7. perform_swap()
#8. prepare_replica_for_md()
#9. prepare_replica_for_exchange()
#10. exchange()
#
#---------------------------------------------------------------------------

import os
import sys
import glob
import pytest
import math
import random
import radical.ensemblemd

from radical.ensemblemd.exceptions import NotImplementedError

#----------------------------------------
#
class _TestReplicaP(radical.ensemblemd.patterns.replica_exchange.Replica):
    def __init__(self, my_id, cores=1):
        self.id = int(my_id)
        self.cores = int(cores)
        self.parameter = random.randint(300, 600)
        self.cycle = 0

        super(_TestReplicaP, self).__init__(my_id)

#-------------------------------------------
class _TestRePattern(radical.ensemblemd.patterns.replica_exchange.ReplicaExchange):
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
        #try:
        self.replicas+1
        #except:
        #    print "Ensemble MD Toolkit Error: Number of replicas must be \
        #    defined for pattern ReplicaExchange!"
        #    raise
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
        return file_name

    # --------------------------------------------------------------------------
    #
    def prepare_replica_for_md(self, replica):
        input_name = self.inp_basename + "_" + \
                     str(replica.id) + "_" + \
                     str(replica.cycle) + ".md"
        output_name = self.inp_basename + "_" + \
                      str(replica.id) + "_" + \
                      str(replica.cycle) + ".out"

        k = radical.ensemblemd.Kernel(name="misc.ccount")
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
        return None
        #pass

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
        print replica_i.parameter
        print replica_j.parameter
        return replica_i.parameter,replica_j.parameter

#----------------------------------------
class TestBasicApi(object):
#----------------------------------------
#testing import
    def test_import(self):
        from radical.ensemblemd import ReplicaExchange

#-----------------------------------------
#Test pattern name
    def test_pattern_name(self):
        from radical.ensemblemd import ReplicaExchange

        re_pattern = ReplicaExchange()
        assert re_pattern.name == 'ReplicaExchange'


#-----------------------------------------
#Test pattern add_replica/get_replica
    def test_add_replicas(self):
        from radical.ensemblemd import ReplicaExchange
        from radical.ensemblemd.patterns.replica_exchange import Replica

        replica = Replica(8)
        re_pattern = ReplicaExchange()
        re_pattern.add_replicas(replica)
        assert re_pattern.get_replicas()== replica


class TestNotImplemented(object):
#-----------------------------------------
#Test pattern initialize_replica not implemented
    def test_pattern_initialize_replicas_not_implemented(self):
        from radical.ensemblemd import ReplicaExchange

        re_pattern = ReplicaExchange()
        with pytest.raises(NotImplementedError):
            re_pattern.initialize_replicas()


#-----------------------------------------
#Test pattern build_input_replica not implemented
    def test_build_input_file_not_implemented(self):
        from radical.ensemblemd import ReplicaExchange
        from radical.ensemblemd.patterns.replica_exchange import Replica

        replica = Replica(8)
        re_pattern = ReplicaExchange()
        with pytest.raises(NotImplementedError):
            re_pattern.build_input_file(replica)



#-----------------------------------------
#Test pattern get_swap_matrix not implemented
    def test_get_swap_matrix_not_implemented(self):
        from radical.ensemblemd import ReplicaExchange
        from radical.ensemblemd.patterns.replica_exchange import Replica
        temp = range(1,3)
        replica = Replica(8)
        re_pattern = ReplicaExchange()
        with pytest.raises(NotImplementedError):
            re_pattern.get_swap_matrix(replica,temp)

    
#-----------------------------------------
#Test pattern perform_swap not implemented
    def test_perform_swap_not_implemented(self):
        from radical.ensemblemd import ReplicaExchange
        from radical.ensemblemd.patterns.replica_exchange import Replica
        replica_i = Replica(8)
        replica_j = Replica(8)
        re_pattern = ReplicaExchange()
        with pytest.raises(NotImplementedError):
            re_pattern.perform_swap(replica_i,replica_j)

#-----------------------------------------
#Test pattern prepare_replica_for_md not implemented
    def test_prepare_replica_for_md_not_implemented(self):
        from radical.ensemblemd import ReplicaExchange
        from radical.ensemblemd.patterns.replica_exchange import Replica
        replica = Replica(8)
        re_pattern = ReplicaExchange()
        with pytest.raises(NotImplementedError):
            re_pattern.prepare_replica_for_md(replica)


#-----------------------------------------
#Test pattern prepare_replica_for_exchange not implemented
    def test_prepare_replica_for_exchange_not_implemented(self):
        from radical.ensemblemd import ReplicaExchange
        from radical.ensemblemd.patterns.replica_exchange import Replica
        replica = Replica(8)
        re_pattern = ReplicaExchange()
        with pytest.raises(NotImplementedError):
            re_pattern.prepare_replica_for_exchange(replica)

#-------------------------------------------------
#TODO : check if correct
#Test pattern exchange not implemented
    def test_exchange_not_implemented(self):
        from radical.ensemblemd import ReplicaExchange
        from radical.ensemblemd.patterns.replica_exchange import Replica
        replicas = []
        temp = range(1,3)
        for k in range(8):
            r = Replica(k)
            replicas.append(r)
        replica = Replica(8)
        re_pattern = ReplicaExchange()
        with pytest.raises(NotImplementedError):
            re_pattern.exchange(replica,replicas,temp)


#---------------------------------------------------
#
class TestImplemented():
    #-----------------------------------------------
    #Test initialize_replica()
    def test_initialize_replica(self):
        re_pattern = _TestRePattern()
        re_pattern.replicas = 8
        assert len(re_pattern.initialize_replicas()) > 0
        #assert re_pattern.initialize_replicas() is not None

    #-----------------------------------------------
    #Test build_input_file
    def test_build_input_file(self):
        replica = _TestReplicaP(8)
        re_pattern = _TestRePattern()
        file_name = re_pattern.build_input_file(replica)
        assert os.path.isfile('./md_input_8_0.md') and os.path.getsize('./md_input_8_0.md') > 0

    #------------------------------------------------
    #Test get_swap_matrix
    def test_get_swap_matrix(self):
        replica1 = _TestReplicaP(1)
        replica2 = _TestReplicaP(2)
        replica3 = _TestReplicaP(3)
        replicas = [replica1, replica2, replica3]
        
        re_pattern = _TestRePattern()
        swap_matrix = re_pattern.get_swap_matrix(replicas)
        assert len(swap_matrix) > 0
        #assert swap_matrix is not None

    #-------------------------------------------------
    #Test perform_swap
    def test_perform_swap(self):
        replica_i = _TestReplicaP(1)
        replica_j = _TestReplicaP(2)
        re_pattern = _TestRePattern()
        
        param_i = replica_i.parameter
        param_j = replica_j.parameter
        
        ret_i, ret_j = re_pattern.perform_swap(replica_i,replica_j)
        assert (param_i == ret_j) and (param_j == ret_i)

    #-----------------------------------------------------
    #Test prepare_replica_for_md
    def test_prepare_replica_for_md(self):
        replica = _TestReplicaP(1)
        re_pattern = _TestRePattern()
        assert type(re_pattern.prepare_replica_for_md(replica)) == radical.ensemblemd.Kernel
        
    #------------------------------------------------------
    #Test prepare_replica_for_exchange
    #TODO: Check
    def test_prepare_replica_for_exchange(self):
        replica = _TestReplicaP(1)
        re_pattern = _TestRePattern()
        assert re_pattern.prepare_replica_for_exchange(replica) is None

    #-------------------------------------------------------
    #Test exchange()
    def test_exchange(self):
        replica1 = _TestReplicaP(1)
        replica2 = _TestReplicaP(2)
        replica3 = _TestReplicaP(3)
        replica_i = _TestReplicaP(4)
        replicas = [replica1, replica2, replica3]
        
        re_pattern = _TestRePattern()
        swap_matrix = re_pattern.get_swap_matrix(replicas)
        assert re_pattern.exchange(replica_i,replicas,swap_matrix) is not None        
