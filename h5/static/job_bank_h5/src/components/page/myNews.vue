<template>
   <div class="newsinfo"  v-if="wxopenid!=''">
      <header class="g-header">
            <h2 class="hd">我的公告收藏</h2>
             <img src="../../assets/imgs/返回_2.png"  @click="backto" class="backimg" alt="">
      </header>
      <div class="new-list mt90">
          <ul class="news-bd-list" style="padding-left:0">
              <li class="news-bd-list-li"  
                v-for="(item,index) in newsList">
                  <router-link  :to="{ name: 'newsInfo', params: { news_id: item.id }}">
                    <div class="item-hd">                        
                        {{item.title}}
                    </div>
                    <div class="item-fd">
                        <div class="fd-left">
                            <i class="mr5">公告时间</i>
                            <i class="mr10 bsk-color">{{item.inputtime}}</i>
                        </div>
                        <div class="fd-right">
                             <i class='bsk-color'>{{item.is_signing}}</i>
                        </div>
                    </div>
                  </router-link>
              </li>
          </ul>
          <div class="load-more" v-if="showmore">
              <button type="button" id="new-next-page" @click="getmore()">加载更多</button>
          </div>
          <div class="no-more" v-else>
              <span><i class="icon-nomore"></i>没有更多内容了哦~</span>
          </div>
      </div>
  </div>
  <div class="newsinfo"  v-else>
    <div class="notlogin-follow">
        <p>登录后才能查看我的公告收藏~</p>
         <button class="btn-red open-register-win" @click="showlogin" >登录</button>
    </div>
     <div v-if="loginmodel">
            <login> </login>          
        </div>
  </div>
</template>

<script>
import { api_get_my_news } from "../../networks/News"
import login from '../smallcommon/login.vue'


export default {
	name: 'newspage',
	data () {
		return {
		   newsList:[],
		   pageNum:1,
		   pageSize:20,
		   showmore:true,
       wxopenid:'',
        loginmodel:false
		}
	},
  components:{
        login
    },
	computed: {
    stateOpenid() {     
      return this.$store.state.openid;
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
        stateOpenid: {
            deep: true,
            handler: function (val) {
                this.get_mynews();
            }
        },
  },
	created: function() {
		   var context = this;
        context.wxopenid=context.stateOpenid;
        if(context.wxopenid!=''){
              context.get_mynews();
        }
   
	},
	methods: {
		get_mynews() {      
        var context = this;
  			var pageNum=context.pageNum;
  			var wxopenid=context.stateOpenid;
  			var promise = api_get_my_news(context,pageNum,wxopenid);
  	        promise.then(function(res) {
  	            console.log(res);

  	            context.newsList= context.newsList.concat(res.job_list);

  	            if (res.job_list==''){                   
  	                context.showmore= false;
  	            }

        }).catch(function(error){
            console.error(error);
        });
    },
		getmore() {      
         var context = this;
         context.pageNum++;
         context.get_mynews();
    },
    gotologin() {   
         this.$router.push({ path: '/login' })

    },
     showlogin(){
        var context = this;
        context.$store.commit("updateShowmodel",true);
        context.loginmodel = true;
        //this.$router.push({ path: '/login' })
    },
     backto() {   
        this.$router.go(-1)
    } 
	}

}
</script>


<style scoped>
.newsinfo{
   width: 100%;
    min-height: 810px;
    background: #fff;
    padding: 15px 15px;
    border: 1px solid #f1f4f6;
}
.bsk-color{
color: #f1514e;
}  
.new-list {
    background: #fff;
 
    border-top: none;
}
.probe-prompt {
    height: 30px;
    line-height: 30px;
    text-align: center;
}
.probe-prompt span {
    display: inline-block;
    font-size: 14px;
    color: #909599;
}
.probe-prompt span i {
    color: #fd6366;
    padding: 0 5px;
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
.news-bd-list-li{
    padding-left:0;
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


.news-bd-list-li:first-child{
    padding-top: 4px;
    padding-bottom: 11px;
    text-decoration:none;
}
.news-bd-list-li:not(:first-child){
    border-top: 1px solid #efefef;
    padding-top: 11px;
    padding-bottom: 11px;
    text-decoration:none;
}
.item-hd {
    font-size:14px;
    line-height: 21px;
    margin-bottom: 11px;
    text-overflow: -o-ellipsis-lastline;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
     text-decoration:none;
}
.item-fd {
    position: relative;
    color: #a5a4a4;
    font-size: 12px;
    overflow: hidden;
}
.item-fd .fd-left {
    float: left;
}
.item-fd .fd-right {
    float: right;
    position: absolute;
    right: 0;
    top: 0;
    z-index: 1;
}

.mr10{
    margin-right: 10px;
}

.mr5{
    margin-right: 5px;
}

.mlr3{
  margin-left: 3px;
 margin-right: 3px;
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
a {
    color: #262626!important;
    text-decoration: none;
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
.backimg{
  width:23px;
    position: absolute;
    top: 10px;
    left: 5px;
}
</style>
