from flask import Flask, render_template, request, send_file
import os
import extended_vigenere
import vigenere_cipher
import playfair_cipher
import affine_cipher
import hill_cipher
import vigenere_cipher_auto_key  # AutoKey Vigenere

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def format_without_spaces(text):
    return ''.join(text.split())

def format_in_groups(text, group_size=5):
    text = format_without_spaces(text)
    return ' '.join([text[i:i+group_size] for i in range(0, len(text), group_size)])

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    formatted_result = None
    download_link = None
    selected_method = None
    selected_mode = None
    entered_text = None
    entered_key = None
    selected_format = None

    if request.method == "POST":
        method = request.form.get("method")
        mode = request.form.get("mode")
        text = request.form.get("text").strip() if request.form.get("text") else None
        key = request.form.get("key").strip()
        format_option = request.form.get("format", "none")

        selected_method = method
        selected_mode = mode
        entered_text = text
        entered_key = key
        selected_format = format_option

        try:
            # Function to process file if available
            def process_file(file, mode, key):
                filename = file.filename
                input_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(input_path)

                output_filename = f"{'encrypted' if mode == 'encrypt' else 'decrypted'}_{filename}"
                output_path = os.path.join(OUTPUT_FOLDER, output_filename)

                if mode == "encrypt":
                    extended_vigenere.encrypt_file(input_path, output_path, key)
                else:
                    extended_vigenere.decrypt_file(input_path, output_path, key)

                return f"/download/{output_filename}", f"File processed successfully. Click to download."

            if method == "1":  # Vigenere Cipher
                if text:
                    text = ''.join(c for c in text.upper() if c.isalpha())
                result = vigenere_cipher.encrypt(text, key) if mode == "encrypt" else vigenere_cipher.decrypt(text, key)

            elif method == "2":  # Playfair Cipher
                if text:
                    text = ''.join(c for c in text.upper() if c.isalpha())
                result = playfair_cipher.encrypt(text, key) if mode == "encrypt" else playfair_cipher.decrypt(text, key)

            elif method == "3":  # Extended Vigenere Cipher
                if "file" in request.files and request.files["file"].filename != "":
                    file = request.files["file"]
                    download_link, result = process_file(file, mode, key)
                elif text:
                    if mode == "encrypt":
                        result = extended_vigenere.encrypt_text(text, key)
                    else:
                        result = extended_vigenere.decrypt_text(text, key)

                    output_filename = f"{'encrypted' if mode == 'encrypt' else 'decrypted'}_text.txt"
                    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(result)

                    download_link = f"/download/{output_filename}"

                if format_option == "no_spaces":
                    formatted_result = format_without_spaces(result)
                elif format_option == "groups":
                    formatted_result = format_in_groups(result)

            elif method == "4":  # Affine Cipher
                if text:
                    text = ''.join(c for c in text.upper() if c.isalpha())
                try:
                    a, b = map(int, key.split(","))
                    result = affine_cipher.affine_encrypt(text, a, b) if mode == "encrypt" else affine_cipher.affine_decrypt(text, a, b)
                except ValueError:
                    error = "Format kunci tidak valid. Format kunci harus a,b"

            elif method == "5":  # Hill Cipher
                if text:
                    text = ''.join(c for c in text.upper() if c.isalpha())

                if len(key) != 4:
                    error = "Kunci Hill Cipher harus 4 huruf."
                else:
                    result = hill_cipher.hill_encrypt(text, key) if mode == "encrypt" else hill_cipher.hill_decrypt(text, key)

                    output_filename = f"{'encrypted' if mode == 'encrypt' else 'decrypted'}_{method}_result.txt"
                    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(result)
                    download_link = f"/download/{output_filename}"

            elif method == "6":  # Vigenere Cipher AutoKey
                if text:
                    text = ''.join(c for c in text.upper() if c.isalpha())
                result = vigenere_cipher_auto_key.encrypt(text, key) if mode == "encrypt" else vigenere_cipher_auto_key.decrypt(text, key)

            else:
                error = "Metode tidak valid."

            if result and text:
                if format_option == "no_spaces":
                    formatted_result = format_without_spaces(result)
                elif format_option == "groups":
                    formatted_result = format_in_groups(result)

        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template("index.html",
                           result=result,
                           formatted_result=formatted_result,
                           download_link=download_link,
                           error=error,
                           selected_method=selected_method,
                           selected_mode=selected_mode,
                           entered_text=entered_text,
                           entered_key=entered_key,
                           selected_format=selected_format)

@app.route("/download/<filename>")
def download_file(filename):
    path = os.path.join(OUTPUT_FOLDER, filename)
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
