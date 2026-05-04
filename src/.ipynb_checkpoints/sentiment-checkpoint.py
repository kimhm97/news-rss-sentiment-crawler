import pandas as pd

POSITIVE_WORDS = [
    "성장", "개선", "상승", "호재", "기대", "혁신", "성공", "확대", "강세", "긍정",
    "수혜", "회복", "돌파", "최고", "활성화", "증가", "발전", "안정", "성과"
]

NEGATIVE_WORDS = [
    "하락", "악재", "우려", "위험", "논란", "감소", "침체", "부정", "손실", "위기",
    "불안", "압박", "규제", "실패", "둔화", "급락", "피해", "갈등", "경고"
]


def calculate_sentiment_score(text: str) -> int:
    """간단한 사전 기반 감정 점수를 계산한다.

    긍정 단어 출현 횟수는 +1, 부정 단어 출현 횟수는 -1로 계산한다.
    """
    text = str(text)
    positive_count = sum(text.count(word) for word in POSITIVE_WORDS)
    negative_count = sum(text.count(word) for word in NEGATIVE_WORDS)
    return positive_count - negative_count


def label_sentiment(score: int) -> str:
    if score > 0:
        return "positive"
    if score < 0:
        return "negative"
    return "neutral"


def add_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["sentiment_score"] = df["clean_text"].apply(calculate_sentiment_score)
    df["sentiment_label"] = df["sentiment_score"].apply(label_sentiment)
    return df
