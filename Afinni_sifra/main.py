import tkinter as tk
import unicodedata

def remove_duplicates(text):
    return "".join(sorted(set(text), key=text.index))

def remove_spaces(text):
    return text.replace(" ", "")

def coding(strng):
    strng = unicodedata.normalize('NFD', strng)
    strng = u"".join([c for c in strng if not unicodedata.combining(c)])
    strng = remove_spaces(strng)
    return strng

def fixed_text(strng):
    CHARS_TO_REMOVE = '''!ˇ´()-[]{};:'",<>./?@#$%^&*_~'''
    for char in CHARS_TO_REMOVE:
        strng = strng.replace(char, "")
    strng = str.lower(strng)
    strng = coding(strng)
    return strng

def create_playfair_table(key):
    key = remove_duplicates(key)
    keyT = [['' for _ in range(5)] for _ in range(5)]
    alphabet = 'abcdefghiklmnopqrstuvwxyz'  # 'j' is omitted
    key += alphabet

    i, j = 0, 0
    for char in key:
        keyT[i][j] = char
        j += 1
        if j == 5:
            i += 1
            j = 0
        if i == 5:
            break

    return keyT

def search(keyT, a, b):
    arr = [0, 0, 0, 0]
    if a == 'w':
        a = 'v'
    elif b == 'w':
        b = 'v'
    for i in range(5):
        for j in range(5):
            if keyT[i][j] == a:
                arr[0], arr[1] = i, j
            elif keyT[i][j] == b:
                arr[2], arr[3] = i, j
    return arr

def mod5(a):
    if a < 0:
        a += 5
    return a % 5

def encrypt(str, keyT):
    ps = len(str)

    # If the length is odd, append a dummy character
    if ps % 2 == 1:
        str += 'x'

    i = 0
    encrypted_pairs = []
    while i < ps:
        # Check if i + 1 is within the bounds of the string
        if i + 1 < ps:
            a = search(keyT, str[i], str[i + 1])
            if a[0] == a[2]:
                encrypted_pairs.append(keyT[a[0]][mod5(a[1] + 1)] + keyT[a[0]][mod5(a[3] + 1)])
            elif a[1] == a[3]:
                encrypted_pairs.append(keyT[mod5(a[0] + 1)][a[1]] + keyT[mod5(a[2] + 1)][a[1]])
            else:
                encrypted_pairs.append(keyT[a[0]][a[3]] + keyT[a[2]][a[1]])
            i += 2
        else:
            # If i + 1 is out of bounds, handle the last character
            a = search(keyT, str[i], 'x')  # Assume 'x' as the dummy character
            encrypted_pairs.append(keyT[a[0]][mod5(a[1] + 1)] + 'x')
            break

    return " ".join(encrypted_pairs)

def decrypt(str, keyT):
    ps = len(str)

    i = 0
    decrypted_pairs = []
    while i < ps:
        # Check if i + 1 is within the bounds of the string
        if i + 1 < ps:
            a = search(keyT, str[i], str[i + 1])
            if a[0] == a[2]:
                decrypted_pairs.append(keyT[a[0]][mod5(a[1] - 1)] + keyT[a[0]][mod5(a[3] - 1)])
            elif a[1] == a[3]:
                decrypted_pairs.append(keyT[mod5(a[0] - 1)][a[1]] + keyT[mod5(a[2] - 1)][a[1]])
            else:
                decrypted_pairs.append(keyT[a[0]][a[3]] + keyT[a[2]][a[1]])
            i += 2
        else:
            # If i + 1 is out of bounds, handle the last character
            a = search(keyT, str[i], 'x')  # Assume 'x' as the dummy character
            decrypted_pairs.append(keyT[a[0]][mod5(a[1] - 1)] + 'x' if str[i] == 'x' else keyT[a[0]][mod5(a[1] - 1)])
            break

    return "".join(decrypted_pairs)

def decrypt_by_playfair_cipher(str, key):
    ks = len(key)
    key = fixed_text(key)
    str = fixed_text(str)
    keyT = create_playfair_table(key)
    return decrypt(str, keyT)

def encrypt_by_playfair_cipher(str, key):
    ks = len(key)
    key = fixed_text(key)
    str = fixed_text(str)
    keyT = create_playfair_table(key)

    # Display the encryption table in the GUI
    key_table_text = "\n".join([" ".join(row) for row in keyT])
    key_table_label.config(text=f"Šifrovací tabulka:\n{key_table_text}")

    return encrypt(str, keyT)

def encrypt_command():
    key = textbox_key.get()
    text = textbox_text.get()
    result = encrypt_by_playfair_cipher(text, key)
    encrypted_result_label.config(text=result)

def decrypt_and_display_command():
    key = textbox_key.get()
    text = textbox_text_decrypt.get()
    result = decrypt_by_playfair_cipher(text, key)
    decrypted_result_label.config(text=result)

root = tk.Tk()
root.geometry("800x800")
root.title("Playfair")

label_key = tk.Label(root, text="Klíč", font=('Arial', 18))
label_key.pack(padx=20, pady=20)
textbox_key = tk.Entry(root, font=('Arial', 16))  # Change from Text to Entry
textbox_key.pack()

label_text = tk.Label(root, text="Zadejte text k zašifrování", font=('Arial', 18))
label_text.pack(padx=20, pady=20)
textbox_text = tk.Entry(root, font=('Arial', 16))  # Change from Text to Entry
textbox_text.pack()

label_text_decrypt = tk.Label(root, text="Zadejte dešifrování", font=('Arial', 18))
label_text_decrypt.pack(padx=20, pady=20)
textbox_text_decrypt = tk.Entry(root, font=('Arial', 16))  # Change from Text to Entry
textbox_text_decrypt.pack()

encrypted_result_label = tk.Label(root, text="", font=('Arial', 16))
encrypted_result_label.pack(pady=20)

decrypted_result_label = tk.Label(root, text="", font=('Arial', 16))
decrypted_result_label.pack(pady=20)

# Add label for displaying encryption table
key_table_label = tk.Label(root, text="", font=('Arial', 16))
key_table_label.pack(pady=20)

Button_encrypt = tk.Button(root, text="Zašifrovat", command=encrypt_command)
Button_encrypt.pack(side=tk.LEFT, padx=20, pady=20)

# Add decryption functionality
Button_decrypt = tk.Button(root, text="Dešifrovat", command=decrypt_and_display_command)
Button_decrypt.pack(side=tk.LEFT, padx=20, pady=20)

root.mainloop()