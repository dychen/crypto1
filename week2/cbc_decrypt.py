import binascii
from Crypto.Cipher import AES

def decrypt(k, ct):
    pt = ''
    kdec = k.decode('hex')
    iv = ct[:AES.block_size * 2]
    ctmsg = ct[AES.block_size * 2:]
    prp = AES.new(kdec, AES.MODE_ECB)
    prev = iv
    i = 0
    while i < len(ctmsg):
        ctblock = ctmsg[i:i + AES.block_size * 2]
        blk = prp.decrypt(ctblock.decode('hex'))
        pt += binascii.unhexlify(hex(long(blk.encode('hex'), 16) ^ long(prev, 16))[2:-1])
        prev = ctblock
        i += AES.block_size * 2
    return pt

if __name__ == '__main__':
    k = raw_input("Enter key (in hex): ")
    ct = raw_input("Enter ciphertext (in hex): ")
    m = decrypt(k, ct)
    print "Decrypted plaintext is: "
    print m
