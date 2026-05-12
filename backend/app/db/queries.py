from datetime import datetime, timezone
from app.db.client import supabase


def insert_company(name, linkedin_url=None, website_url=None, industry=None, location=None, data_source="manual"):
    result = supabase.table("companies").insert({
        "name": name,
        "linkedin_url": linkedin_url,
        "website_url": website_url,
        "industry": industry,
        "location": location,
        "data_source": data_source
    }).execute()
    return result.data[0]


def get_all_companies():
    result = supabase.table("companies").select("*, company_briefs(*)").execute()
    return result.data


def get_company_by_id(company_id):
    result = supabase.table("companies").select("*, company_briefs(*)").eq("id", company_id).execute()
    return result.data[0] if result.data else None


def delete_company(company_id):
    result = supabase.table("companies").delete().eq("id", company_id).execute()
    return result.data


def insert_brief(company_id, summary, service_angle, buying_signal, data_quality, contact_info=None):
    result = supabase.table("company_briefs").insert({
        "company_id": company_id,
        "summary": summary,
        "service_angle": service_angle,
        "buying_signal": buying_signal,
        "data_quality": data_quality,
        "contact_info": contact_info
    }).execute()
    return result.data[0]


def update_buying_signal(company_id, buying_signal):
    result = supabase.table("company_briefs")\
        .update({"buying_signal": buying_signal})\
        .eq("company_id", company_id)\
        .execute()
    return result.data


def update_last_enriched(company_id):
    result = supabase.table("companies")\
        .update({"last_enriched_at": datetime.now(timezone.utc).isoformat()})\
        .eq("id", company_id)\
        .execute()
    return result.data