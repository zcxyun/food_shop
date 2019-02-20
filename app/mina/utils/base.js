import Token from 'token.js';
import {base64_encode} from "./base64";
import Config from 'config';
const app = getApp();

export default class Base {
    constructor() {
        this.baseUrl = Config.getInstance().restUrl;
    }

    /**
     * 当 noRefetch 为 true 时，不做未授权重试机制
     * @param params
     * @param noRefetch
     */
    request(params, noRefetch) {
        var url = this.baseUrl + params.url;
        if (!params.method) {
            params.method = 'GET';
        }
        /*不需要再次组装地址*/
        if (params.setUpUrl == false) {
            url = params.url;
        }
        wx.request({
            url: url,
            header: {
                'Content-Type': 'application/json',
                'Authorization': 'Basic ' + base64_encode(
                    wx.getStorageSync('token') + ':')
            },
            method: params.method,
            data: params.data,
            dataType: 'json',
            responseType: 'text',
            success: res => {
                var code = res.statusCode.toString();
                var startChar = code.charAt(0);
                if (startChar === '2') {
                    params.sCallback && params.sCallback(res.data);
                } else {
                    if (code === '401') {
                        if (!noRefetch) {
                            this._refetch(params);
                        }
                    } else {
                        if (res.data.error_code === 1000) {
                            let msg = res.data.msg;
                            for (const i in msg) {
                                res.data.msg = msg[i][0];
                                break;
                            }
                        }
                        params.eCallback && params.eCallback(res.data);
                    }
                }
            },
            fail: err => {
                app.alert({'content': err})
            }
        });
    }

    _refetch(params) {
        var token = new Token();
        token.getTokenFromServer(token => {
            this.request(params, true);
        });
    }
}

