from channels.generic.websocket import WebsocketConsumer
from medivh.kube import KubeApi
from threading import Thread


class K8SStreamThread(Thread):
    def __init__(self, websocket, container_stream):
        Thread.__init__(self)
        self.websocket = websocket
        self.stream = container_stream

    def run(self):
        while self.stream.is_open():
            if self.stream.peek_stdout():
                stdout = self.stream.read_stdout()
                self.websocket.send(stdout)
            if self.stream.peek_stderr():
                stderr = self.stream.read_stderr()
                self.websocket.send(stderr)
        else:
            self.websocket.close()


class K8SWatchStreamThread(Thread):
    def __init__(self, websocket, container_stream):
        Thread.__init__(self)
        self.websocket = websocket
        self.stream = container_stream

    def run(self):
        try:
            while True:
                self.websocket.send(next(self.stream))
                self.websocket.send("\r\n")
        except:
            print("您没有访问该资源的权限，请联系管理员")
            self.websocket.send("\r\n您没有访问该资源的权限，请联系管理员配置权限\r\n")
            self.websocket.close()


class SSHConsumer(WebsocketConsumer):
    def connect(self):
        if self.scope.get('type') == 'websocket':
            path = self.scope.get('path')
            self.rows_s = 600
            self.cols_s = 600
            self.container = path.split('/')[-1]
            self.pod = path.split('/')[-2]
            self.namespace = path.split('/')[-3]
            self.stream = KubeApi().pod_exec(self.namespace, self.pod, self.container, self.rows_s, self.cols_s)
            if self.stream is None:
                self.accept()
                self.send("\r\n您没有访问该资源的权限，请联系管理员配置权限\r\n")
                self.close()
            else:
                kub_stream = K8SStreamThread(self, self.stream)
                kub_stream.start()
                self.accept()

    def disconnect(self, close_code):
        if self.stream is not None:
            self.stream.write_stdin('exit\r')

    def receive(self, text_data):
        if self.stream is not None:
            self.stream.write_stdin(text_data)


class LogConsumer(WebsocketConsumer):
    def connect(self):
        if self.scope.get('type') == 'websocket':
            path = self.scope.get('path')
            self.tails = 200
            self.container = path.split('/')[-1]
            self.pod = path.split('/')[-2]
            self.namespace = path.split('/')[-3]
            self.stream = KubeApi().pod_log(self.namespace, self.pod, self.container, self.tails)
            kub_stream = K8SWatchStreamThread(self, self.stream)
            kub_stream.start()
            self.accept()
