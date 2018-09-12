import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

/*  获取公众号登录图片 - ~  */
export function api_get_gzh_img(context,app_id) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/gzh/qrcode/login?app_id=7"
      axios.get(base_url).then((response) => {
        resolve(response.data);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};



/*  获取小程序登录图片 - ~  */
export function api_get_qrcode_img(context,app_id) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/xcx/qrcode/login?app_id=7"
      axios.get(base_url).then((response) => {
        resolve(response.data);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};


/*  3秒轮询 - ~  */
export function api_get_polling_login(context,scene) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/gzh/polling/login?app_id=7&scene="+scene
      axios.get(base_url).then((response) => {
        resolve(response);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};



/* 账号密码登录 */

export function api_gzh_login(context,phone,openid,scene,avatarUrl,gender,nickName) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/gzh/qrcode/user_login?app_id=7&phone="+phone+"&openid="+openid+"&scene="+scene+"&avatarUrl="+avatarUrl+"&gender="+gender+"&nickName="+nickName
      
      axios.post(base_url).then((response) => {
        resolve(response);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};
