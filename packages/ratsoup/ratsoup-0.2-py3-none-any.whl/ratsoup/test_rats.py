import sys
from .rats import main

def setup_function(function):
    print ("setting up %s" % function)

def test_func1():
    assert True

def test_myoutput(capsys): # or use "capfd" for fd-level
    # print ("hello")
    sys.stderr.write("world\n")
    out, err = capsys.readouterr()
    import pdb; pdb.set_trace()
    assert out == "hello\n"
    assert err == "world\n"
    print("next")
    out, err = capsys.readouterr()
    assert out == "next\n"
