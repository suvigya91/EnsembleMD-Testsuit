CWD=$HOME"/EnsembleMDTesting"
PWD=$CWD"/patterns"
RWD=$CWD"/reports"
#CWD="/home/suvigya/radical.ensemblemd-master/tests/tests/patterns"

py.test $PWD/test_*.py --junitxml=$RWD/pattern_api.xml --html=$RWD/pattern_api.html

