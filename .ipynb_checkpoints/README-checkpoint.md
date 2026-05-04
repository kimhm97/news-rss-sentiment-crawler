# 뉴스 기사 크롤링 기반 감정 분석 프로젝트

## 1. 프로젝트 개요

본 프로젝트는 Google News RSS를 활용하여 뉴스 기사 목록을 수집하고, 각 기사 링크에 접근하여 제목·요약·본문 텍스트를 기반으로 감정 분석을 수행하는 데이터 수집 및 분석 프로젝트입니다.

단순히 샘플 CSV를 분석하는 것이 아니라, `src/main.py`를 실행하면 실제 RSS 요청을 통해 뉴스 데이터를 수집하고 원본 CSV를 생성합니다.

---

## 2. 프로젝트 목표

- Google News RSS 기반 뉴스 기사 목록 수집
- 기사 링크 기반 본문 텍스트 수집 시도
- 뉴스 텍스트 전처리
- 사전 기반 감정 점수 계산
- 감정 분포 및 주요 키워드 분석
- 분석 결과 CSV 및 그래프 저장

---

## 3. 프로젝트 구조

```bash
news-rss-sentiment-crawler/
│
├── data/
│   ├── raw/                  # 크롤링으로 생성되는 원본 데이터
│   └── processed/            # 전처리 및 감정 분석 완료 데이터
│
├── output/
│   ├── tables/               # 분석 결과 CSV
│   └── figures/              # 분석 그래프 이미지
│
├── src/
│   ├── config.py             # 경로 및 기본 설정
│   ├── crawler.py            # RSS 수집 및 기사 본문 크롤링
│   ├── preprocess.py         # 텍스트 전처리
│   ├── sentiment.py          # 감정 점수 계산
│   ├── analyze.py            # 감정 분포 및 키워드 분석
│   ├── visualize.py          # 그래프 저장
│   └── main.py               # 전체 파이프라인 실행
│
├── notebook/
│   └── 01_news_analysis.ipynb # 분석 과정 기록용 노트북
│
├── docs/
│   └── portfolio_text.md     # 이력서/노션/면접용 설명 문구
│
├── requirements.txt
└── README.md
```

---

## 4. 실행 방법

### 1) 라이브러리 설치

```bash
pip install -r requirements.txt
```

### 2) 기본 실행

```bash
python src/main.py
```

### 3) 검색어와 수집 개수 지정

```bash
python src/main.py --query "인공지능" --limit 50
```

---

## 5. 데이터 수집 방식

본 프로젝트는 Google News RSS URL을 통해 뉴스 기사 목록을 수집합니다.

예시 RSS 구조:

```text
https://news.google.com/rss/search?q=인공지능&hl=ko&gl=KR&ceid=KR:ko
```

수집 항목은 다음과 같습니다.

- 검색 키워드
- 기사 제목
- 기사 링크
- 발행일
- 언론사
- RSS 요약문
- 기사 본문 후보 텍스트
- 수집 시각

기사 본문은 사이트별 HTML 구조와 접근 정책이 다르기 때문에, `article` 태그, `p` 태그, meta description 순서로 수집을 시도합니다. 본문 수집이 제한될 경우 RSS 제목과 요약문을 분석 텍스트로 활용합니다.

---

## 6. 감정 분석 방식

본 프로젝트는 외부 유료 API나 대형 모델을 사용하지 않고, 포트폴리오 학습 목적에 맞춰 간단한 사전 기반 감정 분석을 적용했습니다.

- 긍정 단어 출현: +1
- 부정 단어 출현: -1
- 최종 점수 기준으로 positive / neutral / negative 분류

향후 개선 시 한국어 감정 사전 또는 KoBERT 기반 감정 분류 모델을 적용할 수 있습니다.

---

## 7. 결과물

실행 후 다음 파일이 생성됩니다.

```bash
data/raw/news_articles_raw.csv
```

크롤링으로 수집한 원본 뉴스 데이터입니다.

```bash
data/processed/news_articles_sentiment.csv
```

전처리 및 감정 분석 결과가 포함된 데이터입니다.

```bash
output/tables/sentiment_summary.csv
output/tables/keyword_frequency.csv
```

감정 분포 및 주요 키워드 분석 결과입니다.

```bash
output/figures/sentiment_distribution.png
output/figures/top_keywords.png
```

분석 결과 시각화 이미지입니다.

---

## 8. 프로젝트 의의

본 프로젝트는 데이터 분석 이전 단계인 데이터 수집부터 전처리, 감정 분석, 결과 저장까지 이어지는 전체 흐름을 구현했다는 점에 의미가 있습니다.

특히 단순히 제공된 CSV를 분석하는 것이 아니라, 실제 RSS 요청을 통해 데이터를 수집하고 이를 분석 가능한 형태로 변환하는 파이프라인을 구성했습니다.

---

## 9. 한계 및 개선 방향

- 사이트별 HTML 구조 차이로 인해 본문 수집률이 달라질 수 있음
- 단순 사전 기반 감정 분석은 문맥과 반어 표현을 반영하기 어려움
- 향후 Selenium, newspaper3k, KoBERT 감정 분류 모델 적용 가능
- 수집 데이터의 날짜별 추세 분석 및 언론사별 비교 분석 확장 가능
