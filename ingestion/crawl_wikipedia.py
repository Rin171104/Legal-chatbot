import os
import wikipediaapi

OUTPUT_DIR = "data/raw_docs/overview"
OUTPUT_FILE = "wikipedia.txt"

def crawl_wikipedia():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    wiki = wikipediaapi.Wikipedia(
        language="vi",
        user_agent="HaUI-RAG-Chatbot (edu project)"
    )

    page = wiki.page("Đại học Công nghiệp Hà Nội")

    if not page.exists():
        raise ValueError("❌ Không tìm thấy trang Wikipedia")

    text = page.text.strip()

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"✅ Đã crawl Wikipedia -> {output_path}")
    print(f"📏 Độ dài text: {len(text)} ký tự")


if __name__ == "__main__":
    crawl_wikipedia()
