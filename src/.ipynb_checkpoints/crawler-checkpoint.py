import time
from datetime import datetime
from urllib.parse import quote_plus

import feedparser
import pandas as pd
import requests
from bs4 import BeautifulSoup

from config import RSS_URL, REQUEST_TIMEOUT, CRAWL_DELAY_SECONDS

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def collect_google_news_rss(query: str, limit: int = 30) -> pd.DataFrame:
    """Google News RSS에서 기사 제목, 링크, 발행일, 요약 정보를 수집한다."""
    encoded_query = quote_plus(query)
    rss_url = RSS_URL.format(query=encoded_query)
    feed = feedparser.parse(rss_url)

    articles = []
    for entry in feed.entries[:limit]:
        articles.append(
            {
                "query": query,
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "source": entry.get("source", {}).get("title", "") if isinstance(entry.get("source"), dict) else "",
                "summary": BeautifulSoup(entry.get("summary", ""), "html.parser").get_text(" ", strip=True),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
    return pd.DataFrame(articles)


def extract_article_text(url: str) -> str:
    """기사 URL에 직접 접근하여 본문 후보 텍스트를 추출한다.

    사이트마다 HTML 구조가 다르므로 article 태그, p 태그, meta description 순서로 시도한다.
    본문 수집이 차단되거나 실패하면 빈 문자열을 반환한다.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        response.raise_for_status()
    except requests.RequestException:
        return ""

    soup = BeautifulSoup(response.text, "html.parser")

    # 불필요한 태그 제거
    for tag in soup(["script", "style", "nav", "footer", "aside"]):
        tag.decompose()

    article_tag = soup.find("article")
    if article_tag:
        paragraphs = article_tag.find_all("p")
    else:
        paragraphs = soup.find_all("p")

    text = " ".join(p.get_text(" ", strip=True) for p in paragraphs)
    if len(text) >= 100:
        return text

    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        return meta.get("content", "")

    og_meta = soup.find("meta", attrs={"property": "og:description"})
    if og_meta and og_meta.get("content"):
        return og_meta.get("content", "")

    return text


def collect_article_bodies(df: pd.DataFrame) -> pd.DataFrame:
    """RSS로 수집한 기사 링크를 순회하며 본문 텍스트를 추가한다."""
    df = df.copy()
    bodies = []

    for url in df["link"].fillna(""):
        body = extract_article_text(url)
        bodies.append(body)
        time.sleep(CRAWL_DELAY_SECONDS)

    df["body"] = bodies
    df["content_for_analysis"] = df.apply(
        lambda row: " ".join(
            [str(row.get("title", "")), str(row.get("summary", "")), str(row.get("body", ""))]
        ).strip(),
        axis=1,
    )
    return df
