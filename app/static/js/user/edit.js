;
var user_edit_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        var that = this;
        $(".user_edit_wrap .save").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            var nickname_target = $(".user_edit_wrap input[name=nickname]");
            var nickname = nickname_target.val();

            var email_target = $(".user_edit_wrap input[name=email]");
            var email = email_target.val();

            if (!that.validate(nickname_target, nickname, email_target, email)) {
                return;
            }

            btn_target.addClass("disabled");

            var data = {
                nickname: nickname,
                email: email
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
                    common_ops.alert(res.responseJSON.msg, null);
                },
                complete: function () {
                    btn_target.removeClass("disabled");
                }
            });
        });
    },
    validate: function (nickname_target, nickname, email_target, email) {
        if (!nickname || !(nickname.length >= 3 && nickname.length <= 22)) {
            common_ops.tip("昵称必须为 3 - 22 个字符", nickname_target);
            return false;
        }
        if (!email || email.length < 4) {
            common_ops.tip("请输入符合规范的邮箱", email_target);
            return false;
        }
        return true;
    }
};

$(document).ready(function () {
    user_edit_ops.init();
});