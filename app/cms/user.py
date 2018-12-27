from flask import render_template, request, jsonify, url_for, g, redirect
from flask_login import login_user, login_required, current_user, logout_user

from app import db
from app.libs.error_codes import AuthFailed, Success
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.cms_forms import LoginForm, EditForm, ResetPwdForm
from app.view_model.base import BaseViewModel

cms = Redprint('user')


@cms.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('cms.index+index'))
    if request.method == 'POST':
        form = LoginForm().validate()
        user = User.verify(form.login_name.data, form.login_pwd.data)
        login_user(user)
        next_url = request.args.get('next')
        data = {'next': next_url}
        if not next_url or not next_url.startswith('/'):
            data['next'] = url_for('cms.index+index')
        return jsonify(data)
    return render_template('user/login.html')


@cms.route('/edit', methods=['POST', 'GET'])
@login_required
def edit():
    if request.method == 'POST':
        form = EditForm().validate()
        with db.auto_commit():
            current_user.nickname = form.nickname.data
            current_user.email = form.email.data
            db.session.add(current_user)
        return Success(msg='信息修改成功')

    return render_template('user/edit.html', current='edit')


@cms.route('/reset_pwd', methods=['POST', 'GET'])
@login_required
def reset_pwd():
    if request.method == 'POST':
        form = ResetPwdForm().validate()
        # if form.new_password.data == form.old_password.data:
        #     raise AuthFailed(msg='新密码不能与原密码相同')
        with db.auto_commit():
            current_user.password = form.new_password.data
            db.session.add(current_user)
        return Success(msg='密码修改成功')

    return render_template('user/reset_pwd.html', current='reset_pwd')


@cms.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('cms.user+login'))