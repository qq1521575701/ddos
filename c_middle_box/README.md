### 目录
    cd ddos/c_middle_box

### Attack
    gcc tcp.c -o tcp -pthread && ./tcp ip port packet.txt 2 20

- packet.txt 初始目录 约4000mbp/s

- 反射文件 为 ip:port


### 扫描
        gcc tcpscan.c -o tcpscan && ./tcpscan src_ip src_port packet.txt



### 用 tc 设置出口限速 10Mbps
        sudo tc qdisc add dev ens160 root tbf rate 10mbit burst 32kbit latency 400ms

### 如果之前设置过 tc，需要先清除：
        sudo tc qdisc del dev ens160 root


### 宁外一台服务器抓包
        tcpdump -t -nn tcp src port 80 and dst port 8000 and 'tcp[((tcp[12:1] & 0xf0) >> 2):4] != 0' -q
