import ipaddress
import random

# 读取所有 IP 段
with open('cn_ip_part.txt', 'r', encoding='utf-8') as file:
    networks = [ipaddress.IPv4Network(line.strip()) for line in file]

# 随机抽取 3000 个 IP 段
networks = random.sample(networks, 1000)

with open('cn_ack_ip.txt', 'w', encoding='utf-8') as file:
    for network in networks:
        count = 0
        for ip in network.hosts():
            file.write(f'{ip} {random.randint(20000, 65535)}\n')
            count += 1
            if count == 1000:
                break
