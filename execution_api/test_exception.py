#---------------------------------------------------------------------------
#
#This testcase tests Exceptions thrown by EnsembleMD Kernel
#1. TypeError
#2. FileError
#3. ArgumentError
#4. NoKernelPluginError
#5. NoKernelConfigurationError
#
#---------------------------------------------------------------------------

import os
import sys
import glob
import pytest
import radical.ensemblemd

#------------------------------------------------------------------------------
#Tests TypeError
def test_TypeError():
    from radical.ensemblemd import Kernel
    from radical.ensemblemd.exceptions import TypeError
    try:
        Kernel(name=1)
    except TypeError, er:
        print '--->',er
        assert "Expected (base) type <type 'str'>, but got <type 'int'>." in er
        #raise


#------------------------------------------------------------------------------
#Tests FileError
def test_FileError():
    from radical.ensemblemd.exceptions import FileError
    path = '/File/doesnot/exist'
    if os.path.isfile(path) is False:
	assert "File /File/doesnot/exist doesn't exist." in FileError("File {0} doesn't exist.".format(path))


#------------------------------------------------------------------------------
#Test ArgumentError
def test_ArgumentError():
    from radical.ensemblemd import Kernel
    from radical.ensemblemd.exceptions import ArgumentError
    try:
        k = Kernel(name="misc.hello")
        k.arguments = ["a"]
    except ArgumentError, er:
        print '--->',er
        assert "Invalid argument(s) for kernel 'misc.hello': Unknown / malformed argument 'a'. Valid arguments are {'--file=': {'_value': None, 'mandatory': True, 'description': 'The input file.', '_is_set': False}}." \
               in er
        #raise
    

#------------------------------------------------------------------------------
#Tests NoKernelPluginError
def test_NoKernelPluginError():
    from radical.ensemblemd import Kernel
    from radical.ensemblemd.exceptions import NoKernelPluginError
    try:
        Kernel(name="random")
    except NoKernelPluginError, er:
        print '--->',er
        assert "Couldn't find a kernel plug-in named 'random'" in er
        #raise


#-------------------------------------------------------------------------------
#Tests NoKernalConfigurationError
def test_NoKernelConfigurationError():
    from radical.ensemblemd.exceptions import NoKernelConfigurationError
    
    _KERNEL_INFO = {
    "name":         "misc.ccount",
    "description":  "Counts the character frequency in an ASCII file.",
    "machine_configs": {
        "*": {
            "environment"   : None,
            "pre_exec"      : None,
            "executable"    : "uniq",
            "uses_mpi"      : False
             }
    }
    }
    resource_key = "random"
    if resource_key not in _KERNEL_INFO["machine_configs"]:
	if "hi" in _KERNEL_INFO["machine_configs"]:
		resource_key = "*"
	else:
		assert "Kernel 'misc.ccount' doesn not have a configuration entry for resource key 'random'." in NoKernelConfigurationError(kernel_name=_KERNEL_INFO["name"], resource_key=resource_key)
    

