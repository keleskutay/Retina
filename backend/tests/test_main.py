from fastapi import FastAPI, Request, HTTPException
from fastapi.testclient import TestClient
import base64
from PIL import Image
import io

app = FastAPI()

client = TestClient(app)

@app.post("/query")
async def query(req: Request):
    try:
        data = await req.json()
        image = base64.b64decode(data["image_data"])
        img = Image.open(io.BytesIO(image)).convert("RGB")
        return {"msg": "Success"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

def test_query():
    with open("./test_img/test_1.png", "rb") as f:
        image_bytes = f.read()

    image_b64 = base64.b64encode(image_bytes).decode()
    
    response = client.post("/query", json={"image_data": image_b64})
    assert response.status_code == 200
    assert response.json() == {"msg": "Success"}
