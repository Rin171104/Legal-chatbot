import os
import time
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE_URL = "https://www.haui.edu.vn"
OUTPUT_DIR = "data/raw_docs/overview"
TARGET_URLS = [
    "https://www.haui.edu.vn/vn/html/lich-su",
    "https://www.haui.edu.vn/vn/html/co-so-vat-chat",
    "https://www.haui.edu.vn/vn/html/danh-hieu-khen-thuong",
    "https://www.haui.edu.vn/vn/html/chien-luoc-phat-trien",
    "https://www.haui.edu.vn/vn/html/so-do-to-chuc",
    "https://www.haui.edu.vn/vn/html/dang-uy",
    "https://www.haui.edu.vn/vn/html/ban-giam-hieu",
    "https://www.haui.edu.vn/vn/html/cong-doan",
    "https://www.haui.edu.vn/vn/html/cac-khoa",
    "https://www.haui.edu.vn/vn/html/cac-trung-tam",
    "https://www.haui.edu.vn/vn/html/lien-he",
    "https://www.haui.edu.vn/vn/html/doi-ngu-can-bo",
]

# ✅ CHỈ CRAWL URL CHỨA CÁC KEYWORD NÀY
ALLOW_KEYWORDS = [
    "gioi-thieu",
    "lich-su",
    "tam-nhin",
    "su-menh",
    "co-cau",
    "khoa",
    "vien",
    "phong-ban",
    "dao-tao",
    "nganh"
]

VISITED = set()
MAX_PAGES = 30          # giới hạn để KHÔNG crawl bừa
DELAY = 1.0             # 1 giây / request (lịch sự)

HEADERS = {
    "User-Agent": "HaUI-RAG-Chatbot (edu project)"
}


def is_valid_url(url: str) -> bool:
    if not url.startswith(BASE_URL):
        return False
    return any(key in url for key in ALLOW_KEYWORDS)


def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def fetch_html(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return response.text


def extract_links(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        next_url = urljoin(base_url, a["href"])
        if is_valid_url(next_url):
            links.append(next_url)
    return links


def url_to_filename(url: str) -> str:
    safe = url.replace("https://", "").replace("http://", "")
    safe = safe.strip("/").replace("/", "_")
    if not safe:
        safe = "page"
    return f"{safe}.txt"


def crawl(start_url: str, write_individual_files: bool = True, max_pages: int = MAX_PAGES):
    queue = [start_url]
    collected = []
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    while queue and len(VISITED) < max_pages:
        url = queue.pop(0)
        if url in VISITED or not is_valid_url(url):
            continue

        try:
            print(f"🌐 Crawling: {url}")
            html = fetch_html(url)
            text = clean_html(html)
            VISITED.add(url)
            collected.append((url, text))

            if write_individual_files:
                filename = url.replace(BASE_URL, "").strip("/").replace("/", "_")
                if not filename:
                    filename = "home"
                filename += ".txt"

                with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
                    f.write(text)

            for next_url in extract_links(html, url):
                if next_url not in VISITED:
                    queue.append(next_url)

            time.sleep(DELAY)

        except Exception as e:
            print(f"❌ Lỗi {url}: {e}")

    return collected


def save_to_single_file(pages: list[tuple[str, str]], filename: str):
    if not pages:
        print("⚠️ Không có nội dung để lưu")
        return

    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        for idx, (url, text) in enumerate(pages, start=1):
            f.write(f"## Nguồn {idx}: {url}\n")
            f.write(text)
            f.write("\n\n")

    print(f"✅ Đã lưu nội dung tổng hợp tại {path}")


def crawl_overview():
    start_url = f"{BASE_URL}/gioi-thieu"
    pages = crawl(start_url, write_individual_files=False, max_pages=10)
    save_to_single_file(pages, "haui_overview.txt")


def crawl_target_urls():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pages: list[tuple[str, str]] = []

    for url in TARGET_URLS:
        if url in VISITED:
            continue

        try:
            print(f"🌐 Crawling: {url}")
            html = fetch_html(url)
            text = clean_html(html)
            VISITED.add(url)
            pages.append((url, text))

            filename = url_to_filename(url)
            with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
                f.write(text)

            time.sleep(DELAY)

        except Exception as e:
            print(f"❌ Lỗi {url}: {e}")

    save_to_single_file(pages, "haui_overview.txt")


if __name__ == "__main__":
    crawl_target_urls()
