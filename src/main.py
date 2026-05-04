import argparse

from analyze import keyword_frequency, summarize_sentiment
from config import (
    DATA_PROCESSED_DIR,
    DATA_RAW_DIR,
    DEFAULT_LIMIT,
    DEFAULT_QUERY,
    OUTPUT_FIGURES_DIR,
    OUTPUT_TABLES_DIR,
)
from crawler import collect_article_bodies, collect_google_news_rss
from preprocess import preprocess_articles
from sentiment import add_sentiment
from visualize import save_keyword_bar, save_sentiment_bar


def run_pipeline(query: str, limit: int):
    raw_df = collect_google_news_rss(query=query, limit=limit)
    raw_with_body_df = collect_article_bodies(raw_df)

    raw_path = DATA_RAW_DIR / "news_articles_raw.csv"
    raw_with_body_df.to_csv(raw_path, index=False, encoding="utf-8-sig")

    processed_df = preprocess_articles(raw_with_body_df)
    sentiment_df = add_sentiment(processed_df)

    processed_path = DATA_PROCESSED_DIR / "news_articles_sentiment.csv"
    sentiment_df.to_csv(processed_path, index=False, encoding="utf-8-sig")

    sentiment_summary = summarize_sentiment(sentiment_df)
    keyword_df = keyword_frequency(sentiment_df)

    sentiment_summary_path = OUTPUT_TABLES_DIR / "sentiment_summary.csv"
    keyword_path = OUTPUT_TABLES_DIR / "keyword_frequency.csv"
    sentiment_summary.to_csv(sentiment_summary_path, index=False, encoding="utf-8-sig")
    keyword_df.to_csv(keyword_path, index=False, encoding="utf-8-sig")

    save_sentiment_bar(sentiment_summary, OUTPUT_FIGURES_DIR / "sentiment_distribution.png")
    save_keyword_bar(keyword_df, OUTPUT_FIGURES_DIR / "top_keywords.png")

    print("크롤링 및 분석 완료")
    print(f"원본 데이터 저장: {raw_path}")
    print(f"전처리/감정분석 데이터 저장: {processed_path}")
    print(f"분석 결과 저장: {OUTPUT_TABLES_DIR}")
    print(f"그래프 저장: {OUTPUT_FIGURES_DIR}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google News RSS 기반 뉴스 기사 감정 분석 파이프라인")
    parser.add_argument("--query", default=DEFAULT_QUERY, help="검색 키워드")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help="수집 기사 수")
    args = parser.parse_args()

    run_pipeline(query=args.query, limit=args.limit)
