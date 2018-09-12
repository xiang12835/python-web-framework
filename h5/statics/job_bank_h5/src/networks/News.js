import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

/*  获取资讯分类详情 - ~  */
export function api_get_new_list(context,category_id,areaname,sfarea_name,pageNum,pageSize) {
  var promise = new Promise(function(resolve,reject){
      	var date=new Date;
      	var year=date.getFullYear(); 
     
	    var params = [
	        "category_id="+category_id,
	        "area="+areaname,
	        "district="+sfarea_name,
	        "pageNum="+pageNum,
	        "pageSize="+pageSize
	    ]
	    var str_params = params.join("&");
	    var base_url = "https://api.web.platform.winlesson.com/api/job/news/category/notices?"+str_params;  

      	console.log(base_url);
      	axios.get(base_url).then((response) => {
       	 	resolve(response.data);
      	}).catch((response) => {
      	  	console.log(response);
       	 	reject(response);
      	});
  });
 return promise;
};




/*  获取招考公告资讯分类列表 - ~  */
export function api_get_news_type(context) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/job/news/categorys"
      axios.get(base_url).then((response) => {
        resolve(response.data.result);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};



/*  公告详情 - ~  */
export function api_get_new_info(context,news_id) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/job/news/info?news_id="+news_id
      axios.get(base_url).then((response) => {
        resolve(response.data.data);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};

/*  公告详情 - ~  */
export function api_get_new_info_v2(context,news_id) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/job/news/info?news_id="+news_id
      axios.get(base_url).then((response) => {
        resolve(response.data);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};

/*  我的公告收藏 - ~  */
export function api_get_my_news(context,pageNum,wxopenid) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/jobbank/news/collect/list?pageSize=20&appid=6&pageNum=" + pageNum + '&openid=' + encodeURIComponent(wxopenid)
      axios.get(base_url).then((response) => {
        resolve(response.data.result);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};

/*  收藏公告 - ~  */
export function api_get_collect_news(context,news_id,wxopenid) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/jobbank/news/user/collect?appid=6&news_id=" + news_id + "&openid=" + encodeURIComponent(wxopenid)
      axios.get(base_url).then((response) => {
        resolve(response);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};



