import re
import pandas as pd


def clean_text(text: str) -> str:
    """뉴스 텍스트에서 분석에 불필요한 공백과 특수문자를 정리한다."""
    text = str(text)
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"[^가-힣a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def preprocess_articles(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["clean_text"] = df["content_for_analysis"].apply(clean_text)
    df["text_length"] = df["clean_text"].str.len()
    return df
