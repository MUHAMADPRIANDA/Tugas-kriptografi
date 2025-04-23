from flask import Flask, render_template, request, send_file, Response
import os
import extended_vigenere
# import vigenere_cipher
# import playfair_cipher
# import affine_cipher
import hill_cipher

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
    formatted_result = None  # For formatted output (5-char groups)
    download_link = None

    if request.method == "POST":
        method = request.form.get("method")
        mode = request.form.get("mode")
        text = request.form.get("text").strip() if request.form.get("text") else None
        key = request.form.get("key").strip()
        format_option = request.form.get("format", "none")  # Default to no formatting

        try:
            if method == "1":  # Vigenere Cipher
                # Convert to uppercase and remove non-alphabetic characters for traditional Vigenere
                if text:
                    text = ''.join(c for c in text.upper() if c.isalpha())
                
                if mode == "encrypt":
                    result = vigenere_cipher.encrypt(text, key)
                else:
                    result = vigenere_cipher.decrypt(text, key)
            
            elif method == "2":  # Playfair Cipher
                # Convert to uppercase and remove non-alphabetic characters for Playfair
                if text:
                    text = ''.join(c for c in text.upper() if c.isalpha())
                
                if mode == "encrypt":
                    result = playfair_cipher.encrypt(text, key)
                else:
                    result = playfair_cipher.decrypt(text, key)

            elif method == "3":  # Extended Vigenere Cipher (File or Text)
                if "file" in request.files and request.files["file"].filename != "":
                    # Handling file input
                    file = request.files["file"]
                    filename = file.filename
                    input_path = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(input_path)

                    output_filename = f"{'encrypted' if mode == 'encrypt' else 'decrypted'}_{filename}"
                    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
                    
                    if mode == "encrypt":
                        extended_vigenere.encrypt_file(input_path, output_path, key)
                    else:
                        extended_vigenere.decrypt_file(input_path, output_path, key)

                    download_link = f"/download/{output_filename}"
                    result = f"File processed successfully. Click to download."

                elif text:  # Handling text input
                    if mode == "encrypt":
                        result = extended_vigenere.encrypt_text(text, key)
                    else:
                        result = extended_vigenere.decrypt_text(text, key)
                    
                    # Save to file option
                    output_filename = f"{'encrypted' if mode == 'encrypt' else 'decrypted'}_text.txt"
                    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
                    with open(output_path, "w", encoding="latin1") as f:
                        f.write(result)
                    
                    download_link = f"/download/{output_filename}"

            elif method == "4":  # Affine Cipher
                if text:
                    text = ''.join(c for c in text.upper() if c.isalpha())
                    
                if mode == "encrypt":
                    result = affine_cipher.encrypt(text, key)
                else:
                    result = affine_cipher.decrypt(text, key)

            elif method == "5":  # Hill Cipher
                if text:
                    text = ''.join(c for c in text.upper() if c.isalpha())
                    
                if len(key) != 4:
                    error = "Kunci Hill Cipher harus 4 huruf."
                elif mode == "encrypt":
                    result = hill_cipher.hill_encrypt(text, key)
                else:
                    result = hill_cipher.hill_decrypt(text, key)
            else:
                error = "Metode tidak valid."

            # Apply formatting if result is text (not file)
            if result and not download_link:
                if format_option == "no_spaces":
                    formatted_result = extended_vigenere.format_without_spaces(result)
                elif format_option == "groups":
                    formatted_result = extended_vigenere.format_in_groups(result)

        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template("index.html", 
                          result=result, 
                          formatted_result=formatted_result,
                          download_link=download_link, 
                          error=error)

@app.route("/download/<filename>")
def download_file(filename):
    path = os.path.join(OUTPUT_FOLDER, filename)
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)