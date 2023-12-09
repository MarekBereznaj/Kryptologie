import tkinter as tk
from tkinter import ttk
import pyperclip

# Abecedy pro češtinu a angličtinu
alphabet_CZ = "ABCDEFGHIJKLMNOPQRSTUVXYZ"
alphabet_EN = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

# Funkce pro copy tlačítko
def copy_encrypted_text_to_clipboard():
    pyperclip.copy(encrypted_text.get())

# Funkce pro nahrazení speciálních českých znaků
def replace_special_characters(text):
    replacements = {
        'á': 'a', 'č': 'c', 'ď': 'd', 'é': 'e', 'ě': 'e', 'í': 'i',
        'ň': 'n', 'ó': 'o', 'ř': 'r', 'š': 's', 'ť': 't', 'ú': 'u',
        'ů': 'u', 'ý': 'y', 'ž': 'z',
        'Á': 'A', 'Č': 'C', 'Ď': 'D', 'É': 'E', 'Ě': 'E', 'Í': 'I',
        'Ň': 'N', 'Ó': 'O', 'Ř': 'R', 'Š': 'S', 'Ť': 'T', 'Ú': 'U',
        'Ů': 'U', 'Ý': 'Y', 'Ž': 'Z'
    }
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    return text

# Čištění textu pro šifrování
def clean_text_for_cipher(input_text, language):
    input_text = replace_special_characters(input_text)
    if language == "CZ":
        cleaned_text = input_text.upper().replace(" ", "").replace("W", "V")
        cleaned_text = ''.join(char for char in cleaned_text if char in alphabet_CZ)
    elif language == "EN":
        cleaned_text = input_text.upper().replace(" ", "").replace("J", "I")
        cleaned_text = ''.join(char for char in cleaned_text if char in alphabet_EN)
    return cleaned_text

# Čištění klíče pro šifrování
def clean_key_for_cipher(input_key, language):
    input_key = replace_special_characters(input_key)
    if language == "CZ":
        cleaned_key = input_key.upper().replace(" ", "").replace("W", "V")
    elif language == "EN":
        cleaned_key = input_key.upper().replace(" ", "").replace("J", "I")
    return cleaned_key

# Generování šifrovací matice Playfair
def generate_playfair_key(key, language):
    alphabet = alphabet_CZ if language == "CZ" else alphabet_EN
    key = key.upper()
    if language == "CZ":
        key = key.replace("W", "V")
    else:
        key = key.replace("J", "I")
    key_matrix = ''.join(sorted(set(key), key=lambda x: key.index(x)))
    key_matrix += ''.join([char for char in alphabet if char not in key_matrix])
    return [key_matrix[i:i+5] for i in range(0, 25, 5)]

# Převod čísel na slova
def convert_numbers_to_words(text):
    number_word_mapping = {"0": "ZERO", "1": "ONE", "2": "TWO", "3": "THREE", "4": "FOUR", "5": "FIVE",
                           "6": "SIX", "7": "SEVEN", "8": "EIGHT", "9": "NINE"}
    for digit, word in number_word_mapping.items():
        text = text.replace(digit, word)
    return text

# Převod slov zpět na čísla
def convert_words_to_numbers(text):
    word_number_mapping = {"ZERO": "0", "ONE": "1", "TWO": "2", "THREE": "3", "FOUR": "4", "FIVE": "5",
                           "SIX": "6", "SEVEN": "7", "EIGHT": "8", "NINE": "9"}
    for word, digit in word_number_mapping.items():
        text = text.replace(word, digit)
    return text

# Příprava textu k šifrování
def prepare_text(text, filler='X'):
    text = text.upper().replace("J", "I").replace(" ", "")
    prepared_text = ""
    i = 0
    while i < len(text):
        if i+1 < len(text) and text[i] == text[i+1]:
            prepared_text += text[i] + filler
            i += 1
        elif i+1 < len(text):
            prepared_text += text[i] + text[i+1]
            i += 2
        else:
            prepared_text += text[i] + filler
            i += 1
    return prepared_text

# Nalezení pozice znaku v šifrovací matici
def find_position(letter, key_matrix):
    for row in range(5):
        for col in range(5):
            if key_matrix[row][col] == letter:
                return row, col
    return None, None

# Šifrování/dešifrování textu
def playfair_cipher(text, key, language, encrypt=True):
    key_matrix = generate_playfair_key(key, language)
    text = prepare_text(text)
    result = ""
    for i in range(0, len(text), 2):
        row1, col1 = find_position(text[i], key_matrix)
        row2, col2 = find_position(text[i+1], key_matrix)
        if row1 == row2:
            col1 = (col1 + (1 if encrypt else -1)) % 5
            col2 = (col2 + (1 if encrypt else -1)) % 5
        elif col1 == col2:
            row1 = (row1 + (1 if encrypt else -1)) % 5
            row2 = (row2 + (1 if encrypt else -1)) % 5
        else:
            col1, col2 = col2, col1
        result += key_matrix[row1][col1] + key_matrix[row2][col2]
    return ' '.join([result[i:i+5] for i in range(0, len(result), 5)])

# Aktualizace zobrazení šifrovací matice
def update_key_matrix_display():
    language = lang_var.get()
    key = clean_key_for_cipher(key_entry.get(), language)
    key_matrix = generate_playfair_key(key, language)
    key_matrix_display.delete(1.0, tk.END)
    key_matrix_display.insert(tk.END, '\n'.join([' '.join(row) for row in key_matrix]))

# Funkce pro šifrování textu
def encrypt_text():
    language = lang_var.get()
    key = clean_key_for_cipher(key_entry.get(), language)
    text_with_spaces_replaced = text_entry.get().replace(" ", "QMEZERAQ")
    text_with_numbers_converted = convert_numbers_to_words(text_with_spaces_replaced)
    text = clean_text_for_cipher(text_with_numbers_converted, language)
    encrypted_text.set(playfair_cipher(text, key, language, True))

# Funkce pro dešifrování textu
def decrypt_text():
    language = lang_var.get()
    key = clean_key_for_cipher(key_entry.get(), language)
    decrypted_text_raw = playfair_cipher(text_entry.get(), key, language, False)
    text_with_numbers = clean_text_for_cipher(decrypted_text_raw, language)
    decrypted_text_with_numbers = convert_words_to_numbers(text_with_numbers)
    decrypted_text_with_spaces_restored = decrypted_text_with_numbers.replace("QMEZERAQ", " ")
    decrypted_text.set(decrypted_text_with_spaces_restored)


app = tk.Tk()
app.geometry("400x400")
app.title("Playfair")


lang_var = tk.StringVar(value="EN")
ttk.Radiobutton(app, text="English", variable=lang_var, value="EN").grid(column=0, row=6)
ttk.Radiobutton(app, text="Česky", variable=lang_var, value="CZ").grid(column=1, row=6)

ttk.Label(app, text="Key:").grid(column=0, row=0)
key_entry = ttk.Entry(app)
key_entry.grid(column=1, row=0)
key_entry.bind("<KeyRelease>", lambda event: update_key_matrix_display())

ttk.Label(app, text="Text:").grid(column=0, row=1)
text_entry = ttk.Entry(app)
text_entry.grid(column=1, row=1)

key_matrix_display = tk.Text(app, height=5, width=10)
key_matrix_display.grid(column=1, row=2)

encrypted_text = tk.StringVar()
ttk.Label(app, textvariable=encrypted_text).grid(column=1, row=4)

decrypted_text = tk.StringVar()
ttk.Label(app, textvariable=decrypted_text).grid(column=1, row=5)

encrypt_button = ttk.Button(app, text="Encrypt", command=encrypt_text)
encrypt_button.grid(column=0, row=3)

decrypt_button = ttk.Button(app, text="Decrypt", command=decrypt_text)
decrypt_button.grid(column=1, row=3)

copy_button = ttk.Button(app, text="Copy Encrypted Text", command=copy_encrypted_text_to_clipboard)
copy_button.grid(column=0, row=7)

app.mainloop()
