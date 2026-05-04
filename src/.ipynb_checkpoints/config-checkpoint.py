from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_TABLES_DIR = BASE_DIR / "output" / "tables"
OUTPUT_FIGURES_DIR = BASE_DIR / "output" / "figures"

for path in [DATA_RAW_DIR, DATA_PROCESSED_DIR, OUTPUT_TABLES_DIR, OUTPUT_FIGURES_DIR]:
    path.mkdir(parents=True, exist_ok=True)

RSS_URL = "https://news.google.com/rss/search?q={query}&hl=ko&gl=KR&ceid=KR:ko"
DEFAULT_QUERY = "AI"
DEFAULT_LIMIT = 30
REQUEST_TIMEOUT = 10
CRAWL_DELAY_SECONDS = 1
