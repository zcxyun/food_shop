from flask import g, jsonify

from app.libs.redprint import Redprint
from app.libs.token import auth
from app.models import MemberAddress
from app.validators.api_forms.IDMustBePositive import IDMustBePositive
from app.validators.api_forms.address_forms import NewAddressForm
from app.view_model.api_vm.address_vm import AddressCollection

api = Redprint('address')


@api.route('/index')
@auth.login_required
def index():
    member = g.member
    address_list = MemberAddress.query.filter_by(
        member_id=member.id).order_by(MemberAddress.id.desc()).all()

    addresses = AddressCollection().fill(address_list)
    resp = {'list': addresses}
    return jsonify(resp)


@api.route('/set', methods=['POST'])
def set():
    member = g.member
    id = IDMustBePositive().validate().id.data
    form = NewAddressForm().validate()


