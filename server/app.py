from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urlparse
# import re
# from datetime import datetime
# import textblob


from .check import fact_check

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sending = False
received_urls = []

class VisitLog(BaseModel):
    url: str

@app.get("/send")
def get_flag():
    return {"send": sending}

@app.post("/trigger_send")
def trigger():
    global sending
    sending = True
    return {"status": "will_send"}

@app.post("/log")
def receive_logs(logs: List[VisitLog]):
    print(f"✅ 받은 방문기록 {len(logs)}개")

    for log in logs:
        received_urls.append(log.url)
        print(f"저장된 URL: {log.url}")

    print(fact_check("핵융합은 고온 플라즈마 상태에서 핵자 간의 융합 반응을 통해 에너지를 생성하는 물리 현상으로, 높은 에너지 밀도와 자원 지속 가능성으로 인해 차세대 에너지 기술로 주목받고 있다.", received_urls))

    return {"status": "received", "count": len(logs)}

@app.post("/done")
def clear_flag():
    global sending
    sending = False
    return {"status": "cleared"}


# # 신뢰도 분석 함수들

# emotion_words = ["충격", "끔찍", "분노", "경악", "대참사", "충격적", "경이로움", "소름", "악마", "믿을 수 없는"]
# subjective_phrases = ["나는 생각한다", "내가 보기엔", "분명히", "확실히", "믿는다", "아마도"]

# def fetch_html(url):
#     try:
#         res = requests.get(url, timeout=5)
#         return res.text
#     except Exception as e:
#         print(f"❌ URL fetch 실패: {e}")
#         return ""

# def extract_text(html):
#     soup = BeautifulSoup(html, "html.parser")
#     for s in soup(["script", "style"]):
#         s.extract()
#     return soup.get_text(separator=" ")

# def count_emotional_words(text):
#     return sum(text.count(word) for word in emotion_words)

# def count_subjective_phrases(text):
#     return sum(text.count(phrase) for phrase in subjective_phrases)

# def extract_dates(text):
#     matches = re.findall(r"(19|20)\d{2}", text)
#     years = [int(y) for y in matches if int(y) < datetime.now().year + 1]
#     return max(years) if years else None

# def count_external_links(html, current_url):
#     soup = BeautifulSoup(html, "html.parser")
#     base_domain = urlparse(current_url).netloc
#     external_links = []
#     for tag in soup.find_all("a", href=True):
#         href = tag['href']
#         parsed = urlparse(href)
#         if parsed.netloc and parsed.netloc != base_domain:
#             external_links.append(href)
#     return len(external_links)

# def assess_url_trust(url):
#     html = fetch_html(url)
#     if not html:
#         return {"url": url, "trust_score": 0, "grade": "F", "reason": "URL 접속 실패"}

#     text = extract_text(html)
#     if not text or len(text) < 300:
#         return {"url": url, "trust_score": 20, "grade": "D", "reason": "내용 부족"}

#     # 1. 감정적 언어
#     emotion_score = max(0, 20 - count_emotional_words(text) * 2)

#     # 2. 주관성
#     subjectivity_score = max(0, 20 - count_subjective_phrases(text) * 2)

#     # 3. 최신성
#     latest_year = extract_dates(text)
#     now_year = datetime.now().year
#     if latest_year:
#         delta = now_year - latest_year
#         date_score = max(0, 20 - delta * 5)
#     else:
#         date_score = 10

#     # 4. 외부 링크 수
#     link_score = min(20, count_external_links(html, url) * 5)

#     # 5. 정보성 판단
#     blob = textblob.TextBlob(text)
#     fact_sentences = [s for s in blob.sentences if any(char.isdigit() for char in s)]
#     fact_score = min(20, len(fact_sentences) * 2)

#     total = emotion_score + subjectivity_score + date_score + link_score + fact_score
#     grade = "A" if total >= 85 else "B" if total >= 70 else "C" if total >= 55 else "D" if total >= 40 else "F"

#     return {
#         "url": url,
#         "trust_score": total,
#         "grade": grade,
#         "details": {
#             "emotion_score": emotion_score,
#             "subjectivity_score": subjectivity_score,
#             "date_score": date_score,
#             "link_score": link_score,
#             "fact_score": fact_score
#         }
#     }

