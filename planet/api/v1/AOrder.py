# -*- coding: utf-8 -*-
from planet.common.base_resource import Resource
from planet.control.COrder import COrder


class AOrder(Resource):
    def __init__(self):
        self.corder = COrder()

    def post(self, order):
        apis = {
            'create': self.corder.create,
            'pay': self.corder.pay,
            'alipay_notify': self.corder.alipay_notify,
            'wechat_notify': self.corder.wechat_notify,
            'create_evaluation': self.corder.create_order_evaluation,
            'cancle': self.corder.cancle,
        }
        return apis

    def get(self, order):
        apis = {
            'list': self.corder.list,
            'get': self.corder.get,
            'count': self.corder.get_order_count,
        }
        return apis

