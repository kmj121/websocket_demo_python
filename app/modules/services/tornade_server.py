from tornado import ioloop
from tornado.web import Application
from tornado.websocket import WebSocketHandler


class EchoWebSocket(WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    # 处理client发送的数据
    def on_message(self, message):
        print(message)
        # 将数据发送给连接的client
        self.write_message(u"server said: " + message)

    def on_close(self):
        print("WebSocket closed")

    # 允许所有跨域通讯，解决403问题
    def check_origin(self, origin):
        return True


if __name__ == "__main__":
    application = Application([
      (r"/", EchoWebSocket),
      ])
    application.listen(8080)
    ioloop.IOLoop.current().start()