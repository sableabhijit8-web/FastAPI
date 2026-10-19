
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello, World!"}

@app.get('/about')
def about():
    return {"message": "Abhijit Sable is a clever boy build his first fastapi project"}