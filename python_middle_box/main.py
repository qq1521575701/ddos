from collections import defaultdict

stats = defaultdict(lambda: {"count": 0, "total": 0, "sizes": []})

with open('tcpdump.txt', 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) < 7:
            continue
        try:
            src_ip_port = parts[2]  # 例如：1.14.52.65.80
            size = int(parts[-1])   # 最后一列是大小
            stats[src_ip_port]["count"] += 1
            stats[src_ip_port]["total"] += size
            stats[src_ip_port]["sizes"].append(size)
        except Exception as e:
            print("错误：", e)

# 排序按总大小从大到小
sorted_stats = sorted(stats.items(), key=lambda item: item[1]["total"], reverse=True)

# 写入结果
with open('result.txt', 'w', encoding='utf-8') as f:
    f.write("ip:port\t次数\t大小\t平均大小\t最大包\t最小包\n")
    for ip_port, data in sorted_stats:
        parts = ip_port.split('.')
        ip = '.'.join(parts[:4])
        port = parts[4]
        count = data["count"]
        total = data["total"]
        avg = total // count if count else 0
        max_size = max(data["sizes"]) if data["sizes"] else 0
        min_size = min(data["sizes"]) if data["sizes"] else 0
        f.write(f"{ip}:{port}\t{count}\t{total}\t{avg}\t{max_size}\t{min_size}\n")

print("结果已保存为带统计信息的表格格式到 result.txt")
