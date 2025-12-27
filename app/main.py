from fastapi import FastAPI
from app.http_api import router as http_router
from app.ws_api import router as ws_router


app = FastAPI(
    title="FastAPI Demo Server",
    description="HTTP + WebSocket example",
    version="0.1.0"
)

# 注册路由
app.include_router(http_router)
app.include_router(ws_router)

@app.get("/")
def root():
    return {"msg": "FastAPI server is running"}

