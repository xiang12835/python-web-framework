<template>
  <div class="job-list">
      <div class="probe-prompt">
        <span>探测到<i>{{jobs_count}}</i>个部门，<i>{{total_enrolment_num}}</i>个职位适合我</span>
      </div>
      <ul class="news-bd-list">
          <li class="news-bd-list-li"  
            v-for="(item,index) in job_list">
            <router-link  :to="{ name: 'JobList', params: { department_id: item.department_id }}">
                <div class="item-hd">                        
                        {{item.department_name}}
                </div>
                <div class="item-fd">
                    <div class="fd-left">
                        <i class="">招考人数</i>
                        <i class="mr5 bsk-color">{{item.enrolment_num}}</i>
                        <i class="" v-if="item.application_num!=0">报名人数</i>
                        <i class="mr10 bsk-color" v-if="item.application_num!=0">
                            {{item.application_num}}
                        </i>
                    </div>
                    <div class="fd-right">
                        <em class="t24">职位<i class='bsk-color mlr3' v-if="item.fitness_to_me!=0">{{item.fitness_to_me}}</i>个</em>
                        <!-- <em v-else class="t24">可能有适合的职位</em> -->
                    </div>
                </div>
            </router-link>
          </li>
      </ul>
      <div class="load-more" v-if="showmore">
          <button type="button" id="job-next-page" @click="getmore()">加载更多</button>
      </div>
      <div class="no-more" v-else>
          <span><i class="icon-nomore"></i>没有更多内容了哦~</span>
      </div>
  </div>
</template>

<script>
import { api_get_job_list } from "../../networks/JobList"


export default {
	name: 'HelloWorld',
	data () {
	  return {
	     job_list:[],
       isgk:1,
       area_id:'',
       province_id:'',
       provincearea_id:'',
       type_id:'',
       dept_id:'',
       pageNum:1,
       pageSize:20,
       jobs_count:55,
       total_enrolment_num:565,
       showmore:true,
	  }
	},
	computed: {
      stateIsgk() {     
        return this.$store.state.isgk;
      },
      stateAreaid() {
        return this.$store.state.Areaid;
      },
      stateProvinceid() {  
        return this.$store.state.Provinceid;
      },
      stateProvinAreaid() {
        return this.$store.state.ProvinAreaid;
      },
      stateTypeid() {      
        return this.$store.state.Typeid;
      },
      stateDeptid() {    
        return this.$store.state.Deptid;
      },
      user() {
        return this.$store.state.user
      },
  },
  watch: {
    stateIsgk: {
        deep: true,
        handler: function (val) {
            this.clear();
            this.isgk = val;
            this.get_job_list();
        }
    },
    stateAreaid: {
        deep: true,
        handler: function (val) {
            this.area_id=val;
            this.clear();
            this.get_job_list(); 
        }
    },
    stateProvinceid: {
        deep: true,
        handler: function (val) {
            this.province_id=val; 
            this.clear();
            this.provincearea_id=''; 
            this.get_job_list();
        }
    },
    stateProvinAreaid: {
        deep: true,
        handler: function (val) {
          this.clear();
          //this.provincearea_id=val;
          if(val!=-1){
              this.provincearea_id=val;
          }else{
            this.provincearea_id='';
          }
          this.get_job_list(); 
        }
    },
    stateTypeid: {
        deep: true,
        handler: function (val) {
          this.clear();
          this.type_id=val; 
          this.dept_id=''; 
          this.get_job_list();
        }
    },
    stateDeptid: {
        deep: true,
        handler: function (val) {
          this.clear();
          this.dept_id=val; 
          this.get_job_list();
        }
    },
    user: {
        deep: true,
        handler: function (val) {
            this.clear();
            this.get_new_list();
        }
    },
  },
  created: function() {
    	/*  获取国考下地区  */
    	var context = this;   

      context.isgk=context.stateIsgk;
      context.area_id=context.stateAreaid; 
      context.province_id=context.stateProvinceid; 
      context.provincearea_id=context.stateProvinAreaid; 
      context.type_id=context.stateTypeid;
      context.dept_id=context.stateDeptid;

      context.get_job_list();
		
  },
	methods: {
	  get_job_list() {      
        var context = this;

        if (context.type_id!='-1') {
          var system_id=context.type_id;
        }else{
          var system_id='';
        }

        if (context.dept_id!='-1') {
           var department_id=context.dept_id;
        }else{
          var department_id='';
        }

        if (context.isgk==1) {//国考
            var province_id=1;
            if(context.area_id){
              var area_id=context.area_id;
            }
            else{
              var area_id=1;
            }      
        }
        else{
            var province_id=context.province_id;
            var system_id='';
            var department_id='';
            if (context.provincearea_id!='-1') {
              var area_id=context.provincearea_id;
            }else{
              var area_id='';
            }
        }

        var pageNum=context.pageNum;
        var pageSize=context.pageSize;

        console.log("province_id     "+province_id);
        console.log("area_id     "+area_id);
            var promise = api_get_job_list(context,province_id,area_id,system_id,department_id,pageNum,pageSize);
            promise.then(function(res) {
                console.log(res);
                context.jobs_count=res.jobs_count;
                context.total_enrolment_num=res.total_enrolment_num;


                context.job_list= context.job_list.concat(res.job_list);

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
         context.get_job_list();
    },
    clear(){
          this.pageNum=1;
          this.showmore=true;
          this.job_list=[];
    }
	}
}
</script>


<style scoped>

.bsk-color{
color: #f1514e;
}  
.job-list {
    padding: 10px;
    background: #fff;
    border: 1px solid #f1f4f6;
    border-top: none;
}
.probe-prompt {
    height: 30px;
    line-height: 30px;
    text-align: center;
}
.probe-prompt span {
    display: inline-block;
    font-size: 12px;
    color: #909599;
}
.probe-prompt span i {
    color: #fd6366;
    padding: 0 5px;
}
.load-more {
    padding: 20px 0;
    text-align: center;
    margin-bottom:60px;
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
     margin-bottom:60px;
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
        cursor: pointer;
}
.news-bd-list-li:not(:first-child){
    border-top: 1px solid #efefef;
    padding-top: 11px;
    padding-bottom: 11px;
    text-decoration:none;
        cursor: pointer;
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
.news-bd-list{
  padding-left:0;
}
</style>
