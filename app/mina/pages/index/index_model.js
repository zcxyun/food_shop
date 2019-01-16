import Base from '../../utils/base.js';
const app = getApp();
const http = new Base();

export default class IndexModel {
    constructor() {}

    checkLogin(callback) {
        wx.login({
            success: function(res) {
                if (!res.code) {
                    app.alert({
                        content: '登录失败，请再次点击~~'
                    });
                    callback && callback(false);
                    return;
                }
                // http.request({
                //     url: '/member/verify',
                //     method: 'POST',
                //     data: {
                //         code: res.code
                //     },
                //     sCallback: res => {
                //         if (res.statusCode != 200) {
                //             callback && callback(false);
                //             return;
                //         }
                //         app.setCache('token', res.data.token);
                //         callback && callback(true);
                //     }
                // });
                wx.request({
                    url: app.buildUrl('/member/verify'),
                    method: 'POST',
                    header: app.getRequestHeader(),
                    data: {
                        code: res.code
                    },
                    success: res => {
                        if (res.statusCode != 200) {
                            callback && callback(false);
                            return;
                        }
                        app.setCache("token",
                            res.data.token);
                        callback && callback(true);
                    }
                });
            }
        });
    }

    login(data, callback) {
        wx.login({
            success: function (res) {
                if (!res.code) {
                    app.alert({ 'content': '登录失败，请再次点击~~' });
                    return;
                }
                data['code'] = res.code;
                wx.request({
                    url: app.buildUrl('/member/login'),
                    header: app.getRequestHeader(),
                    method: 'POST',
                    data: data,
                    success: function (res) {
                        if (res.statusCode != 200) {
                            app.alert({ 'content': res.data.msg });
                            return;
                        }
                        app.setCache("token", res.data.token);
                        callback && callback();
                    }
                });
            }
        });
    }
}