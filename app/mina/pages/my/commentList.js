import Base from '../../utils/base.js';
const http = new Base();
var app = getApp();
Page({
    data: {
        list: [
            {
                date: "2018-07-01 22:30:23",
                order_number: "20180701223023001",
                content: "记得周六发货",
            },
            {
                date: "2018-07-01 22:30:23",
                order_number: "20180701223023001",
                content: "记得周六发货",
            }
        ]
    },
    onLoad: function (options) {
        // 生命周期函数--监听页面加载

    },
    onShow: function () {
        this.getCommentList();
    },
    getCommentList:function(){
        var that = this;
        http.request({
            url: '/my/comments',
            sCallback: res => {
                that.setData({
                    // list: res.list
                });
            },
            eCallback: res => {
                app.alert({'content': res.msg});
            }
        });
    }
});
