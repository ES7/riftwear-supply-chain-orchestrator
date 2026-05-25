from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import agents, data

app = FastAPI(
    title="RIFT WEAR Supply Chain Orchestrator",
    version="2.0.0",
    description="AI-powered supply chain for RIFT WEAR — reads from Excel, no database needed"
)

app.include_router(agents.router)
app.include_router(data.router)
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def root():
    return FileResponse("frontend/index.html")


@app.get("/health")
def health():
    return {"status": "running", "version": "2.0.0", "data_source": "data.xlsx"}
