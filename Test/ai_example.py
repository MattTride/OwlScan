import requests
import argparse
import urllib3
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

# 初始化 colorama，让 Windows 终端也能显示颜色
init(autoreset=True)

# 忽略 SSL 证书警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_banner():
    banner = f"""
    {Fore.CYAN}==========================================
    {Fore.GREEN}   🚀 Web Asset Scanner v0.1
    {Fore.YELLOW}   导师制项目 - 实验性原型
    {Fore.CYAN}==========================================
    """
    print(banner)

def scan_target(url):
    # 简单的 URL 格式修补逻辑
    if not url.startswith("http"):
        url = "http://" + url
        
    try:
        # 模拟浏览器 User-Agent，防止部分简单反爬
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        
        # 获取基础信息
        status = response.status_code
        server = response.headers.get("Server", "Unknown")
        x_powered = response.headers.get("X-Powered-By", "Unknown")
        
        # 结果输出
        if status == 200:
            print(f"{Fore.GREEN}[+] Target: {url} is ALIVE (Status: {status})")
        else:
            print(f"{Fore.YELLOW}[!] Target: {url} returned Status: {status}")

        print(f"[*] Server: {Fore.BLUE}{server}")
        print(f"[*] Technology: {Fore.BLUE}{x_powered}")

        # 解析标题
        soup = BeautifulSoup(response.text, "html.parser")
        title_tag = soup.title
        title_text = title_tag.string.strip() if title_tag else "No Title Found"
        print(f"[*] Page Title: {Fore.MAGENTA}{title_text}")

    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}[-][Error] 无法连接到目标: {url}")
    except requests.exceptions.Timeout:
        print(f"{Fore.RED}[-][Error] 请求超时")
    except Exception as e:
        print(f"{Fore.RED}[-][Error] 发生未知错误: {e}")

if __name__ == "__main__":
    get_banner()
    
    # 1. 创建解析器对象
    parser = argparse.ArgumentParser(description="这是一个用于 Web 资产信息收集的轻量级工具。")
    
    # 2. 添加参数
    # -u 是简写，--url 是全名，required=True 表示必须输入
    parser.add_argument("-u", "--url", required=True, help="指定扫描目标的 URL (例如: www.baidu.com)")
    
    # 3. 解析参数
    args = parser.parse_args()
    
    # 4. 执行核心逻辑
    scan_target(args.url)