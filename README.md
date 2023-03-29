# python_tcp_quick

## 我该如何开始?
1. 请先将本项目克隆至您的本地
```
git clone https://github.com/boringmj/python_tcp_quick.git
```
2. 使用您的编辑器打开本项目(建议直接打开目录, 方便查看与修改)
3. 请确保打开项目后, 您的目录是如下结构
```
python_tcp_quick 项目目录
│─ .gitignore gitignore文件, 可删除
│─ client.py 客户端示例, 可删除
│─ LICENSE 开源许可证,请尽量保留在项目目录中
│─ README.md 项目说明文件, 可删除
│─ service.py 服务端示例, 可删除
│
└─tcp_quick tcp_quick的核心包
      │─ client.py 客户端模块
      └─ service.py 服务端模块
```
4. 在正式开始之前, 您可能需要了解以下几个知识点(所有知识点均来源于CSDN, 如有侵权请联系仓库创建者删除)\
    [python中的“类”](https://blog.csdn.net/zhangke0426/article/details/122528384)\
    [谈谈Python的抽象类](https://blog.csdn.net/gongdiwudu/article/details/126575358)\
    如果您不太想了解, 那么您也可以选择直接开始
5. 创建一个或修改已有的服务端类\
    这里是一个创建的示例(您可以参考 [service.py](https://github.com/boringmj/python_tcp_quick/blob/master/service.py) 以便更快理解如何自定义并使用 `tcp_quick` ), 您需要先引入socket模块和服务端模块
    ```
    import socket
    from tcp_quick.service import Service
    ```
    然后你需要定义一个服务端类(示例中定义的是 `OpenService` ), 该类必须继承于抽象类 `Service`
    ```
    class OpenService(Service):
        """开放服务端"""
    ```
    再然后你需要实现 `Service` 抽象类的 `_handle(self,sock:socket.socket,ip:str,port:int)->None` 方法\
    例如我们先向客户端发送一个 `Hello`, 然后接收客户端的回复并打印, 然后断开连接(所有的方法都可以参考 `socket.scoket` )
    ```
    def _handle(self,sock:socket.socket,ip:str,port:int)->None:
        # 请自行验证连接的客户端是否合法, 请自行处理连接超时等问题
        # 向客户端发送 “Hello”
        sock.send('Hello'.encode())
        # 接收客户端数据
        data=sock.recv(1024)
        print('[RECV] '+data.decode())
        # 关闭连接
        sock.close()
    ```
    请注意, `sock.close()` 仅仅是关闭本次连接, 本次连接关闭后该线程就会闲置, 直到下一个连接分配到这个线程
    最后只需要实例化新建的这个类(示例中定义的是 `OpenService` )即可
    ```
    # 实例化并开启服务端
    OpenService('0.0.0.0',9999,1)
    ```
    实例化是最多可以传入三个参数, 实例化时的所有参数均可缺省\
    第一个参数为监听的IP `str` , 默认为 ` str 0.0.0.0` ,表示监听所有IP\
    第二个参数为监听的端口 `int` , 默认为 `int 10901`\
    第三个参数为最大连接线程数 `int` , 默认为 `int 5`, 线程数决定了最大并发数,\
    每个线程数最多同时处理一个连接请求, 只有当上一个连接断开后, 这个线程才可以接入新的请求
    ```
    # 参数
    @param ip: 监听的ip
    @param port: 监听的端口
    @param backlog: 最大连接数
    
    # 最简示例(监听所有IP的10901端口, 最大连接5个线程)
    OpenService()
    ```
    如果您的业务需要, 您可以自定义一个方法来结束服务端的运行\
    服务端结束运行需要等待线程自动关闭后才可以, 如无特殊情况线程会自动抛出套接字错误而停止运行\
    你也可以强制退出文件关闭服务端, 但这样 `socket` 并不一定会被释放, 所以在结束运行前请确保执行过一次服务端类(示例中定义的是 `OpenService` )的 `close()` 方法释放套接字对象
    ```
    # 实例化并开启服务端
    service=OpenService('0.0.0.0',9999,1)
    # 关闭服务端(套接字对象会被释放)并释放服务端类(线程不会强制退出, 如无特殊情况线程会因为抛出异常而停止运行)
    service.close()
    ```
6. 创建一个或修改已有的客户端类
    这里依旧是一个创建示例, 您依旧可以参考已有的 [client.py](https://github.com/boringmj/python_tcp_quick/blob/master/client.py) 快速上手\
    同样, 您需要先引入socket模块和客户端模块
    ```
    import socket
    from tcp_quick.client import Client
    ```
    然后定义一个客户端类并继承抽象类 `Client`
    ```
    class OpenClient(Client):
        """打开客户端"""
    ```
    依旧需要您实现一个 `_handle(self,sock:socket.socket)->None:` 方法, 请注意传入的参数与之前有所不同!
    ```
    def _handle(self,sock:socket.socket)->None:
        """处理数据"""
        # 请自行验证连接接的服务端是否合法, 请自行处理连接接超时等问题
        # 接收服务端数据
        data=self.recv(1024)
        print('[RECV] '+data.decode())
        # 向服务端发送 “World”
        self.send('World'.encode())
        # 关闭连接接
        self.close()
    ```
    不同于服务端的是, 客户端支持 `self.send(self,data:bytes)->None:` 和 `self.recv(self,size:int)->bytes:` 方法来发送和接收数据, 虽然您依旧可以使用 `socket.socket` 来处理这些\
    最后您只需根据服务端类的参数实例化客户端类即可, 请注意 `127.0.0.1` 是一个本地回环, 表示本机地址, `9999` 端口与上面服务器监听的端口相同
    ```
    # 实例化并连接服务端
    OpenClient('127.0.0.1',9999)
    ```
    示例中实例化时传入了两个参数, 这两个参数同样可以缺省\
    第一个参数是服务端的IP地址 `str` , 默认是 `str 127.0.0.1`, 请注意这里填的不是服务端监听的地址, 而是服务端的地址\
    第二个参数是服务器监听的端口 `int` , 默认是 `int 10901`
    ```
    # 参数
    @param ip: 服务端ip
    @param port: 服务端端口
    
    # 最简示例(连接本机监听的10901端口)
    OpenClient()
    ```
    不同于服务端的是, 客户端是单线程运行, 所以 `self.close()` 与 `sock.close()` 并无本质上的区别, 他们都会结束本次 `socket` 会话, 而且您应该在执行结束前断开并释放socket连接
  7. 做好网络安全防护, 严格鉴权客户端连接, 遵守开发规范与开源协议, 做一个优秀的开源社区贡献者
