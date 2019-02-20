from datetime import datetime, timedelta

from flask import jsonify
from flask_login import login_required

from app.libs.enums import Status
from app.libs.redprint import Redprint
from app.libs.utils import date_to_str
from app.models import StatDailySite

cms = Redprint('chart')


@cms.route('/dashboard')
@login_required
def dashboard():
    date_from, date_to = get_date()
    stat_list = StatDailySite.query.filter(
        StatDailySite.date >= date_from,
        StatDailySite.date <= date_to,
        StatDailySite.status == Status.EXIST.value
    ).order_by(
        StatDailySite.id.asc()
    ).all()
    dates = [item.date for item in stat_list]
    member_count = [item.member_count for item in stat_list]
    order_count = [item.order_count for item in stat_list]
    series = {
        '会员总数': member_count,
        '订单总数': order_count
    }
    data = get_chart_data(categories=dates, series=series)
    return jsonify({'data': data})


@cms.route('/finance')
@login_required
def finance():
    date_from, date_to = get_date()
    stat_list = StatDailySite.query.filter(
        StatDailySite.date >= date_from,
        StatDailySite.date <= date_to,
        StatDailySite.status == Status.EXIST.value
    ).order_by(
        StatDailySite.id.asc()
    ).all()
    dates = [item.date for item in stat_list]
    moneys = [float(item.money) for item in stat_list]

    series = {'日营收报表': moneys}
    data = get_chart_data(categories=dates, series=series)

    return jsonify({'data': data})


@cms.route('/share')
@login_required
def share():
    date_from, date_to = get_date()
    stat_list = StatDailySite.query.filter(
        StatDailySite.date >= date_from,
        StatDailySite.date <= date_to,
        StatDailySite.status == Status.EXIST.value
    ).order_by(
        StatDailySite.id.asc()
    ).all()
    dates = [item.date for item in stat_list]
    share_count = [item.share_count for item in stat_list]

    series = {'日分享报表': share_count}
    data = get_chart_data(categories=dates, series=series)

    return jsonify({'data': data})


def get_date():
    date_from = date_to_str(datetime.now() - timedelta(days=30), '%Y-%m-%d')
    date_to = date_to_str(format='%Y-%m-%d')
    return date_from, date_to


def get_chart_data(categories, series):
    series_data = [{'name': key, 'data': series[key]} for key in series]
    return {
        'categories': categories,
        'series': series_data
    }
