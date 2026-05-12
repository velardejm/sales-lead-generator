from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db.queries import insert_company, get_all_companies, get_company_by_id, delete_company, insert_brief, update_last_enriched
from app.services.scraper import search_company
from app.services.ai import generate_brief

router = APIRouter()


class CompanyCreate(BaseModel):
    name: str
    linkedin_url: str | None = None
    website_url: str | None = None


@router.post("/companies")
def create_company(payload: CompanyCreate):
    search_results = search_company(payload.name)
    brief = generate_brief(search_results)

    company = insert_company(
        name=payload.name,
        linkedin_url=payload.linkedin_url,
        website_url=payload.website_url,
        data_source="web"
    )

    insert_brief(
        company_id=company["id"],
        summary=brief["summary"],
        service_angle=brief["service_angle"],
        buying_signal=brief["buying_signal"],
        data_quality=brief["data_quality"],
        contact_info=brief.get("contact_info")
    )

    update_last_enriched(company["id"])

    return get_company_by_id(company["id"])


@router.get("/companies")
def list_companies():
    return get_all_companies()


@router.get("/companies/{company_id}")
def get_company(company_id: str):
    company = get_company_by_id(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.delete("/companies/{company_id}")
def remove_company(company_id: str):
    delete_company(company_id)
    return {"deleted": company_id}