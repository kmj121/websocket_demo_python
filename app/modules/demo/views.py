import json
import time

from flask import request
from flask_restful import Resource


class WebsocketDemo(Resource):
    def get(self, did):
        auth = request.headers.get('Authorization')
        try:
            req_data = json.loads(request.get_data())
        except ValueError:
            req_data = {}

        if did == 'null' or is_twenty_four(did) is None:
            return f'交付单号非法：{did}', 400
        try:
            try:
                delivery = order.find(did)
            except OrderNotFound as e:
                LOG.info(f'交付单为空-{did}')
                return f'交付单为空：{did}', 400
            if 'isExpress' not in req_data or req_data["isExpress"] not in (0, 1, "0", "1"):
                return f'isExpress缺失或非0，1', 400
            now_time = int(time.time())
            timeline = {"event": "express_change".upper(), "message": req_data.get("message", ""),
                        "timestamp": now_time}
            try:
                payload = payload_from_jwt(auth)
                timeline["operatedBy"] = payload['sub']
            except:
                pass
            if "isExpress" in req_data and req_data["isExpress"]:
                isExpress = 1
            else:
                isExpress = 0
            update_dict = {
                "$set": {"extension.isExpress": isExpress},
                "$push": {"extension.timeline": timeline}
            }
            order.update(did, update_dict)
            return timeline, 200
        except Exception as e:
            LOG.error(f'订单加急失败-{e}', exc_info=True)
            return '订单加急失败', 500
