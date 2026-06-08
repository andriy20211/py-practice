from fastapi import FastAPI, HTTPException, status
from settings.db import ping

app = FastAPI(title="FastAPI Docker App")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/healthcheck", status_code=status.HTTP_200_OK)
async def db_healthcheck():
    is_alive = await ping()
    if not is_alive:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed",
        )
    return {"status": "healthy", "database": "connected"}