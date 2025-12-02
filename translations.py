# Render: Übersetzungen für Deutsch und Englisch

TRANSLATIONS = {
    'de': {
        # Header
        'title': 'Base64 Decoder',
        'subtitle': 'Bereit. Laden Sie eine Datei hoch oder fügen Sie Base64 oder einen Text ein.',

        # Buttons
        'upload_file': '📁 XML-Datei hochladen',
        'parse_xml': 'XML parsen und Base64 decodieren',
        'decode_direct': 'Nur Base64 decodieren',
        'extract_patterns': 'Base64-Muster finden',
        'encode_text': 'Text zu Base64 kodieren',
        'clear_all': 'Alles löschen',

        # Labels
        'input_label': 'Eingabe:',
        'output_label': 'Ausgabe:',
        'input_placeholder': 'XML oder Base64-Text hier eingeben...',

        # Messages
        'loaded': 'Geladen',
        'processing': 'Verarbeite XML auf dem Server...',
        'decoded_success': 'Erfolgreich decodiert',
        'binary_data': 'Binärdaten erkannt',
        'found_strings': 'echte Base64-Strings gefunden und dekodiert',
        'ready': 'Bereit',
        'finished': 'Fertig',

        # Errors
        'error_no_input': 'Bitte geben Sie XML-Inhalt ein oder laden Sie eine Datei hoch!',
        'error_no_base64': 'Bitte geben Sie einen Base64-String ein!',
        'error_no_text': 'Bitte geben Sie Text ein!',
        'error_no_encode_text': 'Bitte geben Sie Text zum Kodieren ein!',
        'error_reading_file': 'Fehler beim Lesen der Datei',
        'error_decoding': 'Fehler beim Decodieren',
        'error_encoding': 'Fehler beim Kodieren',
        'error_pattern_search': 'Fehler bei der Mustersuche',

        # Results
        'no_base64_found': 'Keine Base64-Strings gefunden.',
        'hint_title': 'Hinweis:',
        'hint_min_length': '• Mindestlänge: 8 Zeichen',
        'hint_real_base64': '• Nur echte Base64-Strings werden erkannt',
        'hint_filter_words': '• Deutsche Wörter werden herausgefiltert',
        'hint_strict': '• Verschärfte Validierung aktiv',

        # Position
        'position': 'Position',
        'context': 'Kontext',
        'plaintext': 'Klartext',
        'line': 'Zeile',
        'column': 'Spalte',
        'characters': 'Zeichen',
        'bytes': 'Bytes',
        'encoded_label': 'Base64-kodiert',
        'type': 'Typ',
    },
    'en': {
        # Header
        'title': 'Base64 Decoder',
        'subtitle': 'Ready. Upload a file or paste Base64 or text.',

        # Buttons
        'upload_file': '📁 Upload XML File',
        'parse_xml': 'Parse XML and decode Base64',
        'decode_direct': 'Decode Base64 only',
        'extract_patterns': 'Find Base64 patterns',
        'encode_text': 'Encode text to Base64',
        'clear_all': 'Clear all',

        # Labels
        'input_label': 'Input:',
        'output_label': 'Output:',
        'input_placeholder': 'Enter XML or Base64 text here...',

        # Messages
        'loaded': 'Loaded',
        'processing': 'Processing XML on server...',
        'decoded_success': 'Successfully decoded',
        'binary_data': 'Binary data detected',
        'found_strings': 'real Base64 strings found and decoded',
        'ready': 'Ready',
        'finished': 'Done',

        # Errors
        'error_no_input': 'Please enter XML content or upload a file!',
        'error_no_base64': 'Please enter a Base64 string!',
        'error_no_text': 'Please enter text!',
        'error_no_encode_text': 'Please enter text to encode!',
        'error_reading_file': 'Error reading file',
        'error_decoding': 'Error decoding',
        'error_encoding': 'Error encoding',
        'error_pattern_search': 'Error in pattern search',

        # Results
        'no_base64_found': 'No Base64 strings found.',
        'hint_title': 'Note:',
        'hint_min_length': '• Minimum length: 8 characters',
        'hint_real_base64': '• Only real Base64 strings are detected',
        'hint_filter_words': '• Common words are filtered out',
        'hint_strict': '• Strict validation active',

        # Position
        'position': 'Position',
        'context': 'Context',
        'plaintext': 'Plaintext',
        'line': 'Line',
        'column': 'Column',
        'characters': 'characters',
        'bytes': 'bytes',
        'encoded_label': 'Base64-encoded',
        'type': 'Type',
    }
}

def get_translation(lang, key):
    """Holt Übersetzung für einen Key"""
    if lang not in TRANSLATIONS:
        lang = 'de'  # Fallback auf Deutsch
    return TRANSLATIONS[lang].get(key, key)
