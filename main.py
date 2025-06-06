import tkinter as tk
from RC4 import rc4_run
from RSA import rsa_app

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Encryption Selector")
root.geometry("400x300")

# Tạo tiêu đề
title_label = tk.Label(root, text="Select Encryption Method", font=("Arial", 18))
title_label.pack(pady=20)

# Nút chọn RC4
rc4_button = tk.Button(root, text="RC4", font=("Arial", 14), width=15, command=lambda: rc4_run())
rc4_button.pack(pady=10)

# Nút chọn RSA
rsa_button = tk.Button(root, text="RSA", font=("Arial", 14), width=15, command=lambda: rsa_app(root))
rsa_button.pack(pady=10)

# Chạy vòng lặp chính
root.mainloop()
