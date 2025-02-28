from fastapi import FastAPI, HTTPException
import joblib
import numpy as np
import pandas as pd
import re
import jsbeautifier  # Library to deobfuscate JavaScript
import base64
import math
import json

# Load trained ML model and scaler
script_model = joblib.load("keylogger_model_02-19_1058_v4.pkl")
scaler = joblib.load("scaler.pkl")  # Ensures standardization before classification

app = FastAPI()

# Function to calculate string entropy (detect obfuscation)
def shannon_entropy(string):
    if not string:
        return 0
    prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
    entropy = -sum([p * math.log(p, 2) for p in prob])
    return entropy

# Function to detect if the script is encoded (Base64, Hex, URL)
def detect_encoding_type(string):
    if re.fullmatch(r'[A-Za-z0-9+/]*={0,2}', string) and len(string) % 4 == 0:
        return "Base64"
    elif re.search(r'\\x[0-9A-Fa-f]{2}', string):
        return "Hex"
    elif re.search(r'%[0-9A-Fa-f]{2}', string):
        return "URL Encoding"
    elif re.search(r'\\u[0-9A-Fa-f]{4}', string):
        return "Unicode"
    else:
        return "None"

# Function to decode Base64 JavaScript
def decode_base64_js(content):
    base64_match = re.search(r"data:text/javascript;base64,([A-Za-z0-9+/=]+)", content)
    if base64_match:
        try:
            decoded_content = base64.b64decode(base64_match.group(1)).decode("utf-8")
            print("🔓 Decoded Base64 JavaScript:", decoded_content)
            return decoded_content
        except Exception as e:
            print("❌ Failed to decode Base64:", e)
            return content  # Return original if decoding fails
    return content

# Function to analyze JavaScript code for suspicious behavior
def analyze_js_code(script):
    try:
        print(f"\n🔍 Received Script Type: {type(script)}")  # Debugging

        if isinstance(script, dict):  # Extract content if script is a dict
            script = script.get("content", "")

        # Decode Base64 scripts
        script = decode_base64_js(script)

        beautified_script = jsbeautifier.beautify(script)

        # Feature Extraction
        encoded_type = detect_encoding_type(beautified_script)
        encoded_strings = 1 if encoded_type != "None" else 0
        entropy = shannon_entropy(beautified_script)
        eval_usage = 1 if "eval(" in beautified_script or "Function(" in beautified_script else 0

        # Common keylogger characteristics
        COMMON_CHARACTERISTICS = {
            "Event Listeners": ["keydown", "keypress", "keyup"],
            "Key Code Conversion": ["String.fromCharCode", "e.keyCode", "e.which", "e.key"],
            "Data Accumulation": ["record", "keys", "buffer"],
            "Data Transmission": ["$.ajax", "new Image().src", "WebSocket", "ws.send"],
            "Cross-Domain Requests": ["crossDomain: true"],
            "Special Key Handling": ["Backspace", "Enter", "Shift", "Tab", "Ctrl", "Alt", "Esc", "Delete", "CapsLock"],
            "Error Handling": ["success", "error", "onmessage"]
        }

        # Extract feature occurrences from script content
        feature_counts = {category: 0 for category in COMMON_CHARACTERISTICS}

        for category, patterns in COMMON_CHARACTERISTICS.items():
            for pattern in patterns:
                matches = re.findall(re.escape(pattern), beautified_script)
                feature_counts[category] += len(matches)

        # Assign feature values
        event_listeners = feature_counts["Event Listeners"]
        key_code_conversion = feature_counts["Key Code Conversion"]
        data_accumulation = feature_counts["Data Accumulation"]
        data_transmission = feature_counts["Data Transmission"]
        cross_domain_requests = feature_counts["Cross-Domain Requests"]
        special_key_handling = feature_counts["Special Key Handling"]
        error_handling = feature_counts["Error Handling"]

        print("\n🚀 Extracted Features for Debugging:")
        print(f"Event Listeners: {event_listeners}")
        print(f"Key Code Conversion: {key_code_conversion}")
        print(f"Data Accumulation: {data_accumulation}")
        print(f"Data Transmission: {data_transmission}")
        print(f"Special Key Handling: {special_key_handling}")
        print(f"Cross Domain Requests: {cross_domain_requests}")
        print(f"Error Handling: {error_handling}")

        # Convert feature list into a pandas DataFrame
        feature_names = ["Event_Listeners", "Key_Code_Conversion", "Data_Accumulation",
                        "Data_Transmission", "Special_Key_Handling", "Cross_Domain_Requests",
                        "Error_Handling"]

        script_features = pd.DataFrame([[event_listeners, key_code_conversion, data_accumulation,
                                        data_transmission, special_key_handling, cross_domain_requests,
                                        error_handling]], columns=feature_names)

        # <-- Add this print to verify the feature vector:
        print("Extracted feature vector:", script_features.iloc[0].to_dict())

        # Standardize the input before sending it to the ML model
        script_features_scaled = scaler.transform(script_features)
        script_features_scaled = pd.DataFrame(script_features_scaled, columns=script_features.columns)

        probabilities = script_model.predict_proba(script_features_scaled)[0]
        keylogger_probability = round(probabilities[1] * 100, 2)

        # 🚀 Prevent false positives: If all extracted features are 0, assume it's NOT a keylogger
        if sum(script_features.iloc[0]) == 0:
            keylogger_probability = 0.0

        return {
            "deobfuscated_code": beautified_script,
            "likelihood": keylogger_probability
        }
    except Exception as e:
        return {"error": str(e)}

# API Endpoint: Analyze JavaScript from the Chrome Extension
@app.post("/analyze")
async def analyze(payload: dict):
    try:
        print("Received payload:", json.dumps(payload, indent=2))  # Debugging

        scripts = payload.get("scripts", [])
        if not scripts:
            raise ValueError("No scripts received")

        results = [analyze_js_code(script) for script in scripts]

        return {"results": results}

    except Exception as e:
        print("🔥 Error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
