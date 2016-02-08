# content of test_sample.py
def test_answer(cmdopt):
    if cmdopt == "xsede.stampede":
        print ("xsede.stampede")
    elif cmdopt == "local.localhost":
        print ("local.localhost")
    assert 0 # to see what was printed
