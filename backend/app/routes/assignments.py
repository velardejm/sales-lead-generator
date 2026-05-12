from fastapi import APIRouter
from pydantic import BaseModel
from app.db.client import supabase

router = APIRouter()


class AssignmentCreate(BaseModel):
    company_id: str
    salesperson_id: str
    assigned_by: str


class AssignmentUpdate(BaseModel):
    status: str | None = None
    follow_up_date: str | None = None


@router.post("/assignments")
def create_assignment(payload: AssignmentCreate):
    result = supabase.table("lead_assignments").insert({
        "company_id": payload.company_id,
        "salesperson_id": payload.salesperson_id,
        "assigned_by": payload.assigned_by
    }).execute()
    return result.data[0]


@router.patch("/assignments/{assignment_id}")
def update_assignment(assignment_id: str, payload: AssignmentUpdate):
    updates = {k: v for k, v in payload.model_dump().items() if v is not None}
    result = supabase.table("lead_assignments")\
        .update(updates)\
        .eq("id", assignment_id)\
        .execute()
    return result.data[0]


@router.get("/assignments/salesperson/{salesperson_id}")
def get_salesperson_assignments(salesperson_id: str):
    result = supabase.table("lead_assignments")\
        .select("*, companies(*, company_briefs(*))")\
        .eq("salesperson_id", salesperson_id)\
        .order("assigned_at", desc=True)\
        .execute()
    return result.data