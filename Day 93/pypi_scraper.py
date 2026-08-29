"""
Day 93 — Personal Portfolio Project: PyPI Package Info Scraper
Scrapes a live PyPI package page and extracts key details — version,
summary, license, owner, and Python requirement — using requests +
BeautifulSoup (no API involved, pure HTML scraping).

Run: python pypi_scraper.py [package_name]
Defaults to "flask" if no package name is given.
"""

import requests
from bs4 import BeautifulSoup
import sys

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PortfolioScraper/1.0)"}


def scrape_package(package_name: str) -> dict | None:
    """Scrape a PyPI package page and return its key details as a dict.
    Returns None (with a printed message) if the package page can't be loaded."""
    url = f"https://pypi.org/project/{package_name}/"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 404:
        print(f"❌ No PyPI package found named '{package_name}'.")
        return None
    elif response.status_code != 200:
        print(f"⚠️  Unexpected error loading page: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Some sites return HTTP 200 but serve an anti-bot "challenge" page
    # instead of real content when they suspect automated traffic.
    # Always verify you actually got the page you expected, not just a 200.
    page_title = soup.title.text.strip() if soup.title else ""
    if "challenge" in page_title.lower() or "just a moment" in page_title.lower():
        print(f"⚠️  Blocked by an anti-bot challenge page (got '{page_title}').")
        print("    This happens when requests are sent too quickly/frequently.")
        print("    Fix: slow down requests, rotate User-Agent, or use official APIs where available.")
        return None

    # ── Package name + version ──────────────────────────────────
    name_header = soup.find("h1", class_="project-header__name")
    if name_header is None:
        print(f"❌ Couldn't find package '{package_name}' — page structure unrecognized.")
        return None
    full_title = name_header.text.strip()

    # ── Summary/tagline (appears as the first <p> right after the h1) ──
    summary_elem = name_header.find_next("p")
    summary = summary_elem.text.strip() if summary_elem else "(no summary found)"

    # ── Sidebar sections: License, Requires Python, Owner/Author ──
    license_text = "Unknown"
    requires_python = "Unknown"
    owner = "Unknown"
    maintainer = "Unknown"

    for section in soup.find_all("div", class_="sidebar-section"):
        text = section.get_text(separator="|", strip=True)
        parts = [p for p in text.split("|") if p]
        if not parts:
            continue

        if parts[0] == "License expression" and len(parts) > 1:
            license_text = parts[1]

        elif parts[0] == "Requires" and len(parts) >= 3 and parts[1] == "Python":
            requires_python = parts[2]

        elif parts[0] == "Owner" and len(parts) >= 2:
            # Not every package has a verified "Owner" section — only some do
            owner = parts[-1]

        elif parts[0] == "Credits":
            # Fallback: most packages show Author/Maintainer here instead
            if "Author:" in parts:
                idx = parts.index("Author:")
                if idx + 1 < len(parts) and owner == "Unknown":
                    owner = parts[idx + 1]
            if "Maintainer:" in parts:
                idx = parts.index("Maintainer:")
                if idx + 1 < len(parts):
                    maintainer = parts[idx + 1]

    return {
        "package_name": package_name,
        "title_with_version": full_title,
        "summary": summary,
        "license": license_text,
        "requires_python": requires_python,
        "owner": owner,
        "maintainer": maintainer,
        "url": url,
    }


def print_report(data: dict):
    print("=" * 55)
    print(f"  PyPI Package Report — {data['title_with_version']}")
    print("=" * 55)
    print(f"\n📝 Summary:          {data['summary']}")
    print(f"⚖️  License:          {data['license']}")
    print(f"🐍 Requires Python:   {data['requires_python']}")
    print(f"👤 Owner:             {data['owner']}")
    print(f"🛠️  Maintainer:        {data['maintainer']}")
    print(f"🔗 URL:               {data['url']}")


def compare_packages(package_names: list):
    """Scrape multiple packages and print a simple side-by-side summary."""
    results = []
    for name in package_names:
        data = scrape_package(name)
        if data:
            results.append(data)

    if not results:
        print("No packages could be loaded for comparison.")
        return

    print("\n" + "=" * 65)
    print("  Comparison")
    print("=" * 65)
    print(f"{'Package':<20}{'License':<20}{'Requires Python':<20}")
    print("-" * 65)
    for r in results:
        print(f"{r['package_name']:<20}{r['license']:<20}{r['requires_python']:<20}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_package = sys.argv[1]
    else:
        target_package = "flask"

    package_data = scrape_package(target_package)
    if package_data:
        print_report(package_data)
