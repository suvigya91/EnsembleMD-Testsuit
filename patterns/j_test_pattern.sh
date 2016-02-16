CWD=$HOME"/EnsembleMDTesting"
PWD=$CWD"/patterns"
RWD=$CWD"/reports"
#CWD="/home/suvigya/radical.ensemblemd-master/tests/tests/patterns"

#py.test --cov-report xml --cov=. 
py.test ./patterns/test_pipeline_api.py

#EnsembleMD testing framework
#MS Thesis May 2016

