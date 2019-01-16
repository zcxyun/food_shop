from datetime import datetime, timedelta

from flask import render_template
from flask_login import login_required

from app.libs.redprint import Redprint
from app.libs.utils import now_timestamp, before_timestamp
from app.models import StatDailySite
from app.view_model.index import IndexViewModel

cms = Redprint('index')


@cms.route('')
@login_required
def index():
    index_vm = IndexViewModel()
    now,  date_before_30days = now_timestamp(), before_timestamp()

    list = StatDailySite.query.filter(
        StatDailySite.create_time <= now, StatDailySite.create_time >= date_before_30days
    ).order_by(StatDailySite.id.asc()).all()

    data = index_vm.data
    if list:
        for item in list:
            data['finance']['month'] += item.total_pay_money
            data['member']['month_new'] += item.total_new_member_count
            data['member']['total'] = item.total_member_count
            data['order']['month'] += item.total_order_count
            data['shared']['month'] += item.total_shared_count
            if item.date == now:
                data['finance']['today'] = item.total_pay_money
                data['member']['today_new'] = item.total_new_member_count
                data['order']['today'] = item.total_order_count
                data['shared']['today'] = item.total_shared_count

    return render_template('index/index.html', data=data)
