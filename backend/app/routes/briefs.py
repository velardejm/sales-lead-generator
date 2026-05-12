from fastapi import APIRouter
from app.db.queries import get_company_by_id, insert_brief, update_last_enriched
from app.services.scraper import search_company
from app.services.ai import generate_brief as ai_generate_brief

router = APIRouter()


@router.post("/briefs/{company_id}/regenerate")
def regenerate_brief(company_id: str):
    company = get_company_by_id(company_id)
    search_results = search_company(company["name"])
    brief = ai_generate_brief(search_results)

    insert_brief(
        company_id=company_id,
        summary=brief["summary"],
        service_angle=brief["service_angle"],
        buying_signal=brief["buying_signal"],
        data_quality=brief["data_quality"],
        contact_info=brief.get("contact_info")
    )

    update_last_enriched(company_id)
    return get_company_by_id(company_id)