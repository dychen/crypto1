import urllib2
import sys
from multiprocessing import Process, Queue

BYTESIZE = 256      # 256 possible values: 0x00 - 0xff
BLOCKSIZE = 128 / 8 # 128 bits or 16 bytes in AES

TARGET = 'http://crypto-class.appspot.com/po?er='
QUERY = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'

CTBLOCKS = len(QUERY) / 2 / BLOCKSIZE
PTBLOCKS = CTBLOCKS - 1

def get_hexval(ctbyte, guessbyte, bytenum):
    val = int(ctbyte, 16) ^ int(guessbyte, 16) ^ bytenum
    return hex(val)[2:].zfill(2) # Convert int value to formatted hexstr.

# blocknum (int): Block number
# bytenum  (int): Byte index (1 - 16) in the block
# guess    (hex): Guess value for the target byte
# queryarr (lst): Query string list
# msgarr   (lst): List of known message bytes
def construct_query(blocknum, bytenum, guess, queryarr, msgarr):
    # queryarr[0..31]  = IV
    # queryarr[32..63] = c1
    # ...
    # queryarr[(16*2*i)..(16*2*(i+1)-1)] = ci
    # PT   :     |m1|...|m(blocknum-1)||m(blocknum)||<-rightidx
    # CT   : |IV||c1|...|c(blocknum-1)||<-rightidx ...
    # QUERY: |IV||c1|...|XXXX pad here||c(blocknum)|| DISCARD REMAINDER
    rightidx = blocknum * BLOCKSIZE
    # Pad the known bytes
    for offset in range(1, bytenum):
        #print queryarr[rightidx - offset], msgarr[rightidx - offset], bytenum, get_hexval(queryarr[rightidx - offset], msgarr[rightidx - offset], bytenum)
        queryarr[rightidx - offset] = get_hexval(queryarr[rightidx - offset], msgarr[rightidx - offset], bytenum)
    # Pad the guess byte
    queryarr[rightidx - bytenum] = get_hexval(queryarr[rightidx - bytenum], guess, bytenum)
    return ''.join(queryarr[:(blocknum + 1) * BLOCKSIZE]) # Discard extra blocks.

def query(q, first_block):
    target = TARGET + urllib2.quote(q)
    request = urllib2.Request(target)
    try:
        conn = urllib2.urlopen(request)
        conn.close()
        if first_block:
            return False # Edge case: Make sure first query is different from original.
        return True
    except urllib2.HTTPError, e:
        if e.code == 404:
            return True  # The request was correctly padded.
        return False     # The request was incorrectly padded.

def work(b, i, n, arr, msg, q):
    qmod = construct_query(b, i, n, arr, msg)
    if query(qmod, i == 1) == True:
        print "FOUND at " + str(n)
        q.put(n[2:].zfill(2)) # Convert int value to formatted hextr.

def hex_to_char(hexarr):
    return [chr(int(c, 16)) for c in hexarr]

# For a B-block PT, (B+1)-block CT:
# PT:     |m1||m2||...||mB|
# CT: |IV||c1||c2||...||cB|
# The padding oracle decrypts as follows:
# IV -> m1, b1 -> m2, b2 -> m3, ..., b(B-1) -> mB
def decrypt(s):
    # Split query string into mutable array of byte-strings
    arr = [s[i:i+2] for i in range(len(s)) if i % 2 == 0]
    msg = ['00'] * (PTBLOCKS * BLOCKSIZE)
    q = Queue()

    # Iterate backwards over blocks from block B to block 1.
    for b in range(PTBLOCKS, 0, -1):
        # Iterate over bytes in block (1-indexed).
        for i in range(1, BLOCKSIZE + 1):
            print "Block: " + str(b) + ", Idx: " + str(i)
            # Iterate over possible bytes 0x00 - 0xff.
            for n in range(BYTESIZE):
                p = Process(target = work, args = (b, i, hex(n), arr[:], msg[:], q))
                p.start()
            p.join()
            msg[b * BLOCKSIZE - i] = q.get()
    return ''.join(hex_to_char(msg))


if __name__ == "__main__":
    print "Message: " + decrypt(QUERY)
