import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'



/*  获取用户订阅的订阅栏目 - ~  */
export function api_get_user_subslist(context,user_id) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/jobbank/news/user/cate/subs/list?user_id="+user_id
      axios.get(base_url).then((response) => {
        resolve(response.data);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};


/*  提交用户订阅的订阅栏目 - ~  */
export function api_post_user_subslist(context,cate_id,user_id,open_or_close) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/jobbank/news/user/cate/subs?user_id="+user_id+"&cate_id="+cate_id+"&open_or_close="+open_or_close
      axios.get(base_url).then((response) => {
        resolve(response);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};

/*  获取用户订阅消息列表 - ~  */
export function api_get_user_noticeslist(context,user_id,pageNum,pageSize) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/jobbank/news/user/cate/subs/notices?user_id="+user_id+"&pageNum="+pageNum+"&pageSize="+pageSize
      axios.get(base_url).then((response) => {
        resolve(response.data);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};





/*  获取用户订阅的订阅栏目的通知的新闻 - ~  */
export function api_get_user_noticesinfo(context,notice_id) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/jobbank/news/user/cate/subs/notices/info?notice_id="+notice_id
      axios.get(base_url).then((response) => {
        resolve(response.data);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};








