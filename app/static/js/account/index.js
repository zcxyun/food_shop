;
var account_index_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        var that = this;
        $(".wrap_search .search").click(function () {
            $(".wrap_search").submit();
        });

        $(".remove").click(function () {
            that.ops("remove", $(this).attr("data"));
        });

        $(".recover").click(function () {
            that.ops("recover", $(this).attr("data"));
        });
    },
    ops: function (act, id) {
        var callback = {
            'ok': function () {
                $.ajax({
                    url: common_ops.buildUrl("/cms/account/ops/" + id),
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
        common_ops.confirm((act == "remove" ? "确定删除？" : "确定恢复？"), callback);
    }

};

$(document).ready(function () {
    account_index_ops.init();
});