# 一个多线程socket程序
import socket,threading,re
from abc import ABC,abstractmethod

class Service(ABC):
    """
    快速TCP服务端抽象类
    请注意需要重写 `_handle(self,sock:socket.socket,ip:str,port:int)->None` 方法

    @param ip: 监听的ip
    @param port: 监听的端口
    @param backlog: 最大连接数
    """

    def __init__(self,ip:str='0.0.0.0',port:int=10901,backlog:int=5)->None:
        """
        @param ip: 监听的ip
        @param port: 监听的端口
        @param backlog: 最大连接数
        """
        # 严格校验ip地址,每位数字0-255
        if not re.match(r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$',ip):
            raise Exception('ip地址不合法')
        # 校验端口号
        if port<1 or port>65535:
            raise Exception('端口号不合法')
        self._listen_ip=ip
        self._listen_port=port
        self._backlog=backlog
        self._open()

    def _open(self)->None:
        """打开socket"""
        self._sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._sock.bind((self._listen_ip,self._listen_port))
        self._sock.listen(self._backlog)
        # 开启监听线程
        self._clients=[]
        for i in range(self._backlog):
            t=threading.Thread(target=self._listen,args=(i,))
            t.start()
            self._clients.append(t)

    def _listen(self,id:int)->None:
        """监听线程"""
        while True:
            print('[LISTEN] 监听线程'+str(id)+'开始监听')
            try:
                sock,addr=self._sock.accept()
                print('[LISTEN] 监听线程'+str(id)+'接收到客户端连接: '+addr[0]+':'+str(addr[1]))
                self._handle(sock,addr[0],addr[1])
            except Exception as e:
                print('[LISTEN] 监听线程'+str(id)+'异常: '+str(e))

    def close(self)->None:
        """关闭socket"""
        self._sock.close()
        for client in self._clients:
            client.join()
        del self

    # 开启服务端
    @abstractmethod
    def _handle(self,sock:socket.socket,ip:str,port:int)->None:
        pass