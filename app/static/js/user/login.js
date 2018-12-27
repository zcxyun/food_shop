;
var user_login_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        var that = this;
        var login_name = $(".login_wrap input[name=login_name]");
        var login_pwd = $(".login_wrap input[name=login_pwd]");

        $(".login_wrap .do-login").click(function () {
            var btn_target = $(this);
            // if (btn_target.hasClass("disabled")) {
            //     common_ops.alert("正在处理!!请不要重复提交~~");
            //     return;
            // }

            if (!that.validate(login_name, login_pwd)) {
                return;
            }

            btn_target.addClass("disabled");
            var urlParams = getUrlParams()
            $.ajax({
                url: common_ops.buildUrl("/cms/user/login", urlParams),
                type: 'POST',
                data: {'login_name': login_name.val(), 'login_pwd': login_pwd.val()},
                dataType: 'json',
                success: function (res) {
                    location.assign(common_ops.buildUrl(res.next));
                },
                error: function (res) {
                    const error_code = res.responseJSON.error_code;
                    if (error_code === 1001 || error_code === 1005) {
                        common_ops.alert(res.responseJSON.msg, null);
                        return;
                    }
                    const data = {
                        login_name: login_name,
                        login_pwd: login_pwd
                    }
                    msg = res.responseJSON.msg;
                    for (const i in msg) {
                        common_ops.tip(msg[i][0], data[i]);
                        break;
                    }
                },
                complete: function () {
                    btn_target.removeClass("disabled");
                }
            });
        });
    },
    validate: function (login_name, login_pwd) {
        const login_name_val = login_name.val();
        const login_pwd_val = login_pwd.val();
        const login_name_reg = /^1[0-9]{10}$/;
        const login_pwd_reg = /^[A-Za-z0-9_]{6,22}$/;
        if (!login_name_val) {
            common_ops.tip("手机号不能为空", login_name);
            return false;
        }
        // if (!login_name_reg.test(login_name_val)) {
        //     common_ops.tip('手机号码必须是11位数字')
        // }
        if (!login_pwd_val) {
            common_ops.tip('密码不能为空', login_pwd);
            return false;
        }
        if (!login_pwd_reg.test(login_pwd_val)) {
            common_ops.tip("密码格式不对，必须为6到22位字母，数字或下划线", login_pwd);
            return false;
        }
        return true;
    }
};

$(document).ready(function () {
    user_login_ops.init();
});