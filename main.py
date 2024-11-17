from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import base64
import io
from engine import extract_text_from_image

app = FastAPI()

class CanvasData(BaseModel):
    image_base64: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Change this to specific origins if needed.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Paths to the uploaded images
image_path_second = "/home/black/playground/writing-pad/writing-pad-server/received_image.png"


@app.get("/")
def base_path():
    return {"message": "This is the base path route"}

@app.post("/convert-to-text")
async def convert_to_text(data: CanvasData):
    try:
        # Decode the base64 image
        image_data = base64.b64decode(data.image_base64)
        image = Image.open(io.BytesIO(image_data))
        
        # Save the image to see what is coming from the request
        image.save("./received_image.png")
        
        # Use Tesseract OCR to extract text
        extracted_text = extract_text_from_image("./received_image.png")

        if extracted_text["Status"]:  
            print(extracted_text)  
            return extracted_text
        else:
            raise HTTPException(status_code=500, detail=extracted_text["Message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.get("/")
def root():
    return {"message": "Python Backend for Handwriting Recognition"}
