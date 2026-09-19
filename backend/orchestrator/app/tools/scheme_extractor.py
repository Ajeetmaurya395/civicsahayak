"""Scheme extractor — LLM-powered structured extraction from government pages.

Strict JSON output. Unknown fields become null, never a guess.
Never invent a scheme name, benefit, document requirement, department,
or application URL.
"""
import json
import logging
from strands import tool

logger = logging.getLogger(__name__)

EXTRACTION_PROMPT = """You are a precise data extraction assistant. Extract government scheme information from the provided page content.

CRITICAL RULES:
1. ONLY extract information explicitly stated in the text
2. If a field is not mentioned, set it to null — NEVER guess or invent
3. NEVER invent scheme names, benefits, URLs, document requirements, or departments
4. Extract eligibility criteria as structured data where possible
5. Application URLs must come from the page content — never fabricate one

Return a JSON object with this EXACT structure:
{{
  "scheme_name": "string or null",
  "description": "string or null",
  "benefits": "string or null",
  "department": "string or null",
  "government_level": "central or state or district or null",
  "sector": "education/healthcare/agriculture/housing/employment/social_welfare/other or null",
  "official_application_url": "string or null — ONLY if explicitly found in the text",
  "required_documents": ["list of document names"] or null,
  "eligibility": {{
    "age_min": number or null,
    "age_max": number or null,
    "income_max": number or null,
    "income_min": number or null,
    "states": ["list of state names"] or null,
    "categories": ["General", "OBC", "SC", "ST", "EWS"] or null,
    "genders": ["male", "female"] or null,
    "occupations": ["list"] or null,
    "education_levels": ["list"] or null,
    "is_bpl_required": boolean or null,
    "is_farmer_required": boolean or null
  }},
  "how_to_apply": "string or null",
  "state": "string or null"
}}

Page content to extract from:
{content}

Source URL: {url}

Return ONLY the JSON object, no other text."""


@tool
def scheme_extractor(page_content_json: str) -> str:
    """Extract structured scheme information from government page content.

    Takes JSON with page content and URL, uses LLM to extract structured
    scheme data. Unknown fields are null, never invented.
    """
    try:
        page_data = json.loads(page_content_json) if isinstance(page_content_json, str) else page_content_json
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid page content JSON", "schemes": []})

    pages = page_data if isinstance(page_data, list) else [page_data]
    extracted_schemes = []

    from app.services.llm_service import get_model
    from strands import Agent

    extraction_agent = Agent(
        model=get_model(),
        system_prompt="You are a precise data extraction assistant. Extract ONLY what is explicitly stated. Never invent or guess. Return valid JSON only.",
    )

    for page in pages:
        content = page.get("content", "")
        url = page.get("url", "")
        title = page.get("title", "")

        if not content or len(content.strip()) < 50:
            continue

        try:
            prompt = EXTRACTION_PROMPT.format(
                content=content[:5000],  # Cap to avoid token limits
                url=url,
            )
            result = extraction_agent(prompt)
            response_text = str(result.message) if hasattr(result, 'message') else str(result)

            # Try to parse JSON from response
            # Handle cases where LLM wraps JSON in markdown code blocks
            cleaned = response_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()

            scheme_data = json.loads(cleaned)
            scheme_data["source_url"] = url
            scheme_data["source_verified"] = page.get("verified", False)

            # Merge application links found during retrieval
            if not scheme_data.get("official_application_url") and page.get("application_links"):
                links = page["application_links"]
                if links:
                    scheme_data["official_application_url"] = links[0].get("url")

            extracted_schemes.append(scheme_data)

        except json.JSONDecodeError:
            logger.error(f"Failed to parse LLM extraction for {url}")
            # Create minimal scheme from page title
            if title:
                extracted_schemes.append({
                    "scheme_name": title,
                    "source_url": url,
                    "source_verified": page.get("verified", False),
                    "description": content[:500] if content else None,
                })
        except Exception as e:
            logger.error(f"Extraction failed for {url}: {e}")
            continue

    return json.dumps({
        "schemes": extracted_schemes,
        "total_extracted": len(extracted_schemes),
    })
