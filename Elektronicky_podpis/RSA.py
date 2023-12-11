import random
import math

# Pomocné funkce

# Miller-Rabinův test prvočíselnosti
def miller_rabin(n, k):
    # Speciální případy: 2 a 3 jsou prvočísla
    if n == 2 or n == 3:
        return True
    # Vyřazení čísel menších než 2 a sudých čísel
    if n <= 1 or n % 2 == 0:
        return False

    # Nalezení hodnot r a d pro n - 1 = 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Provedení testu k-krát
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)  # Výpočet a^d % n
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Zjistí, zda je číslo prvočíslo s použitím Miller-Rabinova testu
def is_prime(n, k=5):
    return miller_rabin(n, k)

# Generuje kandidáta na prvočíslo
def generate_prime_candidate(length):
    p = random.getrandbits(length)
    p |= (1 << length - 1) | 1
    return p

# Generuje prvočíslo
def generate_prime_number(length=1024):
    p = 4
    while not is_prime(p):
        p = generate_prime_candidate(length)
    return p

# Vypočítá největší společný dělitel
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Vypočítá inverzi modulu
def multiplicative_inverse(e, phi):
    x, y, u = 0, 1, e
    v = phi
    while u != 0:
        q = v // u
        r = v - q * u
        m = x - q * y
        v, u, x, y = u, r, y, m
    return x % phi

# Funkce RSA
# Generuje veřejný a soukromý klíč
def generate_keys():
    p = generate_prime_number()
    q = generate_prime_number()
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    d = multiplicative_inverse(e, phi)
    return ((e, n), (d, n))

# Šifruje text
def encrypt(public_key, plaintext):
    key, n = public_key
    if isinstance(plaintext, str):
        plaintext = ord(plaintext)  # Převede jedno písmeno na jeho Unicode kód
    encrypted = pow(plaintext, key, n)
    return encrypted

# Dešifruje text
def decrypt(private_key, signature):
    key, n = private_key
    decrypted_signature = pow(signature, key, n)
    return decrypted_signature
