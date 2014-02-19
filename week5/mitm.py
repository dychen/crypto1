import gmpy2
from gmpy2 import mpz

p = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171
g = 11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568
h = 3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333
B = 2 ** 20

# Make a dictionary of size 2^20 + 1.
def make_hash(h, g, p, B):
    vals = {}
    for x in range(0, B+1):
        vals[gmpy2.divm(h, gmpy2.powmod(g, x, p), p)] = x
    return vals

# Check if the target value is in the hash set.
def check_inclusion(vals_dict, p, g, B):
    for x in range(0, B+1):
        val = gmpy2.powmod(g, B * x, p)
        if val in vals_dict:
            x_0 = x
            x_1 = vals_dict[val]
            return x_0 * B + x_1
    return None

# Objective: Solve the following discrete log problem for x, 1 <= x <= 2^40:
# h = g^x (mod p)
# We can rewrite this equation as:
# h / g^x_1 = g^(2^20 x_0) (mod p) where x = 2^20 x_0 + x_1
# Using a meet in the middle attack, hash all values of h / g^x_1 for 0 <= x_1 <= 2^20.
# Then, check if g^(2^20 x_0) (mod p) is in the dictionary.
def meet_in_the_middle(p, g, h, B):
    print 'Making hash table...'
    vals_dict = make_hash(h, g, p, B)
    print 'Checking for a collision...'
    print 'x: ' + str(check_inclusion(vals_dict, p, g, B))

if __name__ == '__main__':
    meet_in_the_middle(p, g, h, B)
