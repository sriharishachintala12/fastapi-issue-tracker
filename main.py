from fastapi import FastAPI
from app.routes.issues import router as issues_router
from app.routes.binary_classification import router as binary_router
import pickle
import numpy as np
from pydantic import BaseModel
from app.middleware.timer import timer_middleware
from fastapi.middleware.cors import CORSMiddleware
from app.routes.gym_food_response import router as gym_food_router


app=FastAPI()

app.middleware("http")(timer_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    )
app.include_router(binary_router)
app.include_router(issues_router)
app.include_router(gym_food_router)

