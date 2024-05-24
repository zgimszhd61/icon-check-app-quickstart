import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_favicon_url(url):
    # 发送HTTP请求获取网页内容
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch {url}")
    
    # 解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 查找<link>标签中的favicon URL
    icon_link = soup.find('link', rel=lambda rel: rel and 'icon' in rel.lower())
    if icon_link:
        favicon_url = icon_link.get('href')
        # 处理相对URL
        favicon_url = urljoin(url, favicon_url)
        return favicon_url
    else:
        raise Exception(f"No favicon found for {url}")

def download_favicon(favicon_url, save_path):
    # 发送HTTP请求下载favicon
    response = requests.get(favicon_url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Favicon downloaded and saved to {save_path}")
    else:
        raise Exception(f"Failed to download favicon from {favicon_url}")

# 示例用法
website_url = 'https://www.python.org'
try:
    favicon_url = get_favicon_url(website_url)
    print(f"Favicon URL: {favicon_url}")
    download_favicon(favicon_url, 'python_favicon.ico')
except Exception as e:
    print(e)
