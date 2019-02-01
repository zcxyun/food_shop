;
var comment_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $("select[name=status]").change(function () {
            $('.form-inline.wrap_search').submit();
        });
        $("select[name=food]").change(function () {
            $('.form-inline.wrap_search').submit();
        });
        $("select[name=score]").change(function () {
            $('.form-inline.wrap_search').submit();
        });
    }
};

$(document).ready(function () {
    comment_ops.init();
});