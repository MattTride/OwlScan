import httpx
from bs4 import BeautifulSoup

url = "https://www.gzus.edu.cn/"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

# 使用 httpx 并开启 http2
try:
    with httpx.Client(headers=headers, http2=True, verify=False) as client:
        response = client.get(url, timeout=10.0)
        print(f"状态码: {response.status_code}")
        
        soup = BeautifulSoup(response.text, "html.parser")
        for a_tag in soup.find_all("a"):
            title = a_tag.get_text().strip()
            link = a_tag.get("href")
            if title and link:
                print(f"{title}: {link}")
except Exception as e:
    print(f"依然失败: {e}")
