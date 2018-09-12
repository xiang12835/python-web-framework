<template>
  <div class="new-list">
      <ul class="news-bd-list">
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
</template>

<script>
import { api_get_new_list } from "../../networks/News"


export default {
	name: 'HelloWorld',
	data () {
	  return {
	     newsList:[],
       isgk:1,
       area_name:'',
       province_name:'',
       provincearea_name:'',
       category_id:'',
       pageNum:1,
       pageSize:20,
       showmore:true,
	  }
	},
	computed: {
      stateIsgk() {     
        return this.$store.state.isgk;
      },
      stateAreaname() {
        return this.$store.state.Areaname;
      },
      stateProvincename() {  
        return this.$store.state.Provincename;
      },
      stateProvinAreaname() {
        return this.$store.state.ProvinAreaname;
      },
      stateCategory_id() {
        return this.$store.state.Category_id;
      },
      user() {
        return this.$store.state.user
      },
  },
  watch: {
    stateIsgk: {
        deep: true,
        handler: function (val) {
            this.isgk=val; 
            this.clear();
            this.get_new_list();
        }
    },
    stateAreaname: {
        deep: true,
        handler: function (val) {
            this.area_name=val; 
            this.clear();
            this.get_new_list();
        }
    },
    stateProvincename: {
        deep: true,
        handler: function (val) {
            this.province_name=val; 
            this.provincearea_name='';
            this.$store.commit("updateProvinAreaid",'');
            this.$store.commit("updateProvinAreaname",'');   
            this.clear();
            this.get_new_list();
        }
    },
    stateProvinAreaname: {
        deep: true,
        handler: function (val) {
            this.provincearea_name=val; 
            this.clear();
            this.get_new_list();
        }
    },
    stateCategory_id: {
        deep: true,
        handler: function (val) {
            this.category_id=val;
            this.clear();
            this.get_new_list();
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
      context.area_name=context.stateAreaname; 
      context.province_name=context.stateProvincename; 
      context.provincearea_name=context.stateProvinAreaname; 
      context.category_id=context.stateCategory_id;
      if(context.category_id){
        context.get_new_list();
      }
      
		
  },
	methods: {
	  get_new_list() {      
        var context = this;
        if (context.stateIsgk==1) {//国考
            var areaname=context.area_name;
             var sfarea_name='';
        }
        else{
            var areaname=context.province_name;
            var sfarea_name=context.provincearea_name;
        }

        if (sfarea_name=='全部') {
            var sfarea_name='';
        }

        var category_id=context.category_id;
        var pageNum=context.pageNum;
        var pageSize=context.pageSize;

        
        var promise = api_get_new_list(context,category_id,areaname,sfarea_name,pageNum,pageSize);
        promise.then(function(res) {
            //console.log(res);

            context.newsList= context.newsList.concat(res.news);

            if (res.news==''){                   
                context.showmore= false;
            }


        }).catch(function(error){
            console.error(error);
        });
    },
    getmore() {      
         var context = this;
         context.pageNum++;
         context.get_new_list();
    },
    clear(){
          this.pageNum=1;
          this.showmore=true;
          this.newsList=[];
    }
	}
}
</script>


<style scoped>

.bsk-color{
color: #f1514e;
}  
.new-list {
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
    margin-bottom:50px;
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
     margin-bottom:50px;
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
.news-bd-list{
  padding-left:0px;
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
a {
    color: #262626!important;
    text-decoration: none;
}
</style>
