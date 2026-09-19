"""URL validator — checks if a URL belongs to a trusted government domain.

True only for an accepted government domain — never trust a title
just because it contains the words 'Government Scheme'.
"""
from urllib.parse import urlparse

TRUSTED_SUFFIXES = (
    ".gov.in",
    ".nic.in",
    "data.gov.in",
    "myscheme.gov.in",
    "scholarships.gov.in",
    "pmjay.gov.in",
    "pmkisan.gov.in",
    "india.gov.in",
    "nrega.nic.in",
)

# Known government domains without .gov.in suffix
TRUSTED_EXACT_DOMAINS = {
    "myscheme.gov.in",
    "scholarships.gov.in",
    "india.gov.in",
    "data.gov.in",
}


def is_trusted_government_source(url: str) -> bool:
    """Check if a URL is from a trusted Indian government domain.

    True only for an accepted government domain — never trust a title
    just because it contains the words 'Government Scheme'.
    """
    if not url:
        return False

    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        # Remove www. prefix
        if domain.startswith("www."):
            domain = domain[4:]

        # Check exact matches first
        if domain in TRUSTED_EXACT_DOMAINS:
            return True

        # Check suffixes
        for suffix in TRUSTED_SUFFIXES:
            if domain.endswith(suffix):
                return True

        return False
    except Exception:
        return False


def get_domain(url: str) -> str:
    """Extract the domain from a URL."""
    try:
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except Exception:
        return ""
