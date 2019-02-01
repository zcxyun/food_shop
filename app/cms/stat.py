from flask import current_app, request, render_template
from flask_login import login_required

from app.libs.enums import Status
from app.libs.redprint import Redprint
from app.models import StatDailySite, StatDailyFood, StatDailyMember
from app.validators.cms_forms.stat_forms import StatForm

cms = Redprint('stat')


@cms.route('/index')
@login_required
def index():
    page, _, _, date_from, date_to = StatForm().validate().data.values()
    stat_list = StatDailySite.query.filter(
        StatDailySite.date >= date_from,
        StatDailySite.date <= date_to,
        StatDailySite.status == Status.EXIST.value
    ).order_by(
        StatDailySite.id.desc()
    ).paginate(int(page), current_app.config['PAGE_SIZE'], error_out=False)
    resp = {
        'date_from': date_from,
        'date_to': date_to
    }
    params = resp_params(stat_list, resp, 'index')
    return render_template('stat/index.html', **params)


@cms.route('/food')
@login_required
def food():
    page, _, _, date_from, date_to = StatForm().validate().data.values()
    stat_list = StatDailyFood.query.filter(
        StatDailyFood.status == Status.EXIST.value,
        StatDailyFood.date >= date_from,
        StatDailyFood.date <= date_to
    ).order_by(
        StatDailyFood.id.desc()
    ).paginate(
        int(page), current_app.config['PAGE_SIZE'], error_out=False
    )
    resp = {
        'date_from': date_from,
        'date_to': date_to
    }
    params = resp_params(stat_list, resp, 'food')
    return render_template('stat/food.html', **params)


@cms.route('/member')
@login_required
def member():
    page, _, _, date_from, date_to = StatForm().validate().data.values()
    stat_list = StatDailyMember.query.filter(
        StatDailyMember.status == Status.EXIST.value,
        StatDailyMember.date >= date_from,
        StatDailyMember.date <= date_to
    ).order_by(
        StatDailyMember.id.desc()
    ).paginate(
        int(page), current_app.config['PAGE_SIZE'], error_out=False
    )
    resp = {
        'date_from': date_from,
        'date_to': date_to
    }
    params = resp_params(stat_list, resp, 'member')
    return render_template('stat/member.html', **params)


@cms.route('/share')
@login_required
def share():
    page, _, _, date_from, date_to = StatForm().validate().data.values()
    stat_list = StatDailySite.query.filter(
        StatDailySite.status == Status.EXIST.value,
        StatDailySite.date >= date_from,
        StatDailySite.date <= date_to
    ).order_by(
        StatDailySite.id.desc()
    ).paginate(
        int(page), current_app.config['PAGE_SIZE'], error_out=False
    )
    resp = {
        'date_from': date_from,
        'date_to': date_to
    }
    params = resp_params(stat_list, resp, 'share')
    return render_template('stat/share.html', **params)


def resp_params(stat_list=None, resp=None, current=''):
    return {
        'pagination': stat_list,
        'url': request.endpoint,
        'resp': resp,
        'current': current
    }
