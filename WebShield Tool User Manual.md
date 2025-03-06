# WebShield Tool User Manual

## Table of Contents
1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Project Setup](#project-setup)
4. [Backend Service Setup](#backend-service-setup)
5. [Chrome Extension Installation](#chrome-extension-installation)
6. [Using WebShield](#using-webshield)
7. [Troubleshooting](#troubleshooting)

## Introduction

WebShield Tool is a Chrome extension that detects and alerts users about potential keyloggers on websites they visit. It uses machine learning to analyze JavaScript code and identify patterns consistent with keylogging behavior. The tool consists of two main components:

1. **Backend Service**: A Python-based API that analyzes JavaScript code using a trained machine learning model
2. **Chrome Extension**: Extracts JavaScript from webpages and sends it to the backend for analysis

## System Requirements

### For Backend Service
- Python 3.8+ 
- pip (Python package manager)
- Git
- Ubuntu/Debian or Windows OS

### For Chrome Extension
- Google Chrome browser
- Internet connection

## Project Setup

### Clone the Repository

1. Open your terminal or command prompt
2. Clone the repository:
   ```
   git clone https://github.com/AKSKMY/WEBSEC-GROUP-3
   cd WebShield
   ```

## Backend Service Setup

The backend service can be set up either locally or on an Azure VM.

### Local Installation

1. Navigate to the Backend Files directory:
   ```
   cd "Backend Files"
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Make the service script executable (Linux/Mac only):
   ```
   chmod +x backend-service.sh
   ```

### Azure VM Installation

If you prefer to run the backend on an Azure VM:

1. Set up an Ubuntu VM on Azure
2. Install required packages:
   ```
   sudo apt install nginx -y
   sudo apt install nodejs
   sudo apt install npm
   sudo apt install python3 python3-pip git
   pip3 install -r requirements.txt
   ```

3. Copy backend files to the VM and make the service script executable:
   ```
   chmod +x backend-service.sh
   ```

### Running the Backend Service

The backend-service.sh script provides several commands to manage the service:

1. To start the service in the background:
   ```
   ./backend-service.sh start
   ```

2. To run the service in console mode (for debugging):
   ```
   ./backend-service.sh console
   ```

3. To check service status:
   ```
   ./backend-service.sh status
   ```

4. To view real-time logs:
   ```
   ./backend-service.sh logs
   ```

5. To stop the service:
   ```
   ./backend-service.sh stop
   ```

6. If port 8000 is already in use:
   ```
   ./backend-service.sh check-port   # See what's using the port
   ./backend-service.sh kill-port    # Force close anything on the port
   ```

## Chrome Extension Installation

1. Open Google Chrome
2. Go to chrome://extensions/
3. Enable "Developer mode" (toggle in the top-right corner)
4. Click "Load unpacked"
5. Navigate to the "Chrome Extension" folder in your cloned repository and select it

The extension should now appear in your Chrome toolbar with the WebShield icon.

## Using WebShield

### Basic Usage

1. The extension runs automatically in the background, monitoring JavaScript code on websites you visit
2. If a potential keylogger is detected, a warning alert will appear showing the risk level
3. You can toggle the extension on/off by clicking on the extension icon and using the toggle button

### Pre-scan Feature

The pre-scan feature allows WebShield to analyze websites before you visit them:

1. Click on the WebShield icon in your Chrome toolbar
2. Toggle "Pre-scan Websites" to enable this feature
3. When enabled, WebShield will intercept navigation attempts and scan the website first
4. If a potential keylogger is detected, you'll see a warning page with details
5. You can choose to proceed to the website or return to safety

## Troubleshooting

### Backend Service Issues

1. **Service won't start**: Check if port 8000 is already in use:
   ```
   ./backend-service.sh check-port
   ```
   If needed, free the port:
   ```
   ./backend-service.sh kill-port
   ```

2. **Service crashes**: Check the logs:
   ```
   ./backend-service.sh logs
   ```

3. **Model loading errors**: Ensure the model files are present in the same directory as the backend.py script:
   - keylogger_model_02-19_1058_v4.pkl
   - scaler.pkl

### Chrome Extension Issues

1. **Extension not detecting scripts**: Check the console logs in Chrome Developer Tools for error messages

2. **Communication errors**: Ensure the API_URL in background.js points to your backend service:
   - For local installation: Update to "http://localhost:8000/analyze"
   - For Azure VM: Update to your VM's IP address like "http://20.189.97.207:8000/analyze"

3. **Extension not appearing**: Try reinstalling the extension by removing it from chrome://extensions/ and loading it again

If problems persist, check the browser console (F12 > Console) for detailed error messages.
