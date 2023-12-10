import tkinter as tk
from tkinter import scrolledtext
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
def generate_prime_number(length=256):
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
def encrypt(pk, plaintext):
    key, n = pk
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return cipher

# Dešifruje text
def decrypt(pk, ciphertext):
    key, n = pk
    plain = [chr(pow(char, key, n)) for char in ciphertext]
    return ''.join(plain)

# GUI funkce

# Generuje klíče a zobrazuje je v GUI
def generate_keys_gui():
    public_key, private_key = generate_keys()
    public_key_display.delete(1.0, tk.END)
    public_key_display.insert(tk.END, str(public_key))
    private_key_display.delete(1.0, tk.END)
    private_key_display.insert(tk.END, str(private_key))

# Šifruje text a zobrazuje šifrovaný text v GUI
def encrypt_gui():
    key = eval(public_key_display.get(1.0, "end-1c"))
    plaintext = plaintext_entry.get("1.0", "end-1c")
    ciphertext = encrypt(key, plaintext)
    ciphertext_display.delete("1.0", tk.END)
    ciphertext_display.insert(tk.END, str(ciphertext))

# Dešifruje text a zobrazuje dešifrovaný text v GUI
def decrypt_gui():
    key = eval(private_key_display.get(1.0, "end-1c"))
    ciphertext = eval(ciphertext_display.get("1.0", "end-1c"))
    plaintext = decrypt(key, ciphertext)
    decrypted_text_display.delete("1.0", tk.END)
    decrypted_text_display.insert(tk.END, plaintext)

# Vytvoření hlavního okna
root = tk.Tk()
root.title("RSA Encryptor/Decryptor")

# Vytvoření widgetů
generate_button = tk.Button(root, text="Generovat klíče", command=generate_keys_gui)
generate_button.pack()

tk.Label(root, text="Veřejný klíč:").pack()
public_key_display = scrolledtext.ScrolledText(root, height=5, width=70)
public_key_display.pack()

tk.Label(root, text="Soukromý klíč:").pack()
private_key_display = scrolledtext.ScrolledText(root, height=5, width=70)
private_key_display.pack()

tk.Label(root, text="Text k šifrování:").pack()
plaintext_entry = scrolledtext.ScrolledText(root, height=5, width=70)
plaintext_entry.pack()

encrypt_button = tk.Button(root, text="Šifrovat", command=encrypt_gui)
encrypt_button.pack()

tk.Label(root, text="Šifrovaný text:").pack()
ciphertext_display = scrolledtext.ScrolledText(root, height=5, width=70)
ciphertext_display.pack()

decrypt_button = tk.Button(root, text="Dešifrovat", command=decrypt_gui)
decrypt_button.pack()

tk.Label(root, text="Dešifrovaný text:").pack()
decrypted_text_display = scrolledtext.ScrolledText(root, height=5, width=70)
decrypted_text_display.pack()

# Spuštění GUI
root.mainloop()
