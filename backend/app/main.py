from fastapi import FastAPI
from app.routes.companies import router as companies_router
from app.routes.briefs import router as briefs_router
from app.routes.notes import router as notes_router
from app.routes.assignments import router as assignments_router
from app.routes.outcomes import router as outcomes_router

app = FastAPI(title="QTIC Sales Intelligence")

app.include_router(companies_router)
app.include_router(briefs_router)
app.include_router(notes_router)
app.include_router(assignments_router)
app.include_router(outcomes_router)

@app.get("/health")
def health():
    return {"status": "ok"}