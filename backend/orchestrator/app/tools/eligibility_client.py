"""Eligibility client — calls the Python eligibility engine over HTTP."""
import os
import json
import logging
import httpx
from strands import tool

logger = logging.getLogger(__name__)


@tool
def check_eligibility(request_json: str) -> str:
    """Check eligibility by calling the deterministic Python eligibility engine.

    Takes a JSON string with user_profile and scheme_criteria, sends it to
    the eligibility engine service, and returns the evaluation results.

    The LLM never decides eligibility — only this deterministic engine does.
    """
    try:
        request_data = json.loads(request_json) if isinstance(request_json, str) else request_json
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid request JSON", "results": []})

    engine_url = os.getenv("ELIGIBILITY_ENGINE_URL", "http://localhost:8081")

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                f"{engine_url}/evaluate",
                json=request_data,
            )
            response.raise_for_status()
            return json.dumps(response.json())
    except httpx.ConnectError:
        logger.warning("Eligibility engine not available — using inline evaluation")
        # Fallback: evaluate inline if engine is down
        return _evaluate_inline(request_data)
    except Exception as e:
        logger.error(f"Eligibility check failed: {e}")
        return json.dumps({"error": str(e), "results": []})


def _evaluate_inline(request_data: dict) -> str:
    """Inline fallback evaluation when the eligibility engine service is unreachable."""
    user_profile = request_data.get("user_profile", {})
    scheme_criteria_list = request_data.get("scheme_criteria", [])
    results = []

    for sc in scheme_criteria_list:
        scheme_id = sc.get("scheme_id", "unknown")
        scheme_name = sc.get("scheme_name", "Unknown Scheme")
        eligibility = sc.get("eligibility", {})

        matched = []
        unmatched = []
        missing = []
        explanations = []

        # Age check
        age = user_profile.get("age")
        age_min = eligibility.get("age_min")
        age_max = eligibility.get("age_max")
        if age_min is not None or age_max is not None:
            if age is None:
                missing.append("age")
                explanations.append("⚠ Age: not provided")
            else:
                age_ok = True
                if age_min is not None and age < age_min:
                    age_ok = False
                if age_max is not None and age > age_max:
                    age_ok = False
                if age_ok:
                    matched.append("age")
                    req = f"{age_min or '?'}–{age_max or '?'}"
                    explanations.append(f"✓ Age: {age}, requirement {req}")
                else:
                    unmatched.append("age")
                    req = f"{age_min or '?'}–{age_max or '?'}"
                    explanations.append(f"✗ Age: {age}, requirement {req}")

        # Income check
        income = user_profile.get("annual_family_income")
        income_max = eligibility.get("income_max")
        income_min = eligibility.get("income_min")
        if income_max is not None or income_min is not None:
            if income is None:
                missing.append("income")
                explanations.append("⚠ Income: not provided")
            else:
                income_ok = True
                if income_max is not None and income > income_max:
                    income_ok = False
                if income_min is not None and income < income_min:
                    income_ok = False
                if income_ok:
                    matched.append("income")
                    explanations.append(f"✓ Income: ₹{income:,.0f}, max ₹{income_max:,.0f}" if income_max else f"✓ Income: ₹{income:,.0f}")
                else:
                    unmatched.append("income")
                    gap = income - income_max if income_max and income > income_max else 0
                    explanations.append(f"✗ Income: ₹{income:,.0f} exceeds maximum ₹{income_max:,.0f} by ₹{gap:,.0f}" if income_max else f"✗ Income: ₹{income:,.0f}")

        # State check
        user_state = user_profile.get("state", "").lower()
        required_states = eligibility.get("states", [])
        if required_states:
            if not user_state:
                missing.append("state")
                explanations.append("⚠ State: not provided")
            elif user_state in [s.lower() for s in required_states]:
                matched.append("state")
                explanations.append(f"✓ State: {user_profile.get('state')}")
            else:
                unmatched.append("state")
                explanations.append(f"✗ State: {user_profile.get('state')} not in {required_states}")

        # Category check
        user_category = user_profile.get("category", "").lower()
        required_categories = eligibility.get("categories", [])
        if required_categories:
            if not user_category:
                missing.append("category")
                explanations.append("⚠ Category: not provided")
            elif user_category in [c.lower() for c in required_categories]:
                matched.append("category")
                explanations.append(f"✓ Category: {user_profile.get('category')}")
            else:
                unmatched.append("category")
                explanations.append(f"✗ Category: {user_profile.get('category')} not in {required_categories}")

        # Gender check
        user_gender = user_profile.get("gender", "").lower()
        required_genders = eligibility.get("genders", [])
        if required_genders:
            if not user_gender:
                missing.append("gender")
                explanations.append("⚠ Gender: not provided")
            elif user_gender in [g.lower() for g in required_genders]:
                matched.append("gender")
                explanations.append(f"✓ Gender: {user_profile.get('gender')}")
            else:
                unmatched.append("gender")
                explanations.append(f"✗ Gender: {user_profile.get('gender')} not in {required_genders}")

        # Occupation check
        user_occupation = user_profile.get("occupation", "").lower()
        required_occupations = eligibility.get("occupations", [])
        if required_occupations:
            if not user_occupation:
                missing.append("occupation")
                explanations.append("⚠ Occupation: not provided")
            elif any(user_occupation in occ.lower() or occ.lower() in user_occupation for occ in required_occupations):
                matched.append("occupation")
                explanations.append(f"✓ Occupation: {user_profile.get('occupation')}")
            else:
                unmatched.append("occupation")
                explanations.append(f"✗ Occupation: {user_profile.get('occupation')} not in {required_occupations}")

        # Determine status
        total_criteria = len(matched) + len(unmatched) + len(missing)
        if total_criteria == 0:
            status = "INSUFFICIENT_INFORMATION"
        elif len(unmatched) > 0:
            status = "NOT_ELIGIBLE"
        elif len(missing) > 0:
            status = "POTENTIALLY_ELIGIBLE"
        else:
            status = "ELIGIBLE"

        # Gap description for NOT_ELIGIBLE
        gap_description = None
        if status == "NOT_ELIGIBLE" and unmatched:
            gaps = []
            if "income" in unmatched and income and income_max:
                gaps.append(f"household income exceeds threshold by ₹{income - income_max:,.0f}")
            if "age" in unmatched:
                gaps.append(f"age {age} outside required range {age_min or '?'}–{age_max or '?'}")
            if "state" in unmatched:
                gaps.append(f"state {user_profile.get('state')} not covered")
            if gaps:
                gap_description = "Not eligible — " + "; ".join(gaps)

        results.append({
            "scheme_id": scheme_id,
            "scheme_name": scheme_name,
            "status": status,
            "matched": matched,
            "unmatched": unmatched,
            "missing": missing,
            "explanation": explanations,
            "gap_description": gap_description,
        })

    return json.dumps({"results": results})
