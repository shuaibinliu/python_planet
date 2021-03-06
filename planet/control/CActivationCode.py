import random
import re
import string
import uuid

from flask import request

from planet.common.error_response import ParamsError, SystemError
from planet.common.params_validates import parameter_required
from planet.common.success_response import Success
from planet.common.token_handler import token_required, is_admin, admin_required
from planet.config.enums import UserActivationCodeStatus, ApplyStatus
from planet.control.BaseControl import BASEAPPROVAL
from planet.extensions.register_ext import db
from planet.models import UserActivationCode, ActivationCodeRule, ActivationCodeApply, ApprovalNotes, Approval
from planet.extensions.validates.trade import ActRuleSetFrom


class CActivationCode(BASEAPPROVAL):
    @token_required
    def create_apply(self):
        """提交购买申请"""
        data = parameter_required(('acabankname', 'acabanksn', 'acaname', 'vouchers'))
        acabankname = data.get('acabankname')
        acabanksn = data.get('acabanksn')
        if len(acabanksn) < 10 or len(acabanksn) > 30:
            raise ParamsError('卡号错误')
        if re.findall('\D', acabanksn):
            raise ParamsError('卡号错误')
        acaname = data.get('acaname')
        vouchers = data.get('vouchers')
        if not vouchers or (not isinstance(vouchers, list)) or (len(vouchers) > 4):
            raise ParamsError('凭证有误')
        with db.auto_commit():
            apply = ActivationCodeApply.create({
                'ACAid': str(uuid.uuid1()),
                'USid': request.user.id,
                'ACAname': acaname,
                'ACAbankSn': acabanksn,
                'ACAbankname': acabankname,
                'ACAvouchers': vouchers
            })
            db.session.add(apply)
        self.create_approval('toactivationcode', request.user.id, apply.ACAid)
        return Success('提交成功')

    def get_rule(self):
        """获取规则电话地址以及下方协议以及收款信息"""
        info = ActivationCodeRule.query.filter_by_(ACRisShow=True).first_()
        return Success(data=info)

    def agree_apply(self):
        pass

    @token_required
    def get_user_activationcode(self):
        """获取用户拥有的激活码"""
        if not is_admin():
            usid = request.user.id
            user_act_codes = UserActivationCode.query.filter(
                UserActivationCode.isdelete == False,
                UserActivationCode.USid == usid
            ).order_by(
                UserActivationCode.createtime.desc()
            ).all_with_page()
        elif is_admin():
            data = parameter_required()
            usid = data.get('usid')
            user_act_codes = UserActivationCode.query.filter_(
                UserActivationCode.isdelete == False,
                UserActivationCode.USid == usid
            ).order_by(
                UserActivationCode.createtime.desc()
            ).all_with_page()
            # todo 管理员查看激活码
            pass
        for user_act_code in user_act_codes:
            user_act_code.fill('uacstatus_zh',
                               UserActivationCodeStatus(user_act_code.UACstatus).zh_value)
        return Success(data=user_act_codes)

    @admin_required
    def set_rule(self):
        """设置一些规则"""
        form = ActRuleSetFrom().valid_data()
        with db.auto_commit():
            deleted = ActivationCodeRule.query.delete_()
            rule_instance = ActivationCodeRule.create({
                'ACRid': str(uuid.uuid1()),
                'ACRrule': form.acrrule.data,
                'ACRphone': form.acrphone.data,
                'ACRaddress': form.acraddress.data,
                'ACRname': form.acrname.data,
                'ACRbankSn': form.acrbanksn.data,
                'ACRbankAddress': form.acrbankaddress.data,
                'ACRnum': form.acrnum.data,
                'ACRcash': form.acrcash.data
            })
            db.session.add(rule_instance)
        return Success('添加成功', rule_instance.ACRid)

    @admin_required
    def send_code(self):
        # todo 发放激活码
        pass

    def _generate_activaty_code(self, num=10):
        """生成激活码"""
        code_list = []
        rule = ActivationCodeRule.query.filter_by_(ACRisShow=True).first()
        if rule:
            num = rule.ACRnum or 10

        lowercase = string.ascii_lowercase
        count = 0
        while len(code_list) < num:
            if count > 10:
                raise SystemError('激活码库存不足')
            code = ''.join(random.choice(lowercase) for _ in range(2)) + ''.join(str(random.randint(0, 9)) for _ in range(5))
            # 是否与已有重复
            is_exists = UserActivationCode.query.filter_by_({
                'UACcode': code,
                'UACstatus': UserActivationCodeStatus.wait_use.value
            }).first()
            if not is_exists:
                code_list.append(code)
            else:
                count += 1
        return code_list

    @token_required
    def get_list(self):

        aca_list = ActivationCodeApply.query.filter(
            ActivationCodeApply.USid == request.user.id, ActivationCodeApply.isdelete == False).all()

        for aca in aca_list:
            aca.hide('USid')
            aca.fill('acaapplystatus', ApplyStatus(aca.ACAapplyStatus).name)
            aca.fill('acaapplystatus_zh', ApplyStatus(aca.ACAapplyStatus).zh_value)
            if aca.ACAapplyStatus == ApplyStatus.reject.value:
                reason = ApprovalNotes.query.filter(
                    Approval.AVcontent == aca.ACAid,
                    Approval.PTid == 'toactivationcode',
                    ApprovalNotes.AVid == Approval.AVid
                ).order_by(ApprovalNotes.createtime.desc()).first()
                if not reason:
                    continue
                aca.fill('acareason', reason.ANabo)

        return Success('获取申请列表成功', data=aca_list)

