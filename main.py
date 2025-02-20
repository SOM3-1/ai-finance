from fastapi import FastAPI
from firebase_config import db
from routes.prediction import router as prediction_router

app = FastAPI()

app.include_router(prediction_router)

@app.get("/")
def home():
    return {"message": "ML API with Firebase is running securely!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
