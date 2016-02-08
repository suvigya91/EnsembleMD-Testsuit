import time
 
def test_1():
    print 'test_1'
    time.sleep(1)
    print 'after 1 sec'
    time.sleep(1)
    print 'after 2 sec'
    time.sleep(1)
    print 'after 3 sec'
    assert 1, 'should pass'
 
def test_2():
    print 'in test_2'
    time.sleep(1)
    print 'after 1 sec'
    time.sleep(1)
    print 'after 2 sec'
    time.sleep(1)
    print 'after 3 sec'
    assert 0, 'failing for demo purposes'
