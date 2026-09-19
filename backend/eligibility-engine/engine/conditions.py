"""Eligibility condition evaluators.

Each condition type is a separate class. A scheme with an unusual
eligibility shape doesn't need every field forced into a common
template — unknown/absent condition types are simply skipped.
"""
from typing import Optional


class BaseCondition:
    """Base condition evaluator."""
    name: str = "unknown"

    def evaluate(self, user_profile: dict, eligibility: dict) -> Optional[tuple[str, str]]:
        """Evaluate a condition. Returns (status, detail) or None if N/A.

        status: "matched" | "unmatched" | "missing"
        """
        raise NotImplementedError

    def get_gap_description(self, user_profile: dict, eligibility: dict) -> Optional[str]:
        """Get a description of the gap for NOT_ELIGIBLE status."""
        return None


class AgeCondition(BaseCondition):
    name = "age"

    def evaluate(self, user_profile: dict, eligibility: dict) -> Optional[tuple[str, str]]:
        age_min = eligibility.get("age_min")
        age_max = eligibility.get("age_max")

        if age_min is None and age_max is None:
            return None  # No age criterion for this scheme

        user_age = user_profile.get("age")
        if user_age is None:
            return ("missing", "Age: not provided")

        req = f"{age_min or '?'}–{age_max or '?'}"
        if age_min is not None and user_age < age_min:
            return ("unmatched", f"Age: {user_age}, requirement {req}")
        if age_max is not None and user_age > age_max:
            return ("unmatched", f"Age: {user_age}, requirement {req}")
        return ("matched", f"Age: {user_age}, requirement {req}")

    def get_gap_description(self, user_profile: dict, eligibility: dict) -> Optional[str]:
        user_age = user_profile.get("age")
        age_min = eligibility.get("age_min")
        age_max = eligibility.get("age_max")
        if user_age is None:
            return None
        if age_min and user_age < age_min:
            return f"age {user_age} is below minimum {age_min} by {age_min - user_age} years"
        if age_max and user_age > age_max:
            return f"age {user_age} exceeds maximum {age_max} by {user_age - age_max} years"
        return None


class IncomeCondition(BaseCondition):
    name = "income"

    def evaluate(self, user_profile: dict, eligibility: dict) -> Optional[tuple[str, str]]:
        income_max = eligibility.get("income_max")
        income_min = eligibility.get("income_min")

        if income_max is None and income_min is None:
            return None

        user_income = user_profile.get("annual_family_income")
        if user_income is None:
            return ("missing", "Income: not provided")

        if income_max is not None and user_income > income_max:
            return ("unmatched", f"Income: ₹{user_income:,.0f} exceeds maximum ₹{income_max:,.0f}")
        if income_min is not None and user_income < income_min:
            return ("unmatched", f"Income: ₹{user_income:,.0f} below minimum ₹{income_min:,.0f}")

        detail = f"Income: ₹{user_income:,.0f}"
        if income_max:
            detail += f", max ₹{income_max:,.0f}"
        return ("matched", detail)

    def get_gap_description(self, user_profile: dict, eligibility: dict) -> Optional[str]:
        user_income = user_profile.get("annual_family_income")
        income_max = eligibility.get("income_max")
        if user_income and income_max and user_income > income_max:
            gap = user_income - income_max
            return f"household income exceeds threshold by ₹{gap:,.0f}"
        return None


class StateCondition(BaseCondition):
    name = "state"

    def evaluate(self, user_profile: dict, eligibility: dict) -> Optional[tuple[str, str]]:
        required_states = eligibility.get("states")
        if not required_states:
            return None

        user_state = user_profile.get("state", "")
        if not user_state:
            return ("missing", "State: not provided")

        if user_state.lower() in [s.lower() for s in required_states]:
            return ("matched", f"State: {user_state}")
        return ("unmatched", f"State: {user_state} not in {required_states}")

    def get_gap_description(self, user_profile: dict, eligibility: dict) -> Optional[str]:
        user_state = user_profile.get("state", "")
        required_states = eligibility.get("states", [])
        if user_state and required_states:
            return f"state {user_state} is not covered by this scheme"
        return None


class CategoryCondition(BaseCondition):
    name = "category"

    def evaluate(self, user_profile: dict, eligibility: dict) -> Optional[tuple[str, str]]:
        required = eligibility.get("categories")
        if not required:
            return None

        user_val = user_profile.get("category", "")
        if not user_val:
            return ("missing", "Social category: not provided")

        if user_val.lower() in [c.lower() for c in required]:
            return ("matched", f"Category: {user_val}")
        return ("unmatched", f"Category: {user_val} not in {required}")

    def get_gap_description(self, user_profile: dict, eligibility: dict) -> Optional[str]:
        user_val = user_profile.get("category", "")
        required = eligibility.get("categories", [])
        if user_val and required:
            return f"category {user_val} is not among eligible categories {required}"
        return None


class GenderCondition(BaseCondition):
    name = "gender"

    def evaluate(self, user_profile: dict, eligibility: dict) -> Optional[tuple[str, str]]:
        required = eligibility.get("genders")
        if not required:
            return None

        user_val = user_profile.get("gender", "")
        if not user_val:
            return ("missing", "Gender: not provided")

        if user_val.lower() in [g.lower() for g in required]:
            return ("matched", f"Gender: {user_val}")
        return ("unmatched", f"Gender: {user_val} not in {required}")

    def get_gap_description(self, user_profile: dict, eligibility: dict) -> Optional[str]:
        return f"this scheme is restricted to {eligibility.get('genders', [])}"


class OccupationCondition(BaseCondition):
    name = "occupation"

    def evaluate(self, user_profile: dict, eligibility: dict) -> Optional[tuple[str, str]]:
        required = eligibility.get("occupations")
        if not required:
            return None

        user_val = user_profile.get("occupation", "")
        if not user_val:
            return ("missing", "Occupation: not provided")

        if any(user_val.lower() in occ.lower() or occ.lower() in user_val.lower() for occ in required):
            return ("matched", f"Occupation: {user_val}")
        return ("unmatched", f"Occupation: {user_val} not in {required}")

    def get_gap_description(self, user_profile: dict, eligibility: dict) -> Optional[str]:
        return f"occupation does not match required occupations {eligibility.get('occupations', [])}"


class EducationCondition(BaseCondition):
    name = "education"

    def evaluate(self, user_profile: dict, eligibility: dict) -> Optional[tuple[str, str]]:
        required = eligibility.get("education_levels")
        if not required:
            return None

        user_val = user_profile.get("education_level", "")
        if not user_val:
            return ("missing", "Education level: not provided")

        if any(user_val.lower() in ed.lower() or ed.lower() in user_val.lower() for ed in required):
            return ("matched", f"Education: {user_val}")
        return ("unmatched", f"Education: {user_val} not in {required}")

    def get_gap_description(self, user_profile: dict, eligibility: dict) -> Optional[str]:
        return f"education level does not match required levels {eligibility.get('education_levels', [])}"


class BPLCondition(BaseCondition):
    name = "bpl_status"

    def evaluate(self, user_profile: dict, eligibility: dict) -> Optional[tuple[str, str]]:
        required = eligibility.get("is_bpl_required")
        if required is None:
            return None

        user_val = user_profile.get("is_bpl")
        if user_val is None:
            return ("missing", "BPL status: not provided")

        if required and user_val:
            return ("matched", "BPL status: Below Poverty Line")
        elif required and not user_val:
            return ("unmatched", "BPL status: scheme requires BPL card")
        return ("matched", "BPL status: not required")

    def get_gap_description(self, user_profile: dict, eligibility: dict) -> Optional[str]:
        return "this scheme requires Below Poverty Line (BPL) status"


class FarmerCondition(BaseCondition):
    name = "farmer_status"

    def evaluate(self, user_profile: dict, eligibility: dict) -> Optional[tuple[str, str]]:
        required = eligibility.get("is_farmer_required")
        if required is None:
            return None

        user_val = user_profile.get("is_farmer")
        if user_val is None:
            return ("missing", "Farmer status: not provided")

        if required and user_val:
            return ("matched", "Farmer status: confirmed farmer")
        elif required and not user_val:
            return ("unmatched", "Farmer status: scheme requires farmer status")
        return ("matched", "Farmer status: not required")

    def get_gap_description(self, user_profile: dict, eligibility: dict) -> Optional[str]:
        return "this scheme is restricted to farmers"


class DisabilityCondition(BaseCondition):
    name = "disability"

    def evaluate(self, user_profile: dict, eligibility: dict) -> Optional[tuple[str, str]]:
        required = eligibility.get("disability_required")
        if required is None:
            return None

        user_val = user_profile.get("disability")
        if required and not user_val:
            return ("missing", "Disability status: not provided (scheme may require it)")

        if required and user_val:
            return ("matched", f"Disability: {user_val}")
        return ("matched", "Disability: not required")

    def get_gap_description(self, user_profile: dict, eligibility: dict) -> Optional[str]:
        return "this scheme requires persons with disability status"
