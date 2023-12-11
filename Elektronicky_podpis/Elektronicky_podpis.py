import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import hashlib
import RSA
import base64
import re

# Globální proměnné pro uchování veřejného a soukromého klíče
public_key_content = None
private_key_content = None

# Funkce pro načtení klíče z souboru
def load_key(filepath, is_public=True):
    global public_key_content, private_key_content
    try:
        # Otevření souboru a načtení BASE64 kódovaného klíče
        with open(filepath, 'rb') as file:
            key_base64 = file.read()
            # Dekódování z BASE64 a rozdělení na části
            key_bytes = base64.b64decode(key_base64)   
            key_text = key_bytes.decode()
            key_parts = key_text.split(',')
            key = (int(key_parts[0]), int(key_parts[1]))

            # Uložení klíče do globální proměnné a zobrazení v GUI
            if is_public:
                public_key_content = key
                public_key_display.insert(tk.END, str(key))
            else:
                private_key_content = key
                private_key_display.insert(tk.END, str(key))
    except Exception as e:
        messagebox.showerror("Chyba", f"Chyba při načítání klíče: {e}")

# Funkce pro načtení veřejného klíče pomocí GUI
def load_public_key():
    public_key_file = filedialog.askopenfilename(
        defaultextension=".pub", filetypes=[("Public Key Files", "*.pub"), ("All Files", "*.*")], title="Vybrat veřejný klíč"
    )
    if public_key_file:
        public_key_display.delete(1.0, tk.END)
        load_key(public_key_file, is_public=True)

# Funkce pro načtení soukromého klíče pomocí GUI
def load_private_key():
    private_key_file = filedialog.askopenfilename(
        defaultextension=".priv", filetypes=[("Private Key Files", "*.priv"), ("All Files", "*.*")], title="Vybrat soukromý klíč"
    )
    if private_key_file:
        private_key_display.delete(1.0, tk.END)
        load_key(private_key_file, is_public=False)

# Funkce pro uložení klíče do souboru
def save_key_to_file(key, filename):
    try:
        # Převod klíče na string a poté na bytes, následné kódování do BASE64
        key_bytes = f"{key[0]},{key[1]}".encode()
        key_base64 = base64.b64encode(key_bytes)
        with open(filename, 'wb') as file:
            file.write(key_base64)
    except Exception as e:
        messagebox.showerror("Chyba", f"Chyba při ukládání klíče: {e}")

# Funkce pro generování RSA klíčů a jejich uložení
def generate_keys_gui():
    try:
        public_key, private_key = RSA.generate_keys()
        # Dialog pro uložení veřejného klíče
        public_key_file = filedialog.asksaveasfilename(
            defaultextension=".pub",
            filetypes=[("Public Key Files", "*.pub"), ("All Files", "*.*")],
            title="Uložit veřejný klíč jako"
        )
        if public_key_file:
            save_key_to_file(public_key, public_key_file)
            public_key_display.delete(1.0, tk.END)
            public_key_display.insert(tk.END, f"Veřejný klíč uložen: {public_key_file}")

        # Dialog pro uložení soukromého klíče
        private_key_file = filedialog.asksaveasfilename(
            defaultextension=".priv",
            filetypes=[("Private Key Files", "*.priv"), ("All Files", "*.*")],
            title="Uložit soukromý klíč jako"
        )
        if private_key_file:
            save_key_to_file(private_key, private_key_file)
            private_key_display.delete(1.0, tk.END)
            private_key_display.insert(tk.END, f"Soukromý klíč uložen: {private_key_file}")

    except Exception as e:
        messagebox.showerror("Chyba", f"Chyba při generování klíčů: {e}")

# Funkce pro výpočet hash hodnoty souboru pomocí SHA3-512
def calculate_hash(file_path):
    sha3_512 = hashlib.sha3_512()
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            sha3_512.update(chunk)
    return sha3_512.digest()

# Funkce pro digitální podpis souboru
def sign_file(file_path, private_key, output_file):
    file_hash = calculate_hash(file_path)
    signature = RSA.encrypt(private_key, int.from_bytes(file_hash, byteorder='big'))
    signature_file_path = output_file + '.sign'
    with open(signature_file_path, 'wb') as signature_file:
        signature_file.write(signature.to_bytes((signature.bit_length() + 7) // 8, byteorder='big'))
    return signature_file_path

# Funkce pro ověření digitálního podpisu
def verify_signature(file_path, signature_file_path, public_key):
    file_hash = calculate_hash(file_path)
    print("Vypočítaný hash souboru:", file_hash.hex())
    with open(signature_file_path, 'rb') as signature_file:
        signature = int.from_bytes(signature_file.read(), byteorder='big')
    decrypted_signature = RSA.decrypt(public_key, signature)
    print("Dešifrovaný podpis:", decrypted_signature.to_bytes((decrypted_signature.bit_length() + 7) // 8, byteorder='big').hex())
    is_valid = decrypted_signature == int.from_bytes(file_hash, byteorder='big')
    print("Podpis je", "platný" if is_valid else "neplatný")
    return is_valid

# Funkce pro vybrání souboru pomocí GUI
def select_file():
    file_path = filedialog.askopenfilename()
    file_path_display.delete(1.0, tk.END)
    file_path_display.insert(tk.END, file_path)

# GUI funkce pro podepsání souboru
def sign_file_gui():
    file_path = file_path_display.get("1.0", "end-1c").strip()
    if not file_path:
        messagebox.showerror("Chyba", "Žádný soubor nebyl vybrán")
        return
    private_key = eval(private_key_display.get("1.0", "end-1c"))
    signature_output_file = filedialog.asksaveasfilename(
        defaultextension=".sign",
        filetypes=[("Signature Files", "*.sign"), ("All Files", "*.*")],
        title="Uložit podpis jako"
    )
    if signature_output_file:
        signature_file_path = sign_file(file_path, private_key, signature_output_file)
        signature_display.delete(1.0, tk.END)
        signature_display.insert(tk.END, f"Podpis uložen: {signature_file_path}")

# GUI funkce pro ověření podpisu
def verify_signature_gui():
    file_path = file_path_display.get("1.0", "end-1c").strip()
    signature_file_path = filedialog.askopenfilename(
        defaultextension=".sign",
        filetypes=[("Signature Files", "*.sign"), ("All Files", "*.*")],
        title="Vybrat podpisový soubor pro ověření"
    )
    if not file_path or not signature_file_path:
        messagebox.showerror("Chyba", "Soubor nebo podpis nebyly vybrány")
        return
    public_key = eval(public_key_display.get("1.0", "end-1c"))
    is_valid = verify_signature(file_path, signature_file_path, public_key)
    messagebox.showinfo("Výsledek ověření", f"Podpis je {'platný' if is_valid else 'neplatný'}")

# GUI funkce pro import podpisu
def import_signature_gui():
    signature_file = filedialog.askopenfilename(
        defaultextension=".sign",
        filetypes=[("Signature Files", "*.sign"), ("All Files", "*.*")],
        title="Vybrat podpisový soubor pro import"
    )
    if signature_file:
        with open(signature_file, 'rb') as file:
            signature = file.read()
            signature_display.delete(1.0, tk.END)
            signature_display.insert(tk.END, signature.hex())  # Zobrazí hexadecimální reprezentaci podpisu

root = tk.Tk()
root.title("Elektronický Podpis")
root.geometry("900x800")  # Nastaví velikost okna

# Vytvoření rámu pro tlačítka a přidání do GUI
button_frame = tk.Frame(root)
button_frame.pack(pady=10)


load_public_key_button = tk.Button(button_frame, text="Naimportovat veřejný klíč", command=load_public_key)
load_public_key_button.grid(row=0, column=1, padx=5)

load_private_key_button = tk.Button(button_frame, text="Naimportovat soukromý klíč", command=load_private_key)
load_private_key_button.grid(row=0, column=2, padx=5)

select_file_button = tk.Button(button_frame, text="Vybrat soubor", command=select_file)
select_file_button.grid(row=0, column=3, padx=5)

sign_file_button = tk.Button(button_frame, text="Podepsat soubor", command=sign_file_gui)
sign_file_button.grid(row=0, column=4, padx=5)

verify_signature_button = tk.Button(button_frame, text="Ověřit podpis", command=verify_signature_gui)
verify_signature_button.grid(row=0, column=5, padx=5)

generate_keys_button = tk.Button(button_frame, text="Generovat klíče", command=generate_keys_gui)
generate_keys_button.grid(row=0, column=6, padx=5)

# Textová pole
file_path_display = scrolledtext.ScrolledText(root, height=2, width=70)
file_path_display.pack(pady=10)

signature_display = scrolledtext.ScrolledText(root, height=4, width=70)
signature_display.pack(pady=10)

public_key_display = scrolledtext.ScrolledText(root, height=5, width=70)
public_key_display.pack(pady=10)

private_key_display = scrolledtext.ScrolledText(root, height=5, width=70)
private_key_display.pack(pady=10)

root.mainloop()
