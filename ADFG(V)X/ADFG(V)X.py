from itertools import product
import random
import tkinter as tk
from tkinter import ttk, messagebox
import unicodedata

# Třída pro šifrování/dešifrování pomocí ADFGX/ADFGVX
class ADFGX_Cipher:
    # Normalizace českých znaků (odstranění diakritiky)
    def normalize_czech_characters(self, text):
        normalized = unicodedata.normalize('NFD', text)
        return ''.join(ch for ch in normalized if unicodedata.category(ch) != 'Mn')

    # Konstruktor třídy
    def __init__(self, key, variant, language='EN'):
        self.key = key.upper()  # Klíč pro šifrování
        self.variant = variant  # Varianta šifry (ADFGX nebo ADFGVX)
        self.language = language  # Jazyk (EN nebo CZ)
        self.adfg = 'ADFGX' if variant == "ADFGX" else 'ADFGVX'  # Přiřazení znaků pro variantu
        # Nastavení abecedy dle jazyka a varianty
        if self.language == 'CZ' and self.variant == "ADFGX":
            self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVXYZ'
        else:
            self.alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ' if variant == "ADFGX" else 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.create_transposition_matrix()

    # Vytvoření transpoziční matice
    def create_transposition_matrix(self):
        temp = list(self.alphabet)
        random.shuffle(temp)
        self.matrix = {char: pair for char, pair in zip(temp, product(self.adfg, repeat=2))}

    # Funkce pro šifrování
    def encrypt(self, plaintext):
        # Normalizace vstupu dle jazyka
        if self.language == 'CZ':
            plaintext = self.normalize_czech_characters(plaintext.upper()).replace('W', 'V')
        elif self.language == 'EN':
            plaintext = plaintext.upper().replace('J', 'I')
        
        plaintext = plaintext.replace(' ', 'XMEZERAX')
        substituted = ''.join(''.join(self.matrix[char]) for char in plaintext if char in self.matrix)
        columns = [''.join(substituted[i::len(self.key)]) for i in range(len(self.key))]
        sorted_columns = sorted(zip(self.key, columns), key=lambda x: x[0])
        return ''.join(column for _, column in sorted_columns)

    # Funkce pro dešifrování
    def decrypt(self, ciphertext):
        n = len(ciphertext)
        k = len(self.key)
        column_lengths = [n // k + (i < n % k) for i in range(k)]
        columns = [''] * k
        index = 0
        for i, length in sorted(enumerate(column_lengths), key=lambda x: self.key[x[0]]):
            columns[i] = ciphertext[index:index + length]
            index += length
        rows = [''.join(column[i] for column in columns if i < len(column)) for i in range(max(column_lengths))]
        reversed_matrix = {v: k for k, v in self.matrix.items()}
        plaintext = ''
        for pair in zip(*[iter(''.join(rows))] * 2):
            plaintext += reversed_matrix.get(pair, '')
        decrypted_text = self.normalize_czech_characters(plaintext.replace('XMEZERAX', ' '))
        return decrypted_text

    # Funkce pro získání matice jako seznam
    def get_matrix_as_list(self):
        return [f'{char} -> {"".join(self.matrix[char])}' for char in sorted(self.matrix.keys())]

# Funkce pro validaci klíče
def validate_key():
    key = key_entry.get().upper()
    if not key.isalpha() or len(set(key)) != len(key):
        messagebox.showerror("Error", "Invalid key. Please enter a unique alphabetic string.")
        return False
    return True

# Funkce pro vytvoření šifry
def create_cipher(variant):
    if not validate_key():
        return
    global cipher
    cipher = ADFGX_Cipher(key_entry.get(), variant, language.get())
    update_matrix_display()
    toggle_buttons(True)

# Aktualizace zobrazení matice
def update_matrix_display():
    matrix_listbox.delete(0, tk.END)
    for item in cipher.get_matrix_as_list():
        matrix_listbox.insert(tk.END, item)

# Přepínání stavu tlačítek
def toggle_buttons(state):
    btn_encrypt["state"] = tk.NORMAL if state else tk.DISABLED
    btn_decrypt["state"] = tk.NORMAL if state else tk.DISABLED

# Funkce pro šifrování zprávy
def encrypt_message():
    plaintext = txt_input.get("1.0", "end-1c")
    encrypted = cipher.encrypt(plaintext)
    txt_output.delete("1.0", "end")
    txt_output.insert("1.0", encrypted)

# Funkce pro dešifrování zprávy
def decrypt_message():
    ciphertext = txt_output.get("1.0", "end-1c")
    decrypted = cipher.decrypt(ciphertext)
    txt_input.delete("1.0", "end")
    txt_input.insert("1.0", decrypted)

# Vytvoření hlavního okna
root = tk.Tk()
root.title("ADFGX/ADFGVX Cipher")

# Výběr jazyka
language = tk.StringVar(value='EN')
tk.Radiobutton(root, text="English", variable=language, value='EN').pack()
tk.Radiobutton(root, text="Czech", variable=language, value='CZ').pack()

# Vytvoření widgetů
lbl_key = ttk.Label(root, text="Enter Key:")
lbl_key.pack()
key_entry = ttk.Entry(root)
key_entry.pack()

btn_create_cipher_adfgx = ttk.Button(root, text="Create ADFGX Cipher", command=lambda: create_cipher("ADFGX"))
btn_create_cipher_adfgx.pack()

btn_create_cipher_adfgvx = ttk.Button(root, text="Create ADFGVX Cipher", command=lambda: create_cipher("ADFGVX"))
btn_create_cipher_adfgvx.pack()

lbl_input = ttk.Label(root, text="Input:")
lbl_input.pack()
txt_input = tk.Text(root, height=10, width=40)
txt_input.pack()

btn_encrypt = ttk.Button(root, text="Encrypt", command=encrypt_message)
btn_encrypt.pack()

btn_decrypt = ttk.Button(root, text="Decrypt", command=decrypt_message)
btn_decrypt.pack()

lbl_output = ttk.Label(root, text="Output:")
lbl_output.pack()
txt_output = tk.Text(root, height=10, width=40)
txt_output.pack()

# Seznam pro zobrazení matice
matrix_listbox = tk.Listbox(root, height=10, width=40)
matrix_listbox.pack()

toggle_buttons(False)  # Na začátku vypnout tlačítka pro šifrování a dešifrování

root.mainloop()
