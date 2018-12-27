;
var user_login_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        var that = this;
        $(".login_wrap .do-login").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            var login_name = $(".login_wrap input[name=login_name]").val();
            var login_pwd = $(".login_wrap input[name=login_pwd]").val();

            if (!that.validate(login_name, login_pwd)) {
                return;
            }

            btn_target.addClass("disabled");
            var urlParams = getUrlParams()
            $.ajax({
                url: common_ops.buildUrl("/cms/user/login", urlParams),
                type: 'POST',
                data: {'login_name': login_name, 'login_pwd': login_pwd},
                dataType: 'json',
                success: function (res) {
                    location.assign(common_ops.buildUrl(res.next));
                },
                error: function (res) {
                    common_ops.alert(res.responseJSON.msg, null);
                },
                complete: function () {
                    btn_target.removeClass("disabled");
                }
            });
        });
    },
    validate: function (login_name, login_pwd) {
        if (!login_name) {
            common_ops.alert("请输入正确的登录用户名~~");
            return false;
        }
        if (!login_pwd) {
            common_ops.alert("请输入正确的密码~~");
            return false;
        }
        return true;
    }
};

$(document).ready(function () {
    user_login_ops.init();
});