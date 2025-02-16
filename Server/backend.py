from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

# Load the trained model
model = joblib.load("/home/username/keylogger_model.pkl")

@app.post("/predict")
async def predict(data: dict):
    try:
        # Convert input to DataFrame
        input_data = pd.DataFrame([data])
        prediction = model.predict(input_data)
        return {"prediction": int(prediction[0])}
    except Exception as e:
        return {"error": str(e)}

# To run: uvicorn backend:app --host 0.0.0.0 --port 8000
