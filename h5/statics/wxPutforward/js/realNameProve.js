!function() {
    var o = location.href;
    $(".js_hide").click(function() {
        $(".js_cover").hide(),
        $(".js_fail_info").hide()
    });
    var r = function(e, t) {
        t = "object" == typeof t ? JSON.stringify(t) : t,
        localStorage.setItem(e, t)
    };
    var t = {
        show: !1,
        msg: "提示内容"
    }
      , n = function(e) {
        t.show = !0,
        t.msg = e,
        setTimeout(function() {
            t.show = !1
        }, 3e3)
    };
    Vue.component("pop-component", {
        template: '<transition name="fade" @after-enter="afterEnter"><div class="popInfo" v-show="obj.show">{{obj.msg}}</div></transition>',
        props: ["obj"],
        data: function() {
            return {
                show: !1
            }
        },
        methods: {
            afterEnter: function() {
                console.log("afterEnter")
            }
        }
    });
    var c = new Vue({
        el: "#attestation",
        data: {
            realname: window.localStorage.getItem("realname"),
            idcard: window.localStorage.getItem("idcard"),
            popMsg: t,
            checked: !0,
            isLoading: !1
        },
        computed: {
            passVerify: function() {
                return !!(this.realname && this.idcard && this.checked)
            }
        },
        methods: {
            uploadFile: function(e) {
                var t = e.currentTarget.files[0].size;
                2e7 <= t ? ("cardhand" == e.currentTarget.id ? n("您上传的正面照过大，请重新上传") : n("您上传的反面照过大，请重新上传"),
                $(e.currentTarget).trigger("compress", !0)) : 2e6 <= t ? $(e.currentTarget).trigger("compress", !0) : t < 2e6 && $(e.currentTarget).trigger("compress", !1)
            },
            inputFuns: function(e) {
                var t = String(e.srcElement.name);
                r(t, c[t])
            },
            submitFuns: function() {
                if (c.realname)
                    if (c.idcard) {
                        if (this.passVerify) {
                            var e = c.$refs.cardhand.getAttribute("src")
                              , t = c.$refs.cardback.getAttribute("src");
                            if (e)
                                if (t) {
                                    var r = c.$refs.cardhandFile.files[0] && c.$refs.cardhandFile.files[0].size || 0
                                      , i = c.$refs.cardbackFile.files[0] && c.$refs.cardbackFile.files[0].size || 0;
                                    if (2e7 <= r)
                                        return n("您上传的正面照过大，请重新上传"),
                                        !1;
                                    if (2e7 <= i)
                                        return n("您上传的反面照过大，请重新上传"),
                                        !1;
                                    var a = {
                                        realname: c.realname,
                                        idcard: c.idcard,
                                        cardhand: e,
                                        cardback: t
                                    };
                                    c.isLoading = !0,
                                    $.ajax({
                                        url: "/dealwithsafety/doRealNameProve",
                                        data: a,
                                        type: "post",
                                        success: function(s) {
                                            c.isLoading = !1,
                                            0 === parseInt(s.errno) ? (localStorage.clear(),
                                            n(s.errmsg),
                                            setTimeout(function() {
                                                var e, t, r, i = (e = new RegExp("(^|&)" + "backurl" + "=([^&]*)(&|$)","i"),
                                                t = window.location.search.substr(1).match(e),
                                                r = "",
                                                t && (r = decodeURIComponent(t[2])),
                                                t = e = null,
                                                r || "");
                                                if (i)
                                                    location.href = i;
                                                else if (/iscert/.test(o))
                                                    location.reload(!0);
                                                else {
                                                    var a = /\?/.test(o) ? "&" : "?"
                                                      , n = s.data.isadult ? "1" : "0";
                                                    location.href = o + a + "isadult=" + n + "&iscert=1"
                                                }
                                            }, 600)) : n(s.errmsg)
                                        },
                                        error: function() {
                                            c.isLoading = !1,
                                            n("网络异常，请稍候重试~")
                                        }
                                    })
                                } else
                                    n("请上传身份证背面");
                            else
                                n("请上传手持身份证")
                        }
                    } else
                        n("请输入身份证号");
                else
                    n("请输入真实姓名")
            }
        }
    });
    uploadImg.init({
        id: "#attestation",
        box: ".input-file-btn",
        compressHeight: 600
    }),
    setTimeout(function() {
        $(".js_fail_info").length && ($(".js_fail_info").show(),
        $(".js_cover").show(),
        $(".js_fail_info").css("left", ($(window).width() - $(".js_fail_info").width()) / 2))
    }, 100)
}();
