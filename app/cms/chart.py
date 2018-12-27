from app.libs.redprint import Redprint

cms = Redprint('chart')


@cms.route('/dashboard')
def dashboard():
    pass


@cms.route('/finance')
def finance():
    pass


@cms.route('/share')
def share():
    pass