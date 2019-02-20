import Address from '../../utils/address.js';
import Base from '../../utils/base.js';
const http = new Base();
const address = new Address();
var app = getApp();
Page({
    data: {},
    onLoad() {

    },
    onShow() {
        this.getInfo();
    },
    getInfo:function(){
        var that = this;
        http.request({
            url: '/member/info',
            sCallback: res => {
                that.setData({
                    user_info: res.info
                });
            },
            eCallback: res => {
                app.alert({'content': res.msg});
            }
        });
    },
    myAddress: function() {
        wx.chooseAddress({
            success: res => {
                // address.submitAddress(res, (success, data) => {
                //     if (success) {
                //         app.alert({'content': '地址添加或修改成功'})
                //     }
                // });
            }
        });
    }
});