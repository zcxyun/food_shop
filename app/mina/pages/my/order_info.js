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