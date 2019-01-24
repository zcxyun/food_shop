import Base from '../../utils/base.js';

const http = new Base();
var app = getApp();
Page({
    data: {},
    onLoad: function (e) {
        var that = this;
        that.setData({
            order_sn: e.order_sn
        });
    },
    onShow: function () {
        this.getPayOrderInfo();
    },
    getPayOrderInfo: function () {
        var that = this;
        // wx.request({
        //     url: app.buildUrl("/my/order/info"),
        //     header: app.getRequestHeader(),
        //     data: {
        //         order_sn: that.data.order_sn
        //     },
        //     success: function (res) {
        //         var resp = res.data;
        //         if (resp.code != 200) {
        //             app.alert({"content": resp.msg});
        //             return;
        //         }
        //
        //         that.setData({
        //             info: resp.data.info
        //         });
        //     }
        // });
        http.request({
            url: '/my/order/info',
            method: 'POST',
            data: {
                order_sn: that.data.order_sn
            },
            sCallback: res => {
                that.setData({
                    info: res.info
                });
            },
            eCallback: res => {
                app.alert({'content': res.msg});
            }
        });
    }
});