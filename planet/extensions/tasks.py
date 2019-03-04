# -*- coding: utf-8 -*-
import uuid
from datetime import date, timedelta, datetime
from decimal import Decimal

from flask import current_app
from flask_celery import Celery
from sqlalchemy import cast, Date, extract, func

from planet.common.error_response import NotFound
from planet.common.share_stock import ShareStock
from planet.config.cfgsetting import ConfigSettings
from planet.config.enums import OrderMainStatus, OrderFrom, UserCommissionStatus, ProductStatus, ApplyStatus, ApplyFrom, \
    SupplizerSettementStatus, LogisticsSignStatus, UserCommissionType
from planet.extensions.register_ext import db
from planet.models import CorrectNum, GuessNum, GuessAwardFlow, ProductItems, OrderMain, OrderPart, OrderEvaluation, \
    Products, User, UserCommission, Approval, Supplizer, SupplizerSettlement, OrderLogistics, UserWallet

celery = Celery()


@celery.task(name="fetch_share_deal")
def fetch_share_deal():
    """获取昨日的收盘"""
    with db.auto_commit():
        s_list = []
        share_stock = ShareStock()
        yesterday_result = share_stock.new_result()
        # yesterday = date.today() - timedelta(days=1)
        today = date.today()
        # 昨日结果
        db_today = CorrectNum.query.filter(
            cast(CorrectNum.CNdate, Date) == today
        ).first()
        # if not db_today:  # 昨日
        if not db_today and yesterday_result:  # 今日
            # current_app.logger.info('写入昨日数据')
            current_app.logger.info('写入今日数据')
            correct_instance = CorrectNum.create({
                'CNid': str(uuid.uuid4()),
                'CNnum': yesterday_result,
                'CNdate': today
            })
            s_list.append(correct_instance)
            # 判断是否有猜对的
            # 更新逻辑之后不需要判断是否猜对
        #     guess_nums = GuessNum.query.filter_by({'GNnum': yesterday_result, 'GNdate': db_today}).all()
        #     for guess_num in guess_nums:
        #         exists_in_flow = GuessAwardFlow.query.filter_by_({'GNid': guess_num.GNid}).first()
        #         if not exists_in_flow:
        #             guess_award_flow_instance = GuessAwardFlow.create({
        #                 'GAFid': str(uuid.uuid4()),
        #                 'GNid': guess_num.GNid,
        #             })
        #             s_list.append(guess_award_flow_instance)
        if s_list:
            db.session.add_all(s_list)


@celery.task(name='auto_evaluate')
def auto_evaluate():
    """超时自动评价订单"""
    try:
        cfs = ConfigSettings()
        limit_time = cfs.get_item('order_auto', 'auto_evaluate_day')
        # limit_time = 7
        time_now = datetime.now()
        with db.auto_commit():
            s_list = list()
            current_app.logger.info(">>>>>>  开始检测超过{0}天未评价的商品订单  <<<<<<".format(limit_time))
            from planet.control.COrder import COrder
            corder = COrder()
            count = 0
            wait_comment_order_mains = OrderMain.query.filter(OrderMain.isdelete == False,
                                                              OrderMain.OMstatus == OrderMainStatus.wait_comment.value,
                                                              # OrderMain.OMfrom.in_(
                                                              #     [OrderFrom.carts.value, OrderFrom.product_info.value]),
                                                              OrderMain.updatetime <= time_now - timedelta(
                                                                  days=int(limit_time))
                                                              )  # 所有超过天数 待评价 的商品订单

            complete_comment_order_mains = OrderMain.query.join(OrderLogistics, OrderLogistics.OMid == OrderMain.OMid,
                                                                ).filter(OrderMain.isdelete == False,
                                                                         OrderMain.OMstatus == OrderMainStatus.complete_comment.value,
                                                                         OrderLogistics.isdelete == False,
                                                                         OrderLogistics.OLsignStatus == LogisticsSignStatus.already_signed.value,
                                                                         OrderLogistics.updatetime <= time_now - timedelta(
                                                                             days=int(limit_time))
                                                                         )  # 所有已评价的订单
            order_mains = wait_comment_order_mains.union(complete_comment_order_mains).all()

            if not order_mains:
                current_app.logger.info(">>>>>>  没有超过{0}天未评价的商品订单  <<<<<<".format(limit_time))

            else:
                for order_main in order_mains:
                    order_parts = OrderPart.query.filter_by_(OMid=order_main.OMid).all()  # 主单下所有副单
                    for order_part in order_parts:
                        if order_part.OPisinORA is True:
                            continue
                        user = User.query.filter_by(USid=order_main.USid).first()

                        exist_evaluation = OrderEvaluation.query.filter_by_(OPid=order_part.OPid).first()
                        if exist_evaluation:
                            current_app.logger.info(
                                ">>>>>  该副单已存在评价, OPid : {}, OMid : {}, OMstatus : {}".format(order_part.OPid,
                                                                                              order_part.OMid,
                                                                                              order_main.OMstatus))
                            corder._commsion_into_count(order_part)  # 佣金到账
                            if user:  # 防止因用户不存在,进入下个方法报错停止
                                corder._tosalesvolume(order_main.OMtrueMount, user.USid)  # 销售额统计
                            continue  # 已评价的订单只进行销售量统计、佣金到账，跳过下面的评价步骤

                        ol = OrderLogistics.query.filter_by(OMid=order_part.OMid).first()
                        if not ol or ol.OLsignStatus != LogisticsSignStatus.already_signed.value:
                            continue

                        corder._commsion_into_count(order_part)  # 佣金到账

                        if user and order_main.OMfrom != OrderFrom.trial_commodity.value:

                            usname, usheader = user.USname, user.USheader

                            corder._tosalesvolume(order_main.OMtrueMount, user.USid)  # 销售额统计
                        else:
                            usname, usheader = '神秘的客官', ''

                        evaluation_dict = {
                            'OEid': str(uuid.uuid1()),
                            'USid': order_main.USid,
                            'USname': usname,
                            'USheader': usheader,
                            'OPid': order_part.OPid,
                            'OMid': order_main.OMid,
                            'PRid': order_part.PRid,
                            'SKUattriteDetail': order_part.SKUattriteDetail,
                            'OEtext': '此用户没有填写评价。',
                            'OEscore': 5,
                        }
                        evaluation_instance = OrderEvaluation.create(evaluation_dict)
                        s_list.append(evaluation_instance)
                        count += 1
                        current_app.logger.info(
                            ">>>>>>  评价第{0}条，OPid ：{1}  <<<<<<".format(str(count), str(order_part.OPid)))
                        # 商品总体评分变化
                        try:
                            product_info = Products.query.filter_by_(PRid=order_part.PRid).first()
                            average_score = round((float(product_info.PRaverageScore) + 10) / 2)
                            Products.query.filter_by_(PRid=order_part.PRid).update({'PRaverageScore': average_score})
                        except Exception as e:
                            current_app.logger.info("更改商品评分失败, 商品可能已被删除；Update Product Score ERROR ：{}".format(e))

                    # 更改主单状态为已完成
                    change_status = OrderMain.query.filter_by_(OMid=order_main.OMid).update(
                        {'OMstatus': OrderMainStatus.ready.value})
                    if change_status:
                        current_app.logger.info(">>>>>>  主单状态更改成功 OMid : {}  <<<<<<".format(str(order_main.OMid)))
                    else:
                        current_app.logger.info(">>>>>>  主单状态更改失败 OMid : {}  <<<<<<".format(str(order_main.OMid)))
            if s_list:
                db.session.add_all(s_list)
            current_app.logger.info(">>>>>> 自动评价任务结束，共更改{}条数据  <<<<<<".format(count))
    except Exception as err:
        current_app.logger.error(">>>>>> 自动评价任务出错 : {}  <<<<<<".format(err))


@celery.task(name='deposit_to_account')
def deposit_to_account():
    """试用商品押金到账"""
    try:
        with db.auto_commit():
            current_app.logger.info("-->  开始检测押金是否到期  <--")
            deposits = UserCommission.query.filter(UserCommission.isdelete == False,
                                                   UserCommission.UCstatus == UserCommissionStatus.preview.value,
                                                   UserCommission.UCtype == UserCommissionType.deposit.value,
                                                   UserCommission.UCendTime <= datetime.now()
                                                   ).all()
            current_app.logger.info("-->  共有{}个订单的押金已到期  <--".format(len(deposits)))
            for deposit in deposits:
                current_app.logger.info("-->  'UCid‘ : {}  <--".format(deposit.UCid))
                user_name = getattr(User.query.filter(User.USid == deposit.USid).first(), 'USname', '') or None
                # 更改佣金状态
                deposit.UCstatus = UserCommissionStatus.in_account.value
                db.session.add(deposit)
                # 用户钱包
                user_wallet = UserWallet.query.filter( UserWallet.isdelete == False,
                                                       UserWallet.USid == deposit.USid,
                                                       UserWallet.CommisionFor == deposit.CommisionFor
                                                       ).first()
                if user_wallet:
                    current_app.logger.info("-->  用户 ‘{}’ 已有钱包账户  <--".format(user_name))
                    user_wallet.UWbalance = Decimal(str(user_wallet.UWbalance or 0)) + Decimal(str(deposit.UCcommission or 0))
                    user_wallet.UWtotal = Decimal(str(user_wallet.UWtotal or 0)) + Decimal(str(deposit.UCcommission))
                    user_wallet.UWcash = Decimal(str(user_wallet.UWcash or 0)) + Decimal(str(deposit.UCcommission))
                    current_app.logger.info("此次到账佣金{}；该用户现在账户余额：{}； 账户总额{}； 可提现余额{}".format(
                        deposit.UCcommission, user_wallet.UWbalance, user_wallet.UWtotal, user_wallet.UWcash))
                    db.session.add(user_wallet)
                else:
                    current_app.logger.info("-->  用户 ‘{}’ 没有钱包账户，正在新建  <--".format(user_name))
                    user_wallet_instance = UserWallet.create({
                        'UWid': str(uuid.uuid1()),
                        'USid': deposit.USid,
                        'UWbalance': deposit.UCcommission,
                        'UWtotal': deposit.UCcommission,
                        'UWcash': deposit.UCcommission,
                        'CommisionFor': deposit.CommisionFor
                    })
                    current_app.logger.info("此次到账佣金{}；".format(deposit.UCcommission))
                    db.session.add(user_wallet_instance)
                current_app.logger.info(" {}".format('=' * 30))
            current_app.logger.info(" >>>>>  押金到账任务结束  <<<<<")
    except Exception as e:
        current_app.logger.error("押金到账任务出错 : {}；".format(e))


@celery.task(name='fix_evaluate_status_error')
def fix_evaluate_status_error():
    """修改评价异常数据（已评价，未修改状态）"""
    current_app.logger.info("----->  开始检测商品评价异常数据  <-----")
    with db.auto_commit():
        order_evaluations = OrderEvaluation.query.filter_by_().all()
        count = 0
        for oe in order_evaluations:
            om = OrderMain.query.filter(OrderMain.OMid == oe.OMid, OrderMain.OMfrom.in_([OrderFrom.carts.value,
                                                                                         OrderFrom.product_info.value]
                                                                                        )).first()
            if not om:
                om_info = OrderMain.query.filter(OrderMain.OMid == oe.OMid).first()
                current_app.logger.info("-->  存在有评价，主单已删除或来自活动订单，OMid为{0}, OMfrom为{1}  <--".format(str(oe.OMid), str(om_info.OMfrom)))
                continue
            omid = om.OMid
            omstatus = om.OMstatus
            if int(omstatus) == OrderMainStatus.wait_comment.value:
                current_app.logger.info("-->  已存在评价的主单id为 {}，未修改前的主单状态为{}  <--".format(str(omid), str(omstatus)))
                current_app.logger.info("-->  开始更改状态  <--")
                upinfo = OrderMain.query.filter_by_(OMid=omid).update({'OMstatus': OrderMainStatus.ready.value})
                count += 1
                if upinfo:
                    current_app.logger.info("-->  {}:更改状态成功  <--".format(str(omid)))
                else:
                    current_app.logger.info("-->  {}:更改失败  <--".format(str(omid)))
                current_app.logger.info("--------------分割线----------------------")
                current_app.logger.info("--------------分割线----------------------")
            else:
                current_app.logger.info("----->  没有发现商品评价异常数据  <-----")
        current_app.logger.info("----->  更新结束，共更改{}条数据  <-----".format(str(count)))


@celery.task(name='create_settlenment')
def create_settlenment():
    """每月22号创建结算单"""
    current_app.logger.info("----->  开始创建供应商结算单  <-----")
    with db.auto_commit():
        su_list = Supplizer.query.filter(Supplizer.isdelete == False).all()
        for su in su_list:
            today = datetime.now()
            pre_month = date(year=today.year, month=today.month, day=1) - timedelta(days=1)
            tomonth_22 = date(year=today.year, month=today.month, day=22)
            pre_month_22 = date(year=pre_month.year, month=pre_month.month, day=22)
            su_comiission = db.session.query(func.sum(UserCommission.UCcommission)).filter(
                UserCommission.USid == su.SUid,
                UserCommission.isdelete == False,
                UserCommission.UCstatus == UserCommissionStatus.in_account.value,
                UserCommission.CommisionFor == ApplyFrom.supplizer.value,
                UserCommission.createtime < tomonth_22,
                UserCommission.createtime >= pre_month_22,
            ).first()
            ss_total = su_comiission[0]
            ss = SupplizerSettlement.create({
                'SSid': str(uuid.uuid1()),
                'SUid': su.SUid,
                'SSdealamount': float('%.2f' % float(ss_total)),
                'SSstatus': SupplizerSettementStatus.settlementing.value
            })
            db.session.add(ss)


@celery.task(name='get_logistics')
def get_logistics():
    """获取快递信息, 每天一次"""
    from planet.models import OrderLogistics
    from planet.control.CLogistic import CLogistic
    clogistic = CLogistic()
    time_now = datetime.now()
    order_logisticss = OrderLogistics.query.filter(
        OrderLogistics.isdelete == False,
        OrderLogistics.OLsignStatus != LogisticsSignStatus.already_signed.value,
        OrderLogistics.OMid == OrderMain.OMid,
        OrderMain.isdelete == False,
        OrderMain.OMstatus == OrderMainStatus.wait_recv.value,
        OrderLogistics.updatetime <= time_now - timedelta(days=1)
    ).all()
    current_app.logger.info('获取物流信息, 共{}条快递单'.format(len(order_logisticss)))
    for order_logistics in order_logisticss:
        with db.auto_commit():
            order_logistics = clogistic._get_logistics(order_logistics)


@celery.task(name='auto_confirm_order')
def auto_confirm_order():
    """已签收7天自动确认收货, 在物流跟踪上已经签收, 但是用户没有手动签收的订单"""
    from planet.models import OrderLogistics
    from planet.control.COrder import COrder
    cfs = ConfigSettings()
    auto_confirm_day = int(cfs.get_item('order_auto', 'auto_confirm_day'))
    time_now = datetime.now()
    corder = COrder()
    order_mains = OrderMain.query.filter(
        OrderMain.isdelete == False,
        OrderMain.OMstatus == OrderMainStatus.wait_recv.value,
        OrderLogistics.OMid == OrderMain.OMid,
        OrderLogistics.isdelete == False,
        OrderLogistics.OLsignStatus == LogisticsSignStatus.already_signed.value,
        OrderLogistics.updatetime <= time_now - timedelta(days=auto_confirm_day)
        ).all()
    current_app.logger.info('自动确认收货, 共{}个订单'.format(len(order_mains)))
    for order_main in order_mains:
        with db.auto_commit():
            order_main = corder._confirm(order_main=order_main)


@celery.task(name='check_for_update')
def check_for_update(*args, **kwargs):
    current_app.logger.info('args is {}, kwargs is {}'.format(args, kwargs))
    from planet.control.CUser import CUser
    if 'users' in kwargs:
        users = kwargs.get('users')
    elif 'usid' in kwargs:
        users = User.query.filter(User.isdelete == False, User.USid == kwargs.get('usid')).all()
    elif args:
        users = args
    else:
        users = User.query.filter(
            User.isdelete == False,
              User.CommisionLevel <= 5,
              User.USlevel == 2
        ).all()
    cuser = CUser()
    for user in users:
        with db.auto_commit():
            cuser._check_for_update(user=user)
            db.session.add(user)


@celery.task()
def auto_agree_task(avid):
    current_app.logger.info('avid is {}'.format(avid))
    from planet.control.CApproval import CApproval
    cp = CApproval()
    with db.auto_commit():
        approval = Approval.query.filter(
            Approval.isdelete == False,
            Approval.AVstatus == ApplyStatus.wait_check.value,
            Approval.AVid == avid
        ).first()
        if approval:
            current_app.logger.info('5分钟自动同意')
            current_app.logger.info(dict(approval))
        else:
            current_app.logger.info('该审批已提前处理')
        try:
            cp.agree_action(approval)
            approval.AVstatus = ApplyStatus.agree.value
        except NotFound :
            current_app.logger.info('审批流状态有误')
            # 如果不存在的商品, 需要将审批流失效
            approval.AVstatus = ApplyStatus.cancle.value
        db.session.add(approval)


@celery.task()
def auto_cancle_order(omids):
    for omid in omids:
        from planet.control.COrder import COrder
        order_main = OrderMain.query.filter(OrderMain.isdelete == False,
                                            OrderMain.OMstatus == OrderMainStatus.wait_pay.value,
                                            OrderMain.OMid == omid).first()
        if not order_main:
            current_app.logger.info('订单已支付或已取消')
            return
        current_app.logger.info('订单自动取消{}'.format(dict(order_main)))
        corder = COrder()
        corder._cancle(order_main)


if __name__ == '__main__':
    from planet import create_app
    app = create_app()
    with app.app_context():
        deposit_to_account()
        # fetch_share_deal()
        # create_settlenment()
        # auto_evaluate()
        # check_for_update()
        # auto_confirm_order()
