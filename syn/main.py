import ipaddress
import random

# 定义多个IP段
networks = []

with open('cn_ip_part.txt','r',encoding='utf-8') as file:
    for i in file:
        networks.append(ipaddress.IPv4Network(i.strip()))

networks = random.sample(networks, 3000)


with open('cn_ip.txt','w',encoding='utf-8') as file:
    # 遍历每个网络段
    for network in networks:
        a = 0
        # 获取该网络段中的所有IP地址
        ips = list(network.hosts())

        for ip in ips:
            a += 1
            if a < 5000:
                # 将IP写入文件并打印
                file.write(f'{ip} {random.randint(20000,65535)}\n')
