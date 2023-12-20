import random
import math

# Pomocné funkce

# Miller-Rabinův test prvočíselnosti
def miller_rabin(n):
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
    for _ in range(5):
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


# Generuje kandidáta na prvočíslo
def generate_prime_candidate(length):
    p = random.getrandbits(length)
    p |= (1 << length - 1) | 1
    return p

# Generuje prvočíslo
def generate_prime_number(length=1024):
    p = 4
    while not miller_rabin(p):
        p = generate_prime_candidate(length)
    return p

# Vypočítá největší společný dělitel

# Funkce RSA
# Generuje veřejný a soukromý klíč
def generate_keys():
    p = generate_prime_number()
    q = generate_prime_number()
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(1, phi)
    g = math.gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = math.gcd(e, phi)
    d = pow(e, -1, phi)
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
