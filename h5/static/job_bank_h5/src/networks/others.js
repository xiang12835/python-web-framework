import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'



/*  热门搜索列表 - ~  */
export function api_get_search_list(context) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/job/news/hots/list"
      axios.get(base_url).then((response) => {
        resolve(response.data.data);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};


/*  搜索详情 - ~  */
export function api_get_search_info(context,name,pageNum) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/job/search/news/list?pageSize=20&text="+ name + "&pageNum=" + pageNum
      axios.get(base_url).then((response) => {
        resolve(response.data);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};



/*  保存简历 - ~  */
export function api_post_sub_resume(context,userid,openid,region_id,xl_id,inputzy,xw_id,xb_id,zzmm_id,gzjy_id,jcgzjy_id) {
  var promise = new Promise(function(resolve,reject){
      var params = [
            "user_id="+userid,
            "openid="+openid,
            "area="+region_id,
            "education="+xl_id,
            "degree="+xw_id,
            "professional="+inputzy,
            "gender="+xb_id,
            "political_status="+zzmm_id,
            "work_experience="+gzjy_id,
            "base_course="+jcgzjy_id,
            "app_id=7"
        ]
        var str_params = params.join("&");
        var base_url = "https://api.web.platform.winlesson.com/api/wx/user/resume/submit?"+str_params;  
      console.log(str_params);
      console.log(base_url);
      axios.post(base_url).then((response) => {
        resolve(response.data);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};


/*  获取用户简历 - ~  */
export function api_post_my_resume(context,user_id) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/wx/user/resume/info?user_id=" + encodeURIComponent(user_id) + "&app_id=7"
      axios.get(base_url).then((response) => {
        resolve(response.data);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};





/*  获取正在报名的职位 招考职位  近7日新增职位 - ~  */
export function api_get_somenum(context) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/jobbank/news/update/data"
      axios.get(base_url).then((response) => {
        resolve(response);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};

/*  获取消息角标 - ~  */
export function api_get_count(context,user_id) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/jobbank/news/user/cate/subs/notices/count?user_id="+user_id
      axios.get(base_url).then((response) => {
        resolve(response);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};


/*  获取微信签名 - ~  */
export function api_get_signature(context,fromurl) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/wxpub/get_signature?appId=wx6457a8b0deb2c4e9&pageUrl="+encodeURIComponent(fromurl)
      axios.get(base_url).then((response) => {
        resolve(response);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};



/*  上传文件 - ~  */
export function api_post_uploadimg(context,param) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://h5.platform.winlesson.com/t/upload/image?image="+encodeURIComponent(param)

      axios.post(base_url).then((response) => {
        resolve(response);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};


/*  用户上传头像推荐职位 - ~ - ~  */
export function api_get_recongitionimg(context,image_url) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/jobbank/image/recongition/show?image_url="+encodeURIComponent(image_url)+"&uuid=123";
      axios.get(base_url).then((response) => {
        
        resolve(response);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};





