import Base from '../../utils/base.js';
import IndexModel from './index_model.js';

const http = new Base();
const indexModel = new IndexModel();
const app = getApp();

Page({
    data: {
        remind: '加载中',
        angle: 0,
        userInfo: {},
        regFlag:true
    },
    goToIndex: function () {
        wx.switchTab({
            url: '/pages/food/index',
        });
    },
    onLoad: function () {
        wx.setNavigationBarTitle({
            title: app.globalData.shopName
        });
        this.checkLogin();
    },
    onShow: function () {

    },
    onReady: function () {
        var that = this;
        setTimeout(function () {
            that.setData({
                remind: ''
            });
        }, 1000);
        wx.onAccelerometerChange(function (res) {
            var angle = -(res.x * 30).toFixed(1);
            if (angle > 14) {
                angle = 14;
            }
            else if (angle < -14) {
                angle = -14;
            }
            if (that.data.angle !== angle) {
                that.setData({
                    angle: angle
                });
            }
        });
    },
    checkLogin:function(){
        indexModel.checkLogin(regFlag => {
            this.setData({
                regFlag: regFlag
            })
        });
    },
    login:function( e ){
        var that = this;
        if( !e.detail.userInfo ){
            app.alert( { 'content':'登录失败，请再次点击~~' } );
            return;
        }
        var data = e.detail.userInfo;
        indexModel.login(data, that.goToIndex);
    }
});