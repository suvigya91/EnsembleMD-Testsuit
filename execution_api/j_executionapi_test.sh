CWD=$HOME"/REnsembleMDTesting"
EXWD=$CWD"/execution_api"
RWD=$CWD"/reports"

py.test ./execution_api/test_*.py 
#--junitxml=$RWD/execution_api.xml --html=$RWD/execution_api.html

