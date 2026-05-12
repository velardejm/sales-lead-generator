from fastapi import APIRouter
from pydantic import BaseModel
from app.db.client import supabase

router = APIRouter()


class OutcomeCreate(BaseModel):
    assignment_id: str
    outcome: str
    notes: str | None = None


@router.post("/outcomes")
def log_outcome(payload: OutcomeCreate):
    result = supabase.table("call_outcomes").insert({
        "assignment_id": payload.assignment_id,
        "outcome": payload.outcome,
        "notes": payload.notes
    }).execute()
    return result.data[0]


@router.get("/outcomes/{assignment_id}")
def get_outcomes(assignment_id: str):
    result = supabase.table("call_outcomes")\
        .select("*")\
        .eq("assignment_id", assignment_id)\
        .order("logged_at", desc=True)\
        .execute()
    return result.data