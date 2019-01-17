from app.view_model.base import BaseViewModel


class AddressViewModel(BaseViewModel):
    show_keys = ['id', 'nickname', 'mobile', 'is_default', 'address']

    def __init__(self, address):
        self.id = address.id
        self.nickname = address.nickname
        self.mobile = address.mobile
        self.is_default = address.is_default
        self.address = '{}{}{}{}'.format(
            address.province, address.city, address.county, address.detail)


class AddressCollection:

    def fill(self, address_list):
        return [AddressViewModel(address) for address in address_list]
