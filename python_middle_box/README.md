### 目录
    ddos/python_middle_box

### 安装
    apt install tcpdump -y

### 🎯 使用 iptables 拦截 RST
    sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP

### 📌 还原原状（测试完后一定要清除）：
    sudo iptables -D OUTPUT -p tcp --tcp-flags RST RST -j DROP

### 抓包
    nohup tcpdump -nn 'tcp and dst port 25256 and len > 100' -q >> tcpdump.txt &

### 分析
    python3.8 main.py
