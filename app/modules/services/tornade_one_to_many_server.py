from tornado import ioloop
from tornado.web import Application
from tornado.websocket import WebSocketHandler


class EchoWebSocket(WebSocketHandler):

    users = set()

    def open(self):
        print("WebSocket opened")
        self.users.add(self)

    # 处理client发送的数据
    def on_message(self, message):
        print(message)
        # 将数据发送给当前连接的client
        # self.write_message(u"server said: " + message)
        # 将数据发送给所有连接的client
        for user in self.users:
            user.write_message(u"server said: " + message)

    def on_close(self):
        print("WebSocket closed")
        self.users.discard(self)

    # 允许所有跨域通讯，解决403问题
    def check_origin(self, origin):
        return True


if __name__ == "__main__":
    application = Application([
      (r"/", EchoWebSocket),
      ])
    application.listen(8080)
    ioloop.IOLoop.current().start()
