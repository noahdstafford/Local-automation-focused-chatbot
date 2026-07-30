import re
import feedparser
from newspaper import Article
from chat import ask_ollama


feeds = {
    "Tech & Engineering": "http://feeds.bbci.co.uk/news/technology/rss.xml",
    "Stocks/Business": "http://feeds.bbci.co.uk/news/business/rss.xml",
    "Irish News": "https://www.rte.ie/feeds/rss/?index=/news",
    "UK News": "http://feeds.bbci.co.uk/news/uk/rss.xml",
    "World News": "http://feeds.bbci.co.uk/news/world/rss.xml",
}

def clean_text(text):
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'#+', '', text) 
    return text.strip()


def get_news_digest():
    digest_sections = []

    for category, url in feeds.items():
        print(f"\n--- {category} ---")

        feed = feedparser.parse(url)
        top_entries = feed.entries[:5]

        category_text = ""

        for entry in top_entries:
            try:
                article = Article(entry.link)
                article.download()
                article.parse()
                category_text += f"\n\n{entry.title}\n{article.text}"
            except Exception as e:
                print(f"Could not fetch article: {e}")

        prompt = f"""Summarize the following {category} news articles into a short, natural-sounding spoken briefing. Be concise but informative.

{category_text}"""

        section_summary = ask_ollama(prompt)
        clean_summary = clean_text(section_summary)

        section = f"{category}\n{'-' * len(category)}\n{clean_summary}"
        print(section)

        digest_sections.append(section)

    return "\n\n".join(digest_sections)


if __name__ == "__main__":
    news_digest = get_news_digest()