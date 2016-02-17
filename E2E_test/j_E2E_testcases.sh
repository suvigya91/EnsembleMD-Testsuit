CWD=$HOME"/EnsembleMDTesting"
E2EWD=$CWD"/E2E_test"
RWD=$CWD"/reports"


#py.test $E2EWD/test_*.py --cmdopt=xsede.gordon --junitxml=$RWD/e2e_remote_gordon.xml --html=$RWD/e2e_remote_gordon.html

py.test ./E2E_tests/test_j_pipeline_E2E.py --cmdopt=xsede.stampede #--junitxml=$RWD/e2e_remote_stampede.xml --html=$RWD/e2e_remote_stampede.html
py.test ./E2E_tests/test_j_allpairs_example.py --cmdopt=xsede.stampede
py.test ./E2E_tests/test_j_replicaexchange_E2E.py --cmdopt=xsede.stampede
py.test ./E2E_tests/test_j_simulation_analysis_loop.py --cmdopt=xsede.stampede



