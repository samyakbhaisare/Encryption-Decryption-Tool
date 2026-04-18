from cryptography.fernet import Fernet
import os
import base64
from datetime import datetime

KEY_FILE = "secret.key"
DECRYPTED_OUTPUT_FILE = "decrypted_output.txt"
ENCRYPTED_OUTPUT_FILE = "encrypted_output.txt"
LOG_FILE = "logs.txt"


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def write_log(action, input_text, output_text, status="SUCCESS"):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write(f"Timestamp : {get_timestamp()}\n")
        f.write(f"Action    : {action}\n")
        f.write(f"Status    : {status}\n")
        f.write(f"Input     : {input_text}\n")
        f.write(f"Output    : {output_text}\n")
        f.write("=" * 70 + "\n\n")


def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    print("\n[SUCCESS] Fernet key generated and saved in secret.key")
    write_log("Generate Key", "N/A", "Key saved in secret.key")


def load_key():
    if not os.path.exists(KEY_FILE):
        print("\n[INFO] Key file not found. Generating a new key...")
        generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()


def show_menu():
    print("\n" + "=" * 65)
    print("            ENCRYPTION & DECRYPTION TOOL")
    print("=" * 65)
    print(" 1. Generate Key         2. Fernet Encrypt")
    print(" 3. Fernet Decrypt       4. Base64 Encode")
    print(" 5. Base64 Decode        6. Hex Encode")
    print(" 7. Hex Decode           8. Caesar Encrypt")
    print(" 9. Caesar Decrypt      10. View Saved Logs")
    print("11. Exit")
    print("=" * 65)


def show_result(title, input_text, output_text):
    print("\n" + "-" * 65)
    print(title)
    print("-" * 65)
    print("Input  :", input_text)
    print("Output :", output_text)
    print("-" * 65)


def validate_text(text, field_name="Input"):
    if not text.strip():
        print(f"\n[ERROR] {field_name} cannot be empty.")
        return False
    return True


def save_encrypted_output(text):
    with open(ENCRYPTED_OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[SUCCESS] Encrypted output auto-saved in {ENCRYPTED_OUTPUT_FILE}")


def save_decrypted_output(text):
    with open(DECRYPTED_OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[SUCCESS] Decrypted output auto-saved in {DECRYPTED_OUTPUT_FILE}")


def save_general_output(text, filename="last_output.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[SUCCESS] Output auto-saved in {filename}")


def fernet_encrypt(text, key):
    f = Fernet(key)
    return f.encrypt(text.encode()).decode()


def fernet_decrypt(encrypted_text, key):
    f = Fernet(key)
    return f.decrypt(encrypted_text.encode()).decode()


def base64_encode(text):
    return base64.b64encode(text.encode()).decode()


def base64_decode(encoded_text):
    return base64.b64decode(encoded_text.encode()).decode()


def hex_encode(text):
    return text.encode().hex()


def hex_decode(hex_text):
    return bytes.fromhex(hex_text).decode()


def caesar_encrypt(text, shift):
    shift = shift % 26
    result = ""
    for ch in text:
        if ch.isalpha():
            start = ord("A") if ch.isupper() else ord("a")
            result += chr((ord(ch) - start + shift) % 26 + start)
        else:
            result += ch
    return result


def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)


def view_logs():
    print("\n" + "=" * 65)
    print("                        SAVED LOGS")
    print("=" * 65)

    if not os.path.exists(LOG_FILE):
        print("[INFO] No logs found yet.")
        return

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        print("[INFO] Log file is empty.")
    else:
        print(content)


def main():
    while True:
        show_menu()
        choice = input("Enter choice (1-11): ").strip()

        if choice == "1":
            generate_key()

        elif choice == "2":
            key = load_key()
            text = input("Enter text to encrypt: ")
            if not validate_text(text, "Text"):
                continue

            try:
                encrypted = fernet_encrypt(text, key)
                show_result("FERNET ENCRYPT RESULT", text, encrypted)
                save_encrypted_output(encrypted)
                write_log("Fernet Encrypt", text, encrypted)
            except Exception as e:
                print(f"\n[ERROR] Encryption failed: {e}")
                write_log("Fernet Encrypt", text, "Encryption failed", "FAILED")

        elif choice == "3":
            key = load_key()
            encrypted_text = input("Enter encrypted text: ")
            if not validate_text(encrypted_text, "Encrypted text"):
                continue

            try:
                decrypted = fernet_decrypt(encrypted_text, key)
                show_result("FERNET DECRYPT RESULT", encrypted_text, decrypted)
                save_decrypted_output(decrypted)
                write_log("Fernet Decrypt", encrypted_text, decrypted)
            except Exception:
                print("\n[ERROR] Invalid encrypted text or wrong key.")
                write_log("Fernet Decrypt", encrypted_text, "Invalid encrypted text or wrong key", "FAILED")

        elif choice == "4":
            text = input("Enter text for Base64 encode: ")
            if not validate_text(text, "Text"):
                continue
            try:
                result = base64_encode(text)
                show_result("BASE64 ENCODE RESULT", text, result)
                save_general_output(result, "base64_encoded.txt")
                write_log("Base64 Encode", text, result)
            except Exception as e:
                print(f"\n[ERROR] Base64 encode failed: {e}")
                write_log("Base64 Encode", text, "Encoding failed", "FAILED")

        elif choice == "5":
            encoded_text = input("Enter Base64 text to decode: ")
            if not validate_text(encoded_text, "Base64 text"):
                continue
            try:
                result = base64_decode(encoded_text)
                show_result("BASE64 DECODE RESULT", encoded_text, result)
                save_general_output(result, "base64_decoded.txt")
                write_log("Base64 Decode", encoded_text, result)
            except Exception:
                print("\n[ERROR] Invalid Base64 input.")
                write_log("Base64 Decode", encoded_text, "Invalid Base64 input", "FAILED")

        elif choice == "6":
            text = input("Enter text for Hex encode: ")
            if not validate_text(text, "Text"):
                continue
            try:
                result = hex_encode(text)
                show_result("HEX ENCODE RESULT", text, result)
                save_general_output(result, "hex_encoded.txt")
                write_log("Hex Encode", text, result)
            except Exception as e:
                print(f"\n[ERROR] Hex encode failed: {e}")
                write_log("Hex Encode", text, "Encoding failed", "FAILED")

        elif choice == "7":
            hex_text = input("Enter Hex text to decode: ")
            if not validate_text(hex_text, "Hex text"):
                continue
            try:
                result = hex_decode(hex_text)
                show_result("HEX DECODE RESULT", hex_text, result)
                save_general_output(result, "hex_decoded.txt")
                write_log("Hex Decode", hex_text, result)
            except Exception:
                print("\n[ERROR] Invalid Hex input.")
                write_log("Hex Decode", hex_text, "Invalid Hex input", "FAILED")

        elif choice == "8":
            text = input("Enter text for Caesar encryption: ")
            if not validate_text(text, "Text"):
                continue
            try:
                shift = int(input("Enter shift value: "))
                result = caesar_encrypt(text, shift)
                show_result("CAESAR ENCRYPT RESULT", text, result)
                save_general_output(result, "caesar_encrypted.txt")
                write_log("Caesar Encrypt", text, result)
            except ValueError:
                print("\n[ERROR] Shift value must be an integer.")
                write_log("Caesar Encrypt", text, "Invalid shift value", "FAILED")

        elif choice == "9":
            text = input("Enter Caesar encrypted text: ")
            if not validate_text(text, "Encrypted text"):
                continue
            try:
                shift = int(input("Enter shift value: "))
                result = caesar_decrypt(text, shift)
                show_result("CAESAR DECRYPT RESULT", text, result)
                save_general_output(result, "caesar_decrypted.txt")
                write_log("Caesar Decrypt", text, result)
            except ValueError:
                print("\n[ERROR] Shift value must be an integer.")
                write_log("Caesar Decrypt", text, "Invalid shift value", "FAILED")

        elif choice == "10":
            view_logs()

        elif choice == "11":
            print("\n[INFO] Exiting program...")
            break

        else:
            print("\n[ERROR] Invalid choice.")


if __name__ == "__main__":
    main()