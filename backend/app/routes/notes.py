from fastapi import APIRouter
from pydantic import BaseModel
from app.db.client import supabase

router = APIRouter()


class NoteCreate(BaseModel):
    company_id: str
    note: str


@router.post("/notes")
def add_note(payload: NoteCreate):
    result = supabase.table("manager_notes").insert({
        "company_id": payload.company_id,
        "note": payload.note
    }).execute()
    return result.data[0]


@router.get("/notes/{company_id}")
def get_notes(company_id: str):
    result = supabase.table("manager_notes")\
        .select("*")\
        .eq("company_id", company_id)\
        .order("created_at", desc=True)\
        .execute()
    return result.data