import Base from '../../utils/base.js';
import Address from '../../utils/address.js';

const http = new Base();
const address = new Address();
var app = getApp();

Page({
    data: {
        goods_list: [],
        // default_address: null,
        yun_price: "0.00",
        pay_price: "0.00",
        total_price: "0.00",
        params: null,
        address: null,
        addressInfo: ''
        // express_address_id:0,
    },
    onLoad: function (e) {
        var that = this;
        that.setData({
            params: JSON.parse(e.data)
        });
    },
    onShow: function () {
        var that = this;
        this.getOrderInfo();
    },
    createOrder: function (e) {
        wx.showLoading();
        var that = this;
        var data = {
            type: that.data.params.type,
            goods: JSON.stringify(that.data.params.goods),
            // express_address_id: that.data.default_address.id
            address: JSON.stringify(that.data.address)
        };
        // wx.request({
        //     url: app.buildUrl("/order/create"),
        //     header: app.getRequestHeader(),
        //     method: 'POST',
        //     data: data,
        //     success: function (res) {
        //         wx.hideLoading();
        //         var res = res.data;
        //         if (res.code != 200) {
        //             app.alert({"content": res.msg});
        //             return;
        //         }
        //         wx.navigateTo({
        //             url: "/pages/my/order_list"
        //         });
        //     }
        // });
        http.request({
            url: '/order/create',
            method: 'POST',
            data: data,
            sCallback: res => {
                wx.hideLoading();
                wx.redirectTo({
                    url: '/pages/my/order_list'
                });
            },
            eCallback: res => {
                app.alert({'content': res.msg});
            }
        });
    },
    // addressSet: function () {
    //     wx.navigateTo({
    //         url: "/pages/my/addressSet?id=0"
    //     });
    // },
    selectAddress: function () {
        // wx.navigateTo({
        //     url: "/pages/my/addressList"
        // });
        wx.chooseAddress({
            success: res => {
                this.setData({
                    address: {
                        userName: res.userName,
                        postalCode: res.postalCode,
                        provinceName: res.provinceName,
                        cityName: res.cityName,
                        countyName: res.countyName,
                        detailInfo: res.detailInfo,
                        nationalCode: res.nationalCode,
                        telNumber: res.telNumber,
                        errMsg: res.errMsg
                    },
                    addressInfo: address.setAddressInfo(res)
                });
            }
        });
    },
    getOrderInfo: function () {
        var that = this;
        var data = {
            type: this.data.params.type,
            goods: JSON.stringify(this.data.params.goods)
        };
        // wx.request({
        //     url: app.buildUrl("/order/info"),
        //     header: app.getRequestHeader(),
        //     method: 'POST',
        //     data: data,
        //     success: function (res) {
        //         var res = res.data;
        //         if (res.code != 200) {
        //             app.alert({"content": res.msg});
        //             return;
        //         }
        //
        //         that.setData({
        //             goods_list: res.data.food_list,
        //             default_address: res.data.default_address,
        //             yun_price: res.data.yun_price,
        //             pay_price: res.data.pay_price,
        //             total_price: res.data.total_price,
        //         });
        //
        //         if( that.data.default_address ){
        //             that.setData({
        //                  express_address_id: that.data.default_address.id
        //             });
        //         }
        //     }
        // });
        http.request({
            url: '/order/info',
            method: 'POST',
            data: data,
            sCallback: res => {
                this.setData({
                    goods_list: res.food_list,
                    pay_price: res.pay_price,
                    yun_price: res.yun_price,
                    total_price: res.total_price
                });
            },
            eCallback: res => {
                app.alert({'content': res.msg});
            }
        });
    }
});
