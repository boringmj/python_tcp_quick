import socket,re,threading
from abc import ABC,abstractmethod

class Client(ABC):
    """
    快速TCP客户端抽象类
    请注意需要重写 `_handle(self)->None` 方法
    
    @param ip: 客户端ip
    @param port: 客户端端口
    """

    def __init__(self,ip:str='127.0.0.1',port:int=10901)->None:
        """
        @param ip: 客户端ip
        @param port: 客户端端口
        """
        # 严格校验ip地址,每位数字0-255
        if not re.match(r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$',ip):
            raise Exception('ip地址不合法')
        # 校验端口号
        if port<1 or port>65535:
            raise Exception('端口号不合法')
        self._ip=ip
        self._port=port
        self._link()

    def _link(self)->None:
        """连接服务端"""
        self._sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._sock.connect((self._ip,self._port))
        self._handle()

    def send(self,data:bytes)->None:
        """发送数据"""
        self._sock.send(data)

    def recv(self,size:int)->bytes:
        """接收数据"""
        return self._sock.recv(size)

    def close(self)->None:
        """关闭socket"""
        self._sock.close()
        del self
    
    @abstractmethod
    def _handle(self)->None:
        """处理数据"""
        pass