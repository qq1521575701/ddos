#介绍
- 发送一个包 ack模式
- 发送数据包需要宁外一个服务器接受包
- python3.8 send_packet.py src_ip src_port file_path


### 目录
    cd ddos/python_middle_box

### 安装
    apt install tcpdump -y

### 🎯 使用 iptables 拦截 RST
    sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP

### 抓包
    nohup tcpdump -nn 'tcp and dst port 25256 and len > 100' -q >> tcpdump.txt &

### 分析
    python3.8 main.py

### 📌 还原原状（测试完后一定要清除）：
    sudo iptables -D OUTPUT -p tcp --tcp-flags RST RST -j DROP
