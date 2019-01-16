;
var food_cat_set_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        var that = this;
        var idNode = $(".wrap_cat_set input[name=id]");
        var nameNode = $(".wrap_cat_set input[name=name]");
        var weightNode = $(".wrap_cat_set input[name=weight]");


        $(".wrap_cat_set .save").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }
            if (!that.validate(nameNode, weightNode)) {
                return;
            }
            var dataNode = {
                name: nameNode,
                weight: weightNode
            };
            var data = {
                name: nameNode.val(),
                weight: weightNode.val()
            };
            id = idNode.val() || 0;
            btn_target.addClass("disabled");

            $.ajax({
                url: common_ops.buildUrl("/cms/food/category_set/" + id),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    common_ops.alert(res.msg, function () {
                        location.assign(common_ops.buildUrl('/cms/food/category'))
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
    validate: function (nameNode, weightNode) {
        var name = nameNode.val();
        var weight = weightNode.val();
        if (!(name.length >= 2 && name.length <= 10)) {
            common_ops.tip("请输入2到10个字符分类名称", nameNode);
            return false;
        }

        if (parseInt(weight) < 1) {
            common_ops.tip("请输入符合规范的权重，并且大于或等于1", weightNode);
            return false;
        }
        return true;
    }
};

$(document).ready(function () {
    food_cat_set_ops.init();
});