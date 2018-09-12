// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import store from './store'
import $ from 'jquery'
import ElementUI from 'element-ui'
import './assets/css/element/index.css'
import './assets/css/bootstrap.min.css'
import './assets/js/bootstrap.min'

// import './assets/js/html2canvas.min'
// import './assets/js/canvas2image'
// import './assets/js/base64'




Vue.config.productionTip = false

//element-ui
Vue.use(ElementUI);


Vue.prototype.GetQueryString = function (name, str){
    var s = str || window.location.search;
    var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
    var r = s.substr(1).match(reg);
    if (r != null) return unescape(r[2]);
    return null;

}


//post传参序列化(添加请求拦截器)
axios.interceptors.request.use(function (config) {
	//在发送请求之前做某件事
    if(config.method === 'post') {
    	//配置请求头
        config.headers['Content-Type'] = 'application/x-www-form-urlencoded';
    }
    return config;
  }, function (error) {
     console.log('request响应出错')
    return Promise.reject(error);
})


axios.interceptors.response.use(function (config) {
  return config;
}, function (error) {
  console.log('response响应出错');
  return Promise.reject(error)
})

router.afterEach((to,from,next) => {
  window.scrollTo(0,0);
});


Vue.prototype.wxShare = function (title, desc, link ) {
  
  const fromurl = location.href;
  // 获得签名配置
  var base_url = "https://api.web.platform.winlesson.com/api/wxpub/get_signature?appId=wx6457a8b0deb2c4e9&pageUrl="+encodeURIComponent(fromurl)
   

  axios.get(base_url).then((res) => {
    var Data = res.data.result;
    // config信息验证后会执行ready方法，所有接口调用都必须在config接口获得结果之后，config是一个客户端的异步操作，
    wx.config({
      debug: false, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
      appId:'wx6457a8b0deb2c4e9',  // 必填，公众号的唯一标识
      timestamp: Data.timestamp, // 必填，生成签名的时间戳
      nonceStr: Data.nonceStr,   // 必填，生成签名的随机串
      signature: Data.signature, // 必填，签名，见附录1
      jsApiList: ['onMenuShareAppMessage', 'onMenuShareTimeline','chooseImage','previewImage','uploadImage','downloadImage'] // 必填，需要使用的JS接口列表，所有JS接口列表见附录2
    });
  });
  wx.ready(() => {
    // 所以如果需要在页面加载时就调用相关接口，则须把相关接口放在ready函数中调用来确保正确执行。对于用户触发时才调用的接口，
    // 则可以直接调用，不需要放在ready函数中。
    wx.onMenuShareAppMessage({ // 分享给朋友
      title: title, // 分享标题
      desc: desc,   // 分享描述
      link: link,   // 分享链接 默认以当前链接
      imgUrl: 'https://h5.platform.winlesson.com/static/gklogo.png',// 分享图标
      // 用户确认分享后执行的回调函数
      success: function () {
        // if(!window.localStorage.getItem('token')) return;
        // var params = new URLSearchParams();
        // params.append('token', window.localStorage.getItem('token'));
        // params.append('type', 'share');
        // http.post(shareCallback(), params).then(res => {
        //   if (res.data.error == 0) { // 表示当天分享成功
        //     store.commit('shareChange', {
        //       isShare: true
        //     });

        //   } else {
        //     return;
        //   }
        // })
      },
      // 用户取消分享后执行的回调函数
      cancel: function () {
        console.log('分享到朋友取消');
      }
    });
    //分享到朋友圈
    wx.onMenuShareTimeline({
      title: title, // 分享标题
      desc: desc,
      link: link,
      imgUrl: 'https://h5.platform.winlesson.com/static/gklogo.png',
      // 用户确认分享后执行的回调函数
      success: function () {
        // if(!window.localStorage.getItem('token')) return;
        // var params = new URLSearchParams();
        // params.append('token', window.localStorage.getItem('token'));
        // params.append('type', 'share');
        // http.post(shareCallback(), params).then(res => {
        //   if (res.data.error == 0) { // 表示当天分享成功
        //     store.commit('shareChange', {
        //       isShare: true
        //     });
        //   } else {
        //     return;
        //   }
        // });
      },
      // 用户取消分享后执行的回调函数
      cancel: function () {
        console.log('分享到朋友圈取消');
      }
    });
  });
};


// 用 axios 进行 Ajax 请求
Vue.use(VueAxios, axios);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
