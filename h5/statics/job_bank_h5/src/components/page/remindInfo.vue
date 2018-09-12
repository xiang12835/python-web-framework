<template>
    <div class="logincontent">
      <header class="g-header">
            <h2 class="hd">我的提醒</h2>
            <img src="../../assets/imgs/返回_2.png"  @click="backto" class="backimg" alt="">
       </header>
      <ul class="news-bd-list mt90">
          <li class="news-bd-list-li"  
            v-for="(item,index) in notice_info">
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
    </div>
</template>

<script>

import { api_get_user_noticesinfo } from "../../networks/remind"



export default {
	name: 'HelloWorld',
	data () {
		return {
      notice_info:[],
		}
	},
	computed: {
    router_notice_id() {
      return this.$route.params.notice_id;
    },
  },
  created: function() { 
      var context = this;    
      var notice_id =context.router_notice_id;
         
      var promise = api_get_user_noticesinfo(context,notice_id);
      promise.then(function(res) {
        console.log(res);
        context.notice_info=res.data;     
      }).catch(function(error){
          console.error(error);
      });
  },
  methods: {
  	 backto() {   
            this.$router.push({ path: '/remindpage'}) 
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
.news-bd-list{
  padding-left:0;
}
.news-bd-list-li:first-child{
    padding-top: 4px;
    padding-bottom: 11px;
    text-decoration:none;
    padding-left:0;
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
a {
    color: #262626!important;
    text-decoration: none;
}

em, i {
    font-style: normal;
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
  margin-top:55px;
}
.backimg{
    width:23px;
    position: absolute;
    top: 10px;
    left: 5px;
}
</style>
