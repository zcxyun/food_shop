;
var mod_pwd_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        var that = this;
        var old_password = $("#old_password");
        var new_password = $("#new_password");
        var confirm_password = $("#confirm_password");

        $("#save").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            if (!that.validate(old_password, new_password, confirm_password)) {
                return;
            }

            btn_target.addClass("disabled");

            var data = {
                old_password: old_password.val(),
                new_password: new_password.val(),
                confirm_password: confirm_password.val()
            };

            $.ajax({
                url: common_ops.buildUrl("/cms/user/reset_pwd"),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    common_ops.alert(res.msg, function () {
                        location.reload();
                    });
                },
                error: function (res) {
                    const data = {
                        old_password: old_password,
                        new_password: new_password,
                        confirm_password: confirm_password
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
    validate: function (old_password, new_password, confirm_password) {
        const old_password_val = old_password.val();
        const new_password_val = new_password.val();
        const confirm_password_val = confirm_password.val();
        const pwd_reg = /^[A-Za-z0-9_]{6,22}$/;

        if (!old_password_val) {
            common_ops.tip("密码不能为空", old_password);
            return false;
        }
        if (!pwd_reg.test(old_password_val)) {
            common_ops.tip("密码格式不对，必须为6到22位字母，数字或下划线", old_password);
            return false;
        }
        if (!new_password_val) {
            common_ops.tip("密码不能为空", new_password);
            return false;
        }
        if (!pwd_reg.test(new_password_val)) {
            common_ops.tip("密码格式不对，必须为6到22位字母，数字或下划线~~", new_password);
            return false;
        }
        if (!confirm_password_val) {
            common_ops.tip("密码不能为空", confirm_password);
            return false;
        }
        if (confirm_password_val !== new_password_val) {
            common_ops.tip("两次输入密码不相同", confirm_password);
            return false;
        }
        return true;
    }
};

$(document).ready(function () {
    mod_pwd_ops.init();
});