import Base from '../../utils/base.js'
const http = new Base()
var app = getApp();


Page({
    data: {
        indicatorDots: true,
        autoplay: true,
        interval: 3000,
        duration: 1000,
        loadingHidden: false, // loading
        swiperCurrent: 0,
        categories: [],
        activeCategoryId: 0,
        goods: [],
        scrollTop: "0",
        loadingMoreHidden: true,
        searchInput: '',
        p:1,
        processing:false
    },
    onLoad: function () {
        var that = this;
        wx.setNavigationBarTitle({
            title: app.globalData.shopName
        });
    },
    //解决切换不刷新维内托，每次展示都会调用这个方法
    onShow:function(){
        this.getBannerAndCat();
    },
    scroll: function (e) {
        var that = this, scrollTop = that.data.scrollTop;
        that.setData({
            scrollTop: e.detail.scrollTop
        });
    },
    //事件处理函数
    swiperchange: function (e) {
        this.setData({
            swiperCurrent: e.detail.current
        })
    },
    listenerSearchInput:function( e ){
        this.setData({
            searchInput: e.detail.value
        });
    },
    toSearch:function( e ){
        this.setData({
            p:1,
            goods:[],
            loadingMoreHidden:true
        });
        this.getFoodList();
	},
    tapBanner: function (e) {
        if (e.currentTarget.dataset.id != 0) {
            wx.navigateTo({
                url: "/pages/food/info?id=" + e.currentTarget.dataset.id
            });
        }
    },
    toDetailsTap: function (e) {
        wx.navigateTo({
            url: "/pages/food/info?id=" + e.currentTarget.dataset.id
        });
    },
    getBannerAndCat: function () {
        var that = this;
        // wx.request({
        //     url: app.buildUrl("/food/index"),
        //     header: app.getRequestHeader(),
        //     success: function (res) {
        //         var resp = res.data;
        //         if (res.statusCode != 200) {
        //             app.alert({"content": resp.msg});
        //             return;
        //         }
        //
        //         that.setData({
        //             banners: resp.banner_list,
        //             categories: resp.cat_list
        //         });
        //         that.getFoodList();
        //     }
        // });
        http.request({
            url: '/food/index',
            sCallback: res => {
                 var resp = res.data;
                if (res.statusCode != 200) {
                    app.alert({"content": resp.msg});
                    return;
                }
                that.setData({
                    banners: resp.banner_list,
                    categories: resp.cat_list
                });
                that.getFoodList();
            }
        });
    },
    catClick: function (e) {
        this.setData({
            activeCategoryId: e.currentTarget.id
        });
        this.setData({
            loadingMoreHidden: true,
            p:1,
            goods:[]
        });
        this.getFoodList();
    },
    onReachBottom: function () {
        var that = this;
        setTimeout(function () {
            that.getFoodList();
        }, 500);
    },
    getFoodList: function () {
        var that = this;
        if( that.data.processing ){
            return;
        }

        if( !that.data.loadingMoreHidden ){
            return;
        }

        that.setData({
            processing:true
        });

        // wx.request({
        //     url: app.buildUrl("/food/search"),
        //     header: app.getRequestHeader(),
        //     data: {
        //         cat_id: that.data.activeCategoryId,
        //         mix_kw: that.data.searchInput,
        //         p: that.data.p,
        //     },
        //     success: function (res) {
        //         var resp = res.data;
        //         if (res.statusCode != 200) {
        //             app.alert({"content": resp.msg});
        //             return;
        //         }
        //
        //         var goods = resp.list;
        //         that.setData({
        //             goods: that.data.goods.concat( goods ),
        //             p: that.data.p + 1,
        //             processing:false
        //         });
        //
        //         if( resp.data.has_more == 0 ){
        //             that.setData({
        //                 loadingMoreHidden: false
        //             });
        //         }
        //
        //     }
        // });
        http.request({
            url: '/food/search',
            method: 'POST',
            data: {
                cat_id: that.data.activeCategoryId,
                query_key: that.data.searchInput,
                page: that.data.p,
            },
            sCallback: res => {
                var resp = res.data;
                if (res.statusCode != 200) {
                    app.alert({"content": resp.msg});
                    return;
                }
                var goods = resp.list;
                that.setData({
                    goods: that.data.goods.concat( goods ),
                    p: that.data.p + 1,
                    processing:false
                });
                if( resp.has_more == 0 ){
                    that.setData({
                        loadingMoreHidden: false
                    });
                }
            }
        })
    }
});
