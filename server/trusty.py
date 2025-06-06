# build_trust_domains.py
import re, csv, requests, tldextract
from bs4 import BeautifulSoup
from collections import OrderedDict

SRC_URL = "https://www.htmlstrip.com/alexa-top-1000-most-visited-websites"

# ─────────────────────────────────────────────── #
# 1) 원본 HTML 가져오기
html = requests.get(SRC_URL, headers={"User-Agent": "Mozilla/5.0"}).text
soup = BeautifulSoup(html, "html.parser")

# ─────────────────────────────────────────────── #
# 2) 페이지 전체에서 '도메인' 토큰 추출
raw_text = soup.get_text(" ", strip=True)
candidates = re.findall(r"[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", raw_text)

# 3) 순서를 유지하며 중복 제거
unique_domains = list(OrderedDict.fromkeys(candidates))[:1000]

# ─────────────────────────────────────────────── #
# 4) 아주 단순한 휴리스틱 신뢰도 계산
def trust_score(domain: str) -> float:
    ext = tldextract.extract(domain)
    tld = ext.suffix.lower()

    if tld == "gov":      return 0.95        # 정부
    if tld == "edu":      return 0.90        # 교육/연구
    if domain.endswith((".org", ".int")): return 0.85  # 국제기구·비영리
    if tld in {"com", "co"}:
        # 대형 플랫폼이면 가산, 불명/스팸 패턴이면 감산
        big_brands = {"google", "youtube", "amazon", "facebook",
                      "baidu", "wikipedia", "twitter", "instagram",
                      "bbc", "nytimes", "reuters"}
        base = 0.75
        if ext.domain.lower() in big_brands:
            base += 0.1
        return min(base, 0.9)
    # 그 외는 보수적으로
    return 0.6

# 5) CSV 저장
with open("trust_domains_1000.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["domain", "score"])
    for d in unique_domains:
        writer.writerow([d, round(trust_score(d), 2)])

print("✅ trust_domains_1000.csv 저장 완료 (도메인 수:", len(unique_domains), ")")
