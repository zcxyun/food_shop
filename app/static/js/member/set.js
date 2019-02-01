;
var member_set_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        var that = this;
        var nicknameNode = $(".wrap_member_set input[name=nickname]");
        var nicknameOrgin = nicknameNode.val();

        $(".wrap_member_set .save").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理，请不要重复提交");
                return;
            }
            if (!that.validate(nicknameOrgin, nicknameNode)) {
                return;
            }
            btn_target.addClass("disabled");
            var dataNode = {
                nickname: nicknameNode
            };

            var data = {
                nickname: nicknameNode.val()
            };
            var id = $(".wrap_member_set input[name=id]").val();
            $.ajax({
                url: common_ops.buildUrl("/cms/member/set/" + id),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    common_ops.alert(res.msg, function () {
                        location.assign(common_ops.buildUrl("/cms/member/index"));
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
    validate: function (nicknameOrigin, nicknameNode) {
        var nickname = nicknameNode.val();
        if (nicknameOrigin === nickname) {
            common_ops.tip("输入的昵称与原昵称一样，请重新输入", nicknameNode);
            return false;
        }
        if (nickname.length < 2) {
            common_ops.tip("请输入符合规范的姓名", nicknameNode);
            return false;
        }
        return true;
    }
};

$(document).ready(function () {
    member_set_ops.init();
});