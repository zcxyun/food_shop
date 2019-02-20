import Base from '../../utils/base.js';

const http = new Base();
const app = getApp();
Page({
    data: {},
    onLoad: function () {

    },
    onShow: function () {
        this.getCartList();
    },
    //每项前面的选中框
    selectTap: function (e) {
        var index = e.currentTarget.dataset.index;
        var list = this.data.list;
        if (index !== "" && index != null) {
            list[parseInt(index)].active = !list[parseInt(index)].active;
            this.setPageData(this.getSaveHide(), this.totalPrice(), this.allSelect(), this.noSelect(), list);
        }
    },
    //计算是否全选了
    allSelect: function () {
        var list = this.data.list;
        var allSelect = false;
        for (var i = 0; i < list.length; i++) {
            var curItem = list[i];
            if (curItem.active) {
                allSelect = true;
            } else {
                allSelect = false;
                break;
            }
        }
        return allSelect;
    },
    //计算是否都没有选
    noSelect: function () {
        var list = this.data.list;
        var noSelect = 0;
        for (var i = 0; i < list.length; i++) {
            var curItem = list[i];
            if (!curItem.active) {
                noSelect++;
            }
        }
        if (noSelect == list.length) {
            return true;
        } else {
            return false;
        }
    },
    //全选和全部选按钮
    bindAllSelect: function () {
        var currentAllSelect = this.data.allSelect;
        var list = this.data.list;
        for (var i = 0; i < list.length; i++) {
            list[i].active = !currentAllSelect;
        }
        this.setPageData(this.getSaveHide(), this.totalPrice(), !currentAllSelect, this.noSelect(), list);
    },
    //加数量
    jiaBtnTap: function (e) {
        var index = e.currentTarget.dataset.index;
        var list = this.data.list;
        var i = parseInt(index);
        if (list[i].number < list[i].stock) {
            list[i].number++;
            this.setCart(list[i].food_id, 1, list);
        }
    },
    //减数量
    jianBtnTap: function (e) {
        var index = e.currentTarget.dataset.index;
        var list = this.data.list;
        var i = parseInt(index)
        if (list[i].number > 1) {
            list[i].number--;
            this.setCart(list[i].food_id, -1, list);
        }
    },
    //编辑默认全不选
    editTap: function () {
        var list = this.data.list;
        for (var i = 0; i < list.length; i++) {
            var curItem = list[i];
            curItem.active = false;
        }
        this.setPageData(!this.getSaveHide(), this.totalPrice(), this.allSelect(), this.noSelect(), list);
    },
    //选中完成默认全选
    saveTap: function () {
        var list = this.data.list;
        for (var i = 0; i < list.length; i++) {
            var curItem = list[i];
            curItem.active = true;
        }
        this.setPageData(!this.getSaveHide(), this.totalPrice(), this.allSelect(), this.noSelect(), list);
    },
    getSaveHide: function () {
        return this.data.saveHidden;
    },
    totalPrice: function () {
        var list = this.data.list;
        var totalPrice = 0.00;
        for (var i = 0; i < list.length; i++) {
            if (!list[i].active) {
                continue;
            }
            totalPrice = totalPrice + parseFloat(list[i].price) * list[i].number;
        }
        return totalPrice;
    },
    setPageData: function (saveHidden, total, allSelect, noSelect, list) {
        this.setData({
            list: list,
            saveHidden: saveHidden,
            totalPrice: total,
            allSelect: allSelect,
            noSelect: noSelect,
        });
    },
    //去结算
    toPayOrder: function () {
        var data = {
            type: "cart",
            goods: []
        };

        var list = this.data.list;
        for (var i = 0; i < list.length; i++) {
            if (!list[i].active) {
                continue;
            }
            data['goods'].push({
                "id": list[i].food_id,
                // "total_price": list[i].total_price,
                "number": list[i].number
            });
        }

        wx.navigateTo({
            url: "/pages/order/index?data=" + JSON.stringify(data)
        });
    },
    //如果没有显示去光光按钮事件
    toIndexPage: function () {
        wx.switchTab({
            url: "/pages/food/index"
        });
    },
    //选中删除的数据
    deleteSelected: function () {
        var list = this.data.list;
        var goods = [];
        list = list.filter(function (item) {
            if (item.active) {
                goods.push({
                    "id": item.food_id
                })
            }

            return !item.active;
        });
        if (goods.length == 0) {
            return;
        }
        this.setData({
            list: list
        })
        this.setPageData(this.getSaveHide(), this.totalPrice(), this.allSelect(), this.noSelect(), list);
        //发送请求到后台删除数据
        http.request({
            url: '/cart/delete',
            method: 'POST',
            data: {
                goods: JSON.stringify(goods)
            }
        });
    },
    getCartList: function () {
        var that = this;
        http.request({
            url: '/cart/index',
            sCallback: res => {
                this.setData({
                    list: res.list,
                    saveHidden: true,
                    totalPrice: 0.00,
                    allSelect: true,
                    noSelect: false
                });
                that.setPageData(that.getSaveHide(), that.totalPrice(), that.allSelect(), that.noSelect(), that.data.list);
            },
            eCallback: res => {
                app.alert({'content': res.msg});
            }
        });
    },
    setCart: function (food_id, number, list) {
        var that = this;
        var data = {
            "id": food_id,
            "number": number
        };
        http.request({
            url: '/cart/set',
            method: 'POST',
            data: data,
            sCallback: res => {
                that.setPageData(
                    that.getSaveHide(), that.totalPrice(),
                    that.allSelect(), that.noSelect(), list);
            },
            eCallback: res => {
                app.alert({'content': res.msg});
            }
        });
    }
});
