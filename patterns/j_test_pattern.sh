CWD=$HOME"/EnsembleMDTesting"
PWD=$CWD"/patterns"
RWD=$CWD"/reports"
#CWD="/home/suvigya/radical.ensemblemd-master/tests/tests/patterns"

py.test ./patterns/test_pipeline_api.py --junitxml=$RWD/pattern_api.xml --html=$RWD/pattern_api.html

