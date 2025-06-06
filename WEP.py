import tkinter as tk
from tkinter import filedialog, messagebox
import codecs
import os
import zlib
import random

MOD = 256


def rc4_run():
    # Tạo S box hoán vị
    def ksa(key):
        key_length = len(key)
        S = list(range(MOD))
        j = 0
        for i in range(MOD):
            j = (j + S[i] + ord(key[i % key_length])) % MOD
            S[i], S[j] = S[j], S[i]
        return S

    # Tạo Key Stream
    def prga(S):
        i = 0
        j = 0
        while True:
            i = (i + 1) % MOD
            j = (j + S[i]) % MOD
            S[i], S[j] = S[j], S[i]
            K = S[(S[i] + S[j]) % MOD]
            yield K

    # Lấy giá trị Key Stream khi truyền key vào
    def get_keystream(key):
        S = ksa(key)
        return prga(S)

    # Thuật toán RC4
    def rc4(key, text, iv):
        keystream = get_keystream(key + str(iv))
        res = []
        for c in text:
            res.append(c ^ next(keystream))
        return bytes(res)

    def encrypt(key, plaintext, iv):
        plaintext = [ord(c) for c in plaintext]
        return rc4(key, plaintext, iv)

    def decrypt(key, ciphertext, iv):
        res = rc4(key, ciphertext, iv)
        return res

    def open_file():
        filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if filepath:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            entry_plaintext.delete(1.0, tk.END)
            entry_plaintext.insert(tk.END, content)
            lbl_file.config(text=f"Loaded File: {os.path.basename(filepath)}")

    def save_file(content, filetype="encrypted"):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)
            messagebox.showinfo("Success", f"{filetype.capitalize()} file saved successfully!")

    def perform_encryption():
        key = entry_key.get()
        plaintext = entry_plaintext.get(1.0, tk.END).strip()

        if not key or not plaintext:
            messagebox.showerror("Error", "Key and Plaintext are required!")
            return

        # Compute CRC32 (Integrity Check Value)
        # Chuyển plaintext về dạng byte
        byte_text = plaintext.encode('utf-8')

        # print("byte_text = ", byte_text)
        # print(list(byte_text))

        # Sử dụng hàm crc32 để lấy mã CRC từ byte_text
        crc_text = zlib.crc32(byte_text)
        # Chuyển CRC sang byte rồi gắn vào byte_text
        byte_text += crc_text.to_bytes(4, byteorder='big')

        # Tạo IV (32-bit) (Initialization Vector)
        iv = random.getrandbits(32)

        try:
            ciphertext = rc4(key, byte_text, iv)

            ciphertext_with_iv = f"{iv:08X}" + str(ciphertext)  # Thêm iv vào đầu ciphertext
            # print("ciphertext_with_iv = ", ciphertext_with_iv)
            save_file(ciphertext_with_iv, "encrypted")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def perform_decryption():
        key = entry_key.get()
        ciphertext_with_iv = entry_plaintext.get(1.0, tk.END).strip()

        if not key or not ciphertext_with_iv:
            messagebox.showerror("Error", "Key and Ciphertext are required!")
            return

        try:
            # Tách iv và ciphertext ra khỏi khối
            iv = int(ciphertext_with_iv[:8], 16)
            ciphertext = ciphertext_with_iv[8:]
            ciphertext = ciphertext.encode()
            cleaned_str = ciphertext[2:-1]
            byte_data = codecs.decode(cleaned_str, 'unicode_escape').encode('latin1')

            plaintext_withCRC = decrypt(key, byte_data, iv)
            # print('plain text: ', plaintext_withCRC)

            crc_received = plaintext_withCRC[-4:]
            plaintext = plaintext_withCRC[:-4]

            #         print("CRC: ", crc_received)
            #         print('plain text without crc: ', plaintext)

            # Verify CRC32
            crc_computed = zlib.crc32(plaintext)

            if int.from_bytes(crc_received, byteorder='big') == crc_computed:
                save_file(plaintext.decode('utf-8'), "decrypted")
            else:
                messagebox.showerror("Error", "CRC không khớp, dữ liệu có thể đã bị thay đổi.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # GUI Application
    root = tk.Tk()
    root.title("RC4 Encryption/Decryption")
    root.geometry("500x400")
    root.resizable(False, False)

    # Key
    tk.Label(root, text="Key:", font=("Arial", 12), bg="#f0f0f0", fg="#333333").pack(pady=5)
    entry_key = tk.Entry(root, width=50, font=("Arial", 12))
    entry_key.pack(pady=5)

    # File Info
    lbl_file = tk.Label(root, text="No file loaded", font=("Arial", 10), fg="gray", bg="#f0f0f0")
    lbl_file.pack(pady=5)

    # Text Area
    entry_plaintext = tk.Text(root, height=10, width=60, font=("Arial", 12), bg="#ffffff", fg="#000000")
    entry_plaintext.pack(pady=5)

    # Buttons
    frame_buttons = tk.Frame(root, bg="#f0f0f0")
    frame_buttons.pack(pady=10)

    btn_load = tk.Button(frame_buttons, text="Load File", font=("Arial", 12), bg="#4caf50", fg="white",
                         command=open_file)
    btn_load.grid(row=0, column=0, padx=10)

    btn_encrypt = tk.Button(frame_buttons, text="Encrypt & Save", font=("Arial", 12), bg="#2196f3", fg="white",
                            command=perform_encryption)
    btn_encrypt.grid(row=0, column=1, padx=10)

    btn_decrypt = tk.Button(frame_buttons, text="Decrypt & Save", font=("Arial", 12), bg="#f44336", fg="white",
                            command=perform_decryption)
    btn_decrypt.grid(row=0, column=2, padx=10)

    # Run the application
    root.mainloop()
