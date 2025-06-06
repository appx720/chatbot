# check.py

from sentence_transformers import SentenceTransformer, util
from newspaper import Article
from urllib.parse import urlparse
import re
import csv

# 의미 유사도 모델 로딩
model = SentenceTransformer('all-MiniLM-L6-v2')

trusted_domains = {}
with open("domains.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        domain = row['domain'].strip()
        score = float(row['score'])
        trusted_domains[domain] = score


def get_article_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except:
        return ""

def domain_score(domain):
    for trusted, score in trusted_domains.items():
        if domain.endswith(trusted):
            return score
    return 0.4  # unknown domains get low trust

def fact_check(text: str, reference_urls: list):
    results = []

    for url in reference_urls:
        domain = urlparse(url).netloc
        source_text = get_article_text(url)

        if not source_text or len(source_text) < 200:
            results.append({
                "url": url,
                "domain": domain,
                "status": "No content",
                "similarity": 0.0,
                "trust_score": domain_score(domain) * 100
            })
            continue

        # 의미 유사도 계산
        score = util.cos_sim(model.encode(text, convert_to_tensor=True),
                             model.encode(source_text, convert_to_tensor=True)).item()

        results.append({
            "url": url,
            "domain": domain,
            "status": "Cited" if score > 0.6 else "Not cited",
            "similarity": round(score, 3),
            "trust_score": round(domain_score(domain) * 100 * score, 2)
        })

    return results
