# import re
# import requests
# import json

# # 替换为你的 Google Scholar ID
# SCHOLAR_ID = "kO35itkAAAAJ"

# url = f"https://scholar.google.com/citations?user={SCHOLAR_ID}&hl=en&view_op=list_works&sortby=pubdate"
# html = requests.get(url).text

# match = re.search(r'Citations</a></td><td class="gsc_rsb_std">(\d+)', html)
# citations = match.group(1) if match else "N/A"

# # 生成 shields.io 需要的 JSON 格式
# badge = {
#     "schemaVersion": 1,
#     "label": "Citations",
#     "message": str(citations),
#     "color": "blue"
# }

# with open("citations.json", "w", encoding="utf-8") as f:
#     json.dump(badge, f)

# print(f"Updated badge with citations: {citations}")


import re, json, requests, os
from bs4 import BeautifulSoup

SCHOLAR_ID = "kO35itkAAAAJ"

URL = f"https://scholar.google.com/citations?user={SCHOLAR_ID}&hl=en&view_op=list_works&sortby=pubdate"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def read_old_message():
    if os.path.exists("citations.json"):
        try:
            with open("citations.json", "r", encoding="utf-8") as f:
                return json.load(f).get("message", "0")
        except Exception:
            return "0"
    return "0"

def parse_citations(html: str) -> str:
    # 被验证码拦了
    if "gs_captcha_c" in html:
        return "N/A"
    soup = BeautifulSoup(html, "html.parser")
    # Scholar 右侧统计表 id="gsc_rsb_st" 第一列是指标名，第二列是“全部(ALL)”数字
    table = soup.find(id="gsc_rsb_st")
    if table:
        tds = table.select("td.gsc_rsb_std")
        if tds:
            # 第一个数字一般就是“Citations（All）”
            num = re.sub(r"[^\d]", "", tds[0].get_text(strip=True))
            if num.isdigit():
                return num
    # 正则兜底（避免语言变体）
    m = re.search(r'id="gsc_rsb_st".*?<td class="gsc_rsb_std">\s*([\d,]+)\s*<', html, flags=re.S)
    if m:
        num = re.sub(r"[^\d]", "", m.group(1))
        if num.isdigit():
            return num
    return "N/A"

def main():
    old = read_old_message()
    try:
        r = requests.get(URL, headers=HEADERS, timeout=20)
        r.raise_for_status()
        citations = parse_citations(r.text)
    except Exception:
        citations = "N/A"

    # 若抓取失败（N/A），保留旧值，避免把 badge 变成 0/N/A
    message = citations if citations.isdigit() else old

    badge = {"schemaVersion": 1, "label": "Citations", "message": str(message), "color": "blue"}
    with open("citations.json", "w", encoding="utf-8") as f:
        json.dump(badge, f)
    print("Updated:", badge)

if __name__ == "__main__":
    main()
