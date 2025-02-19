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

# Function to analyze JavaScript code for suspicious behavior
def analyze_js_code(script):
    try:
        print(f"\n🔍 Received Script Type: {type(script)}")  # Debugging

        if isinstance(script, dict):  # Extract content if script is a dict
            script = script.get("content", "")

        beautified_script = jsbeautifier.beautify(script)

        # Feature Extraction
        encoded_type = detect_encoding_type(beautified_script)
        encoded_strings = 1 if encoded_type != "None" else 0
        entropy = shannon_entropy(beautified_script)
        eval_usage = 1 if "eval(" in beautified_script or "Function(" in beautified_script else 0

        # Corrected Regex for Keylogger Hooks Detection
        keystroke_hooks = len(re.findall(r'(onkeydown|onkeypress|onkeyup|addEventListener\s*\(\s*["\']keydown["\']\s*\))', beautified_script))

        # Corrected Regex for External Requests
        external_requests = len(re.findall(r'fetch\s*\(|XMLHttpRequest|new\s+Image\s*\(\s*\)', beautified_script))

        # Corrected Regex for Data Storage Operations
        data_storage = len(re.findall(r'localStorage|sessionStorage|document\.cookie|\+=\s*event\.key', beautified_script))

        # 🔹 Ensure 7 Features Are Passed to the ML Model
        event_listeners = keystroke_hooks
        key_code_conversion = eval_usage
        # Detect if script accumulates keystrokes before sending them
        data_accumulation = 1 if "keys +=" in beautified_script else 0
        data_transmission = external_requests
        # Detect use of keylogging-related key event manipulations
        special_key_handling = len(re.findall(r'String\.fromCharCode|keyCode|which|charCode', beautified_script))
        cross_domain_requests = 1 if "document.domain" in beautified_script else 0
        error_handling = 1 if "try{" in beautified_script else 0

        print("\n🚀 Extracted Features for Debugging:")
        print(f"Event Listeners: {event_listeners}")
        print(f"Key Code Conversion: {key_code_conversion}")
        print(f"Data Accumulation: {data_accumulation}")
        print(f"Data Transmission: {data_transmission}")
        print(f"Special Key Handling: {special_key_handling}")
        print(f"Cross Domain Requests: {cross_domain_requests}")
        print(f"Error Handling: {error_handling}")

        # Convert feature list into a pandas DataFrame (to match ML model training format)
        feature_names = ["Event_Listeners", "Key_Code_Conversion", "Data_Accumulation",
                        "Data_Transmission", "Special_Key_Handling", "Cross_Domain_Requests",
                        "Error_Handling"]

        script_features = pd.DataFrame([[event_listeners, key_code_conversion, data_accumulation,
                                        data_transmission, special_key_handling, cross_domain_requests,
                                        error_handling]], columns=feature_names)

        # Standardize the input before sending it to the ML model
        script_features = pd.DataFrame(script_features, columns=feature_names)

        probabilities = script_model.predict_proba(script_features)[0]
        keylogger_probability = round(probabilities[1] * 100, 2)

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
