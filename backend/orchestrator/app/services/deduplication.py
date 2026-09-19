"""Deduplication service for discovered schemes.

De-dupes on official scheme URL, canonical URL, scheme name, and
government department — the same scheme should never appear multiple times.
"""
from difflib import SequenceMatcher


def normalize_url(url: str) -> str:
    """Normalize a URL for comparison."""
    if not url:
        return ""
    url = url.lower().strip().rstrip("/")
    url = url.replace("http://", "https://")
    url = url.replace("www.", "")
    return url


def name_similarity(a: str, b: str) -> float:
    """Compute similarity between two scheme names."""
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()


def deduplicate_schemes(schemes: list[dict]) -> list[dict]:
    """Remove duplicate schemes based on URL and name similarity.

    De-dupe on official scheme URL, canonical URL, scheme name, and
    government department — the same scheme should never appear five times.
    """
    if not schemes:
        return []

    seen_urls = set()
    unique = []

    for scheme in schemes:
        url = normalize_url(scheme.get("source_url", ""))

        # Skip if we've seen this exact URL
        if url and url in seen_urls:
            continue

        # Check name similarity with already-accepted schemes
        is_duplicate = False
        scheme_name = scheme.get("scheme_name", "")
        for existing in unique:
            existing_name = existing.get("scheme_name", "")
            if name_similarity(scheme_name, existing_name) > 0.85:
                is_duplicate = True
                break

        if not is_duplicate:
            if url:
                seen_urls.add(url)
            unique.append(scheme)

    return unique
