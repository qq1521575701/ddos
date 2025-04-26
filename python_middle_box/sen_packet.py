from scapy.all import IP, TCP
import socket
import ipaddress


with open('cn_ip_part.txt', 'r', encoding='utf-8') as file:
    networks = [ipaddress.IPv4Network(line.strip()) for line in file]

src_ip = '38.180.188.158'
src_port = 25256
s = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_RAW)

pkt_HTTP = IP(src=src_ip) / TCP(sport=src_port, flags='A',seq=2000,ack=3000) / 'GET / HTTP/1.1\r\nHost: freedomhouse.org\r\n\r\n'

for network in networks:
    for ip in network.hosts():

        ip = str(ip)

        pkt_HTTP[TCP].dport = 80
        pkt_HTTP[IP].dst = ip
        
        s.sendto(bytes(pkt_HTTP),(ip,80))
