"""Scrape Coursera listings into a CSV matching the PostgreSQL courses table.

Output columns:
    title, domain, difficulty, duration, description

`duration` is stored as estimated TOTAL HOURS.

Install:
    pip install playwright pandas
    playwright install chromium

Run:
    python scrapping_coursera_updated.py
"""

from __future__ import annotations

import json
import math
import re
import time
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse

import pandas as pd
from playwright.sync_api import Browser, Page, TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.coursera.org"
CATALOG_URL = (
    "https://www.coursera.org/courses"
    "?page={page}&index=prod_all_products_term_optimization"
)
OUTPUT_FILE = Path("coursera_courses.csv")
TARGET_RECORDS = 500

# Include regular courses, guided projects, specializations, and certificates.
ALLOWED_PATH_PREFIXES = (
    "/learn/",
    "/projects/",
    "/specializations/",
    "/professional-certificates/",
)

DOMAIN_KEYWORDS: dict[str, tuple[str, ...]] = {
    "Data Science": (
        "data science", "data analysis", "analytics", "machine learning",
        "deep learning", "artificial intelligence", " ai ", "statistics",
        "pandas", "numpy", "data visualization", "tableau", "power bi",
    ),
    "Computer Science": (
        "computer science", "programming", "python", "java", "javascript",
        "c++", "software", "web development", "algorithm", "database",
        "sql", "cloud computing", "cybersecurity", "network", "devops",
        "linux", "react", "frontend", "backend", "mobile development",
    ),
    "Information Technology": (
        "information technology", "it support", "technical support",
        "system administration", "networking", "cloud", "security",
    ),
    "Business": (
        "business", "management", "marketing", "finance", "accounting",
        "entrepreneurship", "leadership", "project management", "sales",
        "human resources", "strategy", "operations", "supply chain",
    ),
    "Health": (
        "health", "medicine", "medical", "nursing", "patient", "clinical",
        "public health", "nutrition", "psychology", "well-being",
    ),
    "Physical Science and Engineering": (
        "engineering", "physics", "chemistry", "electronics", "robotics",
        "mechanical", "electrical", "civil engineering", "energy",
    ),
    "Arts and Humanities": (
        "art", "music", "history", "philosophy", "literature", "writing",
        "design", "photography", "creative",
    ),
    "Social Sciences": (
        "social science", "economics", "sociology", "politics", "law",
        "education", "teaching", "communication",
    ),
    "Language Learning": (
        "language", "english", "spanish", "french", "german", "chinese",
        "japanese", "korean", "grammar", "vocabulary",
    ),
    "Personal Development": (
        "personal development", "productivity", "career development",
        "mindfulness", "self improvement", "learning how to learn",
    ),
}


def clean_text(value: str | None) -> str:
    """Collapse repeated whitespace and safely handle missing values."""
    return re.sub(r"\s+", " ", value or "").strip()


def normalize_url(href: str) -> str | None:
    """Return an allowed, canonical Coursera product URL."""
    if not href:
        return None

    absolute = urljoin(BASE_URL, href)
    parsed = urlparse(absolute)
    path = parsed.path.rstrip("/") + "/"

    if not any(path.startswith(prefix) for prefix in ALLOWED_PATH_PREFIXES):
        return None

    # Remove query parameters and fragments to avoid duplicate product links.
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path.rstrip('/')}"


def parse_duration_hours(text: str) -> int | None:
    """Convert Coursera duration text into estimated total hours.

    Examples:
        '2 weeks at 10 hours a week' -> 20
        '3 months at 8 hours a week' -> 96
        'Approximately 14 hours' -> 14
        '1.5 hours' -> 2 (rounded up)

    Assumption: 1 month = 4 weeks.
    """
    if not text:
        return None

    normalized = clean_text(text).lower().replace("hrs", "hours").replace("hr", "hour")

    # Most precise format: "2 weeks at 10 hours a week".
    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(week|weeks|month|months)\s*(?:at|,)?\s*"
        r"(\d+(?:\.\d+)?)\s*hours?\s*(?:a|per)\s*week",
        normalized,
    )
    if match:
        count = float(match.group(1))
        unit = match.group(2)
        weekly_hours = float(match.group(3))
        weeks = count * (4 if "month" in unit else 1)
        return max(1, math.ceil(weeks * weekly_hours))

    # Flexible wording such as "2 weeks, 10 hours per week".
    period_match = re.search(r"(\d+(?:\.\d+)?)\s*(week|weeks|month|months)", normalized)
    weekly_match = re.search(r"(\d+(?:\.\d+)?)\s*hours?\s*(?:a|per)\s*week", normalized)
    if period_match and weekly_match:
        count = float(period_match.group(1))
        unit = period_match.group(2)
        weekly_hours = float(weekly_match.group(1))
        weeks = count * (4 if "month" in unit else 1)
        return max(1, math.ceil(weeks * weekly_hours))

    # Direct total duration such as "Approximately 20 hours".
    total_match = re.search(r"(?:approximately|approx\.?|about)?\s*(\d+(?:\.\d+)?)\s*hours?", normalized)
    if total_match:
        return max(1, math.ceil(float(total_match.group(1))))

    # Sometimes only weeks/months are provided. Use a conservative 5 hours/week.
    if period_match:
        count = float(period_match.group(1))
        unit = period_match.group(2)
        weeks = count * (4 if "month" in unit else 1)
        return max(1, math.ceil(weeks * 5))

    return None


def infer_domain(title: str, skills: Iterable[str], description: str) -> str:
    """Infer a broad domain from title, listed skills, and description."""
    haystack = " " + " ".join([title, *skills, description]).lower() + " "

    scores: dict[str, int] = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in haystack:
                # Skills/title matches are more valuable than a random description match.
                score += 2 if keyword.strip() in (title.lower() + " " + " ".join(skills).lower()) else 1
        scores[domain] = score

    best_domain = max(scores, key=scores.get)
    return best_domain if scores[best_domain] > 0 else "General"


def extract_json_ld(page: Page) -> list[dict]:
    """Read JSON-LD objects embedded in a product page."""
    objects: list[dict] = []
    for script in page.locator('script[type="application/ld+json"]').all():
        try:
            raw = script.text_content() or ""
            data = json.loads(raw)
            if isinstance(data, list):
                objects.extend(item for item in data if isinstance(item, dict))
            elif isinstance(data, dict):
                objects.append(data)
        except (json.JSONDecodeError, PlaywrightTimeoutError):
            continue
    return objects


def first_meta_content(page: Page, selectors: list[str]) -> str:
    for selector in selectors:
        locator = page.locator(selector).first
        try:
            if locator.count():
                value = locator.get_attribute("content")
                if clean_text(value):
                    return clean_text(value)
        except PlaywrightTimeoutError:
            continue
    return ""


def extract_title(page: Page, json_ld: list[dict]) -> str:
    for obj in json_ld:
        name = clean_text(str(obj.get("name", "")))
        if name:
            return name

    h1 = page.locator("h1").first
    if h1.count():
        title = clean_text(h1.text_content())
        if title:
            return title

    return first_meta_content(page, ['meta[property="og:title"]', 'meta[name="twitter:title"]'])


def extract_description(page: Page, json_ld: list[dict]) -> str:
    for obj in json_ld:
        description = clean_text(str(obj.get("description", "")))
        if description:
            return description

    return first_meta_content(
        page,
        ['meta[name="description"]', 'meta[property="og:description"]'],
    )


def extract_difficulty(body_text: str) -> str:
    patterns = (
        ("Beginner", r"\bbeginner(?: level)?\b"),
        ("Intermediate", r"\bintermediate(?: level)?\b"),
        ("Advanced", r"\badvanced(?: level)?\b"),
        ("Mixed", r"\bmixed(?: level)?\b"),
    )
    lowered = body_text.lower()
    for label, pattern in patterns:
        if re.search(pattern, lowered):
            return label
    return "Not specified"


def extract_skills(body_text: str) -> list[str]:
    """Extract text following the common 'Skills you'll gain' heading."""
    text = clean_text(body_text)
    match = re.search(
        r"Skills you(?:'|’)ll gain\s*:?\s*(.{0,600}?)(?="
        r"Details to know|Assessments|Taught in|Build toward|There are|$)",
        text,
        flags=re.IGNORECASE,
    )
    if not match:
        return []

    raw = match.group(1)
    # Coursera often renders skills as compact labels separated by punctuation.
    parts = re.split(r"[,•|;]", raw)
    skills = [clean_text(part) for part in parts]
    return [skill for skill in skills if 2 <= len(skill) <= 80][:20]


def extract_duration_text(body_text: str) -> str:
    """Locate the most useful duration phrase in the visible page text."""
    text = clean_text(body_text)
    patterns = [
        r"\d+(?:\.\d+)?\s*(?:weeks?|months?)\s*(?:at|,)?\s*\d+(?:\.\d+)?\s*hours?\s*(?:a|per)\s*week",
        r"(?:approximately|approx\.?|about)?\s*\d+(?:\.\d+)?\s*hours?",
        r"\d+(?:\.\d+)?\s*(?:weeks?|months?)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return clean_text(match.group(0))
    return ""


def collect_product_urls(page: Page, target: int) -> list[str]:
    """Collect distinct product links from Coursera catalog pages."""
    product_urls: list[str] = []
    seen: set[str] = set()

    catalog_page = 1
    while len(product_urls) < target and catalog_page <= 50:
        url = CATALOG_URL.format(page=catalog_page)
        print(f"Catalog page {catalog_page}: {url}")

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60_000)
            page.wait_for_timeout(2_500)

            # Scroll so lazy-loaded product cards are added to the DOM.
            for _ in range(5):
                page.mouse.wheel(0, 1800)
                page.wait_for_timeout(500)

            hrefs = page.locator("a[href]").evaluate_all(
                "elements => elements.map(element => element.getAttribute('href'))"
            )
        except PlaywrightTimeoutError:
            print(f"  Timed out loading catalog page {catalog_page}; skipping.")
            catalog_page += 1
            continue

        before = len(product_urls)
        for href in hrefs:
            normalized = normalize_url(href or "")
            if normalized and normalized not in seen:
                seen.add(normalized)
                product_urls.append(normalized)
                if len(product_urls) >= target:
                    break

        print(f"  Added {len(product_urls) - before} links; total {len(product_urls)}")
        catalog_page += 1

    return product_urls[:target]


def scrape_product(browser: Browser, url: str) -> dict[str, object] | None:
    page = browser.new_page(
        viewport={"width": 1440, "height": 1000},
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
    )

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=60_000)
        page.wait_for_timeout(1_500)

        body_text = clean_text(page.locator("body").inner_text(timeout=20_000))
        json_ld = extract_json_ld(page)

        title = extract_title(page, json_ld)
        description = extract_description(page, json_ld)
        difficulty = extract_difficulty(body_text)
        skills = extract_skills(body_text)
        duration_text = extract_duration_text(body_text)
        duration = parse_duration_hours(duration_text)
        domain = infer_domain(title, skills, description)

        if not title:
            print(f"  Skipped: no title found for {url}")
            return None

        return {
            "title": title,
            "domain": domain,
            "difficulty": difficulty,
            "duration": duration,
            "description": description,
            "url": url
        }
    except Exception as exc:  # Continue scraping even when one page changes/fails.
        print(f"  Failed: {url} ({exc})")
        return None
    finally:
        page.close()


def main() -> None:
    records: list[dict[str, object]] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        catalog_page = browser.new_page(viewport={"width": 1440, "height": 1000})

        try:
            # Collect a few extra links in case some product pages fail.
            urls = collect_product_urls(catalog_page, target=TARGET_RECORDS + 25)
        finally:
            catalog_page.close()

        print(f"\nFound {len(urls)} candidate product URLs.\n")

        for index, url in enumerate(urls, start=1):
            if len(records) >= TARGET_RECORDS:
                break

            print(f"[{index}/{len(urls)}] Scraping {url}")
            record = scrape_product(browser, url)
            if record:
                records.append(record)
                print(
                    f"  Saved: {record['title']} | {record['domain']} | "
                    f"{record['difficulty']} | {record['duration']} hours"
                )

            # Small delay to avoid sending requests too aggressively.
            time.sleep(0.4)

        browser.close()

    dataframe = pd.DataFrame(
        records,
        columns=["title", "domain", "difficulty", "duration", "description","url"],
    )

    dataframe.drop_duplicates(subset=["title"], inplace=True)
    dataframe.sort_values("title", inplace=True)
    dataframe.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print(f"\nSaved {len(dataframe)} rows to: {OUTPUT_FILE.resolve()}")
    print("CSV columns:", list(dataframe.columns))


if __name__ == "__main__":
    main()