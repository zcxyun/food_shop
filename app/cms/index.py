from datetime import datetime, timedelta

from flask import render_template
from flask_login import login_required

from app.libs.enums import Status
from app.libs.redprint import Redprint
from app.libs.utils import date_to_str
from app.models import StatDailySite
from app.view_model.index import IndexViewModel

cms = Redprint('index')


@cms.route('')
@login_required
def index():
    date_from, date_to = get_date()

    list = StatDailySite.query.filter(
        StatDailySite.date <= date_to,
        StatDailySite.date >= date_from,
        StatDailySite.status == Status.EXIST.value
    ).order_by(
        StatDailySite.id.asc()
    ).all()

    data = IndexViewModel.data
    if list:
        for item in list:
            data['finance']['month'] += item.money
            data['member']['month_new'] += item.member_count
            data['member']['total'] = item.all_member_count
            data['order']['month'] += item.order_count
            data['shared']['month'] += item.share_count
            if item.date == date_to:
                data['finance']['today'] = item.money
                data['member']['today_new'] = item.member_count
                data['order']['today'] = item.order_count
                data['shared']['today'] = item.share_count

    return render_template('index/index.html', data=data)


def get_date():
    date_from = date_to_str(datetime.now() - timedelta(days=30), '%Y-%m-%d')
    date_to = date_to_str(format='%Y-%m-%d')
    return date_from, date_to
