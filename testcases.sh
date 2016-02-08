py.test test_execution_context_api.py --html=./reports/execution_context_api_results.html --junitxml=./reports/execution_context_api_results.xml

py.test ./patterns/*.py --html=./reports/patterns_result.html --junitxml=./reports/patterns_result.xml

py.test test_kernel_api.py --html=./reports/kernel_api_result.html --junitxml=./reports/kernel_api_result.xml

py.test test_copy_output_file.py --html=./reports/copy_output_result.html --junitxml=./reports/copy_output_result.xml


