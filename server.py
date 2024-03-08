import socket
from tcp_quick.server import Server

import threading

class OpenServer(Server):
    """开放服务端"""

    def _handle(self,sock:socket.socket,ip:str,port:int)->None:
        # 请自行验证连接的客户端是否合法,请自行处理连接超时等问题
        # 向客户端发送 “Hello”
        sock.send('Hello'.encode())
        # 接收客户端数据
        data=sock.recv(1024)
        print('[RECV] '+data.decode())
        # 关闭连接
        sock.close()

server=OpenServer('0.0.0.0',9999,1)

def end_server():
    """结束服务端"""
    global server
    user_input=input('')
    if user_input=='exit' or user_input=='quit':
        server.close()

# 开启一个多线程,用于结束服务端
threading.Thread(target=end_server).start()