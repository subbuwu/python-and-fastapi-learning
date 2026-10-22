from fastapi import FastAPI
from app.routes import auth


app = FastAPI(
    title="E-Commerce API",
    version="1.0.0"
)

app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "E-Commerce API is running"}
 
 