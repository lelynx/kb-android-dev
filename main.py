import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

load_dotenv()

from database.init_db import init_db
from routers.kb_routers import router

app = FastAPI(
    title="Knowledge Base API",
    description="Web-service de base de connaissances pour développeurs Android",
    version="1.0.0",
)

init_db()

app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", include_in_schema=False)
def read_root():
    return FileResponse("static/kb.html")


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8002"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
