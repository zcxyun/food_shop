from flask_login import login_required

from app.libs.redprint import Redprint

cms = Redprint('chart')


@cms.route('/dashboard')
@login_required
def dashboard():
    pass


@cms.route('/finance')
@login_required
def finance():
    pass


@cms.route('/share')
@login_required
def share():
    pass
