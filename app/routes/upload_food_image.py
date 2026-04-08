from fastapi import APIRouter, UploadFile, File
from openai import OpenAI
import base64
import os
from dotenv import load_dotenv
import json
from fastapi.responses import JSONResponse
import re

load_dotenv()

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/upload-food-image")
async def upload_food_image(file: UploadFile = File(...)):
    try:
        # Read uploaded image
        image_bytes = await file.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        # Prepare prompt
        prompt_text = "You are a nutritionist. Analyze this food image and return JSON with calories, protein (g), carbs (g), fat (g), and suggestions."

        # Call OpenAI Responses API with image
        response = client.responses.create(
            model="gpt-4.1",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt_text},
                        {"type": "input_image", "image_url": f"data:image/jpeg;base64,{base64_image}"}
                    ]
                }
            ]
        )
        
        cleaned = re.sub(r"```json|```", "", response.output_text).strip()
        last_brace = cleaned.rfind("}")
        if last_brace != -1:
            cleaned = cleaned[:last_brace+1]
        nutrition_data = json.loads(cleaned)
        #return {"nutrition_feedback": response.output_text}
        return JSONResponse(content=nutrition_data)

    except Exception as e:
        return {"error": str(e)}