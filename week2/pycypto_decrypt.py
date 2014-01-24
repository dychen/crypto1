from Crypto.Cipher import AES
from Crypto.Util import Counter

def decrypt(mode, k, ct):
    kdec = k.decode('hex')
    ctdec = ct.decode('hex')
    ivdec = ct[:AES.block_size * 2].decode('hex')
    ivint = long(ct[:AES.block_size * 2], 16)
    if mode == "cbc":
        aes = AES.new(kdec, AES.MODE_CBC, ivdec)
    elif mode == "ctr":
        # Implementation note:
        # Subtract 1 from IV because pycrypto implementation increments counter before ECB.
        ctr = Counter.new(AES.block_size * 8, initial_value=ivint-1)
        aes = AES.new(kdec, AES.MODE_CTR, counter=ctr)
    else:
        raise ValueError("Invalid input (make sure encryption mode input is either cbc or ctr).")
    return aes.decrypt(ctdec)[16:]

if __name__ == '__main__':
    mode = raw_input("Enter encryption mode (cbc or ctr): ")
    k = raw_input("Enter key (in hex): ")
    ct = raw_input("Enter ciphertext (in hex): ")
    m = decrypt(mode, k, ct)
    print "Decrypted plaintext is: "
    print m
