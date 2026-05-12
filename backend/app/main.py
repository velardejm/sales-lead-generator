from fastapi import FastAPI

app = FastAPI(title="QTIC Sales Intelligence")

@app.get("/health")
def health():
    return {"status": "ok"}