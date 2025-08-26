import re
import requests
import json

# 替换为你的 Google Scholar ID
SCHOLAR_ID = "kO35itkAAAAJ"

url = f"https://scholar.google.com/citations?user={SCHOLAR_ID}&hl=en&view_op=list_works&sortby=pubdate"
html = requests.get(url).text

match = re.search(r'Citations</a></td><td class="gsc_rsb_std">(\d+)', html)
citations = match.group(1) if match else "N/A"

# 生成 shields.io 需要的 JSON 格式
badge = {
    "schemaVersion": 1,
    "label": "Citations",
    "message": str(citations),
    "color": "blue"
}

with open("citations.json", "w", encoding="utf-8") as f:
    json.dump(badge, f)

print(f"Updated badge with citations: {citations}")
