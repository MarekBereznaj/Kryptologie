import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import hashlib
import RSA
import base64
import re
import os
import time

# Globální proměnné pro uchování veřejného a soukromého klíče
public_key_content = None
private_key_content = None
selected_file_path = None

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
        # Zobrazení chybového hlášení v případě výjimky
        messagebox.showerror("Chyba", f"Chyba při načítání klíče: {e}")

# Funkce pro načtení veřejného klíče pomocí GUI
def load_public_key():
    # Zobrazení dialogu pro výběr souboru s veřejným klíčem
    public_key_file = filedialog.askopenfilename(
        defaultextension=".pub", filetypes=[("Public Key Files", "*.pub"), ("All Files", "*.*")], title="Vybrat veřejný klíč"
    )
    if public_key_file:
        # Načtení a zobrazení veřejného klíče
        public_key_display.delete(1.0, tk.END)
        load_key(public_key_file, is_public=True)

# Funkce pro načtení soukromého klíče pomocí GUI
def load_private_key():
    # Zobrazení dialogu pro výběr souboru se soukromým klíčem
    private_key_file = filedialog.askopenfilename(
        defaultextension=".priv", filetypes=[("Private Key Files", "*.priv"), ("All Files", "*.*")], title="Vybrat soukromý klíč"
    )
    if private_key_file:
        # Načtení a zobrazení soukromého klíče
        private_key_display.delete(1.0, tk.END)
        load_key(private_key_file, is_public=False)

# Funkce pro uložení klíče do souboru
def save_key_to_file(key, filename):
    try:
        # Převod klíče na string a poté na bytes, následné kódování do BASE64
        key_bytes = f"{key[0]},{key[1]}".encode()
        key_base64 = base64.b64encode(key_bytes)
        # Uložení klíče do souboru
        with open(filename, 'wb') as file:
            file.write(key_base64)
    except Exception as e:
        # Zobrazení chybového hlášení v případě výjimky
        messagebox.showerror("Chyba", f"Chyba při ukládání klíče: {e}")

# Funkce pro generování RSA klíčů a jejich uložení
def generate_keys_gui():
    try:
        # Generování veřejného a soukromého klíče
        public_key, private_key = RSA.generate_keys()

        # Dialog pro uložení veřejného klíče
        public_key_file = filedialog.asksaveasfilename(
            defaultextension=".pub",
            filetypes=[("Public Key Files", "*.pub"), ("All Files", "*.*")],
            title="Uložit veřejný klíč jako"
        )
        if public_key_file:
            # Uložení veřejného klíče do souboru
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
            # Uložení soukromého klíče do souboru
            save_key_to_file(private_key, private_key_file)
            private_key_display.delete(1.0, tk.END)
            private_key_display.insert(tk.END, f"Soukromý klíč uložen: {private_key_file}")

    except Exception as e:
        # Zobrazení chybového hlášení v případě výjimky
        messagebox.showerror("Chyba", f"Chyba při generování klíčů: {e}")

# Funkce pro výpočet hash hodnoty souboru pomocí SHA3-512
def calculate_hash(file_path):
    # Inicializace SHA3-512 hashovací funkce
    sha3_512 = hashlib.sha3_512()
    # Otevření souboru a postupné čtení a hashování obsahu
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            sha3_512.update(chunk)
    # Vrácení výsledného hash
    return sha3_512.digest()

# Funkce pro digitální podpis souboru
def sign_file(file_path, private_key, output_file):
    # Výpočet hash hodnoty souboru
    file_hash = calculate_hash(file_path)
    # Šifrování hash hodnoty pomocí soukromého klíče
    signature = RSA.encrypt(private_key, int.from_bytes(file_hash, byteorder='big'))
    # Uložení podpisu do souboru
    signature_file_path = output_file + '.sign'
    with open(signature_file_path, 'wb') as signature_file:
        signature_file.write(signature.to_bytes((signature.bit_length() + 7) // 8, byteorder='big'))
    return signature_file_path

# Funkce pro ověření digitálního podpisu
def verify_signature(file_path, signature_file_path, public_key):
    # Výpočet hash hodnoty původního souboru
    file_hash = calculate_hash(file_path)
    # Načtení a dešifrování podpisu
    with open(signature_file_path, 'rb') as signature_file:
        signature = int.from_bytes(signature_file.read(), byteorder='big')
    decrypted_signature = RSA.decrypt(public_key, signature)
      # Porovnání hash hodnoty s dešifrovaným podpisem
    is_valid = decrypted_signature == int.from_bytes(file_hash, byteorder='big')
    return is_valid


def select_file():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename()
    file_path_display.delete(1.0, tk.END)

    if selected_file_path:
        # Zobrazení cesty k vybranému souboru
        file_path_display.insert(tk.END, selected_file_path + "\n")

        # Získání a zobrazení základních informací o souboru
        file_info = os.stat(selected_file_path)
        file_name = os.path.basename(selected_file_path)
        file_creation_time = time.ctime(file_info.st_ctime)
        file_modification_time = time.ctime(file_info.st_mtime)  # Přidáno pro zobrazení času poslední modifikace
        file_size = file_info.st_size
        file_type = "Directory" if os.path.isdir(selected_file_path) else "File"

        # Formátování a výpis informací o souboru
        info_text = f"Name: {file_name}\n" \
                    f"Path: {selected_file_path}\n" \
                    f"Creation Time: {file_creation_time}\n" \
                    f"Last Modified: {file_modification_time}\n" \
                    f"Type: {file_type}\n" \
                    f"Size: {file_size} bytes\n"
        
        file_path_display.insert(tk.END, info_text)


# Funkce pro podpisování souboru pomocí GUI
def sign_file_gui():
    global selected_file_path
    if not selected_file_path:
        messagebox.showerror("Chyba", "Žádný soubor nebyl vybrán")
        return

    private_key = eval(private_key_display.get("1.0", "end-1c"))
    signature_output_file = filedialog.asksaveasfilename(
        defaultextension=".sign",
        filetypes=[("Signature Files", "*.sign"), ("All Files", "*.*")],
        title="Uložit podpis jako"
    )

    if signature_output_file:
        # Vytvoření podpisu vybraného souboru a uložení do specifikovaného souboru
        signature_file_path = sign_file(selected_file_path, private_key, signature_output_file)
    else:
        messagebox.showerror("Chyba", "Nebyl vybrán žádný výstupní soubor pro podpis")

# Funkce pro ověření podpisu souboru pomocí GUI
def verify_signature_gui():
    global selected_file_path
    if not selected_file_path:
        messagebox.showerror("Chyba", "Soubor nebo podpis nebyly vybrány")
        return
    signature_file_path = filedialog.askopenfilename(
        defaultextension=".sign",
        filetypes=[("Signature Files", "*.sign"), ("All Files", "*.*")],
        title="Vybrat podpisový soubor pro ověření"
    )
    public_key = eval(public_key_display.get("1.0", "end-1c"))
    # Ověření digitálního podpisu vybraného souboru
    is_valid = verify_signature(selected_file_path, signature_file_path, public_key)
    messagebox.showinfo("Výsledek ověření", f"Podpis je {'platný' if is_valid else 'neplatný'}")

# Nastavení GUI aplikace
root = tk.Tk()
root.title("Elektronický Podpis")
root.geometry("900x400")  # Nastaví velikost okna

# Vytvoření a konfigurace rámu pro tlačítka
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Vytvoření a umístění tlačítek pro různé funkce aplikace
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

# Vytvoření a konfigurace textových polí pro zobrazování informací
file_path_display = scrolledtext.ScrolledText(root, height=8, width=70)
file_path_display.pack(pady=10)

public_key_display = scrolledtext.ScrolledText(root, height=5, width=70)
public_key_display.pack(pady=10)

private_key_display = scrolledtext.ScrolledText(root, height=5, width=70)
private_key_display.pack(pady=10)

# Spuštění hlavní smyčky aplikace
root.mainloop()
