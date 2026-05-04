from collections import Counter
import pandas as pd

STOPWORDS = {
    "그리고", "그러나", "하지만", "대한", "관련", "이번", "있는", "없는", "하는", "했다",
    "뉴스", "기사", "기자", "통해", "위해", "등", "및", "수", "것", "더", "그", "이"
}


def summarize_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df["sentiment_label"]
        .value_counts()
        .rename_axis("sentiment_label")
        .reset_index(name="count")
    )
    summary["ratio"] = summary["count"] / summary["count"].sum()
    return summary


def keyword_frequency(df: pd.DataFrame, top_n: int = 30) -> pd.DataFrame:
    words = []
    for text in df["clean_text"].fillna(""):
        for word in str(text).split():
            if len(word) >= 2 and word not in STOPWORDS:
                words.append(word)
    counter = Counter(words)
    return pd.DataFrame(counter.most_common(top_n), columns=["keyword", "count"])
