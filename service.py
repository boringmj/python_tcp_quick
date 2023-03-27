import socket
from tcp_quick.service import Service

import threading

class OpenService(Service):
    """开放服务端"""

    def _handle(self,sock:socket.socket,ip:str,port:int)->None:
        # 请自行验证链接的客户端是否合法,请自行处理链接超时等问题
        # 向客户端发送 “Hello”
        sock.send('Hello'.encode())
        # 接收客户端数据
        data=sock.recv(1024)
        print('[RECV] '+data.decode())
        # 关闭链接
        sock.close()

service=OpenService('0.0.0.0',9999,1).close()

def end_service():
    """结束服务端"""
    global service
    user_input=input('')
    if user_input=='exit' or user_input=='quit':
        service.close()

# 开启一个多线程,用于结束服务端
threading.Thread(target=end_service).start()