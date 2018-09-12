<template>
    <div class="wrap-box">
        <header class="g-header">
            <h2 class="hd">职位列表</h2>
            <img src="../../assets/imgs/返回_2.png"  @click="backto" class="backimg" alt="">
        </header>
		<div class='textcenter f16 mt90'>{{depttitle}}</div>
        <div class="detail-tips" id="job-search-result" v-if="fitness_to_me!=0">
            雷达为您扫描到<em class="t-red suit-job-total" >{{fitness_to_me}}</em>个适合的职位
        </div>


        <div class="jobs-detail-bd" id="jobs-detail-div">
            <div class="content-item" v-for="(item,index) in jobs" >
                <router-link :to="{ name: 'JobInfo', params: { job_id: item.job_id }}">
                    <div :data-id="item.job_id" bindtap="goInfo">
                        <div class="title">
                            <div class='f14'>{{item.major}}</div>
                        </div>

                        <div>
                            <span class="key">
                                <i class="iconfont icon-icon-test"></i>职位名称
                            </span>
                            <span class="f12">{{item.job_name}}</span>
                            <span class="ml5 t-red f12" v-if="item.is_total_fit_to_me==1">匹配度：高</span>

                        </div>
                        <div>
                            <span class="key">
                                <i class="iconfont icon-ren3"></i>招考人数
                            </span>
                            <span class="t-red">{{item.enrolment_num}}</span>
                          
                        </div>
                        <div class="item-fd">                      
                            <span class="badge-solid">查看详情</span>                     
                        </div>
                    </div>
                 </router-link>
            </div>
         </div>

    </div>
</template>

<script>
import { api_get_dept_joblist } from "../../networks/JobList"


export default {
	name: 'HelloWorld',
	data () {
		return {
		   jobs:[],
		   depttitle:'',
           fitness_to_me:'',
		}
	},
	computed: {
        router_department_id() {
        	return this.$route.params.department_id
        },
        stateOpenid() {     
          return this.$store.state.openid;
        },
        user() {
           return this.$store.state.user
        },
    },
    created: function() {
         var context = this;
		context.get_area_list();
       
    },
    methods: {
		get_area_list() { 	  	
	        var context = this;
	        var province_id =context.router_department_id;
            var user_id=context.user.user_id;  
            //var wxopenid='081CUQfY0r6Db126oCgY0S4NfY0CUQfd';  
	        var promise = api_get_dept_joblist(context,province_id,user_id);
	        promise.then(function(res) {
	        	console.log(res);
	        	context.fitness_to_me=res.fitness_to_me;
                context.jobs=res.jobs;
	        	context.depttitle=res.jobs[0].company_name;
                var link = window.location.href;
                context.wxShare(context.depttitle, '公务员实时职位查询_事业单位招聘公告', link);
                
	        }).catch(function(error){
	            console.error(error);
	        });
		},
        backto() {   
            this.$router.push({ path: '/'}) 
        }

    }

}
</script>


<style scoped>
.wrap-box{
    padding:0 8px;
}
.router-link-active {
    background: #f0f3f5;
    border-left: 2px solid #f3554d;
}

.detail-tips{
    text-align: center;
     color: #a5a4a4;
      margin-top: 10px;
     margin-bottom: 15px;
     font-size: 12px;
}

.g-jobs-detail .detail-tips {
    color: #a5a4a4;
    text-align: center;
    background: #fff;
    padding: 11px 0;
    border-bottom: 1px solid #efefef;
  
}
.resume-top{
    padding: 5px;
}
.key{
  font-size: 12px;
  margin-top: 5px;
  line-height: 30px;
}

.g-jobs-detail .detail-tips em {
    margin: 0 0.06665rem;
}

.t-red {
    color: #fc6769;
}

.jobs-detail-bd {
    margin-bottom: 49px;
}
.jobs-detail-bd .content-item .key {
    color: #a5a4a4;
    margin-right: 11px;
}

.jobs-detail-bd .content-item {
    border-bottom: 1px solid #efefef;
    width: 100%;
    box-sizing: border-box;
    line-height: 20px;
    margin-bottom: 11px;
    padding-top: 5px;
}

 .jobs-detail-bd .content-item .item-fd .badge-solid {
    display:inline-block;
    width:106px;
    height:29px;
    line-height:30px;
    box-sizing:border-box;
    text-align:center;
    background-color:#f1514e;
    color:#fff;
    border-radius:12px;
    right: 20px;
    font-size: 14px;
    margin-top: -36px;
}

.jobs-detail-bd .content-item .item-fd {
    text-align: right;
    margin-top: 5px;
    margin-bottom: 11px;
}


.textcenter{
    text-align: center;
}
.f12{
    font-size: 12px;
}
.f14{
    font-size: 14px;
}
.f16{
    font-size: 16px;
}
.f18{
    font-size: 18px;
}
.backimg{
    width:23px;
    position: absolute;
    top: 10px;
    left: 5px;
}
em, i {
    font-style: normal;
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
.ml5{
    margin-left:10px;
}
</style>
