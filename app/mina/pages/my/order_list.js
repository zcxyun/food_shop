import Base from '../../utils/base.js';

const http = new Base();
var app = getApp();
Page({
    data: {
        order_list: [],
        statusType: ["待付款", "待发货", "待收货", "待评价", "已完成", "已关闭"],
        status: [0, 1, 2, 3, 4, -1],
        currentType: 0,
        tabClass: ["", "", "", "", "", ""]
    },
    statusTap: function (e) {
        var curType = e.currentTarget.dataset.index;
        this.setData({
            currentType: curType
        });
        this.getPayOrder();
    },
    orderDetail: function (e) {
        wx.navigateTo({
            url: "/pages/my/order_info?order_sn=" + e.currentTarget.dataset.id
        })
    },
    onLoad: function (options) {
        // 生命周期函数--监听页面加载
    },
    onShow: function () {
        this.getPayOrder();
    },
    orderCancel: function (e) {
        this.orderOps(e.currentTarget.dataset.id, "cancel", "确定取消订单？");
    },
    getPayOrder: function () {
        var that = this;
        http.request({
            url: '/my/order',
            method: 'POST',
            data: {
                status: that.data.status[that.data.currentType]
            },
            sCallback: res => {
                that.setData({
                    order_list: res.pay_order_list
                });
            },
            eCallback: res => {
                // app.alert({'content': res.msg});
                that.setData({
                    order_list: []
                });
            }
        });
    },
    toPay: function (e) {
        var that = this;
        http.request({
            url: '/order/pay',
            method: 'POST',
            data: {
                order_sn: e.currentTarget.dataset.id
            },
            sCallback: res => {
                let pay_info = res.pay_info;
                wx.requestPayment({
                    'timeStamp': pay_info.timeStamp,
                    'nonceStr': pay_info.nonceStr,
                    'package': pay_info.package,
                    'signType': 'MD5',
                    'paySign': pay_info.paySign,
                    'success': res => {
                    },
                    'fail': res => {
                    }
                });
            },
            eCallback: res => {
                app.alert({'content': res.msg});
            }
        });
    },
    orderConfirm: function (e) {
        this.orderOps(e.currentTarget.dataset.id, "confirm", "确定收到？");
    },
    orderComment: function (e) {
        wx.navigateTo({
            url: "/pages/my/comment?order_sn=" + e.currentTarget.dataset.id
        });
    },
    orderOps: function (order_sn, act, msg) {
        var that = this;
        var params = {
            "content": msg,
            "cb_confirm": function () {
                http.request({
                    url: '/order/ops',
                    method: 'POST',
                    data: {
                        order_sn: order_sn,
                        act: act
                    },
                    sCallback: res => {
                        app.alert({'content': res.msg})
                        that.getPayOrder();
                    }
                });
            }
        };
        app.tip(params);
    }
});
