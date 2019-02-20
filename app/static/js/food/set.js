;
var upload = {
    error: function (msg) {
        common_ops.alert(msg);
    },
    success: function (file_key) {
        if (!file_key) {
            return;
        }
        var html = '<img src="' + common_ops.buildPicUrl(file_key) + '"/>'
            + '<span class="fa fa-times-circle del del_image" data="' + file_key + '"></span>';

        if ($(".upload_pic_wrap .pic-each").size() > 0) {
            $(".upload_pic_wrap .pic-each").html(html);
        } else {
            $(".upload_pic_wrap").append('<span class="pic-each">' + html + '</span>');
        }
        food_set_ops.delete_img();
    }
};
var food_set_ops = {
    init: function () {
        var that = this;
        this.ue = null;
        this.initEditor();
        this.ue.ready(function () {
            that.eventBind();
            that.delete_img();
        });
    },
    eventBind: function () {
        var that = this;
        var idNode = $(".wrap_food_set input[name=id]");
        var catIdNode = $(".wrap_food_set select[name=cat_id]");
        var nameNode = $(".wrap_food_set input[name=name]");
        var priceNode = $(".wrap_food_set input[name=price]");

        var summaryNode = $("#editor");

        var mainImageFormNode = $(".wrap_food_set .upload_pic_wrap");
        var mainImageNode = $(".wrap_food_set .upload_pic_wrap input[name=pic]");

        var stockNode = $(".wrap_food_set input[name=stock]");
        var tagsNode = $(".wrap_food_set input[name=tags]");


        mainImageNode.change(function () {
            mainImageFormNode.submit();
        });

        catIdNode.select2({
            language: "zh-CN",
            width: '100%'
        });

        var tagsNode = tagsNode.tagsInput({
            width: 'auto',
            height: 40,
            onAddTag: function (tag) {
            },
            onRemoveTag: function (tag) {
            }
        });

        $(".wrap_food_set .save").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }
            var dataNode = {
                cat_id: catIdNode,
                name: nameNode,
                price: priceNode,
                summary: summaryNode,
                main_image: mainImageNode,
                stock: stockNode,
                tags: tagsNode.parent()
            };
            var summary = $.trim(that.ue.getContent());
            if (!that.validate(catIdNode, nameNode, priceNode, summaryNode, summary, mainImageNode,
                stockNode, tagsNode)) {
                return;
            }
            btn_target.addClass("disabled");
            var data = {
                cat_id: catIdNode.val(),
                name: nameNode.val(),
                price: priceNode.val(),
                summary: summary,
                main_image: $(".wrap_food_set .pic-each .del_image").attr("data"),
                stock: stockNode.val(),
                tags: $.trim(tagsNode.val())
            };
            var id = idNode.val() || 0;
            $.ajax({
                url: common_ops.buildUrl("/cms/food/set/" + id),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    common_ops.alert(res.msg, function () {
                        location.assign(common_ops.buildUrl('/cms/food/index'));
                    });
                },
                error: function (res) {
                    errorTipOrAlert(res, 'tip', dataNode);
                },
                complete: function () {
                    btn_target.removeClass("disabled");
                }
            });
        });
    },
    initEditor: function () {
        this.ue = UE.getEditor('editor', {
            toolbars: [
                ['undo', 'redo', '|',
                    'bold', 'italic', 'underline', 'strikethrough', 'removeformat', 'formatmatch', 'autotypeset', 'blockquote', 'pasteplain', '|', 'forecolor', 'backcolor', 'insertorderedlist', 'insertunorderedlist', 'selectall', '|', 'rowspacingtop', 'rowspacingbottom', 'lineheight'],
                ['customstyle', 'paragraph', 'fontfamily', 'fontsize', '|',
                    'directionalityltr', 'directionalityrtl', 'indent', '|',
                    'justifyleft', 'justifycenter', 'justifyright', 'justifyjustify', '|', 'touppercase', 'tolowercase', '|',
                    'link', 'unlink'],
                ['imagenone', 'imageleft', 'imageright', 'imagecenter', '|',
                    'insertimage', '|',
                    'horizontal', 'spechars', '|', 'inserttable', 'deletetable', 'insertparagraphbeforetable', 'insertrow', 'deleterow', 'insertcol', 'deletecol', 'mergecells', 'mergeright', 'mergedown', 'splittocells', 'splittorows', 'splittocols']

            ],
            enableAutoSave: true,
            saveInterval: 60000,
            elementPathEnabled: false,
            zIndex: 4,
            serverUrl: common_ops.buildUrl('/cms/upload/ueditor')
        });
    },
    delete_img: function () {
        $(".wrap_food_set .del_image").unbind().click(function () {
            $(this).parent().remove();
        });
    },
    validate: function (catIdNode, nameNode, priceNode, summaryNode, summary, mainImageNode, stockNode, tagsNode) {
        var cat_id = catIdNode.val(),
            name = nameNode.val(),
            price = priceNode.val(),
            summary = summary,
            stock = stockNode.val(),
            tags = $.trim(tagsNode.val());
        var priceReg = /^\d+\.?\d{0,2}$/;

        if (!cat_id || !parseInt(cat_id) || parseInt(cat_id) < 1) {
            common_ops.tip("请指定商品种类", catIdNode);
            return false;
        }
        if (!(name.length >=2 && name.length <=20)) {
            common_ops.tip("商品名必须为2到20个字符", nameNode);
            return false;
        }
        if (!priceReg.test(price)) {
            common_ops.tip("商品价格必须为正数，可以保留1到2个小数位", priceNode);
            return false;
        }
        if ($(".wrap_food_set .pic-each").size() < 1) {
            common_ops.tip("请上传封面图", mainImageNode);
            return false;
        }
        if (!summary) {
            common_ops.tip("请写一些商品信息", summaryNode);
            return false;
        }
        if (!stock || !parseInt(stock) || parseInt(stock) < 0) {
            common_ops.tip("商品库存不能小于0且是正整数", stockNode);
            return false;
        }
        if (tags.length < 1) {
            common_ops.tip("至少填写一个商品标签, 并按回车键确认", tagsNode.parent());
            return false;
        }
        return true;
    }
};

$(document).ready(function () {
    food_set_ops.init();
});