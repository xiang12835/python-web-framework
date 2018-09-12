<template>
    <div class="f8" >
        
        <div class="p10 bgfff">
             <header class="g-header mb10">
                <h2 class="hd">职位详情</h2>
                <img src="../../assets/imgs/返回_2.png"  @click="backto" class="backimg" alt="">
                 <img src="../../assets/imgs/home.png"  @click="backtohome" class="iconxxtx" alt="">
            </header>
            <div class="widtitle mt90" v-if="JobInfo.job_score_list">职位历年面试分数线及招考比</div>
            <div class="table" v-if="JobInfo.job_score_list">
                <div class="table-tr">
                    <div class="table-td">年份</div>
                    <div class="table-td" v-for="item in JobInfo.job_score_list">{{item.year}}</div>
                </div>
                <div class="table-tr">
                    <div class="table-td">面试分数线</div>
                    <div class="table-td" v-for="item in JobInfo.job_score_list">{{item.score}}</div>
                </div>
                <div class="table-tr">
                    <div class="table-td">招录人数</div>
                    <div class="table-td" v-for="item in JobInfo.job_score_list">{{item.enrolment_num}}</div>
                </div>
                <div class="table-tr">
                    <div class="table-td">报名人数</div>
                    <div class="table-td" v-for="item in JobInfo.job_score_list">{{item.application_num}}</div>
                </div>
                <div class="table-tr">
                    <div class="table-td">竞争比</div>
                    <div class="table-td" v-for="item in JobInfo.job_score_list">{{item.application_num}}:{{item.enrolment_num}}</div>
                </div>
            </div>

             <button  class='g-detail-btn' @click="scjob()">{{scname}}</button> 
        </div>



       


        <div class="mt30">   
            <div class="widtitle">{{JobInfo.job_name}}职位详情</div>       
            <div class="fontweightbold">地区信息</div>
            <div class="fontlab" v-if="JobInfo.relation">
                <div class="cl-6 color9">机构层级：</div>
                <div class="cl-18 ">{{JobInfo.relation}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.registered_place">
                <div class="cl-6 color9">地区：</div>
                <div class="cl-18 ">{{JobInfo.registered_place}}</div>
            </div>

            <div class="fontlab" v-if="JobInfo.company_property">
                <div class="cl-6 color9">机构性质：</div>
                <div class="cl-18 ">{{JobInfo.company_property}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.department_agency" style="border-bottom:none;">
                <div class="cl-6 color9">用人司局：</div>
                <div class="cl-18 ">{{JobInfo.department_agency}}</div>
            </div>

        </div>

        <div class="mt10">
            <div class="fontweightbold">单位信息</div>
            <div class="fontlab" v-if="JobInfo.company_name">
                <div class="cl-6 color9">单位名称：</div>
                <div class="cl-18 ">{{JobInfo.company_name}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.company_code">
                <div class="cl-6 color9">单位代码：</div>
                <div class="cl-18 ">{{JobInfo.company_code}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.system">
                <div class="cl-6 color9">类别：</div>
                <div class="cl-18 ">{{JobInfo.system}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.consult_telephone">
                <div class="cl-6 color9">咨询电话：</div>
                <div class="cl-18 ">{{JobInfo.consult_telephone}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.company_addr" style="border-bottom:none;">
                <div class="cl-6 color9">单位地址：</div>
                <div class="cl-18 ">{{JobInfo.company_addr}}</div>
            </div>
        </div>

        <div class="mt10">
            <div class="fontweightbold">职位信息</div>
            <div class="fontlab" v-if="JobInfo.job_name">
                <div class="cl-6 color9">职位名称：</div>
                <div class="cl-18 ">{{JobInfo.job_name}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.job_code">
                <div class="cl-6 color9">职位代码：</div>
                <div class="cl-18 ">{{JobInfo.job_code}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.job_attribute">
                <div class="cl-6 color9">职位属性：</div>
                <div class="cl-18 ">{{JobInfo.job_attribute}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.job_desc">
                <div class="cl-6 color9">职位简介：</div>
                <div class="cl-18 ">{{JobInfo.job_desc}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.job_level">
                <div class="cl-6 color9">职务层次：</div>
                <div class="cl-18 ">{{JobInfo.job_level}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.enrolment_num">
                <div class="cl-6 color9">招考人数：</div>
                <div class="cl-18 ">{{JobInfo.enrolment_num}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.application_num">
                <div class="cl-6 color9">报名人数：</div>
                <div class="cl-18 ">{{JobInfo.application_num}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.other" style="border-bottom:none;">
                <div class="cl-6 color9">其他要求：</div>
                <div class="cl-18 ">{{JobInfo.other}}</div>
            </div>
        </div>



        <div class="mt10">
            <div class="fontweightbold">报名条件</div>
            <div class="fontlab" v-if="JobInfo.education">
                <div class="cl-6 color9">学历：</div>
                <div class="cl-18 ">{{JobInfo.education}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.degree">
                <div class="cl-6 color9">学位：</div>
                <div class="cl-18 ">{{JobInfo.degree}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.major">
                <div class="cl-6 color9">专业：</div>
                <div class="cl-18 ">{{JobInfo.major}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.politics_status">
                <div class="cl-6 color9">政治面貌：</div>
                <div class="cl-18 ">{{JobInfo.politics_status}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.age">
                <div class="cl-6 color9">年龄：</div>
                <div class="cl-18 ">{{JobInfo.age}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.nation">
                <div class="cl-6 color9">民族：</div>
                <div class="cl-18 ">{{JobInfo.nation}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.nation">
                <div class="cl-6 color9">民族：</div>
                <div class="cl-18 ">{{JobInfo.nation}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.household_registration">
                <div class="cl-6 color9">户籍：</div>
                <div class="cl-18 ">{{JobInfo.household_registration}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.apply_person">
                <div class="cl-6 color9">招考对象：</div>
                <div class="cl-18 ">{{JobInfo.apply_person}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.orther_condition">
                <div class="cl-6 color9">其他报考条件：</div>
                <div class="cl-18 ">{{JobInfo.orther_condition}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.professional_competence_test">
                <div class="cl-6 color9">是否在面试阶段组织专业能力测试：</div>
                <div class="cl-18 ">{{JobInfo.professional_competence_test}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.face_to_village_official">
                <div class="cl-6 color9">是否面向大学生村官招考：</div>
                <div class="cl-18 ">{{JobInfo.face_to_village_official}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.face_to_soldier">
                <div class="cl-6 color9">是否面向退役大学生士兵招考：</div>
                <div class="cl-18 ">{{JobInfo.face_to_soldier}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.face_to_fresh_graduate">
                <div class="cl-6 color9">是否要求应届高校毕业生：</div>
                <div class="cl-18 ">{{JobInfo.face_to_fresh_graduate}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.face_to_full_time_education">
                <div class="cl-6 color9">是否要求报考学历为普通高等教育全日制学历：</div>
                <div class="cl-18 ">{{JobInfo.face_to_full_time_education}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.face_to_base_project_personnel">
                <div class="cl-6 color9">是否定向录取服务基层项目人员</div>
                <div class="cl-18 ">{{JobInfo.face_to_base_project_personnel}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.face_to_politics">
                <div class="cl-6 color9">是否面向村党组织书记、村委会主任招录职位</div>
                <div class="cl-18 ">{{JobInfo.face_to_politics}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.face_to_shortage_job">
                <div class="cl-6 color9">是否属于紧缺职位</div>
                <div class="cl-18 ">{{JobInfo.face_to_shortage_job}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.face_to_police">
                <div class="cl-6 color9">是否人民警察职位</div>
                <div class="cl-18 ">{{JobInfo.face_to_police}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.face_to_merge_job">
                <div class="cl-6 color9">是否合并职位招录</div>
                <div class="cl-18 ">{{JobInfo.face_to_merge_job}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.work_experience" style="border-bottom:none;">
                <div class="cl-6 color9">服务基层工作经历：</div>
                <div class="cl-18 ">{{JobInfo.work_experience}}</div>
            </div>
        </div>

        <div class="mt10">
            <div class="fontweightbold">考试信息</div>
             <div class="fontlab" v-if="JobInfo.exam_num">
                <div class="cl-6 color9">考试科目数量:</div>
                <div class="cl-18 "> {{JobInfo.exam_num}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.entrance_examination_range">
                <div class="cl-6 color9">招考范围：</div>
                <div class="cl-18 "> {{JobInfo.entrance_examination_range}}</div>
            </div>
             <div class="fontlab" v-if="JobInfo.expound_category">
                <div class="cl-6 color9">申论类别：</div>
                <div class="cl-18 ">{{JobInfo.expound_category}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.professional_course">
                <div class="cl-6 color9">专业科目：</div>
                <div class="cl-18 ">{{JobInfo.professional_course}}</div>
            </div>
             <div class="fontlab" v-if="JobInfo.need_professional_examination">
                <div class="cl-6 color9">是否组织专业考试：</div>
                <div class="cl-18 ">{{JobInfo.need_professional_examination}}</div>
            </div>
             <div class="fontlab" v-if="JobInfo.need_psychological_test">
                <div class="cl-6 color9">是否组织心理测试：</div>
                <div class="cl-18 ">{{JobInfo.need_psychological_test}}</div>
            </div>
             <div class="fontlab" v-if="JobInfo.need_health_test">
                <div class="cl-6 color9">是否组织体测：</div>
                <div class="cl-18 ">{{JobInfo.need_health_test}}</div>
            </div>

            <div class="fontlab" v-if="JobInfo.competitive_ratio">
                <div class="cl-6 color9">竞争比：</div>
                <div class="cl-18 ">{{JobInfo.competitive_ratio}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.exam_proportion">
                <div class="cl-6 color9">面试人数与录用人数比例：</div>
                <div class="cl-18 ">{{JobInfo.exam_proportion}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.application_num">
                <div class="cl-6 color9">合格人数：</div>
                <div class="cl-18 ">{{JobInfo.application_num}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.score">
                <div class="cl-6 color9">分数线：</div>
                <div class="cl-18 "> {{JobInfo.score}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.interdiv_num">
                <div class="cl-6 color9">面试人数：</div>
                <div class="cl-18 "> {{JobInfo.interdiv_num}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.exam_category">
                <div class="cl-6 color9">考试类别：</div>
                <div class="cl-18 ">{{JobInfo.exam_category}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.domain">
                <div class="cl-6 color9">专业专项：</div>
                <div class="cl-18 ">{{JobInfo.domain}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.work_place">
                <div class="cl-6 color9">工作地点：</div>
                <div class="cl-18 "> {{JobInfo.work_place}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.registered_place">
                <div class="cl-6 color9">落户地点：</div>
                <div class="cl-18 "> {{JobInfo.registered_place}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.job_distribution" style="border-bottom:none;">
                <div class="cl-6 color9">职位分布：</div>
                <div class="cl-18 "> {{JobInfo.job_distribution}}</div>
            </div>
        </div>

        <div class="mt10">
            <div class="fontweightbold">其他信息</div>
            <div class="fontlab" v-if="JobInfo.company_web">
                <div class="cl-6 color9">部门网站：</div>
                <div class="cl-18 ">{{JobInfo.company_web}}</div>
            </div>
            <div class="fontlab" v-if="JobInfo.consult_telephone" style="border-bottom:none;">
                <div class="cl-6 color9">咨询电话：</div>
                <div class="cl-18 ">{{JobInfo.consult_telephone}}</div>
            </div>
        </div>

        <div class="mt10">
            <a href="http://www.winlesson.com/" target="_blank">
                <div class="fontweightbold"  style="border-bottom:none;">免费试听课程
                    <i class="title-i">行测、申论、面试、公共基础知识</i>
                    <div class="arrow"></div>
                </div>
            </a>
        </div>

        <div class="perfectnbox">
            <!--  <navigator url="../myresume/myresume"> -->
                <button class="btn-perfectnbox" @click="gotomyresume">职位匹配不够准确？快来完善你的简历吧
                    <i class="arrow-bg"></i>
                </button>
            <!--  </navigator> -->
            <div class='perfectnbox-p'>＊职位内容由必胜公考根据官方职位表独家整理，</div>
            <div class='perfectnbox-p'>具体职位信息请结合必胜公考APP</div>
        </div>


    </div>
</template>

<script>

import { api_get_job_info } from "../../networks/JobList"

import { api_get_collect_job } from "../../networks/JobList"


export default {
	name: 'HelloWorld',
	data () {
		return {
		    JobInfo: [],
		    jobid: '',
            scname:'收藏职位',
		}
	},
	computed: {
        user() {
           return this.$store.state.user
        },
        router_job_id() {
        	return this.$route.params.job_id
        },
        stateOpenid() {     
            return this.$store.state.openid;
        },
    },
    created: function() {
         var context = this;
		context.get_job_info();

      
    },
    methods: {
		get_job_info() { 	  	
	        var context = this;
	        var job_id =context.router_job_id;
	        var promise = api_get_job_info(context,job_id);
	        promise.then(function(res) {
	        	console.log(res);
	        	context.JobInfo=res.job;
                
                    var link = window.location.href;
                    var job_name=context.JobInfo.job_name;
                    console.log(job_name);
                    context.wxShare(job_name, '你的朋友给你分享了一个职位，快来查看吧', link);
	        }).catch(function(error){
	            console.error(error);
	        });
		},
        scjob(){
            var context = this;
            var job_id =context.router_job_id;
            var wxopenid=context.stateOpenid;
            var userid=context.user.user_id;
            if(userid!=''){
                var promise = api_get_collect_job(context,job_id,wxopenid);
                promise.then(function(res) {
                    console.log(res.data.code);
                    if (res.data.code == '200') {
                          message: '收藏成功',
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
        gotomyresume() {   
            if(wxopenid!=''){
              this.$router.push({ path: '/myresume' })
            }
        },
        backtohome() {   
            this.$router.push({ path: '/' })
        },

    }

}
</script>


<style scoped>
.content .wrap-content .content-box .wrap-box {
    width: 100%;
    min-height: 810px;
    padding: 15px 15px;
    border: 1px solid #f1f4f6;
}

.mt50{
  margin-top:50px;
}  
.toptitlelist{
    height: 40px;
    position: fixed;
    max-width: 460px;
    top: 0;
    z-index: 99;
    background-color: #ffbc40;
    color: #fff;
    padding-top: 10px;
    width: 100%;
}
.textcenter{
      text-align: center;
}
.dd-card{
  width:88%;
  background-color:#fff;
  color: #303133;
  transition: .3s;
  margin-left: auto;
  margin-right: auto;
  padding: 10px;
  position: relative;
  border-radius: 10px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
}
.borde-b-s{
  border-bottom: 1px solid #eee;
}
.borde-b-d{
  border-bottom: 1px dotted #eee;
}

.borde-t-s{
   border-top: 1px solid #ebeef5;
}

.borde-lr-s{
  border-left: 1px solid #ebeef5;
  border-right: 1px solid #ebeef5;
}

.fontweightbold{
    padding: 10px 13px;
    border-bottom: 1px solid #eee;
    position: relative;
    background-color: #fff;
}
.fontweightbold:before{
    content: "";
    background: #f1514e;
    width: 3px;
    height: 18px;
    position: absolute;
    top: 11px;
    left: 0;
    display: inline-block;  
}
.fontlab{
  font-size:14px;
background-color:#fff;
border-bottom:1px dotted #eee;
padding:10px 0px;
display:flex;
align-items:center;
margin:0px 13px;

}
.mb50{
   margin-bottom: 50px;
}
.color9{
  color:#909399;
}
.table {padding: 0;font-size: 14px;font-family: Arial, 宋体, Helvetica, sans-serif;}   
.table {display: table;  border-collapse: collapse; border-top: 1px solid #eee;}   
.table-tr {display: table-row; height: 30px;}   
.table-th {
    display: table-cell;
    height: 100%;
    border: 1px solid gray;
    text-align: center;
    vertical-align: middle;}   
.table-td,
.table-tdd{
    display: table-cell;
    border-bottom: 1px solid #eee; 
    text-align: center;
    vertical-align: middle;
    color: #606266;
    height: 30px; 
} 
.table-td{
    background: #fff;
}
.table-tdd{
    background: #f9f9f9;
}
.mb50 {
    margin-bottom: 50px;
}

.mt10 {
    margin-top: 10px;
    background-color:#fff;
    box-shadow: 6px 5px 5px #f3f7f9;
}

.mt50 {
    margin-top: 50px;
}

.f8{
    background-color: #f8f8f8;
    overflow-x: hidden;
}

.widtitle{
    width: 100%;
    height: 40px;
    display: flex;
   align-items: center;
   padding-left: 16px;

}

.cl-6{
    width: 25%;
   
}
.cl-18{
    width: 75%;
    padding-left:2%;

}
.arrow{
    width: 7px;
    height: 7px;
    border-top: 1px solid #999;
    border-right: 1px solid #999;
    position: absolute;
    right: 6px;
    transform: rotate(45deg);
    top:11px;
}
.arrow-bg{
    width: 10px;
    height: 10px;
    border-top: 1px solid #fff;
    border-right: 1px solid #fff;
    position: absolute;
    right: 10px;
    transform: rotate(45deg);
    top:11px;
}
.title-i{
    float:right;
color:#999;
font-size:12px;
padding-right:4px;
padding-top:3px;

}
.perfectnbox {
    padding: 13px;
    text-align: center;
    margin-bottom:50px;
}
.btn-perfectnbox{
    display: block;
    line-height: 28px;
    font-size: 13px;
    text-align: center;
    background-color: #f1514e;
    color: #fff;
    border-radius: 5px;
    margin: 8px auto;
    width: 100%;
    height: 33px;
    border:none;
}

.perfectnbox-p {
    text-align: center;
    line-height: 17px;
    color: #aaa;
    font-size: 12px;
        margin: 0;
    padding: 0;
}
.g-detail-footer {
    position: fixed;
    left: 0;
    bottom: 0;
    z-index: 1;
    display: flex;
     justify-content: flex-end; 
    float: right;
    align-items: center;
    border-top: 1px solid #efefef;
    width: 100%;
    height: 38px;
    box-sizing: border-box;
    background-color: #fff;
    font-size: 12px;
    opacity: 0.9;
    }
    .g-detail-btn {
        background-color: #f1514e;
    position: absolute;
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
}

.i-extend {
 position:absolute;
top:-13.5px;
right:4px;
color:#fff;
font-size:22px;

}

.btnshare{
    width:30px;
height:30px;
position:absolute;
right:4px;
top:4px;
background-color:#f1514e;
border:1px solid #f1514e;

}

.arrowleft{
     width: 10px;
    height: 10px;
    border-top: 1px solid #fff;
    border-right: 1px solid #fff;
    position: absolute;
    left: 10px;
    transform: rotate(225deg);
    top:9px;
}

.btnback{
width:30px;
height:30px;
position:absolute;
left:4px;
top:4px;
background-color:#f1514e;
border:1px solid #f1514e;


}

.p10{
    padding:10px;
}

.bgfff{
    background-color:#fff;
}
a{
     text-decoration: none;
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
.f8 {
    background-color:#f8f8f8;
    overflow-x:hidden;
}
.mt30{
    margin-top:30px;
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
