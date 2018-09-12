<template>
  <div class="newsinfo" v-if="wxopenid!=''">
        <header class="g-header">
            <h2 class="hd">我的简历</h2>
             <img src="../../assets/imgs/返回_2.png"  @click="backto" class="backimg" alt="">
        </header>
      	<div class="resume-top mt90">
            <span class="resume-top-span">简历完整度：<i>{{percentage_str}}</i></span>
            <span class="resume-top-p">简历完整度越高，职位匹配更精准哦~</span>
        </div>
        <form class="form-horizontal mt20">
        	  <div class="form-group">
        	    <label for="inputEmail3" class="col-sm-4 control-label">报考地区</label>
        	    <div class="col-sm-4">
        	     	<select  v-model="region_id"  class='form-control'>  
        	     		<option  v-for="(item,index) in get_region_json" :value='index+1'>{{item.area_name}}</option>
        			</select>
        	    </div>
        	    <div class="col-sm-4"></div>
        	  </div>
        	  <div class="form-group">
        	    <label for="inputPassword3" class="col-sm-4 control-label">学历</label>
        	    <div class="col-sm-4">
        	    	<select   v-model="xl_id"  class='form-control'>  
        	     		<option  v-for="(item,index) in get_xl_name" :value='index'>{{item}}</option>
        			</select> 
        	    </div>
        	    <div class="col-sm-4"></div>
        	  </div>
        	  <div class="form-group">
        	    <label for="inputPassword3" class="col-sm-4 control-label">专业</label>
        	    <div class="col-sm-4">
        	     	  <input type="text"  v-model="inputzy" class="form-control" id="inputzy" placeholder="专业">
        	    </div>
        	    <div class="col-sm-4"></div>
        	  </div>
        	  <div class="form-group">
        	    <label for="inputPassword3" class="col-sm-4 control-label">学位</label>
        	    <div class="col-sm-4">	    	 
        	     	<select  v-model="xw_id"  class='form-control'>  
        	     		<option  v-for="(item,index) in get_xw_name" :value='index'>{{item}}</option>
        			</select> 
        	    </div>
        	    <div class="col-sm-4"></div>
        	  </div>
        	  <div class="form-group">
        	    <label for="inputPassword3" class="col-sm-4 control-label">性别</label>
        	    <div class="col-sm-4">
        	     	<select  v-model="xb_id" class='form-control'>  
        	     		<option  v-for="(item,index) in get_xb_name" :value='index'>{{item}}</option>
        			</select> 
        	    </div>
        	    <div class="col-sm-4"></div>
        	  </div>
        	  <div class="form-group">
        	    <label for="inputPassword3" class="col-sm-4 control-label">政治面貌</label>
        	    <div class="col-sm-4">
        	     	 <select  v-model="zzmm_id" class='form-control'>  
        	     		<option  v-for="(item,index) in get_zzmm_name" :value='index'>{{item}}</option>
        			</select> 
        	    </div>
        	    <div class="col-sm-4"></div>
        	  </div>
        	  <div class="form-group">
        	    <label for="inputPassword3" class="col-sm-4 control-label">工作经验</label>
        	    <div class="col-sm-4">
        	     	<select  v-model="gzjy_id" class='form-control'>  
        	     		<option  v-for="(item,index) in get_gzjy_name" :value='index'>{{item}}</option>
        			</select> 
        	    </div>
        	    <div class="col-sm-4"></div>
        	  </div>
        	  <div class="form-group">
        	    <label for="inputPassword3" class="col-sm-4 control-label">服务基层工作经历</label>
        	    <div class="col-sm-4">
        	     	<select  v-model="jcgzjy_id"  class='form-control'>  
        	     		<option  v-for="(item,index) in get_jcgzjy_name" :value='index'>{{item}}</option>
        			</select>
        	    </div>
        	    <div class="col-sm-4"></div>
        	  </div>
        	  <div class="form-group">
        	    <!-- <div class="col-sm-offset-2 col-sm-10"> -->
        	    <div class="col-sm-12 center">
        	      <span  class="btn determine-btn" @click="saveBtn">保存</span>
        	    </div>
        	  </div>
    	</form>
  </div>
  
  <div class="newsinfo"  v-else>
    <div class="notlogin-follow">
        <p>登录后才能查看我的简历信息~</p>
         <button class="btn-red open-register-win" @click="showlogin" >登录</button>
    </div>
    <div v-if="loginmodel">
        <login> </login>          
    </div>
  </div>
</template>

<script>
import { api_get_area_list } from "../../networks/Conditions"
import { api_post_sub_resume} from "../../networks/others"
import { api_post_my_resume} from "../../networks/others"
import login from '../smallcommon/login.vue'

export default {
  name: 'newspage',
  data () {
    return {
       get_region_json: [],
       percentage_str:'88%',
       get_xl_name: [
          "请选择",
          "专科",
          "本科",
          "硕士",
          "博士"
      ],
      get_xw_name: [
          "请选择",
          "学士",
          "硕士",
          "博士",
          "无限制",   
      ],
      get_zzmm_name: [
          "请选择",    
          "共青团员",
          "党员",
          "民主党派",
          "群众",
          "无限制",
      ],
      get_gzjy_name: [
          "请选择",
          "无工作经验",
          "一年",
          "二年",
          "三年",
          "四年",
          "五年及以上",
          "无限制",
      ],
      get_xb_name: [
          "请选择",
          "女",
           "男"
      ],
      get_jcgzjy_name: [
            "请选择",
            "无服务基层工作经历",
            "四项目人员",
            "村官",
            "西部志愿者",
            "退役士兵",
            "特岗计划教师",
            "三支一扶",
      ],
      region_id:1,
      xl_id:'',
      inputzy:'',
      xw_id:'',
      xb_id:'',
      zzmm_id:'',
      gzjy_id:'',
      jcgzjy_id:'',
      wxopenid:'',
       loginmodel:false
    }
  },
    components:{
        login
    },
  computed: {
     user() {
           return this.$store.state.user
    },
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
                this.get_area_list(1);
                this.getUseResume();
            }
        },
    },
  created: function() {
      var context = this;
      context.wxopenid=context.stateOpenid;      
      if(context.wxopenid!=''){
         /*  获取地区  */
        context.get_area_list(1);
         /*  获取用户简历  */
        context.getUseResume();
      }
     
  },
  methods: {
	  /*  获取地区  */
	  get_area_list(province_id) { 	  	
        var context = this;
        var promise = api_get_area_list(context,province_id);
        promise.then(function(res) {
        	context.get_region_json=res.areas;
        }).catch(function(error){
            console.error(error);
        });
	  },
	  saveBtn() { 	  	
        var context = this;
         var userid=context.user.user_id;
        var wxopenid=context.stateOpenid;
        var region_id = context.region_id;
        if (xl_id!='0') {
  			var xl_id = context.xl_id;
        }else{
        	var xl_id = '';
        }

        if (inputzy!='0') {
        	var inputzy = context.inputzy;
        }else{
        	var inputzy = '';
        }


        if (xw_id!='0') {
        	var xw_id = context.xw_id;
        }else{
        	var xw_id = '';
        }

        if (xb_id!='0') {
        	 var xb_id = context.xb_id;
        }else{
        	var xb_id = '';
        }

        if (zzmm_id!='0') {
        	var zzmm_id = context.zzmm_id;
        }else{
        	var zzmm_id = '';
        }

        if (gzjy_id!='0') {
        	 var gzjy_id = context.gzjy_id;
        }else{
        	var gzjy_id = '';
        }

        if (jcgzjy_id!='0') {
        	 var jcgzjy_id = context.jcgzjy_id;
        }else{
        	var jcgzjy_id = '';
        }
        var promise = api_post_sub_resume(context,userid,wxopenid,region_id,xl_id,inputzy,xw_id,xb_id,zzmm_id,gzjy_id,jcgzjy_id);
        promise.then(function(res) {
        	console.log(res);
          if (res.success) {
              context.$message({
                  message: '保存成功',
                  type: 'success'
              });
            context.getUseResume();
          }
        }).catch(function(error){
            console.error(error);
        });
	  },
     getUseResume() {       
        var context = this;
        var user_id=context.user.user_id;
        var promise = api_post_my_resume(context,user_id);
        promise.then(function(res) {
                console.log(res);
                context.region_id=res.user_resume.area;
                context.xl_id=res.user_resume.education;    
                context.inputzy=res.user_resume.professional;
                context.xw_id=res.user_resume.degree;
                context.xb_id=res.user_resume.gender;          
                context.zzmm_id=res.user_resume.political_status;
                context.gzjy_id=res.user_resume.work_experience;
                context.jcgzjy_id=res.user_resume.base_course;
                 context.percentage_str=res.user_resume.percentage_str;
            }).catch(function(error){
                console.error(error);
            });
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

  },
 
   
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
 .resume-top {
    padding-top: 11px;
    text-align: center;
    margin-left: 11px;
    margin-right: 11px;
    border-bottom: 1px solid #efefef;
    padding-bottom: 8px;
}

.resume-top-span{
    display: block;
    line-height: 21px;
    color: #f1514e;
     font-size: 16px;
    margin-bottom: 5px;
    text-align: center;
}

.resume-top-p {
    display: block;
    text-align: center;
    font-size: 12px;
    color: #aaa;
}
.mt20{
	 margin-top: 20px;
}
.center{
	text-align:center;
}
.determine-btn {
    width: 207px;
    height: 37px;
    border-radius: 20px;
    background: #f1514e;
    color: #fff!important;
    font-size: 16px;
    margin-top: 20px;
    margin-bottom: 40px;
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
em, i {
    font-style: normal;
}
</style>
