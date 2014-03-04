import binascii
import gmpy2

# Part 1
N1 = 179769313486231590772930519078902473361797697894230657273430081157732675805505620686985379449212982959585501387537164015710139858647833778606925583497541085196591615128057575940752635007475935288710823649949940771895617054361149474865046711015101563940680527540071584560878577663743040086340742855278549092581

# Part 2
N2 = 648455842808071669662824265346772278726343720706976263060439070378797308618081116462714015276061417569195587321840254520655424906719892428844841839353281972988531310511738648965962582821502504990264452100885281673303711142296421027840289307657458645233683357077834689715838646088239640236866252211790085787877

# Part 3
N3 = 720062263747350425279564435525583738338084451473999841826653057981916355690188337790423408664187663938485175264994017897083524079135686877441155132015188279331812309091996246361896836573643119174094961348524639707885238799396839230364676670221627018353299443241192173812729276147530748597302192751375739387929

# Part 4
CT = 22096451867410381776306561134883418017410069787892831071731839143676135600120538004282329650473509424343946219751512256465839967942889460764542040581564748988013734864120452325229320176487916666402997509188729971690526083222067771600019329260870009579993724077458967773697817571267229951148662959627934791540

E = 65537

BUFFER_CHAR = '00'


# To factor N = pq, where p, q are distinct primes, p < q:
# Guess an A = avg(p, q) = (p + q) / 2 ~ sqrt(N)
# p = A - x, q = A + x, N = pq = A^2 - x^2
# x = sqrt(A^2 - N)
# Keep incrementing this guess until (A-x)(A+x) = N
def factor(n):
    avg_guess = gmpy2.isqrt(n) + (0 if gmpy2.is_square(n) else 1)
    while True:
        x = gmpy2.isqrt(avg_guess ** 2 - n)
        p = avg_guess - x
        q = avg_guess + x
        if (p * q == n):
            break
        else:
            avg_guess += 1
    return (p, q)

def quadform(a, b, c):
    det = gmpy2.isqrt(b ** 2 - 4 * a * c)
    r1 = gmpy2.div((-b + det), 2 * a)
    r2 = gmpy2.div((-b - det), 2 * a)
    return (r1, r2)

# Same as above, except we have a different bound:
# |3p - 2q| < N^1/4 => avg(3p, 2q) ~ sqrt(6N)
# Since 3p is odd and 2q is even, A = (3p + 2q) / 2 is not an integer.
# Let A' = ceil(A). Then, A' = (3p + 2q + 1) / 2
# Then, if 3p < 2q: 3p + x + 1 = A' and 2q - x = A' => p = (A' - x - 1) / 3, q = (A' + x) / 2
#       if 3p > 2q: 3p - x = A' and 2q + x + 1 = A' => p = (A' + x) / 3, q = (A' - x - 1) / 2
# Either way, we get: N = pq = (A' + x) (A' - x - 1) / 6
# Solving this gives: 6N = A'^2 - A' - x^2 - x
# We can use the quadratic formula to solve for x: x^2 + x + (6N - A'^2 + A') = 0
def factor2(n):
    avg_guess = gmpy2.isqrt(6 * n) + (0 if gmpy2.is_square(n) else 1)
    while True:
        a = gmpy2.mpz(1)
        b = gmpy2.mpz(1)
        c = 6 * n - avg_guess ** 2 + avg_guess
        x_roots = quadform(a, b, c)
        for x in x_roots:
            # Check for 3p < 2q
            p = gmpy2.div((avg_guess - x - 1), 3)
            q = gmpy2.div((avg_guess + x), 2)
            if (p * q == n):
                return (p, q)
            # Check for 3p > 2q
            p = gmpy2.div((avg_guess + x), 3)
            q = gmpy2.div((avg_guess - x - 1), 2)
            if (p * q == n):
                return (p, q)
        avg_guess += 1

# Returns the integer RSA decryption of the input ciphertext.
def decrypt_rsa(ct, e, n):
    p, q = factor(n)
    phi = (p - 1) * (q - 1)
    # The pair (e, d) is chosen s.t. ed = 1 (mod phi(N))
    d = gmpy2.invert(e, phi)
    return gmpy2.powmod(ct, d, n)

def find_message(m):
    _, pt = m.split(BUFFER_CHAR)
    return binascii.unhexlify(pt)

def decode_ciphertext(ct, e, n):
    m = find_message(hex(decrypt_rsa(ct, e, n)))
    return m

def print_factors(p, q, n):
    print 'Prime factors of ' + str(n) + ':'
    print 'Smaller: ' + str(p)
    print 'Larger: ' + str(q)
    print ''

if __name__ == '__main__':
    p, q = factor(N1)
    print_factors(p, q, N1)
    p, q = factor(N2)
    print_factors(p, q, N2)
    p, q = factor2(N3)
    print_factors(p, q, N3)
    print decode_ciphertext(CT, E, N1)
