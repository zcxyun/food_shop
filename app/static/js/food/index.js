;
var food_index_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        var that = this;
        $(".remove").click(function () {
            that.ops("remove", $(this).attr("data"))
        });

        $(".recover").click(function () {
            that.ops("recover", $(this).attr("data"))
        });

        $(".wrap_search .search").click(function () {
            $(".wrap_search").submit();
        });
    },
    ops: function (act, id) {
        var callback = {
            'ok': function () {
                $.ajax({
                    url: common_ops.buildUrl("/cms/food/ops/" + id),
                    type: 'POST',
                    data: {
                        act: act
                    },
                    dataType: 'json',
                    success: function (res) {
                        common_ops.alert(res.msg, function () {
                            location.reload();
                        });
                    },
                    error: function (res) {
                        errorTipOrAlert(res, 'alert');
                    }
                });
            },
            'cancel': null
        };
        common_ops.confirm(act === "remove" ? "确定删除?" : "确定恢复?", callback);
    }
};

$(document).ready(function () {
    food_index_ops.init();
});