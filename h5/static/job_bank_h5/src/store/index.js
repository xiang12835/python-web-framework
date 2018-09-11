import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import md5 from 'js-md5'


import VuexPersistence from 'vuex-persist'
const vuexLocal = new VuexPersistence({//配置
    storage: window.localStorage,
    supportCircular: true,
});

Vue.use(Vuex)

const state = {
  user:{
    user_id:'',
    username: '',
    nickname: '',
    current_exam_type_id: '',
    is_fighting_user: 0,
    image_url: '',
    sex: 0, //(1, '男'), (2, '女')
    type: 0, //(0, '普通用户'), (1, '老师'), (2, '助教'), (9, '测试帐号'),
    vip: 0,   
  },
  userInfo:{
    city:'',
    country:'',
    headimgurl:'',
    language:'',
    nickname:'',
    openid:'',
    privilege:'',
    province:'',
    sex:''
  },
  historylist:[],
  openid:'',
  scene:'',
  loginmodel:false,
  //国考省考地区 
  isgk:1,
  Areaid:'',
  Areaname:'',
  Provinceid:'',
  Provincename:'',
  ProvinAreaid:'',
  ProvinAreaname:'',
  Typeid:'',
  Deptid:'',
  Category_id:'',
  firstshowimg:'',
  prszimg:'',
  imgdata:{
    image_url:'',
    show:'',
    title:''
  },
}

const store = {
  state,
  mutations: {   
    //国考 省考 地区 
    updateIsgk(state,isgk){
      state.isgk=isgk;    
    },
    updateAreaid(state,id){
      state.Areaid=id;
    },
    updateProvinceid(state,id){
      state.Provinceid=id;
    },   
    updateProvinAreaid(state,id){
      state.ProvinAreaid=id;
    },
    updateAreaname(state,name){
      state.Areaname=name;
    },
    updateProvincename(state,name){
      state.Provincename=name;
    },
    updateProvinAreaname(state,name){
      state.ProvinAreaname=name;
    },
    //系统类型  招考单位
    updateSystemid(state,id){
      state.Typeid=id;
    },
    updateDepartmentid(state,id){
      state.Deptid=id;
    },
    //资讯
    updateCategory_id(state,id){
      state.Category_id=id;
    },
    //小程序登录标识
    updateScene(state,scene){
      state.scene=scene;
    },
    //登录窗口显示和隐藏
    updateShowmodel(state,dd){
      state.loginmodel=dd;
    },
     // 账号：
    userLogin(state, user_info) {
      for (var key in user_info) {
        state.user[key] = user_info[key]
        localStorage.setItem(key, state.user[key])
      }
      return state.user
    },
    getopenid(state,openid) {
      state.openid=openid;
      localStorage.setItem("openid", openid)
    },
    keep_user_login(state) {
      if (state.user.user_id != '') return false
      for (var key in state.user) {
        state.user[key] = localStorage.getItem(key)
      }
    },
    user_logout(state) {//退出
      
      for (var key in state.user) {
        state.user[key] = ''
      }
      state.openid = ''
    },
    //搜索de历史记录
     updatehistorylist(state,historylist) {
      state.historylist=historylist;
    },
    //获取userinfo
    userInfoLogin(state, user_info) {
      for (var key in user_info) {
        state.userInfo[key] = user_info[key]
      }
      return state.userInfo
    },
    //引导图仅第一次显示
    updatafirstshowimg(state, val) {
        state.firstshowimg=val;    
    },
    //后台返回的照片地址
    updateimg(state, val) {
        state.prszimg=val;    
    },
    //拍颜识值结果用于分享
    updateperson(state, data) {
      for (var key in data) {
        state.imgdata[key] = data[key]
      }
      return state.imgdata 
    },
  },
  actions: {
    userLogin(context, user_id) {
      var urls='https://api.web.platform.winlesson.com/user/info/detail'
      axios.get(urls + "?user_id=" + user_id).then(function(response) {
        if (response.data.code != 200) {
          return false
        }
        context.commit('userLogin', response.data.userinfo);
      })
    },
    
  },
  plugins: [vuexLocal.plugin]//添加插件
}
export default new Vuex.Store(store)
