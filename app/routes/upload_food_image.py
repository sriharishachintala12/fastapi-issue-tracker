from pydantic import BaseModel

from fastapi import APIRouter, UploadFile, File,HTTPException,Depends,Security
from fastapi.security import APIKeyHeader
from openai import OpenAI
import base64
import os
from dotenv import load_dotenv
import json
from fastapi.responses import JSONResponse
import re

load_dotenv()

router = APIRouter()
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

endpoint_api_key=os.getenv("ENDPOINT_API_KEY")
API_KEY_NAME="x-api-key"
api_key_header=APIKeyHeader(name=API_KEY_NAME,auto_error=False)

def verify_api_key(end_api_key:str=Security(api_key_header)):
    if end_api_key==endpoint_api_key:
        return True
    raise HTTPException(status_code=401,detail="Unauthorized")

@router.post("/upload-food-image/")
async def upload_food_image(file: UploadFile = File(...),api_key:str=Depends(verify_api_key)):
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


class GymFoodResponse(BaseModel):
    username:str
    food:str

@router.post("/gym-food-response/")
def gym_food_response(food_response:GymFoodResponse,api_key:str=Depends(verify_api_key)):
    #prompt=f"Hello {food_response.username},you had {food_response.food}. "
    #"Give friendly advice on nutrition for someone who goes to the gym."

    prompt = f"""
            Hello {food_response.username},you had {food_response.food}.

            Give:
            - protein feedback '\'
            - calories comment
            - muscle gain suggestion
            - next meal recommendation
            """

    #call openai chatcompletion API
    response=client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"system","content":"You are a fitness and nutrition assistant."},
                 {"role":"user","content":prompt}
                ],
            max_tokens=100
    )
    answer=response.choices[0].message.content
    answer = answer.replace("\\n", "\n")
    return {"advice": answer}
    