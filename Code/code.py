import requests
import argparse
import urllib3
from bs4 import BeautifulSoup

# 忽略 SSL 证书警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_banner():
    print("-" * 40)
    print("   🌐 Web 资产探测工具 v0.1")
    print("-" * 40)

def scan_target(url):
    try:

        response = requests.get(url, verify=False, timeout=10)
        stat = response.status_code
        
        # 修复了 Server 的拼写
        # requests 的 headers 是大小写不敏感的，所以写 Server 即可
        server = response.headers.get("Server", "未知")
        x_powered = response.headers.get("X-Powered-By", "未知")

        if stat == 200:
            print(f"[+] 目标 {url} 存活 (状态码: {stat})")
        else:
            print(f"[-] 目标服务异常或有反爬 (状态码: {stat})")

        print(f"[*] 服务器类型: {server}")
        print(f"[*] 后端类型: {x_powered}")

        # 提取标题
        soup = BeautifulSoup(response.text, "html.parser")
        titles = soup.find_all("h1")
        if titles:
            print("\n[*] 发现的 h1 标题:")
            for t in titles:
                print(f"    - {t.get_text(strip=True)}")

    except requests.exceptions.SSLError:
        print("[!] SSL 证书验证失败，请检查网络代理或证书设置。")
    except requests.exceptions.RequestException as e:
        print(f"[!] 请求发生错误: 目标无法访问或超时。详细信息: {e}")

if __name__ == "__main__":
    get_banner()
   
    parser = argparse.ArgumentParser(description="轻量级 Web 资产扫描器")
    parser.add_argument("-u", "--url", 
                        default="https://www.youtube.com/",   
                        help="输入要扫描的目标 URL")
   
    args = parser.parse_args()
    scan_target(args.url)