import tkinter as tk
from tkinter import filedialog, messagebox

# Fungsi untuk menghapus karakter non-alfabet
def filter_alphabet(text):
    return ''.join([char for char in text if char.isalpha()])


# Vigenere Cipher
def vigenere_encrypt(plaintext, key):
    ciphertext = ""
    key_length = len(key)
    plaintext = filter_alphabet(plaintext)  # Hanya gunakan alfabet
    for i, char in enumerate(plaintext):
        if char.isalpha():
            shift = ord(key[i % key_length].upper()) - ord('A')
            ciphertext += chr((ord(char.upper()) - 65 + shift) % 26 + 65)
    return ciphertext

def vigenere_decrypt(ciphertext, key):
    plaintext = ""
    key_length = len(key)
    ciphertext = filter_alphabet(ciphertext)  # Hanya gunakan alfabet
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            shift = ord(key[i % key_length].upper()) - ord('A')
            plaintext += chr((ord(char) - 65 - shift) % 26 + 65)
    return plaintext

# Fungsi untuk enkripsi file menggunakan Extended Vigenere Cipher
def extended_vigenere_encrypt_file(filepath, key):
    with open(filepath, 'rb') as file:
        file_bytes = file.read()
    
    key_length = len(key)
    encrypted_bytes = bytearray()
    
    # Dapatkan ekstensi asli file
    file_extension = filepath.split('.')[-1]
    extension_length = len(file_extension)
    
    # Masukkan panjang ekstensi dan ekstensi itu sendiri di awal file terenkripsi
    encrypted_bytes.append(extension_length)  # Simpan panjang ekstensi
    encrypted_bytes.extend(file_extension.encode('utf-8'))  # Simpan ekstensi asli

    for i, byte in enumerate(file_bytes):
        shift = ord(key[i % key_length])
        encrypted_byte = (byte + shift) % 256
        encrypted_bytes.append(encrypted_byte)
    
    return encrypted_bytes

# Fungsi untuk dekripsi file menggunakan Extended Vigenere Cipher
def extended_vigenere_decrypt_file(filepath, key):
    with open(filepath, 'rb') as file:
        encrypted_bytes = file.read()
    
    key_length = len(key)
    decrypted_bytes = bytearray()

    # Baca panjang ekstensi
    extension_length = encrypted_bytes[0]
    file_extension = encrypted_bytes[1:1 + extension_length].decode('utf-8')

    # Sisanya adalah isi file terenkripsi
    encrypted_content = encrypted_bytes[1 + extension_length:]

    for i, byte in enumerate(encrypted_content):
        shift = ord(key[i % key_length])
        decrypted_byte = (byte - shift) % 256
        decrypted_bytes.append(decrypted_byte)
    
    return decrypted_bytes, file_extension

# Fungsi untuk memilih file dan melakukan enkripsi
def encrypt_file():
    filepath = filedialog.askopenfilename()
    if not filepath:
        return
    
    key = key_input.get().strip()
    if not key:
        messagebox.showwarning("Key Error", "Kunci tidak boleh kosong.")
        return
    
    encrypted_bytes = extended_vigenere_encrypt_file(filepath, key)
    save_path = filedialog.asksaveasfilename(defaultextension=".enc", filetypes=[("Encrypted files", "*.enc")])
    if not save_path:
        return
    
    with open(save_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_bytes)
    
    messagebox.showinfo("Success", f"File berhasil dienkripsi dan disimpan di {save_path}")

# Fungsi untuk memilih file dan melakukan dekripsi
def decrypt_file():
    filepath = filedialog.askopenfilename(filetypes=[("Encrypted files", "*.enc")])
    if not filepath:
        return
    
    key = key_input.get().strip()
    if not key:
        messagebox.showwarning("Key Error", "Kunci tidak boleh kosong.")
        return
    
    decrypted_bytes, file_extension = extended_vigenere_decrypt_file(filepath, key)
    
    # Menyimpan file didekripsi dengan ekstensi aslinya
    save_path = filedialog.asksaveasfilename(defaultextension=f".{file_extension}", filetypes=[(f"{file_extension} files", f"*.{file_extension}")])
    if not save_path:
        return
    
    with open(save_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_bytes)
    
    messagebox.showinfo("Success", f"File berhasil didekripsi dan disimpan di {save_path}")


# Playfair Cipher

def generate_playfair_matrix(key):
    key = filter_alphabet(key.upper().replace("J", "I"))
    key = ''.join(sorted(set(key), key=key.index))  # Hapus duplikat dan urutkan
    key += ''.join([chr(i) for i in range(65, 91) if chr(i) not in key])  # Tambahkan huruf sisa
    matrix = [key[i:i + 5] for i in range(0, 25, 5)]
    return matrix

def playfair_encrypt(plaintext, key):
    matrix = generate_playfair_matrix(key)
    plaintext = filter_alphabet(plaintext.upper().replace("J", "I"))  # Hanya alfabet
    plaintext_pairs = []

    i = 0
    while i < len(plaintext):
        a = plaintext[i]
        b = plaintext[i + 1] if (i + 1) < len(plaintext) else 'X'
        if a == b:
            b = 'X'
            i -= 1
        plaintext_pairs.append((a, b))
        i += 2

    encrypted = ""
    for a, b in plaintext_pairs:
        row_a, col_a = next((r, c) for r, row in enumerate(matrix) for c, val in enumerate(row) if val == a)
        row_b, col_b = next((r, c) for r, row in enumerate(matrix) for c, val in enumerate(row) if val == b)

        if row_a == row_b:
            encrypted += matrix[row_a][(col_a + 1) % 5] + matrix[row_b][(col_b + 1) % 5]
        elif col_a == col_b:
            encrypted += matrix[(row_a + 1) % 5][col_a] + matrix[(row_b + 1) % 5][col_b]
        else:
            encrypted += matrix[row_a][col_b] + matrix[row_b][col_a]

    return encrypted

def playfair_decrypt(ciphertext, key):
    matrix = generate_playfair_matrix(key)
    ciphertext = filter_alphabet(ciphertext.upper().replace("J", "I"))

    ciphertext_pairs = []
    for i in range(0, len(ciphertext), 2):
        a = ciphertext[i]
        b = ciphertext[i + 1] if (i + 1) < len(ciphertext) else 'X'
        ciphertext_pairs.append((a, b))

    decrypted = ""
    for a, b in ciphertext_pairs:
        row_a, col_a = next((r, c) for r, row in enumerate(matrix) for c, val in enumerate(row) if val == a)
        row_b, col_b = next((r, c) for r, row in enumerate(matrix) for c, val in enumerate(row) if val == b)

        if row_a == row_b:
            decrypted += matrix[row_a][(col_a - 1) % 5] + matrix[row_b][(col_b - 1) % 5]
        elif col_a == col_b:
            decrypted += matrix[(row_a - 1) % 5][col_a] + matrix[(row_b - 1) % 5][col_b]
        else:
            decrypted += matrix[row_a][col_b] + matrix[row_b][col_a]

    return decrypted

# One-time Pad
def one_time_pad_encrypt(plaintext, key):
    ciphertext = ""
    plaintext = filter_alphabet(plaintext)  # Hanya alfabet
    key = filter_alphabet(key)
    key_length = len(key)
    for i, char in enumerate(plaintext):
        shift = ord(key[i % key_length].upper()) - ord('A')
        ciphertext += chr((ord(char.upper()) - 65 + shift) % 26 + 65)
    return ciphertext

def one_time_pad_decrypt(ciphertext, key):
    plaintext = ""
    ciphertext = filter_alphabet(ciphertext)  # Hanya alfabet
    key = filter_alphabet(key)
    key_length = len(key)
    for i, char in enumerate(ciphertext):
        shift = ord(key[i % key_length].upper()) - ord('A')
        plaintext += chr((ord(char) - 65 - shift) % 26 + 65)
    return plaintext

# Simple Enigma Machine (Mockup)
class SimpleEnigma:
    def __init__(self):
        self.shift = 3  # Perubahan sederhana untuk contoh

    def encrypt_char(self, char):
        if char.isalpha():
            return chr((ord(char) - 65 + self.shift) % 26 + 65)  # Pergeseran huruf
        return char

    def decrypt_char(self, char):
        if char.isalpha():
            return chr((ord(char) - 65 - self.shift) % 26 + 65)  # Pembalikan pergeseran
        return char

# File operations
def load_file():
    filepath = filedialog.askopenfilename()
    if not filepath:
        return
    with open(filepath, 'r') as file:
        content = file.read()
        text_input.delete('1.0', tk.END)
        text_input.insert(tk.END, content)

def save_ciphertext(ciphertext):
    if not ciphertext:
        messagebox.showwarning("Save Error", "No ciphertext to save.")
        return
    
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if not filepath:
        return
    with open(filepath, 'w') as file:
        file.write(ciphertext)

def load_key_file():
    filepath = filedialog.askopenfilename()
    if not filepath:
        return
    with open(filepath, 'r') as file:
        key_content = file.read()
        key_input.delete(0, tk.END)
        key_input.insert(tk.END, key_content)

# Display modes for ciphertext
def display_ciphertext(ciphertext, mode='normal'):
    if mode == 'grouped':
        return ' '.join([ciphertext[i:i + 5] for i in range(0, len(ciphertext), 5)])
    return ciphertext.replace(" ", "")

# GUI Setup
def update_buttons_state():
    if cipher_var.get() == 2:  # Extended Vigenere Cipher
        encrypt_buttonEXC.config(state=tk.NORMAL)
        decrypt_buttonEXC.config(state=tk.NORMAL)
    else:
        encrypt_buttonEXC.config(state=tk.DISABLED)
        decrypt_buttonEXC.config(state=tk.DISABLED)

# Panggil fungsi update_buttons_state() saat ada perubahan pilihan cipher
    cipher_var.trace("w", lambda *args: update_buttons_state())

def encrypt_text():
    plaintext = text_input.get("1.0", tk.END).strip()
    key = key_input.get().strip()
    
    if cipher_var.get() == 1:  # Vigenere
        ciphertext = vigenere_encrypt(plaintext, key)
    elif cipher_var.get() == 2:  # Extended Vigenere
        ciphertext = extended_vigenere_encrypt(plaintext, key)
    elif cipher_var.get() == 3:  # Playfair
        ciphertext = playfair_encrypt(plaintext, key)
    elif cipher_var.get() == 4:  # One-time Pad
        ciphertext = one_time_pad_encrypt(plaintext, key)
    elif cipher_var.get() == 5:  # Enigma
        enigma = SimpleEnigma()
        ciphertext = ''.join(enigma.encrypt_char(char) for char in plaintext)
    
    display_mode = display_mode_var.get()
    formatted_ciphertext = display_ciphertext(ciphertext, display_mode)
    ciphertext_output.delete('1.0', tk.END)
    ciphertext_output.insert(tk.END, formatted_ciphertext)

def decrypt_text():
    ciphertext = text_input.get("1.0", tk.END).strip()
    key = key_input.get().strip()
    
    if cipher_var.get() == 1:  # Vigenere
        plaintext = vigenere_decrypt(ciphertext, key)
    elif cipher_var.get() == 2:  # Extended Vigenere
        plaintext = extended_vigenere_decrypt(ciphertext, key)
    elif cipher_var.get() == 3:  # Playfair
        plaintext = playfair_decrypt(ciphertext, key)
    elif cipher_var.get() == 4:  # One-time Pad
        plaintext = one_time_pad_decrypt(ciphertext, key)
    elif cipher_var.get() == 5:  # Enigma
        enigma = SimpleEnigma()
        plaintext = ''.join(enigma.decrypt_char(char) for char in ciphertext)

    plaintext_output.delete('1.0', tk.END)
    plaintext_output.insert(tk.END, plaintext)

root = tk.Tk()
root.title("Cipher Algorithms")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

cipher_var = tk.IntVar()
cipher_var.set(1)  # Default to Vigenere

cipher_options = [
    ("Vigenere Cipher", 1),
    ("Extended Vigenere Cipher", 2),
    ("Playfair Cipher", 3),
    ("One-time Pad", 4),
    ("Enigma Machine", 5)
]
for text, value in cipher_options:
    tk.Radiobutton(frame, text=text, variable=cipher_var, value=value).pack(anchor=tk.W)

key_label = tk.Label(frame, text="Key:")
key_label.pack()
key_input = tk.Entry(frame)
key_input.pack()

text_label = tk.Label(frame, text="Text:")
text_label.pack()
text_input = tk.Text(frame, height=5, width=50)
text_input.pack()

ciphertext_label = tk.Label(frame, text="Ciphertext:")
ciphertext_label.pack()
ciphertext_output = tk.Text(frame, height=5, width=50)
ciphertext_output.pack()

plaintext_label = tk.Label(frame, text="Plaintext:")
plaintext_label.pack()
plaintext_output = tk.Text(frame, height=5, width=50)
plaintext_output.pack()

display_mode_var = tk.StringVar()
display_mode_var.set('normal')  # Default display mode
display_mode_options = [
    ("Tanpa spasi", 'normal'),
    ("Kelompok 5-huruf", 'grouped')
]
for text, value in display_mode_options:
    tk.Radiobutton(frame, text=text, variable=display_mode_var, value=value).pack(anchor=tk.W)

button_frame = tk.Frame(root)
button_frame.pack(pady=5)
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)
encrypt_button = tk.Button(button_frame, text="Enkripsi text", command=encrypt_text)
encrypt_button.pack(side=tk.LEFT, padx=5)

decrypt_button = tk.Button(button_frame, text="Deskripsi text", command=decrypt_text)
decrypt_button.pack(side=tk.LEFT, padx=5)

encrypt_buttonEXC = tk.Button(frame, text="Enkripsi File(hanya untuk Extended Vigenere Cipher)", command=encrypt_file)
encrypt_buttonEXC.grid(row=1, column=0, padx=5, pady=5)

decrypt_buttonEXC = tk.Button(frame, text="Deskripsi File(hanya untuk Extended Vigenere Cipher)", command=decrypt_file)
decrypt_buttonEXC.grid(row=1, column=1, padx=5, pady=5)

load_file_button = tk.Button(button_frame, text="Masukan File", command=load_file)
load_file_button.pack(side=tk.LEFT, padx=5)

save_button = tk.Button(button_frame, text="Simpan Ciphertext", command=lambda: save_ciphertext(ciphertext_output.get("1.0", tk.END).strip()))
save_button.pack(side=tk.LEFT, padx=5)

load_key_file_button = tk.Button(button_frame, text="Masukan kunci file", command=load_key_file)
load_key_file_button.pack(side=tk.LEFT, padx=5)

update_buttons_state()

root.mainloop()