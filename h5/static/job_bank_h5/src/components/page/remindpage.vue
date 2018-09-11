<template>
    <!-- 已登录 -->
    <div class="logincontent" v-if="user.user_id!=''">
       <header class="g-header">
            <h2 class="hd">我的提醒</h2>
            <img src="../../assets/imgs/返回_2.png"  @click="backto" class="backimg" alt="">
       </header>
       <div class="tc mt90" v-if="noticeslist==''">
          <p class="no-message">前方暂未消息传来，雷达情报搜集中</p>
          <button type="button" class="no-message-button" @click="ShowModel">开启职位订阅</button>
       </div>
       <div v-else class="mt90">
          <div class="sp-title">
                <div class="remind-setting">
                    <button class="remind-trigger"  @click="ShowModel"> 修改订阅设置 </button>
                </div>
          </div>
          <div class="notices" v-for="item in noticeslist">
            <router-link  :to="{ name: 'remindInfo', params: { notice_id: item.id }}" >
               <span class="title" v-if="item.status==0">{{item.notice_info}}</span>
               <span class="ydtitle" v-else>{{item.notice_info}}</span>
               <span class="time">{{item.create_time}}</span>
            </router-link>
          </div>
          <div class="load-more" v-if="showmore">
              <button type="button" id="job-next-page" @click="getmore()">加载更多</button>
          </div>
          <div class="no-more" v-else>
              <span><i class="icon-nomore"></i>没有更多内容了哦~</span>
          </div>
       </div>
      

      <!--  订阅设置 模态框 -->
        <div v-show="showmodel" class="mask login"  @click.self="cancel_change_login">   
            <div class="form">
               <img class='close' src='../../assets/imgs/close.png'  @click.self='cancel_change_login'>
              <div id="" class="layui-layer-content">
                  <div class="set_content">
                      <div class="set_head">
                          <h3 style="margin: 0">订阅设置</h3>
                      </div>
                      <div class="set-region">
                          <div class="region-t type-t mt40px">
                              <span>报考地区</span>
                          </div>
                          <div class="region-c">
                              <span>北京</span>
                              <em>修改地区请在"<a @click="gotomyjl">我的简历</a>"中编辑</em>
                          </div>
                      </div>
                          <div class="set-type">
                              <div class="region-t type-t">
                                  <span>考试类型</span>
                              </div>
                              <div class="type-c">
                                <ul>
                                  <li v-for="(item,index) in news_type" :key="index">
                                    <label :id="item.id" class="switch-ios"  :data-id="item.id" 
                                      @click.prevent="selectli(item.id,$event)">
                                        <input type="checkbox" :value="item.id" name="remindset">
                                        <i style="left: 0px;"></i>
                                    </label>
                                    <span>{{item.title}}</span>
                                  </li>                                                    
                                </ul>                              
                              </div>
                          </div>
                      <div class="set-preserve">
                          <!-- <button type="button" class="save-remind-set">保存</button> -->
                          <span>开启后，公考黑板报每天都会为你推送适合你的岗位哦</span>
                      </div>
                  </div>
              </div>
            </div>
        </div>
    </div>



    <!-- 未登录 -->
    <div class="logincontent"  v-else>
      <header class="g-header">
            <h2 class="hd">我的提醒</h2>
            <img src="../../assets/imgs/返回_2.png"  @click="backto" class="backimg" alt="">
       </header>
      <div class="notlogin-follow">
          <p>登录后才能查看我的消息~</p>
          <button class="btn-red open-register-win" @click="showlogin" >登录</button>
      </div>
      <div v-if="loginmodel">
          <login> </login>          
      </div>
    </div>
</template>

<script>

import { api_get_news_type } from "../../networks/News"
import { api_get_user_subslist } from "../../networks/remind"
import { api_post_user_subslist } from "../../networks/remind"

import { api_get_user_noticeslist } from "../../networks/remind"

import login from '../smallcommon/login.vue'




export default {
	name: 'HelloWorld',
	data () {
		return {
      showmodel:false,
      news_type:[],
      noticeslist:[],
      showmore:true,
      pageNum:1,
      loginmodel:false
		}
	},
	computed: {
     user() {
           return this.$store.state.user
      },
       updateShowmodel() {
          return this.$store.state.loginmodel
        },
  },
  watch: {
        updateShowmodel: {
            deep: true,
            handler: function (val) {
                this.loginmodel = val;
            }
        },
        user: {
            deep: true,
            handler: function (val) {
                this.getnoticeslist();
            }
        },
    },
  created: function() { 
      var context = this;
      var promise = api_get_news_type(context);
      promise.then(function(res) {
        context.news_type=res.cates;
        //console.log(res.cates);  
        context.getusersubslist();        
      }).catch(function(error){
          console.error(error);
      });

      //获取列表list
      context.getnoticeslist();
  },
  methods: {
  	  getusersubslist() { //1.获取用户的订阅type
            var context = this;
            var user_id=this.user.user_id;
            //var user_id='110119';
            var promise = api_get_user_subslist(context,user_id);
            promise.then(function(res) {
                //console.log(res);
                if (res.code == '200') {
                   for (var i = 0; i<res.data.length ; i++) {
                      for (var j = 0; j<context.news_type.length ; j++) {
                          var cate_id=res.data[i].cate_id;
                          var news_type_id=context.news_type[j].id;
                          if(cate_id==news_type_id){
                              $("#"+cate_id).addClass('open');
                              $("#"+cate_id).find('i').animate({left: 20}, 200);
                          }
                          
                      }
                   }
                }

            }).catch(function(error){
                console.error(error);
            });
      },
      ShowModel() { 
           var context = this;
           context.showmodel=true;
      },
      cancel_change_login() { 
           var context = this;
           context.showmodel=false;
      },
      selectli(id,event){  //2.选择订阅类型
          var context = this;
          var el = event.target.className;
          if(event.target.id==id){
              if(el.indexOf("open") != -1 ){
                  //关
                  event.target.className='switch-ios';
                  $("#"+id).find('i').animate({left: 0}, 200);
                  context.postusersubslist(id,0);
              }
              else{//开
                  event.target.className='switch-ios open';
                  $("#"+id).find('i').animate({left: 20}, 200);
                   context.postusersubslist(id,1);
              }
          }
      },
      postusersubslist(id,isopen){  //3.开始订阅
            var context = this;
            var user_id=context.user.user_id;
            //var user_id='110119';          
            var promise = api_post_user_subslist(context,id,user_id,isopen);
            promise.then(function(res) {
              console.log(res);         
            }).catch(function(error){
                console.error(error);
            });

      },
      getnoticeslist(){  //4.获取订阅消息列表
          var context = this;
          var user_id=context.user.user_id;
          var pageNum=context.pageNum;
          var pageSize=20;
          //var user_id='110119';          
          var promise = api_get_user_noticeslist(context,user_id,pageNum,pageSize);
          promise.then(function(res) {
             console.log("获取订阅消息列表");     
             console.log(res);     
             if(res.code=='200'){
                context.noticeslist= context.noticeslist.concat(res.data);
                if (res.data==''){                   
                    context.showmore= false;
                }
             }    
          }).catch(function(error){
              console.error(error);
          });

      },
      showlogin(){
          var context = this;
          var user_id=context.user.user_id;
          if(user_id==''){
                context.$router.push({ path: '/login'})
          }    
          
      }, 
      getmore() {      
         var context = this;
         context.pageNum++;
         context.getnoticeslist();
       },
       gotomyjl() {      
          this.$router.push({ path: '/myresume' })
       },
       backto() {   
            this.$router.push({ path: '/personpage'}) 
        }

  }

}
</script>


<style scoped>
.logincontent{
   width: 100%;
    min-height: 810px;
    background: #fff;
    padding: 15px 15px;
    border: 1px solid #f1f4f6;
}
.no-message-button {
    display: block;
    padding: 0 50px;
    height: 35px;
    line-height: 35px;
    background: #fff;
    border: 1px solid #ff6666;
    color: #ff6666;
    font-size: 14px;
    margin: 25px auto;
}
.no-message{
        text-align: center;
    padding-top: 20px;
    font-size: 14px;
    color: #A6B6C7;
        outline: none;
}
.login .form {
     width: 100%;
    padding: 20px 5px 40px 5px;
    margin: auto;
    margin-top: 4%;
    left: 0;
    right: 0;
    background: #fff;

        border-radius: 5px;
}
.mask {
    position: fixed;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    background: rgba(0, 0, 0, 0.4);
    z-index: 999;
}
.close{
      right: 20px;
    top: 20px;
    cursor: pointer;
    width: 20px;
}
.set_content {
       width: 100%;
    background: #fff;
    padding: 22px 16px;
}
.set_content .set_head {
    height: 34px;
    color: #202a34;
}

.set_content .set_head h3 {
    font-size: 18px;
    line-height: 34px;
    float: left;
    display: inline-block;
}
.set_content .region-t {
    height: 30px;
    line-height: 30px;
    font-size: 14px;
    color: #959ba0;
    position: relative;
    margin-top: 18px;
}
.set_content .region-t:before {
    content: "";
    width: 530px;
    height: 1px;
    display: block;
    background: #edf1f2;
    line-height: 30px;
    position: absolute;
    top: 15px;
    left: 70px;
}

.set_content .region-t span {
    width: 80px;
    background: #fff;
    height: 30px;
    line-height: 30px;
    font-size: 14px;
}
.set_content .region-c {
    height: 24px;
    padding-left: 80px;
}
.set_content .region-c span {
    font-size: 14px;
    color: #202a34;
    height: 24px;
    line-height: 24px;
    display: inline-block;
}
.set_content .region-c em {
    float: right;
    color: #667275;
    font-size: 12px;
    padding: 0;
}

em, i {
    font-style: normal;
}
a {
    color: #262626;
    text-decoration: none;
    cursor: pointer;
}

.set_content .type-t {
    margin-top: 10px;
}

.set_content .set-preserve {
    clear: both;
    height: 36px;
    line-height: 36px;
    margin-top: 35px;
    margin-bottom: 10px;
}
.set_content .set-preserve span {
    color: #667275;
    font-size: 14px;
}
.tc{
  text-align:center;
  margin-top:50px;
}

.layui-layer-page .layui-layer-content {
    position: relative;
    overflow: auto;
}

.set_content .set-type ul {
    padding: 8px 0;
    height: 120px;
}
.set_content .set-type ul li {
    width: 50%;
    height: 40px;
    line-height: 40px;
    float: left;
    padding-left: 27px;
}
.set_content .set-type ul li .switch-ios {
    position: relative;
    top: 15px;
}

.switch-ios.open {
    background: #f89e9a;
}
.switch-ios {
    height: 6px;
    width: 34px;
    background: #cdd5d7;
    -moz-border-radius: 25px;
    -webkit-border-radius: 25px;
    -o-border-radius: 25px;
    -ms-border-radius: 25px;
    -khtml-border-radius: 25px;
    border-radius: 25px;
    position: relative;
    cursor: pointer;
}
.switch-ios input {
    opacity: 0;
    filter: alpha(opacity=0);
    -moz-opacity: 0;
    -khtml-opacity: 0;
}
.switch-ios.open i {
    background: #f3554d;
}

.switch-ios i {
    position: absolute;
    left: 0;
    top: -5px;
    display: inline-block;
    width: 15px;
    height: 15px;
    -moz-border-radius: 50%;
    -webkit-border-radius: 50%;
    -o-border-radius: 50%;
    -ms-border-radius: 50%;
    -khtml-border-radius: 50%;
    border-radius: 50%;
    background: #969fa1;
}
em, i {
    font-style: normal;
}
.set_content .set-type ul li span {
    display: inline-block;
    height: 40px;
    font-size: 14px;
    padding-left: 10px;
}
.notlogin-follow {
    text-align: center;
    padding-top: 200px;
}
.notlogin-follow p {
    font-size: 16px;
    line-height: 40px;
    color: #666666;
    margin-bottom: 20px;
}

.notlogin-follow button {
    width: 200px;
    height: 40px;
    line-height: 40px;
    -moz-border-radius: 5px;
    -webkit-border-radius: 5px;
    -o-border-radius: 5px;
    -ms-border-radius: 5px;
    -khtml-border-radius: 5px;
    border-radius: 5px;
    font-size: 16px;
}
.btn-red {
    background: #f3554d !important;
    color: #fff;
    border: none;
}
.sp-title {
    color: #202a34;
    padding-bottom: 20px;
    padding-top: 10px;
}
.sp-title span {
    font-size: 18px;
    margin-left:15px;
}
.sp-title .remind-setting {
    float: right;
    position: relative;
}
.sp-title .remind-setting .remind-trigger {
    float: right;
    background: #fff;
    -moz-border-radius: 2px;
    -webkit-border-radius: 2px;
    -o-border-radius: 2px;
    -ms-border-radius: 2px;
    -khtml-border-radius: 2px;
    border-radius: 2px;
    border: 1px solid #fd6367;
    padding: 0 10px;
    color: #fd6367;
    line-height: 23px;
}
.notices {
  padding:10px;
  cursor: pointer;
   border-bottom: 1px solid #efefef;
   
}
.notices .title{
  font-size:14px;
 color:#606266;
 }
.notices .ydtitle{
  font-size:14px;
 color:#ccc;
 }


.notices .time{
  font-size:12px;
  color:#909399;
  margin-left:15px;
}



.load-more {
    padding: 20px 0;
    text-align: center;
}
.load-more button {
    padding: 0 50px;
    height: 35px;
    line-height: 35px;
    background: #fff;
    border: 1px solid #ff6666;
    color: #ff6666;
    font-size: 14px;
    outline:none;
}
.no-more {
    padding: 20px 0;
    text-align: center;
}

.hide {
    display: none!important;
}
.no-more span {
    display: inline-block;
    font-size: 14px;
    color: #BCC6D1;
    background: #fff;
    height: 30px;
    line-height: 30px;
    z-index: 1;
}
.no-more span i {
    float: left;
    margin-right: 15px;
    font-size: 45px;
}
em, i {
    font-style: normal;
}
.isread{
  color:#ccc;
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
    text-align: center!important;
    padding: 0 12px;
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
  margin-top:30px;
}
.backimg{
    width:23px;
    position: absolute;
    top: 10px;
    left: 5px;
}

</style>
