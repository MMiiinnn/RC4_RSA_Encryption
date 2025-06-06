import random
from math import gcd
import tkinter as tk
from tkinter import messagebox


def is_prime(num):
    """Kiểm tra số nguyên tố."""
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True


def generate_prime(is_large=False):
    """Tạo số nguyên tố, nếu is_large=True sẽ tạo số nguyên tố lớn."""
    if is_large:
        start, end = 10000, 100000  # Phạm vi số nguyên tố lớn
    else:
        start, end = 10, 100  # Phạm vi số nguyên tố nhỏ

    primes = [i for i in range(start, end) if is_prime(i)]
    return random.choice(primes)


def mod_inverse(e, phi):
    """Thuật toán Euclid mở rộng để tìm nghịch đảo modulo."""
    d = 0
    x1, x2  , y1 = 0, 1, 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi, e = e, temp2
        x = x2 - temp1 * x1
        y = d - temp1 * y1
        x2, x1 = x1, x
        d, y1 = y1, y

    if temp_phi == 1:
        return d + phi


def generate_keys(is_large=False):
    """Tạo khóa công khai và khóa riêng với số nguyên tố nhỏ hoặc lớn."""
    p = generate_prime(is_large)
    q = generate_prime(is_large)
    while p == q:
        q = generate_prime(is_large)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(2, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)

    d = mod_inverse(e, phi)

    return ((e, n), (d, n), p, q, n, e, d)


def encrypt(public_key, plaintext):
    """Mã hóa thông điệp với khóa công khai."""
    e, n = public_key
    ciphertext = [pow(ord(char), e, n) for char in plaintext]
    return ciphertext


def decrypt(private_key, ciphertext):
    """Giải mã thông điệp với khóa riêng."""
    d, n = private_key
    plaintext = ''.join([chr(pow(char, d, n)) for char in ciphertext])
    return plaintext


# GUI Application
def rsa_app():
    def generate_keys_gui():
        """Tạo và hiển thị khóa công khai, khóa riêng với số nguyên tố nhỏ."""
        global public_key, private_key, p, q, n, e, d
        public_key, private_key, p, q, n, e, d = generate_keys(is_large=False)
        # Hiển thị các giá trị trong các widget Entry
        p_entry.delete(0, tk.END)
        p_entry.insert(0, str(p))
        q_entry.delete(0, tk.END)
        q_entry.insert(0, str(q))
        n_entry.delete(0, tk.END)
        n_entry.insert(0, str(n))
        e_entry.delete(0, tk.END)
        e_entry.insert(0, str(e))
        d_entry.delete(0, tk.END)
        d_entry.insert(0, str(d))
        pub_key_entry.delete(0, tk.END)
        pub_key_entry.insert(0, str(public_key))
        priv_key_entry.delete(0, tk.END)
        priv_key_entry.insert(0, str(private_key))

    def generate_pq_gui():
        """Tạo tự động p và q với số nguyên tố nhỏ và hiển thị giá trị."""
        global p, q
        p = generate_prime(is_large=False)
        q = generate_prime(is_large=False)
        while p == q:
            q = generate_prime(is_large=False)

        # Hiển thị giá trị p và q trong các widget Entry
        p_entry.delete(0, tk.END)
        p_entry.insert(0, str(p))
        q_entry.delete(0, tk.END)
        q_entry.insert(0, str(q))

        # Xóa các giá trị của khóa công khai, khóa riêng, n, e, và d
        pub_key_entry.delete(0, tk.END)
        priv_key_entry.delete(0, tk.END)
        n_entry.delete(0, tk.END)
        e_entry.delete(0, tk.END)
        d_entry.delete(0, tk.END)

        # Đặt giá trị toàn cục về None để tránh nhầm lẫn
        global public_key, private_key, n, e, d
        public_key = None
        private_key = None
        n = e = d = None

    def generate_large_keys_gui():
        """Tạo khóa với số nguyên tố lớn."""
        global public_key, private_key, p, q, n, e, d
        public_key, private_key, p, q, n, e, d = generate_keys(is_large=True)
        # Hiển thị các giá trị trong các widget Entry
        p_entry.delete(0, tk.END)
        p_entry.insert(0, str(p))
        q_entry.delete(0, tk.END)
        q_entry.insert(0, str(q))
        n_entry.delete(0, tk.END)
        n_entry.insert(0, str(n))
        e_entry.delete(0, tk.END)
        e_entry.insert(0, str(e))
        d_entry.delete(0, tk.END)
        d_entry.insert(0, str(d))
        pub_key_entry.delete(0, tk.END)
        pub_key_entry.insert(0, str(public_key))
        priv_key_entry.delete(0, tk.END)
        priv_key_entry.insert(0, str(private_key))

    def encrypt_message():
        """Mã hóa thông điệp nhập vào."""
        try:
            n = int(n_entry.get())
            e = int(e_entry.get())
            plaintext = message_entry.get()

            if not plaintext:
                messagebox.showerror("Lỗi", "Vui lòng nhập thông điệp cần mã hóa.")
                return

            ciphertext = [pow(ord(char), e, n) for char in plaintext]
            encrypted_message.set(ciphertext)
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ trong các trường 'n' và 'e'.")
        except Exception as ex:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi mã hóa: {ex}")

    def decrypt_message():
        """Giải mã thông điệp đã mã hóa."""
        try:
            n = int(n_entry.get())
            d = int(d_entry.get())
            ciphertext = eval(encrypted_message.get())

            if not ciphertext:
                messagebox.showerror("Lỗi", "Không có thông điệp mã hóa để giải mã.")
                return

            plaintext = ''.join([chr(pow(char, d, n)) for char in ciphertext])
            decrypted_message.set(plaintext)
            # So sánh plaintext với thông điệp ban đầu
            if plaintext != message_entry.get():
                messagebox.showwarning(
                    "Cảnh báo",
                    "Decrypt và Plain text không trùng khớp, giá trị đã bị thay đổi ở đâu đó!"
                )
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ trong các trường 'n' và 'd'.")
        except Exception as ex:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi giải mã: {ex}")

    root = tk.Tk()
    root.title("RSA - Nhóm 14 ATM")

    main_frame = tk.Frame(root)
    main_frame.pack(expand=True, fill=tk.BOTH)

    tk.Label(main_frame, text="Thông điệp (message):").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    message_entry = tk.Entry(main_frame, width=50)
    message_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Button(main_frame, text="Tạo Khóa", command=generate_keys_gui).grid(row=1, column=0, padx=10, pady=10)
    tk.Button(main_frame, text="Tạo tự động p và q", command=generate_pq_gui).grid(row=1, column=1, padx=10, pady=10)
    tk.Button(main_frame, text="Tạo khóa với số lớn\n(5 chữ số)", command=generate_large_keys_gui).grid(row=1, column=2, padx=10, pady=10)

    tk.Label(main_frame, text="Số nguyên tố p:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    p_entry = tk.Entry(main_frame, width=50)
    p_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(main_frame, text="Số nguyên tố q:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    q_entry = tk.Entry(main_frame, width=50)
    q_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(main_frame, text="Khóa công khai:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    pub_key_entry = tk.Entry(main_frame, width=50)
    pub_key_entry.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(main_frame, text="Khóa riêng:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    priv_key_entry = tk.Entry(main_frame, width=50)
    priv_key_entry.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(main_frame, text="n:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
    n_entry = tk.Entry(main_frame, width=50)
    n_entry.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(main_frame, text="e:").grid(row=7, column=0, padx=10, pady=5, sticky="e")
    e_entry = tk.Entry(main_frame, width=50)
    e_entry.grid(row=7, column=1, padx=10, pady=5)

    tk.Label(main_frame, text="d:").grid(row=8, column=0, padx=10, pady=5, sticky="e")
    d_entry = tk.Entry(main_frame, width=50)
    d_entry.grid(row=8, column=1, padx=10, pady=5)

    tk.Button(main_frame, text="Mã hóa", command=encrypt_message).grid(row=9, column=0, padx=10, pady=10)
    tk.Button(main_frame, text="Giải mã", command=decrypt_message).grid(row=9, column=1, padx=10, pady=10)

    encrypted_message = tk.StringVar()
    tk.Label(main_frame, text="Thông điệp mã hóa:").grid(row=10, column=0, padx=10, pady=10, sticky="e")
    tk.Entry(main_frame, textvariable=encrypted_message, width=50).grid(row=10, column=1, padx=10, pady=10)

    decrypted_message = tk.StringVar()
    tk.Label(main_frame, text="Thông điệp giải mã:").grid(row=11, column=0, padx=10, pady=10, sticky="e")
    tk.Entry(main_frame, textvariable=decrypted_message, width=50).grid(row=11, column=1, padx=10, pady=10)

    root.mainloop()


public_key = None
private_key = None
p = q = n = e = d = None
rsa_app()
