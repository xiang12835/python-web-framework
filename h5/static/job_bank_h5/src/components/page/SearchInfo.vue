<template>
    <div class="wrap-box">
        <div class="title">
            搜索结果
        </div>
       <ul class="news-bd-list" id="exam-list-div">     
            <li class='news-bd-list-li' v-for="item in newslist" >
                <router-link  :to="{ name: 'newsInfo', params: { news_id: item.id }}">
                    <div class="item-hd">                       
                            {{item.title}}
                    </div>
                    <div class="item-fd">
                        <div class="fd-left">
                            <i class="mr5">公告时间</i>
                            <i class=" bsk-color">{{item.inputtime}}</i>
                        </div>
                        <div class="fd-right">
                            <em  class="t24">
                                <i class='bsk-color'>{{item.is_signing}}</i>
                            </em>
                        </div>
                    </div>
                </router-link>                    
            </li>                                                          
        </ul>

        <div class="badge-btn next-page-btn"  v-if="showbtn" @click="getmore">点击加载更多</div>
        <div v-else class="list-no-more">
            <div class="baseline"><span class="baseline-span">无更多数据啦</span></div>
        </div> 
    </div>
</template>

<script>
import { api_get_search_info} from "../../networks/others"


export default {
	name: 'HelloWorld',
	data () {
		return {
		   newslist:[],
		   depttitle:'',
           pageNum:1,
           showbtn:true,
		}
	},
	computed: {
        router_search_name() {
        	return this.$route.params.searchname
        },
    },
    watch: {
        router_search_name: {
            deep: true,
            handler: function (val) {
                this.newslist=[];
                this.showbtn=true;
                this.get_search_info();
            }
        },
    },
    created: function() {
		this.get_search_info();
    },
    methods: {
		get_search_info() { 	  	
	        var context = this;
	        var name =context.router_search_name;
            var pageNum =context.pageNum;
	        var promise = api_get_search_info(context,name,pageNum);
	        promise.then(function(res) {
                if(res!=''){
                    context.newslist=context.newslist.concat(res.data);
                }      	
                if (res.data == ''||res=='') {
                   context.showbtn=false;
                }
	        }).catch(function(error){
	            console.error(error);
	        });
		},
        getmore() {  
            var context = this;
            context.pageNum++;
            context.get_search_info();
        },  

    }

}
</script>


<style scoped>


.content .wrap-content .content-box .wrap-box {
    width: 100%;
    min-height: 810px;
    background: #fff;
    padding: 15px 15px;
    border: 1px solid #f1f4f6;
}
.router-link-active {
    background: #f0f3f5;
    border-left: 2px solid #f3554d;
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

.news-bd-list-li:not(:first-child){
    border-top: 1px solid #efefef;
    padding-top: 11px;
    padding-bottom: 11px;
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


.badge-btn {
    width: 207px;
    height: 38px;
    text-align: center;
    line-height: 38px;
    margin: 11px auto;
    border: 1px solid #f1514e;
    color: #f1514e;
    font-size: 16px;
    border-radius: 26px;
}

.baseline {
    padding: 20px 0;
    text-align: center;
    position: relative;
    height: 22px;
    line-height: 22px;
}

.baseline:before {
    position: absolute;
    top: 31px;
    left: 50%;
    margin-left: -40%;
    content: '';
    display: block;
    width: 80%;
    height: 1px;
    background: #dfdfdf;
}

.baseline-span {
    position: relative;
    display: inline-block;
    background: #f8f8f8;
    padding: 0 0.2667rem;
    font-size: 12px;
}
.floatright{
  float:right;
z-index:2;
width:30px;
text-align:center;

}


.title{
        font-size: 16px;
    margin-bottom: 20px;
}
a {
    color: #262626!important;
    text-decoration: none;
}
em, i {
    font-style: normal;
}
</style>
