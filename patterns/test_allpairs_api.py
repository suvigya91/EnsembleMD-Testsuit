
#---------------------------------------------------------------------------
#
#This testcase tests AllPair Pattern APIs
#1. import
#2. name
#3. permutation
#4. set1_elements
#5. set2_elements
#6. set1_initialization()
#7. set2_initialization()
#8. element_comparision()
#
#---------------------------------------------------------------------------


import os
import sys
import glob
import pytest
import math
import radical.ensemblemd

from radical.ensemblemd.exceptions import NotImplementedError

#-----------------------------------------------------------
class _TestAllPairs(radical.ensemblemd.AllPairs):
    def __init__(self,set1elements, windowsize1, set2elements=None, windowsize2=None):
        radical.ensemblemd.AllPairs.__init__(self, set1elements=set1elements,windowsize1=windowsize1,
            set2elements=set2elements,windowsize2=windowsize2)
        
    def set1element_initialization(self,element):
        # Creating an ASCII file by using the misc.mkfile kernel. Each file represents
        # a element of the set.
        print "Creating Element {0}".format(element)
        k = radical.ensemblemd.Kernel(name = "misc.mkfile")
        k.arguments = ["--size=10000", "--filename=asciifile_{0}.dat".format(element)]
        return k

    def set2element_initialization(self,element):
        # Creating an ASCII file by using the misc.mkfile kernel. Each file represents
        # a element of the set.
        print "Creating Element {0}".format(element)
        k = radical.ensemblemd.Kernel(name = "misc.mkfile")
        k.arguments = ["--size=10000", "--filename=newfile_{0}.dat".format(element)]
        return k

    def element_comparison(self, elements1, elements2):
        input_filename1 = "asciifile_{0}.dat".format(elements1[0])
        input_filename2 = "newfile_{0}.dat".format(elements2[0])
        output_filename = "comparison_{0}_{1}.log".format(elements1[0], elements2[0])
        print "\nComparing {0} with {1}. Saving result in {2}".format(input_filename1,input_filename2,output_filename)

        # Compare the previously generated files with the misc.diff kernel and
        # write the result of each comparison to a specific output file.

        k = radical.ensemblemd.Kernel(name="misc.diff")
        k.arguments            = ["--inputfile1={0}".format(input_filename1),
                                  "--inputfile2={0}".format(input_filename2),
                                  "--outputfile={0}".format(output_filename)]

        # Download the result files.
        k.download_output_data = output_filename
        return k

#-------------------------------------------------------------


class TestBasicApi(object):
#----------------------------------------
#testing import
    def test_import(self):
        from radical.ensemblemd import AllPairs

#----------------------------------------
#Test pattern name   
    def test_pattern_name(self):
        from radical.ensemblemd import AllPairs

        ElementsSet1 = range(1,2)
        pattern = AllPairs(ElementsSet1,1)
        assert pattern.name == 'AllPairs'

#----------------------------------------
#Test permutations
#Set of 5 elements
    def test_pattern_permutatuions(self):
        from radical.ensemblemd import AllPairs

        ElementsSet1 = range(1,6)
        pattern = AllPairs(ElementsSet1,1)
        assert pattern.permutations == 10

#----------------------------------------
#Test returns list of elements from set 1
#Set of 5 elements
    def test_pattern_set_1_elements(self):
        from radical.ensemblemd import AllPairs

        ElementsSet1 = range(1,2)
        pattern = AllPairs(ElementsSet1,1)
        assert pattern.set1_elements is not None
    
#----------------------------------------
#Test returns list of elements from set 1
#Set of 5 elements
    def test_pattern_set_2_elements(self):
        from radical.ensemblemd import AllPairs

        ElementsSet1 = range(1,2)
        pattern = AllPairs(ElementsSet1,1)
        assert pattern.set2_elements is not None
    

class TestNotImplemented(object):
#----------------------------------------
#Test set 1 elements initialization not implemented exception
#Set of 5 elements
    def test_pattern_set1_initialization(self):
        from radical.ensemblemd import AllPairs

        ElementsSet1 = range(1,6)
        pattern = AllPairs(ElementsSet1,1)
        with pytest.raises(NotImplementedError):
            pattern.set1element_initialization(1)

#----------------------------------------
#Test set 2 elements initialization implemented exception
#Set of 5 elements
    def test_pattern_set2_initialization(self):
        from radical.ensemblemd import AllPairs

        ElementsSet1 = range(1,6)
        pattern = AllPairs(ElementsSet1,1)
        with pytest.raises(NotImplementedError):
            pattern.set2element_initialization(5)

#--------------------------------------------
#Test element_comparision()
    def test_element_comparision_not_implemented(self):
        from radical.ensemblemd import AllPairs
        
        elements1 =[1]
        elements2 =[1]
        ElementSet1 = range(1,6)
        pattern = AllPairs(ElementSet1,1)
        with pytest.raises(NotImplementedError):
            pattern.element_comparison(elements1,elements2)
        

#--------------------------------------------
#Test actual implementation using kernel
#TODO: check if this is right way
class TestImplemented(object):
    def test_set_1_initialization(self):
        try:
            ElementSet1 = range(1,6)
            test = _TestAllPairs(set1elements=ElementSet1,windowsize1=1)
            assert type(test.set1element_initialization(5)) == radical.ensemblemd.Kernel
        except Exception:
            print 'set1element_initialization() Test Failed'
            raise
        
    #----------------------------------------------        
    def test_set_2_initialization(self):
        try:
            ElementSet1 = range(1,6)
            test = _TestAllPairs(set1elements=ElementSet1,windowsize1=1)
            assert type(test.set2element_initialization(ElementSet1)) == radical.ensemblemd.Kernel
        except Exception:
            print 'set1element_initialization() Test Failed'
            raise

    #-----------------------------------------------    
    def test_element_comparision(self):
        try:
            ElementSet1 = range(1,6)
            test = _TestAllPairs(set1elements=ElementSet1,windowsize1=1)
            #elements1 = open("./files/asciifile_1.dat")
            #elements2 = open("./files/asciifile_2.dat")
            elements1 =[1]
            elements2 =[1]
            assert type(test.element_comparison(elements1,elements2)) == radical.ensemblemd.Kernel
        except Exception:
            print 'element_comparison() Test Failed'
            raise
