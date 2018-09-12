<template>
  <div id="app">

    <bsk-sidebar></bsk-sidebar>

    <router-view></router-view> 

  </div>
</template>

<script>
import bskSidebar from './components/common/bskSidebar.vue'
import { api_get_signature } from "./networks/others"


export default {
  name: 'app',
  data() {
    return {

    }
  },
  components:{
    bskSidebar,

  },
  computed: {
      stateOpenid() {     
          return this.$store.state.openid;
      },
      
  },
  created: function() {
      var that= this;
      var wxopenid=that.stateOpenid;  
      var access_code=that.GetQueryString('code');      
      if (wxopenid==""){  
          console.log(location.href); 
          console.log("access_code      "+access_code);
          if ($.isEmptyObject(access_code))  
          {     
              var fromurl=location.href; 
              var url='https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx6457a8b0deb2c4e9&redirect_uri='+encodeURIComponent(fromurl)+'&response_type=code&scope=snsapi_userinfo&state=STATE&connect_redirect=1#wechat_redirect';  
              location.href=url;  
          }  
          else  
          {    
            //获取openid和userInfo
            that.getUserInfo(access_code);
          } 
      } 

  },
  methods: {
        getUserInfo(access_token){
             var that= this;
             var app_id='7';
             //获取userINfo
             var urls="https://api.web.platform.winlesson.com/api/wx/access/user?code="+access_token+"&app_id="+app_id;
              this.axios.post(urls).then(function(res){        
                    console.log("=====获取用户信息=======");
                    console.log(res.data);
                    console.log(res.data.userinfo);
                    that.$store.commit('userInfoLogin', res.data.userinfo);
                    
                    that.$store.commit('getopenid', res.data.userinfo.openid);
                    
              })
        },
     
  },


}
</script>

<style>

  html,
  body {
    width: 100%;
    height: 100%;
    font-family: -apple-system, BlinkMacSystemFont, PingFang SC, Helvetica, Tahoma, Arial, Hiragino Sans GB, Microsoft YaHei, SimSun, Heiti, sans-serif !important;
    background-color: #FFF !important;
  }
  
  @media screen and (min-width: 769px) {
    html,
    body {
      width: 460px;
      margin: 0 auto;
    }
    body {
      /*box-shadow: 0 0 30px gray;*/
      background-color: #FFF !important;
    }
  }
  
  a {
    position: relative;
    text-decoration: none;
    cursor: pointer;
  }
  .el-message {
    min-width: 179px !important;
    text-align:center;
  }

</style>