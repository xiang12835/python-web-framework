import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

  /*  职位检索 - ~  */
export function api_get_job_list(context,province_id,area_id,system_id,department_id,pageNum,pageSize) {
  var promise = new Promise(function(resolve,reject){
     
      var params = [
            "province_id="+province_id,
            "area_id="+area_id,
            "system_id="+system_id,
            "department_id="+department_id,
            "pageNum="+pageNum,
            "pageSize="+pageSize,
            "app_id=7"
        ]
        var str_params = params.join("&");
        var base_url = "https://api.web.platform.winlesson.com/api/jobbank/v6/nation/item_list?"+str_params;  

      console.log(base_url);
      axios.get(base_url).then((response) => {
        resolve(response.data.result);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};



/*  职位库职位列表 - ~  */
export function api_get_dept_joblist(context,department_id,user_id) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/jobbank/fit/job_list?department_id=" + department_id+"&user_id="+user_id+"&app_id=7"
      axios.get(base_url).then((response) => {
        resolve(response.data.result);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};





/*  职位库职位详情 - ~  */
export function api_get_job_info(context,job_id) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/jobbank/v5/job_detail?job_id=" + job_id
      axios.get(base_url).then((response) => {
        resolve(response.data.result);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};

/*  我的职位收藏 - ~  */
export function api_get_my_jobs(context,pageNum,wxopenid) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/jobbank/collect/list?pageSize=20&appid=6&pageNum=" + pageNum + '&openid=' + encodeURIComponent(wxopenid)
      axios.get(base_url).then((response) => {
        resolve(response.data.result);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};


/*  收藏职位 - ~  */
export function api_get_collect_job(context,jobid,wxopenid) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/jobbank/user/collect?appid=6&job_id=" + jobid + "&openid=" + encodeURIComponent(wxopenid)
      axios.get(base_url).then((response) => {
        resolve(response);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};







