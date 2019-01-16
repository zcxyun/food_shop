;
var user_edit_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        var that = this;
        var nickname = $(".user_edit_wrap input[name=nickname]");
        var email = $(".user_edit_wrap input[name=email]");

        $(".user_edit_wrap .save").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            if (!that.validate(nickname, email)) {
                return;
            }

            btn_target.addClass("disabled");

            var dataNode = {
                nickname: nickname,
                email: email
            };

            var data = {
                nickname: nickname.val(),
                email: email.val()
            };

            $.ajax({
                url: common_ops.buildUrl("/cms/user/edit"),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    common_ops.alert(res.msg, function () {
                        location.reload();
                    });
                },
                error: function (res) {
                    errorTipOrAlert(res, 'tip', dataNode);
                },
                complete: function () {
                    btn_target.removeClass("disabled");
                }
            });
        });
    },
    validate: function (nickname, email) {
        const nicknameValue = nickname.val();
        const emailValue = email.val();
        const emailReg = /^\w{3,}(\.\w+)*@[A-z 0-9]+(\.[A-z]{2,5}){1,2}$/;

        if (!nicknameValue || !(nicknameValue.length >= 3 && nicknameValue.length <= 22)) {
            common_ops.tip("昵称必须为 3 - 22 个字符", nickname);
            return false;
        }
        if (!emailValue || !emailReg.test(emailValue)) {
            common_ops.tip("电子邮件格式不符合规范", email);
            return false;
        }
        return true;
    }
};

$(document).ready(function () {
    user_edit_ops.init();
});