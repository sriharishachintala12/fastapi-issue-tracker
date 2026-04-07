from fastapi import APIRouter
import pickle
import numpy as np
from pydantic import BaseModel

router=APIRouter()

items=[{"id":1,"name":"Item1"},{"id":2,"name":"Item2"},{"id":3,"name":"Item3"}]
item_numbers=[{"name": f"item{i}"} for i in range(100)]

@router.get("/")
def home():
    return {"message":"Welcome to FastAPI KNN Model"}


@router.get("/items/")
def get_items():
    return items

@router.get("/items/{item_id}")
def get_itemid(item_id:int):
    for item in items:
        if item["id"]==item_id:
            return {"item_id":item_id}
    return {"error": "Item not found"}

@router.get("/read_items/")
def read_items(skip:int=0,limit:int=10):
    return items[skip:skip+limit]



with open("knn_model.pkl","rb") as f:
    model=pickle.load(f)

class InputData(BaseModel):
    # Define your input data schema here
    Age:int
    EstimatedSalary:float



@router.post("/predict/")
def predict(data:InputData):
    input_data=np.array([[data.Age,data.EstimatedSalary]])
    prediction=model.predict(input_data)
    return {"prediction":int(prediction[0])}

