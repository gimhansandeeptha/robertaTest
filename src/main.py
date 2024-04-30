from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from model.main import ModelProcess

appapi = FastAPI()

# CORS configuration
appapi.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

model_process = ModelProcess()
model_process.inference_process()

@appapi.post("/send_message/{message_id}")
async def send_message(message_id: str, request: Request):
    data = await request.json()
    new_message = data.get("message")
    if not new_message:
        raise HTTPException(status_code=400, detail="Message not provided in request")

    sentiment = model_process.inference(new_message)
    return {"status": "Message sent successfully", "prediction": [sentiment]}

if __name__ == "__main__":
    uvicorn.run(appapi, host="127.0.0.1", port=8000)
