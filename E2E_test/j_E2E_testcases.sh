CWD=$HOME"/EnsembleMDTesting"
E2EWD=$CWD"/E2E_test"
RWD=$CWD"/reports"


#py.test $E2EWD/test_*.py --cmdopt=xsede.gordon --junitxml=$RWD/e2e_remote_gordon.xml --html=$RWD/e2e_remote_gordon.html

py.test ./E2E_tests/jenkins_test/test_*.py --cmdopt=xsede.stampede #--junitxml=$RWD/e2e_remote_stampede.xml --html=$RWD/e2e_remote_stampede.html




