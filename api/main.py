from fastapi import FastAPI, File, UploadFile
import uvicorn
import numpy as np
from PIL import Image
import io
from tensorflow import keras
import tensorflow as tf
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

endpoints="http://localhost:8501/v1/models:predict"

MODEL = tf.keras.models.load_model("C:/Users/vasum/Desktop/plant_desease_project/models/1/model.keras")
CLASS=['EARLY_BLIIGHT','HEALTHY','LATE_BLIGHT']

origins=[
    "http://localhost"
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read the uploaded file as bytes and convert to an image
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    # Convert the image to a numpy array
    image_array = np.array(image)
    Image_batch=np.expand_dims(image_array,axis=0)
    prediction=MODEL.predict(Image_batch)
    index=np.argmax(prediction[0])
    prediction_class=CLASS[index]
    confidence=np.max(prediction[0])
    
    # Return the numpy array as a list (JSON serializable)
    return {"class": prediction_class, "confidence": float(confidence)}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
