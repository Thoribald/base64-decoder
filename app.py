"""
Flask-Version des Base64 Decoders für Render.com
Alle Features aus der Anvil-Version
"""

from flask import Flask, render_template, request, jsonify
import base64
import re
from xml.etree import ElementTree as ET
from xml.dom import minidom

app = Flask(__name__)

# --- Routen ---

@app.route('/')
def index():
    """Hauptseite"""
    return render_template('index.html')

@app.route('/decode_direct', methods=['POST'])
def decode_direct():
    """Base64 direkt dekodieren"""
    try:
        encoded_text = request.form.get('input_text', '').strip()

        if not encoded_text:
            return jsonify({'error': 'Bitte geben Sie einen Base64-String ein!'}), 400

        # Entferne Whitespace
        encoded_text = re.sub(r'\s+', '', encoded_text)

        # Dekodiere
        decoded_bytes = base64.b64decode(encoded_text)

        # Versuche UTF-8
        try:
            decoded_text = decoded_bytes.decode('utf-8')
            # Prüfe ob es XML ist
            try:
                ET.fromstring(decoded_text)
                xml_str = minidom.parseString(decoded_text).toprettyxml(indent="  ")
                decoded_text = "\n".join([line for line in xml_str.split('\n') if line.strip()])
                result_type = "XML"
            except ET.ParseError:
                result_type = "Text"
        except UnicodeDecodeError:
            # Binärdaten
            decoded_text = f"Binärdaten (Länge: {len(decoded_bytes)} Bytes):\n{bytes_to_hex_dump(decoded_bytes)}"
            result_type = "Binär"

        return jsonify({
            'success': True,
            'result': decoded_text,
            'type': result_type
        })

    except Exception as e:
        return jsonify({'error': f'Fehler beim Decodieren: {str(e)}'}), 400

@app.route('/extract_patterns', methods=['POST'])
def extract_patterns():
    """Base64-Muster im Text finden"""
    try:
        text_content = request.form.get('input_text', '')

        if not text_content.strip():
            return jsonify({'error': 'Bitte geben Sie Text ein!'}), 400

        # Regex für Base64-Strings
        pattern = r'[A-Za-z0-9+/]{2,}={0,2}'
        matches = re.finditer(pattern, text_content)

        results = []
        valid_count = 0
        seen_positions = set()

        for match in matches:
            base64_string = match.group()
            start_pos = match.start()

            if start_pos in seen_positions:
                continue

            if looks_like_base64(base64_string):
                try:
                    decoded_bytes = base64.b64decode(base64_string)

                    # VERSCHÄRFTE FILTER
                    if len(base64_string) < 8:
                        continue

                    if len(decoded_bytes) < 3:
                        continue

                    null_ratio = decoded_bytes.count(0) / len(decoded_bytes)
                    if null_ratio > 0.2:
                        continue

                    unique_bytes = len(set(decoded_bytes))
                    if unique_bytes < 2 and len(decoded_bytes) > 4:
                        continue

                    if looks_like_german_word(base64_string):
                        continue

                    # Dekodiere UTF-8
                    try:
                        decoded_text = decoded_bytes.decode('utf-8')

                        printable_ratio = sum(1 for c in decoded_text if c.isprintable() or c.isspace()) / len(decoded_text)
                        if printable_ratio < 0.8:
                            continue

                        special_chars = sum(1 for c in decoded_text if not c.isalnum() and not c.isspace())
                        if special_chars > len(decoded_text) * 0.3:
                            continue

                        decoded_display = decoded_text
                        decoded_type = "Text"
                    except UnicodeDecodeError:
                        if unique_bytes < len(decoded_bytes) / 3:
                            continue

                        decoded_display = bytes_to_hex_dump(decoded_bytes)
                        decoded_type = f"Binärdaten ({len(decoded_bytes)} Bytes)"

                    # Zeile und Spalte
                    line_num = text_content[:start_pos].count('\n') + 1
                    col_num = start_pos - text_content[:start_pos].rfind('\n')

                    # Kontext
                    context_start = max(0, start_pos - 20)
                    context_end = min(len(text_content), start_pos + len(base64_string) + 20)
                    context = text_content[context_start:context_end].replace('\n', ' ')

                    results.append({
                        'position': f"Zeile {line_num}, Spalte {col_num}",
                        'context': f"...{context}...",
                        'base64': base64_string,
                        'decoded': decoded_display,
                        'type': decoded_type
                    })
                    valid_count += 1
                    seen_positions.add(start_pos)

                except Exception:
                    pass

        if not results:
            return jsonify({
                'success': True,
                'results': [],
                'count': 0,
                'message': 'Keine Base64-Strings gefunden.'
            })

        return jsonify({
            'success': True,
            'results': results,
            'count': valid_count
        })

    except Exception as e:
        return jsonify({'error': f'Fehler bei der Mustersuche: {str(e)}'}), 400

@app.route('/encode', methods=['POST'])
def encode():
    """Text zu Base64 kodieren"""
    try:
        plaintext = request.form.get('input_text', '').strip()

        if not plaintext:
            return jsonify({'error': 'Bitte geben Sie Text zum Kodieren ein!'}), 400

        # Kodiere zu Base64
        encoded_bytes = plaintext.encode('utf-8')
        base64_string = base64.b64encode(encoded_bytes).decode('ascii')

        return jsonify({
            'success': True,
            'plaintext': plaintext,
            'plaintext_length': len(plaintext),
            'encoded': base64_string,
            'encoded_length': len(base64_string)
        })

    except Exception as e:
        return jsonify({'error': f'Fehler beim Kodieren: {str(e)}'}), 400

@app.route('/parse_xml', methods=['POST'])
def parse_xml():
    """XML parsen und Base64 decodieren"""
    try:
        xml_content = request.form.get('input_text', '').strip()

        if not xml_content:
            return jsonify({'error': 'Bitte geben Sie XML-Inhalt ein!'}), 400

        # Parse XML
        root = ET.fromstring(xml_content)

        # Durchsuche nach Base64
        results = []
        find_base64_in_element(root, results)

        if not results:
            return jsonify({
                'success': True,
                'results': ['Keine Base64-kodierten Inhalte in der XML-Datei gefunden.'],
                'count': 0
            })

        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })

    except ET.ParseError as e:
        return jsonify({'error': f'Fehler beim Parsen der XML: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Unerwarteter Fehler: {str(e)}'}), 400

# --- Hilfsfunktionen ---

def looks_like_base64(text):
    """Prüft, ob der Text wie Base64 aussieht"""
    if not text:
        return False
    text = re.sub(r'\s+', '', text)
    if len(text) < 4:
        return False
    return re.match(r'^[A-Za-z0-9+/]+=*$', text) is not None and len(text) % 4 == 0

def looks_like_german_word(text):
    """Filtert deutsche Wörter"""
    text_lower = text.lower()

    german_words = [
        'hallo', 'test', 'datum', 'name', 'wert', 'text', 'data',
        'email', 'adresse', 'firma', 'kunde', 'nummer', 'status',
        'beispiel', 'standard', 'normal', 'master', 'system'
    ]

    if text_lower in german_words:
        return True

    if text.isalpha() and len(text) < 12:
        lower_ratio = sum(1 for c in text if c.islower()) / len(text)
        if lower_ratio > 0.9 or lower_ratio < 0.1:
            return True

    return False

def bytes_to_hex_dump(data, bytes_per_line=16):
    """Konvertiert Bytes in einen lesbaren Hex-Dump"""
    if not data:
        return "(leer)"

    result = []
    for i in range(0, len(data), bytes_per_line):
        chunk = data[i:i + bytes_per_line]
        hex_part = ' '.join(f'{b:02x}' for b in chunk)
        ascii_part = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
        padding_length = (bytes_per_line * 3) - 1
        result.append(f"{i:08x}  {hex_part.ljust(padding_length)}  |{ascii_part}|")
    return '\n'.join(result)

def find_base64_in_element(element, results, path=""):
    """Rekursive Funktion zum Durchsuchen von XML-Elementen"""
    current_path = f"{path}/{element.tag}" if path else element.tag

    if element.text and looks_like_base64(element.text.strip()):
        try:
            decoded = decode_base64_content(element.text.strip())
            results.append(f"--- Gefunden in: {current_path} ---\n{decoded}\n")
        except Exception as e:
            results.append(f"--- Konnte Inhalt von {current_path} nicht decodieren: {str(e)} ---\n")

    for attr, value in element.attrib.items():
        if looks_like_base64(value):
            try:
                decoded = decode_base64_content(value)
                results.append(f"--- Gefunden in Attribut: {current_path}/@{attr} ---\n{decoded}\n")
            except Exception as e:
                results.append(f"--- Konnte Attribut {attr} nicht decodieren: {str(e)} ---\n")

    for child in element:
        find_base64_in_element(child, results, current_path)

def decode_base64_content(text):
    """Versucht Base64-String zu decodieren"""
    try:
        text = re.sub(r'\s+', '', text)
        decoded_bytes = base64.b64decode(text)
        try:
            return decoded_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return f"Binärdaten ({len(decoded_bytes)} Bytes):\n{bytes_to_hex_dump(decoded_bytes)}"
    except Exception as e:
        raise ValueError(f"Ungültiger Base64-String: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
