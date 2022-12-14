import json
import os

import uvicorn

from enum import Enum
from typing import Union

from dotenv import load_dotenv
from fastapi import FastAPI
# from fastapi import File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from model_methods import (
    get_liveness,
    get_classification_report_from_corpus,
    predict_from_corpus
)

# load environment variables
load_dotenv()

# setup api w/ CORS
api = FastAPI()
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# model class for handling predictions using different models
class ModelName(str, Enum):
    inception = 'inceptionv3'
    simclr = 'simclrv2'

class LivenessOut(BaseModel):
    service: str
    status: str


@api.get('/', response_model=LivenessOut)
async def root():
    # endpoint for api liveness status
    response = get_liveness()
    return response


@api.get('/classification_report/')
async def classification_report(model_name: ModelName):
    # endpoint to get classification report for entire sample (batteries-incl.) corpus
    response = get_classification_report_from_corpus(model_name.value)
    return response


@api.get('/corpus_predict/')
async def predict(model_name: ModelName, num_samples: int=1, stratify: bool=False):
    # endpoint to do inference on instance from curated corpus
    response = predict_from_corpus(model_name.value, num_samples, stratify)
    return response


if __name__ == '__main__':
    uvicorn.run(api, host="0.0.0.0", port=8000)