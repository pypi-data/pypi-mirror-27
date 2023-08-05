from compander import Compander
import os
import subprocess


def setup():
    with open("text.test", "w") as f:
        f.write("Hello World")


def teardown():
    for f in ["text.test", "text.test.bz2", "text.test.gz", "text.test.uncompressed"]:
        try:
            os.remove(f)
        except:
            pass


def test_compress_bz2():
    with Compander('bz2') as c:
        c.compress("text.test", "text.test.bz2")
    out = call(["bzcat", "text.test.bz2"])
    assert out.decode() == "Hello World"


def test_uncompress_bz2():
    with Compander('bz2') as c:
        c.compress("text.test", "text.test.bz2")
        c.uncompress("text.test.bz2", "text.test.uncompressed")
    with open("text.test.uncompressed", "rb") as f:
        out = f.read()
    assert out.decode() == "Hello World"


def test_compress_gz():
    with Compander('gz') as c:
        c.compress("text.test", "text.test.gz")
    out = call(["zcat", "text.test.gz"])
    assert out.decode() == "Hello World"


def test_uncompress_gz():
    with Compander('gz') as c:
        c.compress("text.test", "text.test.gz")
        c.uncompress("text.test.gz", "text.test.uncompressed")
    with open("text.test.uncompressed", "rb") as f:
        out = f.read()
    assert out.decode() == "Hello World"


def call(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    if proc.returncode and proc.returncode != 0:
        raise Exception("Nonzero return code: {}".format(proc.returncode))
    return proc.communicate()[0]
