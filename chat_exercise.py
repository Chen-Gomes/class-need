"""
聊天室机制思路（重点思想）

功能 ： 类似qq群功能
【1】 有人进入聊天室需要输入姓名，姓名不能重复

    *　客户端input姓名，服务端验证是否存在姓名，服务端有记录
【2】 有人进入聊天室时，其他人会收到通知：xxx 进入了聊天室

【3】 一个人发消息，其他人会收到：xxx ： xxxxxxxxxxx

    *　经过服务器转发客户端消息
【4】 有人退出聊天室，则其他人也会收到通知:xxx退出了聊天室

    * 随时发送随时接受（sendto,recvfrom）发送接收互不干扰

【5】 扩展功能：服务器可以向所有用户发送公告:管理员消息： xxxxxxxxx

# 服务器有多个客户端
# 服务器向所有客户端发送消息（公告）
# 架构先写服务端，功能先写客户端
# 写一个测一个
# 抓大放小
　执行流程架构
１.需求认知


２．基本的技术类型

    ×　网络传输 -->TCP（一个客户端断开，服务器用不了）  UDP(群聊)
    ×　服务端需要存储用户（存储什么信息，怎么存（用户名，地址）（数据结构：列表[(name,adderss),]   {name:adderss})
    ×　服务器要给所有人发消息（要知道所有人地址）
    ×　转发机制(发送接收互不干扰）（发送消息，接受消息各一个进程）
    ×　区分请求类型(固定模型思路）－－》定协议

３．功能模块划分（拆）
    一个功能一个函数

    函数封装

    ×　架构模型搭建
    ×　进入聊天室
    ×　聊天
    ×　退出聊天室

４．每一个功能具体实现逻辑

    ×　架构模型搭建
        客户端：创建udp套接字，准备给服务端发请求
        　　　　
        服务端：创建udp套接字，等待客户端请求
        （每个客户端发的请求不同，请求类型也不同）

    ×　进入聊天室
        客户端：
            输入姓名
            将姓名发送给服务端
            等待服务端反馈结果

        服务端：
            接收客户端姓名
            判断该用户是否存在
            将结果发送给客户端
            【如果不能进入聊天室(原因），结束】
            【能进入,(ok)，存储用户信息；告知他人】

    ×　聊天
        客户端：
            创建新进程
            父进程负责循环输入内容，发送消息
            子进程负责循环接收，打印
            
        服务端：
            接收消息
            转发给其他人

    ×　退出聊天室
        客户端：
            输入quit(或者直接ctrl+c)
            告知服务端
            进程退出
        服务端；
            接收消息
            将其从用户字典中删除
            告知其他人






５．通信协议(双方的约定）

    客户端请求类型：

        进入聊天室

            L　name (请求类型　　请求参量）


        聊天
        　　 C name msg

        退出聊天室

            Q ****

6.优化修改
    ×　注释添加
    ×　代码的重构
    ×　细节修改
"""
