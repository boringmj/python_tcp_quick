from tcp_quick.client import Client

import threading

class OpenClient(Client):
    """打开客户端"""

    def _handle(self)->None:
        """处理数据"""
        while True:
            # 接收服务端数据
            data=self.recv(1024)
            if data:
                print('[RECV] '+data.decode())
                # 向服务端发送 “World”
                self.send('World'.encode())
            else:
                break
        self.close()

# 循环10个客户端连接
for i in range(10):
    t=threading.Thread(target=OpenClient)
    t.start()