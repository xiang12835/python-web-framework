import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
  /*  获取国考下地区  */
export function api_get_area_list(context,province_id) {
  var promise = new Promise(function(resolve,reject){
      var date=new Date;
      var year=date.getFullYear(); 
      var base_url = "https://api.web.platform.winlesson.com/api/jobbank/v5/area_list?province_id=" + province_id+"&year="+ year;   
      axios.get(base_url).then((response) => {
        resolve(response.data.result);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};

/*  获取省考下省份  */
export function api_get_province_list(context) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/jobbank/v5/province_list"
      axios.get(base_url).then((response) => {
        resolve(response.data.result);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};


/*  获取国考下系统类型 */
export function api_get_type_list(context,area_id) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/jobbank/v5/system_list?province_id=1&area_id=" + area_id
      axios.get(base_url).then((response) => {
        resolve(response.data.result);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};



/*  获取招考单位 */
export function api_get_dept_list(context,area_id, system_id) {
  var promise = new Promise(function(resolve,reject){
      var base_url = "https://api.web.platform.winlesson.com/api/jobbank/v5/system/departments?province_id=1&area_id=" + area_id + '&system_id=' + system_id
      axios.get(base_url).then((response) => {
        resolve(response.data.result);
      }).catch((response) => {
        console.log(response);
        reject(response);
      });
  });
 return promise;
};






















