// 页面配置项
// var urls = new UrlsList('test');
// var user_id='110119';
var urls = new UrlsList();

// ---------------------------- LIB ------------------------------ //
// 定义变量：
function UrlsList(n) {
  // this.base = "http://api.platform.winlesson.com";
  this.base ="http://api.msg.platform.winlesson.com";
  this.test = "http://test.api.platform.winlesson.com";
  var base_url = n == 'test' ? this.test : this.base;
  this.activity_id = n == 'test' ? 2 : 1;
  this.activity = base_url + "/api/user_register/activity_page/info"; // 老带新活动页面
  this.share = base_url + "/api/user_register/share_page/info"; // 老带新分享页面
  this.collect = base_url + "/api/user_register/collect"; // 领取礼包
  return this;
}
// ------------------------------------LIB-----------------------------------//
// 获取URL参数
function getQueryString(name, str) {
  var s = str || window.location.search;
  var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
  var r = s.substr(1).match(reg);
  if (r != null) return unescape(r[2]);
  return null;
}
// 阻止默认事件
function stopDefault(e) {
  //阻止默认浏览器动作(W3C)
  if (e && e.preventDefault) e.preventDefault();
  //IE中阻止函数器默认动作的方式
  else window.event.returnValue = false;
  return false;
}
// 默认从APP获取user_id的函数：
function postUserIdStr(str) {
  window.user_id = str;
}
