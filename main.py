
from fastapi import FastAPI

app = FastAPI(
    title="Phase 3 CI/CD Integration API",
    description="FastAPI REST service",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Phase 3 API is running",
        "status": "success"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
