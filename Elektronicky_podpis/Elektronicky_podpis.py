import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import hashlib
import RSA

public_key_content = None
private_key_content = None

def load_public_key():
    global public_key_content
    public_key_file = filedialog.askopenfilename(
        defaultextension=".pub",
        filetypes=[("Public Key Files", "*.pub"), ("All Files", "*.*")],
        title="Vybrat veřejný klíč"
    )
    if public_key_file:
        with open(public_key_file, 'r') as file:
            public_key = file.read()
            public_key_content = public_key
            public_key_display.delete(1.0, tk.END)
            public_key_display.insert(tk.END, public_key)
            messagebox.showinfo("Informace", "Veřejný klíč načten")

def load_private_key():
    global private_key_content
    private_key_file = filedialog.askopenfilename(
        defaultextension=".priv",
        filetypes=[("Private Key Files", "*.priv"), ("All Files", "*.*")],
        title="Vybrat soukromý klíč"
    )
    if private_key_file:
        with open(private_key_file, 'r') as file:
            private_key = file.read()
            private_key_content = private_key
            private_key_display.delete(1.0, tk.END)
            private_key_display.insert(tk.END, private_key)
            messagebox.showinfo("Informace", "Soukromý klíč načten")

def save_key_to_file(key, filename):
    with open(filename, 'w') as file:
        file.write(str(key))

def load_key_from_file(filename):
    with open(filename, 'r') as file:
        key = eval(file.read())
    return key

def generate_keys_gui():
    public_key, private_key = RSA.generate_keys()

    public_key_file = filedialog.asksaveasfilename(
        defaultextension=".pub",
        filetypes=[("Public Key Files", "*.pub"), ("All Files", "*.*")],
        title="Uložit veřejný klíč jako"
    )
    if public_key_file:
        save_key_to_file(public_key, public_key_file)
        public_key_display.delete(1.0, tk.END)
        public_key_display.insert(tk.END, f"Veřejný klíč uložen: {public_key_file}")

    private_key_file = filedialog.asksaveasfilename(
        defaultextension=".priv",
        filetypes=[("Private Key Files", "*.priv"), ("All Files", "*.*")],
        title="Uložit soukromý klíč jako"
    )
    if private_key_file:
        save_key_to_file(private_key, private_key_file)
        private_key_display.delete(1.0, tk.END)
        private_key_display.insert(tk.END, f"Soukromý klíč uložen: {private_key_file}")

def calculate_hash(file_path):
    sha3_512 = hashlib.sha3_512()
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            sha3_512.update(chunk)
    return sha3_512.digest()

def sign_file(file_path, private_key, output_file):
    file_hash = calculate_hash(file_path)
    signature = RSA.encrypt(private_key, int.from_bytes(file_hash, byteorder='big'))

    signature_file_path = output_file + '.sign'
    with open(signature_file_path, 'wb') as signature_file:
        signature_file.write(signature.to_bytes((signature.bit_length() + 7) // 8, byteorder='big'))

    return signature_file_path

def verify_signature(file_path, signature, public_key):
    with open(file_path, "rb") as f:
        file_hash = hashlib.sha3_512(f.read()).digest()  # Keep it as bytes

    decrypted_signature = RSA.decrypt(public_key, signature)

    is_valid = decrypted_signature == file_hash
    return is_valid


def select_file():
    file_path = filedialog.askopenfilename()
    file_path_display.delete(1.0, tk.END)
    file_path_display.insert(tk.END, file_path)

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

def verify_signature_gui():
    file_path = file_path_display.get("1.0", "end-1c").strip()
    signature_file = filedialog.askopenfilename(
        defaultextension=".sign",
        filetypes=[("Signature Files", "*.sign"), ("All Files", "*.*")],
        title="Vybrat podpisový soubor pro ověření"
    )
    if not file_path or not signature_file:
        messagebox.showerror("Chyba", "Soubor nebo podpis nebyly vybrány")
        return

    with open(signature_file, 'rb') as file:
        signature_bytes = file.read()

    signature = [int(byte) for byte in signature_bytes]

    public_key = eval(public_key_display.get("1.0", "end-1c"))

    is_valid = verify_signature(file_path, signature, public_key)
    messagebox.showinfo("Výsledek ověření", f"Podpis je {'platný' if is_valid else 'neplatný'}")

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
            signature_display.insert(tk.END, signature)
            messagebox.showinfo("Informace", "Podpis načten")

root = tk.Tk()
root.title("Elektronický Podpis")

import_signature_button = tk.Button(root, text="Naimportovat podpis", command=import_signature_gui)
import_signature_button.pack()

load_public_key_button = tk.Button(root, text="Naimportovat veřejný klíč", command=load_public_key)
load_public_key_button.pack()

load_private_key_button = tk.Button(root, text="Naimportovat soukromý klíč", command=load_private_key)
load_private_key_button.pack()

file_path_display = scrolledtext.ScrolledText(root, height=2, width=70)
file_path_display.pack()

select_file_button = tk.Button(root, text="Vybrat soubor", command=select_file)
select_file_button.pack()

sign_file_button = tk.Button(root, text="Podepsat soubor", command=sign_file_gui)
sign_file_button.pack()

signature_display = scrolledtext.ScrolledText(root, height=4, width=70)
signature_display.pack()

verify_signature_button = tk.Button(root, text="Ověřit podpis", command=verify_signature_gui)
verify_signature_button.pack()

public_key_display = scrolledtext.ScrolledText(root, height=5, width=70)
public_key_display.pack()

private_key_display = scrolledtext.ScrolledText(root, height=5, width=70)
private_key_display.pack()

generate_keys_button = tk.Button(root, text="Generovat klíče", command=generate_keys_gui)
generate_keys_button.pack()

root.mainloop()
