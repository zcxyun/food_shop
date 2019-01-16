import Config from 'config.js';

export default class Token {
    constructor() {
        this.verifyUrl = Config.getInstance().restUrl + '/member/verify_token';
        this.loginUrl = Config.getInstance().restUrl + '/member/login';
    }

    verify() {
        var token = wx.getStorageSync('token');
        if (!token) {
            this.getTokenFromServer();
        } else {
            this.verifyFromServer(token);
        }
    }

    verifyFromServer(token) {
        wx.request({
            url: this.verifyUrl,
            method: 'POST',
            data: {
                token: token
            },
            success: res => {
                if (res.statusCode != 200) {
                    this.getTokenFromServer();
                }
            }
        });
    }

    getTokenFromServer(callback) {
        wx.login({
            success: res => {
                wx.request({
                    url: this.loginUrl,
                    method: 'POST',
                    data: {
                        code: res.code
                    },
                    success: res => {
                        wx.setStorageSync('token', res.data.token);
                        callback && callback(res.data.token);
                    }
                });
            }
        });
    }
}