;
var finance_pay_info_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".express_send").click(function () {
            var id = $(this).attr("data");
            var callback = {
                'ok': function () {
                    $.ajax({
                        url: common_ops.buildUrl("/cms/finance/ops/"+id),
                        type: 'POST',
                        data: {
                            act: "deliver"
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
            common_ops.confirm("确定已发货了？", callback);
        });
    }
};

$(document).ready(function () {
    finance_pay_info_ops.init();
});

