# -*- coding:utf8 -*-
from datetime import datetime

from sqlalchemy import Column, create_engine, Integer, String, Text, Float, Boolean, orm, DateTime

from planet.common.base_model import Base
from planet.config import secret as cfg
import json


DB_PARAMS = "{0}://{1}:{2}@{3}/{4}?charset={5}".format(
    cfg.sqlenginename,
    cfg.username,
    cfg.password,
    cfg.host,
    cfg.database,
    cfg.charset)
mysql_engine = create_engine(DB_PARAMS, echo=False)


class Products(Base):
    """
    商品
    """
    __tablename__ = "Products"
    PRid = Column(String(64), primary_key=True)



class ProductScene(Base):
    """
    场景
    """


class ProductCategory(Base):
    """
    商品分类(3级)
    """

class ProductSku(Base):
    """
    商品SKU
    """

class ProductImage(Base):
    """
    商品图片
    """

class Carts(Base):
    """
    购物车
    """

class OrderMain(Base):
    """
    订单主单
    """

class OrderPart(Base):
    """
    订单副单
    """

class Users(Base):
    """
    用户表
    """

class Items(Base):
    """
    标签
    """

class ProductItems(Base):
    """
    商品标签关联表
    """

class Reviews(Base):
    """
    评论
    """

class ProductBrand(Base):
    """
    商品品牌
    """

class PlanetNews(Base):
    """
    资讯
    """

class ShoppingAddress(Base):
    """
    收货地址
    """

class Logistics(Base):
    """
    物流
    """

class Card(Base):
    """
    优惠券
    """

class CardPackage(Base):
    """
    优惠券卡包
    """

class CoinList(Base):
    """
    积分记录
    """

class SaleMessage(Base):
    """
    商家推广信息
    """

class TrialCommodity(Base):
    """
    试用商品
    """

class UserInvite(Base):
    """
    用户邀请
    """