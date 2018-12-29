;
var account_set_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        var that = this;
        var nickname = $(".wrap_account_set input[name=nickname]");
        var mobile = $(".wrap_account_set input[name=mobile]");
        var email = $(".wrap_account_set input[name=email]");
        var login_name = $(".wrap_account_set input[name=login_name]");
        var login_pwd = $(".wrap_account_set input[name=login_pwd]");

        $(".wrap_account_set .save").click(function () {
            var btn_target = $(this);
            if( btn_target.hasClass("disabled") ){
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }
            if (!that.validate(login_name, login_pwd, nickname, email, mobile)) {
                return false;
            }
            btn_target.addClass("disabled");
            const id = $(".wrap_account_set input[name=id]").val() || 0;

            var data_node = {
                nickname: nickname,
                mobile: mobile,
                email: email,
                login_name: login_name,
                login_pwd: login_pwd
            };
            var data = {};
            for (var i in data_node) {
                data[i] = data_node[i].val()
            }

            $.ajax({
                url: common_ops.buildUrl("/cms/account/set/" + id),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    common_ops.alert(res.msg, function () {
                        location.assign(common_ops.buildUrl("/cms/account/index"));
                    });
                },
                error: function (res) {
                    msg = res.responseJSON.msg;
                    for (const i in msg) {
                        common_ops.tip(msg[i][0], data_node[i]);
                        break;
                    }
                },
                complete: function () {
                    btn_target.removeClass("disabled");
                }
            });
        });
    },
    validate: function (login_name, login_pwd, nickname, email, mobile) {
        var login_name_val = login_name.val(),
            login_pwd_val = login_pwd.val(),
            nickname_val = nickname.val(),
            email_val = email.val(),
            mobile_val = mobile.val();

        var login_name_reg = /^1[0-9]{10}$/,
            login_pwd_reg = /^[A-Za-z0-9_]{6,22}$/,
            email_reg = /^\w{3,}(\.\w+)*@[A-z 0-9]+(\.[A-z]{2,5}){1,2}$/;
        mobile_reg = /^1[0-9]{10}$/;

        // 昵称校验 -----------------------------------------------------------------
        if (!nickname_val) {
            common_ops.tip('昵称不允许为空', nickname);
            return false;
        }
        if (!(nickname_val.length >= 3 && nickname_val.length <= 22)) {
            common_ops.tip('昵称必须为 3 - 22 个字符', nickname);
            return false;
        }
        // 手机号校验 -----------------------------------------------------------------
        if (!mobile_val) {
            common_ops.tip('手机号不允许为空', mobile);
            return false;
        }
        // if (!mobile_reg.test(mobile_val)) {
        //     common_ops.tip('手机号码必须是11位数字', mobile);
        //     return false;
        // }
        // 电子邮件校验 -----------------------------------------------------------------
        if (!email_val) {
            common_ops.tip('电子邮箱不能为空', email);
            return false;
        }
        if (!email_reg.test(email_val)) {
            common_ops.tip('电子邮件格式不符合规范', email);
            return false;
        }
        // 用户名校验 -----------------------------------------------------------------
        if (!login_name_val) {
            common_ops.tip('用户名不能为空', login_name);
            return false;
        }
        // if (!login_name_reg.test(login_name_val)) {
        //     common_ops.tip('用户名码必须是11位手机号码', login_name);
        //     return false;
        // }
        // 密码校验 -----------------------------------------------------------------
        if (!login_pwd_val) {
            common_ops.tip('密码不能为空', login_pwd);
            return false;
        }
        if (!login_pwd_reg.test(login_pwd_val)) {
            common_ops.tip('密码格式不对，必须为6到22位字母，数字或下划线', login_pwd);
            return false;
        }
        return true;
    }
};

$(document).ready(function () {
    account_set_ops.init();
});