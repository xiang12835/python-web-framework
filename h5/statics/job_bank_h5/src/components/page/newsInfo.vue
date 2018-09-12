<template>
  <div class="newsinfo">
      <header class="g-header mb10">
          <h2 class="hd">公告详情</h2>
          <img src="../../assets/imgs/返回_2.png"  @click="backto" class="backimg" alt="">
          <img src="../../assets/imgs/home.png"  @click="backtohome" class="iconxxtx" alt="">
      </header>
      <div v-html="maintext" class="mt90">
        {{maintext}}
      </div>
      <div class="center">
        <button  class='g-detail-btn'  @click="scNews">{{scname}}</button>
      </div>
      
  </div>
</template>

<script>
import { api_get_new_info_v2 } from "../../networks/News"
import { api_get_collect_news } from "../../networks/News"



export default {
  name: 'newsinfo',
  data () {
    return {
        maintext:'',
        scname: '收藏公告',
    }
  },
  computed: {
    user() {
        return this.$store.state.user
    },
    router_news_id() {
      return this.$route.params.news_id;
    },
    stateOpenid() {     
        return this.$store.state.openid;
    },
  },
  created: function() {
      var context = this;
      context.get_news_info();

      

  },
  methods: {
    get_news_info() {       
          var context = this;
          var new_id =context.router_news_id;
          var promise = api_get_new_info_v2(context,new_id);
          promise.then(function(res) {
            console.log(res);
              context.maintext =res.data.content;
              var maintext=context.maintext;
              
              // var maintext = maintext.replace(/<\/?[^>]*>/g, ''); //去除HTML Tag
              // maintext = maintext.replace(/(^\s*)|(\s*$)/g, "") //去除行尾空格
              // maintext = maintext.replace(/&npsp;/ig, ''); //去掉npsp
              var link = window.location.href;
              var title = res.news.title;
              context.wxShare(title, '你的朋友给你分享了一个职位，快来查看吧', link);
          }).catch(function(error){
              console.error(error);
          });
    },
    scNews(){
          var context = this;
          var new_id =context.router_news_id;
          var wxopenid=context.stateOpenid;
          var userid=context.user.user_id;
          if(userid!=''){
              var promise = api_get_collect_news(context,new_id,wxopenid);
              promise.then(function(res) {
                  console.log(res);
                  if (res.data.code == '200') {
                    context.$message({
                          message: '收藏成功',
                          type: 'success'

                        });
                    context.scname="已收藏";
                  }

              }).catch(function(error){
                  console.error(error);
              });
          }
          else{
             context.$message({
                  message: '请先登录',
                  type: 'warning'
                });
              //去登录
               context.$router.push({ path: '/login'})
          }
         
      },
      backto() {   
            this.$router.go(-1)
      },
      backtohome() {   
            this.$router.push({ path: '/' })
      },

  }

}
</script>


<style scoped>
.newsinfo{
   width: 100%;
    min-height: 810px;
    background: #fff;
    padding: 15px 15px;
    margin-bottom:70px;
}
  .g-detail-btn {
        background-color: #f1514e;
    color: #fff;
    line-height: 31px;
    font-size: 12px;
    -webkit-box-flex: 1;
    -ms-flex: 1;
    flex: 1;
    border-radius: 5px!important;
    right: 10px;
    top: 51px;
    padding: 0px 9px;
    border: none;
    outline: none;
    height: 30px;
    margin-top:10px;
}
.backimg{
    width:23px;
     position: absolute;
    top: 10px;
    left: 5px;
}

.mb10{
    margin-bottom:10px;
}

.center{
      text-align: center;
}
.g-header {
    position: fixed;
    left: 0;
    top: 0;
    z-index: 1;
    z-index: 8;
    width: 100%;
    height: 45px;
    line-height: 45px;
    background-color: #f1514e;
    color: #fff;
  
}
.g-header .hd {
    font-size: 16px;
    text-align: center;
    text-overflow: -o-ellipsis-lastline;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
       margin: 14px auto;
       width: 100px;
          display: flex;
    justify-content: center;
}
.mt90{
  margin-top:45px;
}
.g-header .iconxxtx{
   position: absolute;
    right: 10px;
    top: 10px;
    z-index: 1;
    color: #fff;
    font-size: 0.67rem;
    width: 23px;
    text-align: center;
}
</style>
