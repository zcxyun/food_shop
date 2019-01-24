import Base from 'base.js';

export default class Address extends Base {
    /**
     * 获得自己的收货地址
     * @param callback
     */
    // getAddress(callback) {
    //     this.request({
    //         url: '/address/get',
    //         sCallback: res => {
    //             res.totalDetail = this.setAddressInfo(res);
    //             callback && callback(res);
    //         }
    //     });
    // }

    /**
     * 处理要返回的地址信息
     * @param address
     * @returns {*}
     */
    setAddressInfo(address) {
        let province = address.provinceName || address.province,
            city = address.cityName || address.city,
            county = address.countyName || address.county,
            detail = address.detailInfo || address.detail;
        let totalDetail = city + county + detail;
        if (!this.isCenterCity(province)) {
            totalDetail = province + totalDetail;
        }
        return totalDetail;
    }

    /**
     * 是否为直辖市
     * @param province
     * @returns {boolean}
     */
    isCenterCity(province) {
        let centerCities = ['北京市', '天津市', '上海市', '重庆市'];
        return centerCities.includes(province);
    }

    /**
     * 提交新地址
     * @param data
     * @param callback
     */
    // submitAddress(data, callback) {
    //     data = this._setUpAddress(data);
    //     this.request({
    //         url: '/address/set',
    //         method: 'POST',
    //         data: data,
    //         sCallback: res => {
    //             callback && callback(true, res.data);
    //         },
    //         eCallback: res => {
    //             callback && callback(false, res.data);
    //         }
    //     })
    // }

    /**
     * 处理地址信息
     * @param data
     * @returns {{userName: *, telNumber: *, provinceName: *, cityName: *, countyName: *, detailInfo: *}}
     * @private
     */
    // _setUpAddress(data) {
    //     let formData = {
    //         userName: data.userName,
    //         telNumber: data.telNumber,
    //         provinceName: data.provinceName,
    //         cityName: data.cityName,
    //         countyName: data.countyName,
    //         detailInfo: data.detailInfo
    //     }
    //     return formData;
    // }
}