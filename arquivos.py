import os
import mmap

def makeEmptyBin(filename, size):
    with open(filename, 'wb') as f:
        for i in xrange(size):
            f.seek(i)
            f.write(b'\xff')
        f.close()


def memory_map(filename, access=mmap.ACCESS_WRITE):
    size = os.path.getsize(filename)
    fd = os.open(filename, os.O_RDWR)
    return mmap.mmap(fd, size, access=access)
