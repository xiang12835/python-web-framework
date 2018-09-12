<template>
  <div class="head-info clearfix"><!--头部信息-->
  	 <div class="zone-box clearfix">
  	    <div class='btnflex ml10 mr10'>
  	        <div class="btngk btnmm"   :class="{btnmmactive:updateIsgk==1}"  @click='btngk'>国考</div>
  	        <div class="btnsk btnmm"   :class="{btnmmactive:updateIsgk==0}"  @click='btnsk'>省考</div>
  	    </div>
  	    <div v-if="stateIsgk" class='flexsb mr10 '> 
  	    	<span>关注地区：</span> 
  	    	<a href="#" data-toggle="modal" data-target="#showRegion">{{gkareaname}}</a>
  	    </div>   
  	    <div v-else class='flexsb '>  
    			<div>
    				<span>省份：</span> 
    		    <a  href="#" data-toggle="modal" data-target="#showProvince">{{skprovincename}}</a> 
    			</div>


    			<div class="ml100">
    				<span>地区：</span> 
    		    	<a  href="#" data-toggle="modal" data-target="#showProvinceRegion">{{skareaname}}</a> 
    			</div>
  	    </div>      
    </div>

<!-- 省份 -->
<div class="modal fade" id="showProvince" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title" id="myModalLabel">选择省份</h4>
      </div>
      <div class="modal-body">
    	 <div class="area-list">
           <ul class="province">
                <li class="select-province" 
                	:class="{active:item.province_id==province_id}" 
                	:data-id="item.province_id"  
                	v-for="(item,index) in province_list" 
                	@click="selectProvince(item.province_id,item.province_name)">
                	{{item.province_name}}
                </li>
            </ul>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">取消</button>
        <button type="button" class="btn btn-primary" @click="btnsaveprovince">保存</button>
      </div>
    </div>
  </div>
</div>

<!-- 省考下地区 -->
<div class="modal fade" id="showProvinceRegion" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title" id="myModalLabel">选择地区</h4>
      </div>
      <div class="modal-body">
    	 <div class="area-list">
           <ul class="provincearea">
                <li class="select-province" 
                  :class="{active:item.area_id==province_area_id}" 
                   :data-id="item.area_id"  
                   v-for="(item,index) in province_areslist" 
                   @click="selectProvinceArea(item.area_id,item.area_name)">
                	{{item.area_name}}
                </li>
            </ul>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">取消</button>
        <button type="button" class="btn btn-primary" @click="btnsaveprovincearea">保存</button>
      </div>
    </div>
  </div>
</div>


<!-- 国考下地区 -->
<div class="modal fade" id="showRegion" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title" id="myModalLabel">选择地区</h4>
      </div>
      <div class="modal-body">
    	 <div class="area-list">
           <ul class="area">
                <li class="select-province" 
                	:class="{active:item.area_id==area_id}" 
                	:data-id="item.area_id"  
                  :data-name="item.area_name"  
                	v-for="(item,index) in areslist" 
                	@click="selectArea(item.area_id,item.area_name)">
                	{{item.area_name}}
                </li>
            </ul>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">取消</button>
        <button type="button" class="btn btn-primary" @click="btnsavearea">保存</button>
      </div>
    </div>
  </div>
</div>




  </div>
</template>

<script>
import { api_get_area_list } from "../../networks/Conditions"
import { api_get_province_list } from "../../networks/Conditions"
import { api_post_my_resume} from "../../networks/others"
import { api_post_sub_resume} from "../../networks/others"

export default {
	name: 'HelloWorld',
	data () {
	  return {
	  	 updateIsgk:1,
	     areslist:[],
	     province_list:[],
	     province_areslist:[],
	     gkareaname:'北京',
	     skprovincename:'北京',
	     skareaname:'全部',
	     area_id:1,
	     area_name:"",
	     province_id:2,
	     province_name:"",
	     province_area_id:-1,
	     province_area_name:"",
       wxopenid:"",
	  }
	},
	computed: {
    user() {
           return this.$store.state.user
    },
    stateIsgk() {
      return this.$store.state.isgk
    },
    stateAreaid() {
      return this.$store.state.Areaid;
    },
    stateAreaname() {
      return this.$store.state.Areaname;
    },
    stateProvinceid() {  
      return this.$store.state.Provinceid;
    },
    stateProvincename() {  
      return this.$store.state.Provincename;
    },
    stateProvinAreaid() {
      return this.$store.state.ProvinAreaid;
    },
    stateProvinAreaname() {
      return this.$store.state.ProvinAreaname;
    },
    stateOpenid() {     
        return this.$store.state.openid;
    },

  },  
  created: function() {
  	
  	var context = this;

    context.wxopenid=context.stateOpenid;      
      
      context.gkareaname = context.stateAreaname;
      context.skprovincename = context.stateProvincename;
      context.skareaname = context.stateProvinAreaname;
      context.area_id = context.stateAreaid;
      context.province_id = context.stateProvinceid;
      context.province_area_id = context.stateProvinAreaid;
      context.updateIsgk = context.stateIsgk;

       //登录
      if(context.stateAreaid==''){
        //第一次加载
        context.$store.commit("updateAreaid",1);
        context.$store.commit("updateAreaname",'北京'); 
      } 
      if(context.stateProvinceid==''&&context.stateProvinAreaid==''){
        //第一次加载
        context.$store.commit("updateProvinceid",2);
        context.$store.commit("updateProvincename",'北京'); 
        context.$store.commit("updateProvinAreaid",'');
        context.$store.commit("updateProvinAreaname",'全部');
        context.gkareaname = "北京";
        context.skareaname = "全部";
      }
      if(context.updateIsgk==0){
          $(".btnmmactive").removeClass('btnmmactive');
          $(".btnsk").addClass('btnmmactive'); 
          context.get_area_list(context.province_id);
      } 
      else{
          context.get_area_list(1);
          if(context.wxopenid!=''){ //已登录
               //获取地区
              context.get_area_list(1);
               //获取用户简历
              context.getUseResume();
          }
      }

      context.get_province_list();
 
  },  
	methods: {
	  /*  获取地区  */
	  get_area_list(province_id) { 	  	
        var context = this;
        var promise = api_get_area_list(context,province_id);
        promise.then(function(res) {
        	//console.log(res);
        	if(context.updateIsgk){
        			context.areslist=res.areas;
        	}else{
        		res.areas.unshift({ 'area_id': '-1','area_name': '全部' });

        		context.province_areslist=res.areas;
        	}
        }).catch(function(error){
            console.error(error);
        });
	  },
	  /*  获取省份  */
	  get_province_list() { 	  	
        var context = this;
        var promise = api_get_province_list(context);
        promise.then(function(res) {
        	//console.log(res);
        	context.province_list=res.provinces.slice(1);
            // context.$store.commit('setIndexNav', index_nav);
        }).catch(function(error){
            console.error(error);
        });
	  },
	   /*  选择国考下地区  */
	  btnsavearea() { 
	  	var context = this;
	  	context.$store.commit("updateAreaid",context.area_id);
	  	context.$store.commit("updateAreaname",context.area_name); 	
	  	context.gkareaname=context.area_name;

      var wxopenid=context.stateOpenid;
       var userid=context.user.user_id;
      if(context.userid!=''){ //已登录
          //保存简历
          context.saveUseResume();
      }   
	  	$('#showRegion').modal('hide');

	  },
	   /*  选择省考下省份 */
	  btnsaveprovince() { 
	  	var context = this;
	  	context.get_area_list(context.province_id);
	  	context.skareaname="全部";
	  	localStorage.removeItem('ProvinAreaid');
	  	localStorage.removeItem('ProvinAreaname');
	  	context.province_area_id=-1;

	  	context.$store.commit("updateProvinceid",context.province_id);
	  	context.$store.commit("updateProvincename",context.province_name); 	
	  	context.skprovincename=context.province_name;
	  	$('#showProvince').modal('hide');
	  },
	  /*  选择省考下地区 */
	  btnsaveprovincearea() { 
	  	var context = this;
	  	context.$store.commit("updateProvinAreaid",context.province_area_id);
	  	context.$store.commit("updateProvinAreaname",context.province_area_name); 	
	  	context.skareaname=context.province_area_name;
	  	$('#showProvinceRegion').modal('hide');
	  },
	  selectArea(area_id,area_name) { 
	  	var context = this;
	  	context.area_id=area_id;
	  	context.area_name=area_name;
	  	$(".area .active").removeClass('active');
	  	$('.area li[data-id='+area_id+']').addClass('active');
	  },
	  selectProvince(province_id,province_name) { 
	  	var context = this;
	  	context.province_id=province_id;
	  	context.province_name=province_name;
	  	$(".province .active").removeClass('active');
	  	$('.province li[data-id='+province_id+']').addClass('active');
	  },
	  selectProvinceArea(province_area_id,province_area_name) { 
	  	var context = this;
	  	context.province_area_id=province_area_id;
	  	context.province_area_name=province_area_name;
	  	$(".provincearea .active").removeClass('active');
	  	$('.provincearea li[data-id='+province_area_id+']').addClass('active');
	  },
	  btngk() { 
      var context = this;
	  	 context.updateIsgk=1;
	  	 context.$store.commit("updateIsgk",1);
       context.get_area_list(1);
	  	 $(".btnmmactive").removeClass('btnmmactive');
	     $(".btngk").addClass('btnmmactive');
	  },
	  btnsk() { 
      var context = this;
	  	 context.updateIsgk=0;
	  	 context.$store.commit("updateIsgk",0);
	     $(".btnmmactive").removeClass('btnmmactive');
	     $(".btnsk").addClass('btnmmactive');	

       console.log("stateProvinceid        "+context.stateProvinceid);  
       console.log("stateProvinAreaid        "+context.stateProvinAreaid);

        if(context.stateProvinceid==''&&context.stateProvinAreaid==''){
          //第一次加载
          context.$store.commit("updateProvinceid",2);
          context.$store.commit("updateProvincename",'北京'); 
          context.$store.commit("updateProvinAreaid",'');
          context.$store.commit("updateProvinAreaname",'全部');
          context.gkareaname = "北京";
          context.skareaname = "全部";
        }
	     context.get_area_list(context.province_id);  
	  },
    /*获取用户简历*/
    getUseResume() {       
        var context = this;
        var wxopenid=context.stateOpenid;
        var promise = api_post_my_resume(context,wxopenid);
        promise.then(function(res) {
                console.log(res);
                context.area_id=res.user_resume.area;
                context.$store.commit("updateAreaid",context.area_id);
                var areslist = context.areslist;
                for (var i = 0; i < areslist.length;i++){
                      if (res.user_resume.area == areslist[i].area_id){
                          context.$store.commit("updateAreaname",areslist[i].area_name);  
                          context.gkareaname=areslist[i].area_name; 
                          context.area_name=areslist[i].area_name;       
                      }
                }  

                context.area_id
            }).catch(function(error){
                console.error(error);
            });
      },
      saveUseResume() { 
        var context = this;
        var userid=context.user.user_id;
        var wxopenid=context.stateOpenid;
        var region_id=context.area_id;
        var xl_id='';
        var inputzy='';
        var xw_id='';
        var xb_id='';
        var zzmm_id='';
        var gzjy_id='';
        var jcgzjy_id='';

        var promise = api_post_sub_resume(context,userid,wxopenid,region_id,xl_id,inputzy,xw_id,xb_id,zzmm_id,gzjy_id,jcgzjy_id);
        promise.then(function(res) {
          console.log(res);
        }).catch(function(error){
            console.error(error);
        });
      },
	}
}
</script>


<style scoped>
.head-info {
    position: relative;
    background: #fff;
    min-height: 50px;
      display: flex;
     align-items: center;
}
.btnflex{
    display: flex;
}
.btnmm{
   padding:5px 5.5px;
    color:#606266;
    font-size:12px;
    min-width:37px;
}

.btngk{
 border:1px solid #eee;
 border-top-left-radius:5px;
  border-bottom-left-radius:5px;
      cursor: pointer;
}
.btnsk{
 border-top:1px solid #eee;
 border-right:1px solid #eee;
 border-bottom:1px solid #eee;
  border-top-right-radius:5px;
  border-bottom-right-radius:5px;
      cursor: pointer;
}

.btnmmactive{
    background: #f1514e;
    color: #fff;
    border:0px solid #eee;
}
.ml10{
   margin-left: 10px;
}
.mr10{
    margin-right: 10px;
}
.w20{
    width: 12%
}
.w50{
    width: 50%
}
.w30{
  width: 30%
}
.flexsb{
    display:flex;
    font-size: 12px;
}
.zone-box .center{
    display: flex;
     align-items: center;
     justify-content: center; 
}

.zone-box{
    display: flex;
    justify-content:  flex-start;
     align-items: center;
    width: 100%;
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
    padding: 0 10px;
    margin: 0 10px;
    border: 1px solid #f1f1f1;
    cursor: pointer;
    font-size: 14px;
    margin-bottom: 10px;
    min-width: 64px;
    text-align: center;
}

.active{
	      border: 1px solid #f3554d;
    color: #f3554d;
}
.area-list{
	overflow: auto;
}

.ml100{
	margin-left:20px;
}
.info-center ul li {
    float: left;
    font-size: 14px;
    color: #92a3b5;
    padding-right: 15px;
    line-height: 30px;
}
.info-center ul li span {
    font-size: 14px;
    color: #f1514e;
    padding: 0 10px;
}
.info-center ul li i {
    color: #202a34;
}
em, i {
    font-style: normal;
}

</style>
