from fastapi import FastAPI
from api.v1.router import router as router_v1

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

app.include_router(router_v1, prefix='/fast_api_address/api/v1')