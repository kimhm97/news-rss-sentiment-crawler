import matplotlib.pyplot as plt
import pandas as pd


def save_sentiment_bar(summary_df: pd.DataFrame, save_path):
    plt.figure(figsize=(7, 4))
    plt.bar(summary_df["sentiment_label"], summary_df["count"])
    plt.title("Sentiment Distribution")
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()


def save_keyword_bar(keyword_df: pd.DataFrame, save_path):
    top_df = keyword_df.head(15).sort_values("count")
    plt.figure(figsize=(8, 6))
    plt.barh(top_df["keyword"], top_df["count"])
    plt.title("Top Keywords")
    plt.xlabel("Count")
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
