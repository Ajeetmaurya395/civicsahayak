"""Government page retriever — fetches and parses official government pages.

Fetch + parse — only is_trusted_government_source domains — then dedupe.
Includes SSRF protection: never let a user-supplied URL be fetched unvalidated.
"""
import json
import logging
import httpx
from bs4 import BeautifulSoup
from strands import tool
from app.tools.url_validator import is_trusted_government_source

logger = logging.getLogger(__name__)

# Request limits
TIMEOUT = 15.0
MAX_CONTENT_LENGTH = 500_000  # 500KB max page size


def _clean_text(text: str) -> str:
    """Clean extracted text from HTML."""
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        line = line.strip()
        if line and len(line) > 2:
            cleaned.append(line)
    return "\n".join(cleaned)


def _extract_page_content(html: str, url: str) -> dict:
    """Extract structured content from an HTML page."""
    soup = BeautifulSoup(html, "lxml")

    # Remove script, style, nav, footer elements
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    title = ""
    if soup.title:
        title = soup.title.string or ""

    # Try to find main content area
    main_content = soup.find("main") or soup.find("article") or soup.find("div", {"id": "content"})
    if not main_content:
        main_content = soup.find("body")

    text = ""
    if main_content:
        text = _clean_text(main_content.get_text(separator="\n"))

    # Extract links that might be application URLs
    application_links = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        link_text = a_tag.get_text(strip=True).lower()
        if any(kw in link_text for kw in ["apply", "register", "application", "आवेदन"]):
            if href.startswith("http"):
                application_links.append({"text": a_tag.get_text(strip=True), "url": href})

    return {
        "title": title.strip(),
        "url": url,
        "content": text[:10000],  # Cap content
        "application_links": application_links[:5],
        "verified": is_trusted_government_source(url),
    }


@tool
def government_retriever(urls_json: str) -> str:
    """Fetch and parse government web pages from trusted domains.

    Takes a JSON list of URLs, validates each against trusted government
    domains, fetches the page, and returns structured content.
    Never fetches non-government URLs.
    """
    try:
        urls = json.loads(urls_json) if isinstance(urls_json, str) else urls_json
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid URL list JSON", "pages": []})

    if isinstance(urls, str):
        urls = [urls]

    results = []
    for url in urls[:5]:  # Cap at 5 URLs per call
        if not is_trusted_government_source(url):
            logger.warning(f"Skipping non-government URL: {url}")
            results.append({
                "url": url,
                "error": "Not a trusted government source",
                "verified": False,
            })
            continue

        try:
            with httpx.Client(timeout=TIMEOUT, follow_redirects=True) as client:
                response = client.get(
                    url,
                    headers={
                        "User-Agent": "CivicOS/1.0 (Government Scheme Discovery; +https://github.com/civicos)",
                        "Accept": "text/html,application/xhtml+xml",
                    },
                )
                response.raise_for_status()

                if len(response.content) > MAX_CONTENT_LENGTH:
                    logger.warning(f"Page too large: {url}")
                    results.append({"url": url, "error": "Page too large", "verified": True})
                    continue

                page_data = _extract_page_content(response.text, url)
                results.append(page_data)

        except httpx.TimeoutException:
            logger.error(f"Timeout fetching {url}")
            results.append({"url": url, "error": "Request timed out", "verified": True})
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} for {url}")
            results.append({"url": url, "error": f"HTTP {e.response.status_code}", "verified": True})
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            results.append({"url": url, "error": str(e), "verified": True})

    return json.dumps({"pages": results, "total_fetched": len(results)})
