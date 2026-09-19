"""Deterministic Rule Evaluator.

One class per condition type (AgeCondition, IncomeCondition, etc.)
so a scheme with an unusual eligibility shape doesn't need every field
forced into a common template — unknown/absent condition types are
simply skipped, not treated as failures.

The four statuses:
- ELIGIBLE: every criterion satisfied, nothing left unchecked
- POTENTIALLY_ELIGIBLE: everything checked so far passes, but some fields missing
- NOT_ELIGIBLE: at least one criterion explicitly violated
- INSUFFICIENT_INFORMATION: too many core fields missing to evaluate at all
"""
from engine.conditions import (
    AgeCondition,
    IncomeCondition,
    StateCondition,
    CategoryCondition,
    GenderCondition,
    OccupationCondition,
    EducationCondition,
    BPLCondition,
    FarmerCondition,
    DisabilityCondition,
)

# All condition evaluators
CONDITION_EVALUATORS = [
    AgeCondition(),
    IncomeCondition(),
    StateCondition(),
    CategoryCondition(),
    GenderCondition(),
    OccupationCondition(),
    EducationCondition(),
    BPLCondition(),
    FarmerCondition(),
    DisabilityCondition(),
]


def evaluate_eligibility(user_profile: dict, scheme_criteria: list[dict]) -> list[dict]:
    """Evaluate user against multiple schemes. Returns detailed results."""
    results = []

    for scheme_criterion in scheme_criteria:
        scheme_id = scheme_criterion.get("scheme_id", "unknown")
        scheme_name = scheme_criterion.get("scheme_name", "Unknown Scheme")
        eligibility = scheme_criterion.get("eligibility", {})

        if not eligibility:
            results.append({
                "scheme_id": scheme_id,
                "scheme_name": scheme_name,
                "status": "INSUFFICIENT_INFORMATION",
                "matched": [],
                "unmatched": [],
                "missing": [],
                "explanation": ["No eligibility criteria available for this scheme."],
                "gap_description": None,
            })
            continue

        matched = []
        unmatched = []
        missing = []
        explanations = []

        for evaluator in CONDITION_EVALUATORS:
            result = evaluator.evaluate(user_profile, eligibility)
            if result is None:
                # This condition type doesn't apply to this scheme
                continue

            status, detail = result
            if status == "matched":
                matched.append(evaluator.name)
                explanations.append(f"✓ {detail}")
            elif status == "unmatched":
                unmatched.append(evaluator.name)
                explanations.append(f"✗ {detail}")
            elif status == "missing":
                missing.append(evaluator.name)
                explanations.append(f"⚠ {detail}")

        # Determine overall status
        total_criteria = len(matched) + len(unmatched) + len(missing)
        core_fields_missing = sum(1 for f in ["age", "state"] if f in missing)

        if total_criteria == 0:
            status = "INSUFFICIENT_INFORMATION"
        elif core_fields_missing >= 2:
            status = "INSUFFICIENT_INFORMATION"
        elif len(unmatched) > 0:
            status = "NOT_ELIGIBLE"
        elif len(missing) > 0:
            status = "POTENTIALLY_ELIGIBLE"
        else:
            status = "ELIGIBLE"

        # Build gap description for NOT_ELIGIBLE
        gap_description = None
        if status == "NOT_ELIGIBLE":
            gaps = []
            for evaluator in CONDITION_EVALUATORS:
                if evaluator.name in unmatched:
                    gap = evaluator.get_gap_description(user_profile, eligibility)
                    if gap:
                        gaps.append(gap)
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

    return results
