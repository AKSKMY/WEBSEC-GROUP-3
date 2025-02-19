from fastapi import FastAPI, HTTPException
import joblib
import numpy as np
import re
import jsbeautifier  # Library to deobfuscate JavaScript
import base64
import math

# Load trained ML model
script_model = joblib.load("keylogger_model_02-19_1058_v4.pkl")

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
        # Beautify JavaScript code (remove minification, make readable)
        beautified_script = jsbeautifier.beautify(script)

        # Feature Extraction
        encoded_type = detect_encoding_type(beautified_script)
        encoded_strings = 1 if encoded_type != "None" else 0  # Flag if encoding detected
        entropy = shannon_entropy(beautified_script)  # Detect randomness/obfuscation
        eval_usage = 1 if "eval(" in beautified_script or "Function(" in beautified_script else 0
        keystroke_hooks = len(re.findall(r'onkeydown|onkeypress|onkeyup|addEventListener\("keydown"', beautified_script))
        external_requests = len(re.findall(r'fetch\(|XMLHttpRequest|new Image\(\)', beautified_script))
        data_storage = len(re.findall(r'localStorage|sessionStorage|document.cookie|+= event.key', beautified_script))

        # Feature vector for the ML model
        script_features = np.array([[encoded_strings, eval_usage, keystroke_hooks, external_requests, data_storage]])

        # Run the script through the trained ML model
        probabilities = script_model.predict_proba(script_features)[0]
        keylogger_probability = round(probabilities[1] * 100, 2)  # Get likelihood of being a keylogger

        return {
            "deobfuscated_code": beautified_script,
            "encoded_strings": encoded_strings,
            "entropy": round(entropy, 2),
            "eval_usage": eval_usage,
            "keystroke_hooks": keystroke_hooks,
            "external_requests": external_requests,
            "data_storage": data_storage,
            "encoding_detected": encoded_type,
            "likelihood": keylogger_probability
        }
    except Exception as e:
        return {"error": str(e)}

# API Endpoint: Analyze JavaScript from the Chrome Extension
@app.post("/deobfuscate_scripts")
async def analyze_scripts(scripts: dict):
    try:
        results = []
        for script in scripts["scripts"]:
            analysis_result = analyze_js_code(script["content"])
            results.append(analysis_result)

        # Return the highest likelihood from all scripts analyzed
        highest_likelihood = max(result["likelihood"] for result in results)
        return {"likelihood": highest_likelihood, "details": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
