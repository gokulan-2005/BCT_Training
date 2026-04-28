from pathlib import Path
from urllib.parse import parse_qs, quote_plus, unquote, urlparse
import re
import requests
from bs4 import BeautifulSoup
from crewai.tools import tool

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "outputs"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "article"


@tool("search_google_news")
def search_google_news(topic: str) -> str:
    """Search for recent news results and return up to 5 article titles with direct URLs."""
    try:
        url = f"https://duckduckgo.com/html/?q={quote_plus(topic + ' latest news')}"
        response = requests.get(url, timeout=20, headers={"User-Agent": USER_AGENT})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        links = soup.select("a.result__a")
        if not links:
            return f"No recent news results found for: {topic}"

        results = []
        seen_urls = set()
        for link_tag in links:
            href = (link_tag.get("href") or "").strip()
            parsed = urlparse(href)
            if "duckduckgo.com" in parsed.netloc and parsed.path.startswith("/l/"):
                target = parse_qs(parsed.query).get("uddg", [""])[0]
                href = unquote(target) if target else href

            if not href.startswith("http") or href in seen_urls:
                continue

            seen_urls.add(href)
            title = link_tag.get_text(" ", strip=True) or "Untitled"
            results.append(f"{len(results) + 1}. {title}\nURL: {href}")
            if len(results) == 5:
                break

        if not results:
            return f"No direct article URLs found for: {topic}"

        return "\n\n".join(results)
    except Exception as exc:
        return f"Error searching news for '{topic}': {exc}"


@tool("scrape_website")
def scrape_website(url: str) -> str:
    """Fetch a webpage and return the first useful paragraphs of article text."""
    try:
        response = requests.get(url, timeout=20, headers={"User-Agent": USER_AGENT})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = [
            p.get_text(" ", strip=True)
            for p in soup.find_all("p")
            if p.get_text(" ", strip=True)
        ]
        if not paragraphs:
            return f"No paragraph content found at {url}"

        preview = " ".join(paragraphs[:20])
        return f"URL: {url}\n\n{preview}"
    except Exception as exc:
        return f"Error scraping {url}: {exc}"


@tool("save_markdown_article")
def save_markdown_article(content: str, topic: str = "ai-news") -> str:
    """Save markdown content to the outputs directory and return the file path."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    file_path = OUTPUT_DIR / f"{_slugify(topic)}.md"
    file_path.write_text(content, encoding="utf-8")
    return f"Saved article to {file_path}"
