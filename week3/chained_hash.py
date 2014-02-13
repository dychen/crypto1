# Implements backwards SHA256 on chaining on file blocks.

import os
from Crypto.Hash import SHA256

BLOCKSIZE = 1024
TEST_FILE = r'6 - 2 - Generic birthday attack (16 min).mp4'
TARGET_FILE = r'6 - 1 - Introduction (11 min).mp4'
filename = TARGET_FILE

def chash(f, size):
    fp = size / BLOCKSIZE * BLOCKSIZE
    if fp == BLOCKSIZE:
        fp -= BLOCKSIZE
    block_hash = ''
    # Read through the file backwards
    while fp >= 0:
        f.seek(fp)
        block = f.read(BLOCKSIZE)
        h = SHA256.new(block + block_hash)
        block_hash = h.digest()
        fp -= BLOCKSIZE
    return str.encode(block_hash, 'hex')

if __name__ == '__main__':
    f = open(filename)
    size = os.path.getsize(filename)
    h0 = chash(f, size)
    print "Hash of the first block (h0) is: " + h0
    f.close()
