// 微信分享页面：
var appId = "wx0b1eadfbf4f45765",
  wxtitle = "送你《公务员考试白皮书》", //标题
  wxlink = window.location.hostname + "/static/local_html" + "/invitatiton_activity/share.html?user_id" + window.user_id, //默认为空
  wximg = window.location.hostname + "/static/local_html" + "/invitatiton_activity/img/icon.png", //分享图片
  wxdesc = "必胜公考，提供资讯、做题、上课、答疑一站式备考服务"; //描述
// 获取微信接口
$.ajax({
  url: "http://api.msg.platform.winlesson.com/api/wxpub/get_signature?appId=" + appId + "&pageUrl=" + window.location.hostname,
  type: 'get',
  async: false,
  success: function(res){
    wx.config({
      debug: true,
      appId: appId,
      timestamp: res.result.timestamp,
      nonceStr: res.result.nonceStr,
      signature: res.result.signature,
      jsApiList: ['onMenuShareTimeline', //分享朋友圈
        'onMenuShareAppMessage', //分享给好友
      ]
    });
  }
})
// 具体执行：
wx.error(function(res) {
  console.log(res);
});
wx.ready(function() {
  console.log("weixin ready");
  wx.onMenuShareTimeline({
    title: wxtitle, // 分享标题
    link: wxlink, // 分享链接
    imgUrl: wximg, // 分享图标
    success: function(data) {
      // 用户确认分享后执行的回调函数
      console.log(data);
    },
  });
  wx.onMenuShareAppMessage({
    title: wxtitle,
    desc: wxdesc,
    link: wxlink,
    imgUrl: wximg,
    type: '', // 分享类型,music、video或link，不填默认为link
    dataUrl: '', // 如果type是music或video，则要提供数据链接，默认为空
    success: function(data) {
      // 用户确认分享后执行的回调函数
      console.log(data);
    },
  });
});
