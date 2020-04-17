"""
服务端
"""
from socket import *
import os,sys

# 服务地址
ADDR = ('0.0.0.0',8888)

# 存储用户  {name:[address,num]}
user = {}

# 敏感词
words = ['蔡旭困','xx','qq','oo']

# 黑名单
ips = []

def warn(name,text):
    for word in words:
        if word in text:
            user[name][1] += 1
            return False
    return True

# 进入处理
def do_login(s,name,addr):
    if name in user or '管理' in name or addr[0] in ips:
        s.sendto(b'FAIL',addr)
        return
    s.sendto(b'OK',addr)

    # 通知其他人
    msg = "\n欢迎%s进入聊天室"%name
    for i in user:
        s.sendto(msg.encode(),user[i][0])
    # 将其添加到用户字典
    user[name] = [addr,0]

# 聊天
def do_chat(s,name,text):
    if not warn(name,text):
        if user[name][1] >= 3:
            msg = "\n%s 被踢出群聊" %name
            ips.append(user[name][0][0]) # IP拉黑
            for i in user:
                # 刨除本人
                if i != name:
                    s.sendto(msg.encode(), user[i][0])
                else:
                    s.sendto(b'EXIT', user[name][0])
            del user[name]
        else:
            msg = "\n警告 %s 请你善良"%name
            s.sendto(msg.encode(), user[name][0])
    else:
        msg = "\n%s : %s"%(name,text)
        for i in user:
            # 刨除本人
            if i != name:
                s.sendto(msg.encode(),user[i][0])

#退出
def do_quit(s,name):
    msg = "\n%s退出群聊"%name
    for i in user:
        if i != name:
            # 告知其他人
            s.sendto(msg.encode(),user[i][0])
        else:
            # 让他本人的接收进程退出
            s.sendto(b'EXIT',user[i][0])
    del user[name]

# 功能分发函数
def do_request(s):
    while True:
        # 循环接受请求
        data,addr = s.recvfrom(1024)
        tmp = data.decode().split(' ',2)
        # 根据请求类型，选择功能模块去处理
        # L   C   Q
        if tmp[0] == 'L':
            do_login(s,tmp[1],addr) # 具体函数处理具体功能
        elif tmp[0] == 'C':
            do_chat(s,tmp[1],tmp[2])
        elif tmp[0] == 'Q':
            do_quit(s,tmp[1])

# 启动函数
def main():
    # udp网络服务
    s = socket(AF_INET,SOCK_DGRAM)
    s.bind(ADDR)

    pid = os.fork()
    if pid < 0:
        return
    elif pid == 0:
        # 管理员消息的发送
        while True:
            text = input("管理员消息:")
            msg = "C 管理员 "+text
            # 将消息从子进程发送给父进程
            s.sendto(msg.encode(),ADDR)
    else:
        do_request(s) # 父进程处理请求


if __name__ == '__main__':
    main()


