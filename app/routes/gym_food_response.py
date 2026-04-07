from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

router=APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
class GymFoodResponse(BaseModel):
    username:str
    food:str

@router.post("/gym-food-response")
def gym_food_response(food_response:GymFoodResponse):
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
    