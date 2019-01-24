import hashlib, requests, uuid, datetime
import xml.etree.ElementTree as ET

from flask import current_app


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
        r.encoding = 'utf-8'
        current_app.logger.info(r.text)
        if r.status_code == 200:
            prepay_id = self.xml_2_dict(r.text).get('prepay_id')
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
