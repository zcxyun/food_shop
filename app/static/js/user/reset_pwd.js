;
var mod_pwd_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        var that = this;
        $("#save").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            var old_password = $("#old_password").val();
            var new_password = $("#new_password").val();
            var confirm_password = $("#confirm_password").val()

            if (!that.validate(old_password, new_password, confirm_password)) {
                return;
            }

            btn_target.addClass("disabled");

            var data = {
                old_password: old_password,
                new_password: new_password,
                confirm_password: confirm_password
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
                    common_ops.alert(res.responseJSON.msg, null);
                },
                complete: function () {
                    btn_target.removeClass("disabled");
                }
            });
        });
    },
    validate: function (old_password, new_password, confirm_password) {
        if (!old_password) {
            common_ops.alert("请输入原密码~~");
            return false;
        }

        if (!new_password || !(new_password.length >= 6 && new_password.length <= 22)) {
            common_ops.alert("请输入6位到22位的新密码~~");
            return false;
        }

        if (!confirm_password || confirm_password != new_password) {
            common_ops.alert("两次输入密码不相同");
            return false;
        }
        return true;
    }
};

$(document).ready(function () {
    mod_pwd_ops.init();
});