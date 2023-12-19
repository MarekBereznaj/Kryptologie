import tkinter as tk
from math import gcd
import string
import unicodedata

# Inicializace hlavního okna
root = tk.Tk()
root.geometry("800x800")
root.title("Afinní šifra")

# Vytvoření labelu a textového pole pro klíč A
label_A = tk.Label(root, text="Klíč A", font=('Arial', 18))
label_A.pack(padx=20, pady=20)
textbox_A = tk.Text(root, height=1, font=('Arial', 16))
textbox_A.pack()

# Vytvoření labelu a textového pole pro klíč B
label_B = tk.Label(root, text="Klíč B", font=('Arial', 18))
label_B.pack(padx=20, pady=20)
textbox_B = tk.Text(root, height=1, font=('Arial', 16))
textbox_B.pack()

# Label pro zadání textu k šifrování
label_text = tk.Label(root, text="Zadejte text k zašifrování", font=('Arial', 18))
label_text.pack(padx=20, pady=20)
textbox_text = tk.Text(root, height=1, font=('Arial', 16))
textbox_text.pack()

# Label pro zobrazení dešifrovaného textu
desifrovan_label = tk.Label(root, text="")
desifrovan_label.pack(pady=10)

# Label pro zadání textu k dešifrování
label_text_d = tk.Label(root, text="Zadejte text k dešifrování", font=('Arial', 18))
label_text_d.pack(padx=20, pady=20)
textbox_text_d = tk.Text(root, height=1, font=('Arial', 16))
textbox_text_d.pack()

# Label pro zobrazení výsledku
my_label = tk.Label(root, text="")
my_label.pack(pady=20)

# Funkce pro normalizaci a odstranění diakritiky
def coding(strng):
    strng = unicodedata.normalize('NFD', strng)
    strng = u"".join([c for c in strng if not unicodedata.combining(c)])
    return strng
# Funkce pro odstranění speciálních znaků a volání funkce pro normalizaci znaků
def fixedtext(strng):
    CHARS_TO_REMOVE = '''!ˇ´()-[]{};:'",<>./?@#$%^&*_~'''

    for char in CHARS_TO_REMOVE:
        strng = strng.replace(char, "")

    strng = str.lower(strng)
    strng=coding(strng)
    return strng
# Funkce pro zašifrování textu
def get_text():
    my_label.config(text="")  # Vymazání výstupního labelu
    OT = textbox_text.get(1.0, "end-1c")
    a = int(textbox_A.get(1.0, "end-1c"))
    b = int(textbox_B.get(1.0, "end-1c"))
    OT = fixedtext(OT)

    if gcd(a, 26) != 1 or not (1 <= a <= 25):
        my_label.config(text="Neplatný klíč A. Klíč A musí být nesoudělný s 26 a v rozmezí [1, 25].")
        return

    encrypted_text = ""
    for j in OT:
        if j.isspace():
            encrypted_text += "XMEZERAX"
        elif j.isalpha():
            output = (a * (ord(j) - (65 + (32 * (ord(j) > 96)))) + b) % 26
            encrypted_text += string.ascii_uppercase[output]
        elif j.isdigit():
            encrypted_text += str((int(j) + b) % 10)

    from textwrap import wrap
    encrypted_text = wrap(encrypted_text, 5)
    encrypted_text = " ".join(encrypted_text)
    my_label.config(text=encrypted_text)

# Funkce pro dešifrování textu
def desifruj_text():
    desifrovan_label.config(text="")
    a = int(textbox_A.get(1.0, "end-1c"))
    b = int(textbox_B.get(1.0, "end-1c"))
    desifrovan = textbox_text_d.get(1.0, "end-1c")
    desifrovan = str.lower(desifrovan)
    add = ""
    desifrovan = desifrovan.replace(" ", "")

    desifrovan = desifrovan.replace("xmezerax", " ")

    for h in desifrovan:
        if h.isspace():
            add += " "
        elif h.isalpha():
            alphabet = string.ascii_lowercase
            ot = alphabet.find(h)
            position = (pow(a, -1, 26) * (ot - b)) % 26
            add += string.ascii_uppercase[position]
        elif h.isdigit():
            add += str((int(h) - b) % 10)

    desifrovan_label.config(text=add)

# Funkce pro kopírování výstupu z šifrování
def copy_encryption_output():
    root.clipboard_clear()
    root.clipboard_append(my_label.cget("text"))
    root.update()

# Funkce pro kopírování výstupu z dešifrování
def copy_decryption_output():
    root.clipboard_clear()
    root.clipboard_append(desifrovan_label.cget("text"))
    root.update()

# Vytvoření tlačítek pro šifrování, dešifrování a kopírování výstupu
Button_encrypt = tk.Button(root, text="Zašifrovat", command=get_text)
Button_encrypt.pack(side=tk.LEFT, padx=20, pady=20)

Button_decrypt = tk.Button(root, text="Dešifrovat", command=desifruj_text)
Button_decrypt.pack(side=tk.LEFT, padx=20, pady=20)

Button_copy_encrypt = tk.Button(root, text="Kopírovat výstup z šifrování", command=copy_encryption_output)
Button_copy_encrypt.pack(side=tk.LEFT, padx=20, pady=20)

Button_copy_decrypt = tk.Button(root, text="Kopírovat výstup z dešifrování", command=copy_decryption_output)
Button_copy_decrypt.pack(side=tk.LEFT, padx=20, pady=20)

# Spuštění hlavní smyčky
root.mainloop()
