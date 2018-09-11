<template>
  <div  v-if="stateIsgk" class="job-myinfor"><!--头部信息-->
    <div class="bordertop">  
    	 <div class="zone-box clearfix"> 
  	    <div class='flexsb w80'>  		
          <div class="f12">
    				<span>系统类型：</span> 
    		    	<a href="#" data-toggle="modal" data-target="#showType">{{typename}}</a> 
    			</div>


    			<div class="ml20 f12">
    				<span>招考单位：</span> 
    		    	<a href="#" data-toggle="modal" data-target="#showDept">{{deptaname}}</a> 
    			</div>
  	    </div>       
      </div>
    </div>

<!-- 系统类型： -->
<div class="modal fade" id="showType" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title" id="myModalLabel">选择系统类型</h4>
      </div>
      <div class="modal-body">
    	 <div class="area-list">
           <ul class="system">
                <li class="select-province" 
                	:class="{active:item.system_id==system_id}" 
                	:data-id="item.system_id"  
                	v-for="(item,index) in type_list" 
                	@click="selectType(item.system_id,item.system_name)">
                	{{item.system_name}}
                </li>
            </ul>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">取消</button>
        <button type="button" class="btn btn-primary" @click="btnsaveType">保存</button>
      </div>
    </div>
  </div>
</div>

<!-- 招考单位： -->
<div class="modal fade" id="showDept" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title" id="myModalLabel">选择招考单位</h4>
      </div>
      <div class="modal-body">
    	 <div class="area-list">
           <ul class="department">
                <li class="select-province" 
                  :class="{active:item.department_id==department_id}" 
                   :data-id="item.department_id"  
                   v-for="(item,index) in department_list" 
                   @click="selectDept(item.department_id,item.department_name)">
                	{{item.department_name}}
                </li>
            </ul>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">取消</button>
        <button type="button" class="btn btn-primary" @click="btnsaveDept">保存</button>
      </div>
    </div>
  </div>
</div>


  </div>
</template>

<script>
import { api_get_type_list } from "../../networks/Conditions"
import { api_get_dept_list } from "../../networks/Conditions"

export default {
	name: 'HelloWorld',
	data () {
	  return {
	     type_list:[],
	     department_list:[],
	     typename:'全部',
	     deptaname:'全部',
	     system_id:-1,
	     department_id:-1,
	  }
	},
	computed: {
      stateIsgk() {
        return this.$store.state.isgk
      },
      stateAreaid() {
        return this.$store.state.Areaid
      },
  },
  watch: {
    stateAreaid: {
        deep: true,
        handler: function (val) {
            this.get_type_list(val);
            this.system_id=-1;
            this.department_id=-1;
            this.typename="全部";
            this.deptaname="全部";
            this.$store.commit("updateSystemid",this.system_id);
            this.$store.commit("updateDepartmentid",this.department_id);
        }
    }
  },
  created: function() {
  	/*  获取国考下地区  */
  	var context = this;   
    console.log("系统类型  Areaid"+context.stateAreaid);  
    if(context.stateAreaid==''){
        //第一次加载
        // context.$store.commit("updateAreaid",1);
        // context.$store.commit("updateAreaname",'北京'); 
        context.get_type_list(1); 
    }  
    else{
      context.get_type_list(context.stateAreaid); 
    }

    context.system_id=-1;
    context.department_id=-1;
    context.$store.commit("updateSystemid",context.system_id);
    context.$store.commit("updateDepartmentid",context.department_id);
  },
	methods: {
	  /*  获取系统类型  */
	  get_type_list(area_id) {
        if (area_id) {  	
          var context = this;
          var promise = api_get_type_list(context,area_id);
          promise.then(function(res) {
              console.log("area_id   "+area_id);
              console.log("获取系统类型");
          	  console.log(res);
          		res.system_list.unshift({ 'system_id': '-1','system_name': '全部' });
          		context.type_list=res.system_list;
          }).catch(function(error){
              console.error(error);
          });
        }   
	  },
	  /*  获取单位  */
	  get_department_list(area_id,system_id) { 	  	
        var context = this;
        var promise = api_get_dept_list(context,area_id,system_id);
        promise.then(function(res) {
        	console.log(res);
          res.department_list.unshift({ 'department_id': '-1','department_name': '全部' });
          context.department_list=res.department_list;
        }).catch(function(error){
            console.error(error);
        });
	  },
	  selectType(system_id,system_name) { 
	  	var context = this;
	  	context.system_id=system_id;
	  	context.system_name=system_name;
	  	$(".system .active").removeClass('active');
	  	$('.system li[data-id='+system_id+']').addClass('active');
	  },
    selectDept(department_id,department_name) { 
      var context = this;
      context.department_id=department_id;
      context.department_name=department_name;
      $(".department .active").removeClass('active');
      $('.department li[data-id='+department_id+']').addClass('active');
    },
    /*  选择系统类型 */
    btnsaveType() { 
      var context = this;
      if (context.stateAreaid) {
        context.get_department_list(context.stateAreaid,context.system_id);
      }
      else{
        context.get_department_list(1,context.system_id);
      }
      
      context.deptaname="全部";
      context.department_id=-1;
      context.$store.commit("updateSystemid",context.system_id);
      context.typename=context.system_name;
      $('#showType').modal('hide');
    },
    /*  选择部门 */
    btnsaveDept() { 
      var context = this;
      context.$store.commit("updateDepartmentid",context.department_id);
      context.deptaname=context.department_name;
      $('#showDept').modal('hide');
    },
	}
}
</script>


<style scoped>
.job-myinfor {
   padding:0 10px;
    background: #fff;
    border-bottom: none;
}
.flexsb{
    display:flex;

}
.zone-box .center{
    display: flex;
     align-items: center;
     justify-content: center; 
}
.bordertop{
     border-top: 1px solid #f1f4f6;
}
.zone-box{
    display: flex;
    justify-content:  flex-start;
     align-items: center;
    width: 100%;
      min-height: 50px;
}

.info-switch {
    line-height: 38px;
    font-size: 14px;
    color: #f1514e;
    cursor: pointer;
    margin-left:5px;
}
.fl {
    float: left;
}

.select-province{
	    float: left;
    cursor: pointer;
    font-size: 14px;
    margin-bottom: 10px;
    min-width: 64px;
    text-align: center;
    width:100%;
}

.active{

    color: #f3554d;
}
.area-list{
	overflow: auto;
}

.ml20{
	margin-left:20px;
}
.ml10{
  margin-left:10px;
}
.system{
  padding-left:0;
}
.f12{
  font-size:12px;
}
</style>
