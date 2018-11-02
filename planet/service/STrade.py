# -*- coding: utf-8 -*-
from planet.common.base_service import SBase, close_session
from planet.models.trade import Carts


class STrade(SBase):
    @close_session
    def get_card_list(self, args):
        """获取购物车列表"""
        brands = self.session.query(Carts).filter_by_(**args)
        pbids = brands.group_by(Carts.PBid).all_with_page()
        return brands.filter(Carts.PBid.in_([x.PBid for x in pbids])).\
            order_by(Carts.createtime).all()

    @close_session
    def get_card_one(self, args, error=None):
        return self.session.query(Carts).filter_by_(**args).first_(error)

