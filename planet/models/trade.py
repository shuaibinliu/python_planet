# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean

from planet.common.base_model import Base


class Carts(Base):
    """
    购物车
    """
    __tablename__ = 'Carts'
    CAid = Column(String(64), primary_key=True)
    USid = Column(String(64), nullable=False, comment='用户id')
    SKUid = Column(String(64), nullable=False, comment='商品sku')
    CAnums = Column(Integer, default=1, comment='数量')
    PBid = Column(String(64), comment='品牌id')
    PRid = Column(String(64), comment='商品id')


class OrderMain(Base):
    """
    订单主单, 下单时每种品牌单独一个订单, 但是一并付费
    """
    __tablename__ = 'OrderMain'
    OMid = Column(String(64), primary_key=True)
    OMno = Column(String(64), nullable=False, comment='订单编号')
    OPayno = Column(String(64), comment='付款流水号,与orderpay对应')
    USid = Column(String(64), nullable=False, comment='用户id')
    UseCoupon = Column(Boolean, default=False, comment='是否优惠券')
    OMfrom = Column(Integer, default=0, comment='来源: 0: 购物车, 10: 商品详情')
    PBname = Column(String(32), nullable=False, comment='品牌名')
    PBid = Column(String(64), nullable=False, comment='品牌id')
    OMclient = Column(Integer, default=0, comment='下单设备: 0: 微信, 10: app')
    OMfreight = Column(Float, default=0, comment='运费')
    OMmount = Column(Float, nullable=False, comment='总价')
    OMtrueMount = Column(Float, nullable=False, comment='实际总价')
    OMstatus = Column(Integer, default=0, comment='订单状态 0待付款,10待发货,20待收货,30完成,-40取消交易')
    OMinRefund = Column(Boolean, default=False, comment='有商品在售后状态')
    OMmessage = Column(String(255), comment='留言')
    # 收货信息
    OMrecvPhone = Column(String(11), nullable=False, comment='收货电话')
    OMrecvName = Column(String(11), nullable=False, comment='收货人姓名')
    OMrecvAddress = Column(String(255), nullable=False, comment='地址')


class OrderPay(Base):
    """
    付款流水
    """
    __tablename__ = 'OrderPay'
    OPayid = Column(String(64), primary_key=True)
    OPayno = Column(String(64), comment='交易号, 自己生成')
    OPayType = Column(Integer, default=0, comment='支付方式 0 微信 10 支付宝')
    OPaytime = Column(DateTime, comment='付款时间')
    OPayMount = Column(Integer, comment='付款金额')
    OPaysn = Column(String(64), comment='第三方支付流水')
    OPayJson = Column(Text, comment='回调原文')
    OPaymarks = Column(String(255), comment='备注')


class OrderCoupon(Base):
    __tablename__ = 'OrderRaward'
    OCid = Column(String(64), primary_key=True)
    CPid = Column(String(64), nullable=False, comment='优惠券')
    OCnum = Column(Integer, default=1, comment='使用数量')
    OCreduce = Column(Float, nullable=False, comment='减额')
    # 其他


class OrderPart(Base):
    """
    订单副单
    """
    __tablename__ = 'OrderPart'
    OPid = Column(String(64), primary_key=True)
    OMid = Column(String(64), nullable=False, comment='订单id')
    SKUid = Column(String(64), nullable=False, comment='skuid')
    PRid = Column(String(64),  nullable=False, comment='商品id')
    PRattribute = Column(Text, comment='商品属性 ["网络","颜色","存储"]')
    SKUattriteDetail = Column(Text, nullable=False, comment='sku详情[]')
    SKUprice = Column(Float, nullable=False, comment='单价')
    PRtitle = Column(String(255), nullable=False, comment='商品标题')
    PRmainpic = Column(String(255), nullable=False, comment='主图')
    OPnum = Column(Integer, default=1, comment='数量')
    OPsubTotal = Column(Float, default=SKUprice, comment='价格小计')
    OPstatus = Column(Integer, default=0, comment='状态: 售后状态,0未发起售后, 10 申请售后 -10 售后已取消 -20 已拒绝  20 处理中 200 处理完毕')


class OrderRefundApply(Base):
    """订单售后申请"""
    __tablename__ = 'OrderRefundApply'
    ORAid = Column(String(64), primary_key=True)
    ORAsn = Column(String(64), nullable=False, comment='售后编号')
    OMid = Column(String(64), nullable=False, comment='主单id')
    OPid = Column(String(64), nullable=False, comment='副单id')
    USid = Column(String(64), nullable=False, comment='用户id')
    ORAstate = Column(Integer, default=0, comment='类型: 0 退货退款 10 暂定')
    ORAreason = Column(String(255), nullable=False, comment='退款原因')
    ORAproductStatus = Column(Integer, default=0, comment='0已收货, 10 未收货')
    ORAstatus = Column(Integer, default=0, comment='状态 -1 拒绝 0 未审核 1审核通过')
    ORAcheckReason = Column(String(255), comment='审核原因')
    ORAcheckTime = Column(DateTime, comment='审核时间')


class OrderRefund(Base):
    """订单售后表"""
    __tablename__ = 'OrderRefund'
    ORid = Column(String(64), primary_key=True)
    OMid = Column(String(64), nullable=False, comment='订单id')
    # 其他



#
# class OrderLogistic(Base):
#     """物流"""