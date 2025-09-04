from fastapi import FastAPI, Request, HTTPException
from similarity_query import SimilarityQuery
import base64
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("URI")
TOKEN = os.getenv("TOKEN")

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def similarity_query(img: bytes):
    inst = SimilarityQuery(uri=URI, token=TOKEN)
    return inst.query(img)


@app.post("/query")
async def query(req: Request):
    try:
        data = await req.json()
        image = base64.b64decode(data["image_data"])

        results = similarity_query(image)

        return {"msg": results}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")