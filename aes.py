import tkinter as tk
from tkinter import messagebox
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def pad(data):
    while len(data) % 16 != 0:
        data += b' '
    return data

def encrypt(plaintext, key, mode_str):
    iv = os.urandom(16)
    key = key.encode('utf-8').ljust(16, b'0')[:16]
    plaintext = pad(plaintext.encode('utf-8'))

    if mode_str == "ECB":
        mode = modes.ECB()
    elif mode_str == "CBC":
        mode = modes.CBC(iv)
    elif mode_str == "CFB":
        mode = modes.CFB(iv)
    else:
        raise ValueError("Invalid mode")

    cipher = Cipher(algorithms.AES(key), mode, backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(plaintext) + encryptor.finalize()

    with open("ciphertext.txt", "wb") as f:
        f.write(iv + ct)

def decrypt(key, mode_str):
    try:
        with open("ciphertext.txt", "rb") as f:
            data = f.read()
    except FileNotFoundError:
        return "ciphertext.txt not found."

    iv, ct = data[:16], data[16:]
    key = key.encode('utf-8').ljust(16, b'0')[:16]

    if mode_str == "ECB":
        mode = modes.ECB()
    elif mode_str == "CBC":
        mode = modes.CBC(iv)
    elif mode_str == "CFB":
        mode = modes.CFB(iv)
    else:
        raise ValueError("Invalid mode")

    cipher = Cipher(algorithms.AES(key), mode, backend=default_backend())
    decryptor = cipher.decryptor()
    pt = decryptor.update(ct) + decryptor.finalize()
    return pt.rstrip(b' ').decode()

# GUI
def run_crypto():
    mode = mode_var.get()
    action = action_var.get()
    key = key_entry.get()
    text = input_text.get("1.0", tk.END).strip()

    if not key:
        messagebox.showerror("Error", "Please enter a secret key.")
        return

    if action == "Encrypt":
        if not text:
            messagebox.showerror("Error", "Please enter text to encrypt.")
            return
        encrypt(text, key, mode)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Text encrypted and saved to ciphertext.txt.")
    else:
        result = decrypt(key, mode)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, result)

# GUI Setup
root = tk.Tk()
root.title("AES Encryption / Decryption System")
root.geometry("500x500")

tk.Label(root, text="Input Text (to encrypt or leave blank to decrypt):").pack()
input_text = tk.Text(root, height=5)
input_text.pack()

tk.Label(root, text="Secret Key (max 16 characters):").pack()
key_entry = tk.Entry(root, show="*")
key_entry.pack()

tk.Label(root, text="Action:").pack()
action_var = tk.StringVar(value="Encrypt")
tk.Radiobutton(root, text="Encrypt", variable=action_var, value="Encrypt").pack()
tk.Radiobutton(root, text="Decrypt", variable=action_var, value="Decrypt").pack()

tk.Label(root, text="Cipher Mode:").pack()
mode_var = tk.StringVar(value="ECB")
tk.OptionMenu(root, mode_var, "ECB", "CBC", "CFB").pack()

tk.Button(root, text="Run", command=run_crypto).pack(pady=10)

tk.Label(root, text="Result:").pack()
result_text = tk.Text(root, height=5)
result_text.pack()

root.mainloop()
