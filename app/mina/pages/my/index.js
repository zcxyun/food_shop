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
        // wx.request({
        //     url: app.buildUrl("/member/info"),
        //     header: app.getRequestHeader(),
        //     success: function (res) {
        //         var resp = res.data;
        //         if (resp.code != 200) {
        //             app.alert({"content": resp.msg});
        //             return;
        //         }
        //         that.setData({
        //            user_info:resp.data.info
        //         });
        //     }
        // });
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