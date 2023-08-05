import bz2
import gzip
import shutil


class Compander(object):

    formats = {
        'bz2': bz2.BZ2File,
        'gz': gzip.open
    }

    def __init__(self, format='bz2'):
        self.compressor = self.formats[format]

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def compress(self, src, dst):
        with self.compressor(dst, 'wb') as output:
            with open(src, 'rb') as input:
                shutil.copyfileobj(input, output)

    def uncompress(self, src, dst):
        with self.compressor(src, 'rb') as input:
            with open(dst, 'wb') as output:
                shutil.copyfileobj(input, output)
