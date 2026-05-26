from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index_root():
    return {"message": "Hello World!"}
