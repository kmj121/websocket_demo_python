from flask_restful import Api

from modules.demo.views import WebsocketDemo


api = Api()

api.add_resource(WebsocketDemo, '/websocket/sendEveryOneInfo')  # 发送不同的信息给每个人
