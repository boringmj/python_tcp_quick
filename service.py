import socket
from tcp_quick.service import Service

import time

class OpenService(Service):
    """开放服务端"""

    def _handle(self,sock:socket.socket,ip:str,port:int)->None:
        print('[HANDLE] 客户端连接: '+ip+':'+str(port))
        # 向客户端发送 “Hello”
        sock.send('Hello'.encode())
        # 接收客户端数据
        data=sock.recv(1024)
        if data:
            print(data.decode())
        # 关闭客户端连接
        time.sleep(10)
        sock.close()
        print('[HANDLE] 结束客户端连接: '+ip+':'+str(port))

service=OpenService()