class AddressService:

    def set_address_info(self, address):
        """
        根据传进来的字典地址合成详细字符串地址
        :param address:
        :return: 字符串地址
        """
        address_info = ''
        if type(address) == dict:
            province = address.get('provinceName', '')
            city = address.get('cityName', '')
            county = address.get('countyName', '')
            detail = address.get('detailInfo', '')
            address_info = province + city + county + detail
            if self.is_center_city(province):
                address_info = city + county + detail
        return address_info

    @staticmethod
    def is_center_city(province):
        center_cities = ('北京市', '天津市', '上海市', '重庆市')
        return province in center_cities
