import socket
from tcp_quick.client import Client

class OpenClient(Client):
    """打开客户端"""

    def _handle(self,sock:socket.socket)->None:
        """处理数据"""
        # 请自行验证链接的服务端是否合法,请自行处理链接超时等问题
        # 接收服务端数据
        data=self.recv(1024)
        print('[RECV] '+data.decode())
        # 向服务端发送 “World”
        self.send('World'.encode())
        # 关闭链接
        self.close()

client=OpenClient('127.0.0.1',9999)