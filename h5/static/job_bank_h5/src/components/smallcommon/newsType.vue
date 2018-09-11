<template>
<div class="job-myinfor">
	<div class="tag-box">
		<ul class="clearfix" id="exam_category">
            <li v-for="(item,index) in news_type" 
            	class="ml10" 
            	:data-id="item.id"
            	:class="{active:item.id==category_id}" 
            	 @click="selectCategory(item.id)">
            	<span>{{item.title}}</span> 
            </li>
    	</ul>
	</div>
</div>
</template>

<script>
import { api_get_news_type } from "../../networks/News"

export default {
	name: 'HelloWorld',
	data () {
	  return {
	     news_type:[],
	     category_id: '',
	  }
	},
	computed: {
	    stateCategoryid() {	    	
	      return this.$store.state.Category_id
	    },
	},
	created: function() {
		/*  获取招考公告资讯分类列表  */
		var context = this;    
		context.category_id=context.stateCategoryid; 
		context.get_newstype();	
	},
	methods: {
	  /*  获取系统类型  */
	  get_newstype() { 	  	
	    var context = this;
	    var promise = api_get_news_type(context);
	    promise.then(function(res) {
	    	context.news_type=res.cates;
	    	if(context.stateCategoryid==''){
			   context.category_id=res.cates[0].id;
			   context.$store.commit("updateCategory_id",res.cates[0].id);
			   
	    	}
	    }).catch(function(error){
	        console.error(error);
	    });
	  },
	  selectCategory(category_id){
	  	var context = this;
	  	context.category_id=category_id;
	  	context.$store.commit("updateCategory_id",category_id);
	  	$(".clearfix .active").removeClass('active');
	  	$('.clearfix li[data-id='+category_id+']').addClass('active');
	  }
	  
	}
}
</script>


<style scoped>


.job-myinfor {
    border: 1px solid #f1f4f6;
    background: #fff;
    border-bottom: none;
    margin-top:10px;

}
.clearfix{
    width:100%;
    white-space: nowrap;
    overflow-x:scroll;
    overflow-y:hidden;
    padding-left:0px;
    display: flex;
    line-height:1px;
        border-bottom: 1px solid #eee;
        margin-bottom: 0px;
  }
  .clearfix li{
    width:80px;
    height:30px;
    padding:20px 0;
  }
  .clearfix li.active{
	    color: #f1514e;
  }

  .ml10{
  	margin-left: 10px;
  }
</style>
