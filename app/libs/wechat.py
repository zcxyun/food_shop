import hashlib, requests, uuid
from datetime import datetime, timedelta
import json
import xml.etree.ElementTree as ET

from flask import current_app

from app.libs.utils import now_timestamp
from app.models import AccessToken, db


class WeChatService:

    def __init__(self, merchant_key=None):
        if merchant_key:
            self.merchant_key = merchant_key

    def create_sign(self, pay_data):
        """
        生成签名
        :param pay_data:
        :return:
        """
        stringA = '&'.join(['{}={}'.format(k, pay_data[k]) for k in sorted(pay_data)])
        string_sign_temp = '{}&key={}'.format(stringA, self.merchant_key)
        sign = hashlib.md5(string_sign_temp.encode('utf-8')).hexdigest()
        return sign.upper()

    def get_pay_info(self, pay_data):
        """
        获取支付信息
        :param pay_data:
        :return:
        """
        sign = self.create_sign(pay_data)
        pay_data['sign'] = sign
        xml_data = self.dict_2_xml(pay_data)
        headers = {'Content-Type': 'application/xml'}
        url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        r = requests.post(url=url, data=xml_data, headers=headers)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            current_app.logger.info(r.text)
            data = self.xml_2_dict(r.text)
            if data['return_code'] == 'SUCCESS' and data['result_code'] == 'SUCCESS':
                prepay_id = data.get('prepay_id')
                pay_sign_data = {
                    'appId': pay_data.get('appId'),
                    'timeStamp': pay_data.get('out_trade_no'),
                    'nonceStr': pay_data.get('nonceStr'),
                    'package': 'prepay_id={}'.format(prepay_id),
                    'signType': 'MD5'
                }
                pay_sign = self.create_sign(pay_sign_data)
                pay_sign_data.pop('appId')
                pay_sign_data['paySign'] = pay_sign
                pay_sign_data['prepay_id'] = prepay_id
                return pay_sign_data
        return False

    @staticmethod
    def dict_2_xml(dict_data):
        xml = ['<xml>']
        for k, v in dict_data.items():
            xml.append('<{0}>{1}</{0}>'.format(k, v))
        xml.append('</xml>')
        return ''.join(xml)

    @staticmethod
    def xml_2_dict(xml_data):
        dict = {}
        root = ET.fromstring(xml_data)
        for child in root:
            dict[child.tag] = child.text
        return dict

    @staticmethod
    def get_nonce_str():
        """
        获取随机字符串
        :return:
        """
        return str(uuid.uuid4()).replace('-', '')

    @staticmethod
    def get_access_token():
        token = None
        token_info = AccessToken.query.filter_by(AccessToken.expired_time >= now_timestamp()).first()
        if token_info:
            token = token_info.access_token
            return token

        mina_config = current_app.config['MINA_APP']
        url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}" \
            .format(mina_config['appid'], mina_config['appkey'])
        r = requests.get(url=url)
        r.encoding = 'utf-8'
        if r.status_code != 200 or not r.text:
            return None

        data = json.loads(r.text)
        now = datetime.now()
        date = now + timedelta(seconds=data['expires_in'] - 200)
        with db.auto_commit():
            token_info = AccessToken()
            token_info.access_token = data['access_token']
            token_info.expired_time = date.timestamp()
            db.session.add(token_info)
        return data['access_token']
