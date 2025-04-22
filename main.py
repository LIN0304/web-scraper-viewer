#!/usr/bin/env python3
"""
Web Scraper Script:
$ python main.py --url https://example.com --max-pages 100
Generates:
  scraped_data/page_0.md
  scraped_data/page_0_original.json
  ...
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json, os, re, argparse, sys

def scrape_page(url: str) -> dict | None:
    """Scrape a single page, returns {title, content, url, links}."""
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        title = (soup.find("title").text.strip()
                 if soup.find("title") else "No title found")

        main = (soup.find("main")
                or soup.find("article")
                or soup.find("div", class_="content")
                or soup.body)

        content = (main.get_text("\n", strip=True)
                   if main else "No content found")

        base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
        links = [
            urljoin(base, a["href"])
            for a in soup.find_all("a", href=True)
            if not urlparse(a["href"]).netloc      # Relative links
            or urlparse(a["href"]).netloc == urlparse(url).netloc
        ]

        return {"title": title, "content": content, "url": url, "links": links}

    except requests.RequestException as e:
        print(f"[ERROR] {url}: {e}", file=sys.stderr)
        return None

def scrape_website(start_url: str, max_pages: int = 100) -> list[dict]:
    """BFS crawl, max of max_pages pages."""
    visited, to_visit, pages = set(), [start_url], []
    while to_visit and len(pages) < max_pages:
        cur = to_visit.pop(0)
        if cur in visited:
            continue
        visited.add(cur)
        print(f"[SCRAPE] {cur}")
        page = scrape_page(cur)
        if page:
            pages.append(page)
            for link in page["links"]:
                if link not in visited and link not in to_visit:
                    to_visit.append(link)
    return pages

def format_content(raw: str) -> str:
    """Format plain text as Markdown: headings/paragraphs/line breaks."""
    lines, out, lvl, para = raw.split("\n"), [], 0, []
    for line in lines:
        line = line.strip()
        if not line:
            if para:
                out.append(" ".join(para)); para = []
            continue
        # Assume "short line not ending with period" is a heading
        if len(line) <= 100 and not line.endswith("."):
            if para:
                out.append(" ".join(para)); para = []
            lvl = 1 if lvl == 0 or len(line) < 50 else min(lvl + 1, 3)
            out.append(f"{'#'*lvl} {line}")
        else:
            para.append(line)
    if para:
        out.append(" ".join(para))
    return "\n\n".join(out)

def save_pages(pages: list[dict]) -> None:
    os.makedirs("scraped_data", exist_ok=True)
    for i, p in enumerate(pages):
        md_path = f"scraped_data/page_{i}.md"
        json_path = f"scraped_data/page_{i}_original.json"

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# {p['title']}\n\n{format_content(p['content'])}")

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(p, f, ensure_ascii=False, indent=2)

    print(f"[DONE] {len(pages)} pages saved to scraped_data/")

def main():
    parser = argparse.ArgumentParser(description="Simple website scraper → Markdown")
    parser.add_argument("--url", required=True, help="start URL")
    parser.add_argument("--max-pages", type=int, default=100, help="max pages to scrape")
    args = parser.parse_args()

    pages = scrape_website(args.url, args.max_pages)
    save_pages(pages)

if __name__ == "__main__":
    main()
