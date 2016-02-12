CWD=$HOME"/radical.ensemblemd-master/tests/tests"
EXWD=$CWD"/execution_api"
RWD=$CWD"/reports"

py.test $EXWD/test_*.py --junitxml=$RWD/execution_api.xml --html=$RWD/execution_api.html

