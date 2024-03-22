#为了满足您的要求，我对 get_location 函数进行了修改，以便在第一次尝试获取IP地址的国家代码失败时，使用备用的API进行第二次尝试。以下是更新后的代码：

import requests
import socket

def get_ips_from_url(url):
try:
response = requests.get(url)
if response.status_code == 200:
return response.text.splitlines()
else:
print(f"Failed to fetch IPs from {url}. Status code: {response.status_code}")
except Exception as e:
print(f"Error fetching IPs from {url}: {e}")
return []

def get_location(ip):
try:
response = requests.get(f"http://ip-api.com/json/{ip}")
data = response.json()
if data['status'] == 'success':
return data['countryCode']
else:
# 第二次尝试使用备用API
response = requests.get(f"https://ipleak.net/json/{ip}")
data = response.json()
return data['country']
except Exception as e:
print(f"Error fetching location for IP {ip}: {e}")
return None

def scan_ports(ip):
open_ports = []
for port in [8443, 2053, 2083, 2087]:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1)
result = s.connect_ex((ip, port))
if result == 0:
open_ports.append(port)
break
if not open_ports:
open_ports.append(443)
return open_ports

def convert_ips(input_urls, output_files):
for input_url, output_file in zip(input_urls, output_files):
ips = get_ips_from_url(input_url)  # 获取URL中的IP地址列表

with open(output_file, 'w') as f:
for line in ips:
ip = line.split()[0]  # 提取行中的第一个单词作为IP地址
try:
socket.inet_aton(ip)  # 检查IP地址格式是否正确
except socket.error:
f.write(f"{line}\n")  # IP地址格式不正确，直接保存原文
continue

open_ports = scan_ports(ip)
location = get_location(ip)
if location:
f.write(f"{ip}:{open_ports[0]}#{location}\n")
else:
f.write(f"{ip}:443#火星star\n")

if __name__ == "__main__":
input_urls = ["https://ipdb.api.030101.xyz/?type=bestproxy", "https://ipdb.api.030101.xyz/?type=bestcf", 'https://raw.githubusercontent.com/China-xb/zidonghuaip/main/ip.txt', 'https://addressesapi.090227.xyz/CloudFlareYes' , 'https://kzip.pages.dev/a.csv?token=mimausb8']  # 包含IP地址的txt文件的多个URL
output_files = ["bestproxy.txt", "bestcf.txt", 'ip.txt', 'cfip.txt', 'kzip.txt']
convert_ips(input_urls, output_files)

#请注意，我假设 https://ipleak.net/json/{ip} API返回的JSON响应中包含一个名为 country 的字段，其中包含国家代码。如果该API的响应结构不同，请根据实际情况调整代码。如果您需要进一步的帮助，请告诉我！
