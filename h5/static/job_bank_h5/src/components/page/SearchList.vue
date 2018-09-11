<template>
   <div class="d-search js-search js-panel">
    <img src="../../assets/imgs/blackback.png"  @click="backto" class="backimg" alt="">
            <div class="search-hd">
                <div class="item-left">
                    <div class="iconfont icon-guanbi"></div>
                    <input placeholder="搜索感兴趣的内容" class="search-input" id="searchKeywords" v-model='input_search' > 
                    </input>
                    <img src="../../assets/imgs/删除x.png" class="icon-chacha" @click='btnDel'>
                </div>
                 <div class='btn-search' @click='btnSearch'>搜索</div>  
                
            </div>
            <div class="search-panel" v-if="hidelist">
                <div class="title">热门搜索</div>
                <div class="search-list">
                    <div class='search-list-li' v-for="(item,index)  in hotslist"   
                        @click='gotosearchlist(item)' :data-id="item"> 
                      <em class="t-red">{{index+1}}.</em>{{item}}
                    </div>
                </div>
            </div>
            <div class="search-panel js-search-panel "  v-if="hidelist">
                <div class="title">历史搜索
                    <img src="../../assets/imgs/删除.png" class="iconfont icon-lajitong floatright f18" @click='clearhistorylist'>
                    
                </div>
                <div class="search-list his-search-list">
                    <div class='search-list-li ' v-for="(item,index) in historylist"  > 
                    <i @click='gotosearchlist(item)'   :data-id="item"> {{item}}</i>
                    <img src="../../assets/imgs/删除x.png" class="iconfont icon-chacha floatright mt15" @click='delnowhistory(item)' 
                    :data-title="item">
                    </div>
                </div>
            </div>



            <div class="search-panel" v-if="!hidelist">
                <div class='news'>
                    <div class="news-bd" id="exam_info_div">
                        <div class="news-bd-list" id="exam-list-div">     
                            <div class='news-bd-list-li' v-for="item in newslist">
                                <router-link :to="{ name: 'newsInfo', params: { news_id: item.id }}">
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
                            </div>   
                                                                        
                        </div>

                        <div class="badge-btn next-page-btn" @click='getmore'  v-if="showbtn">点击加载更多</div>
                        <div v-else class="list-no-more">
                            <div class="baseline"><span class="baseline-span">无更多数据啦</span></div>
                        </div> 
                    </div>
                </div>
            </div>

</div>
</template>

<script>
import { api_get_search_list } from "../../networks/others"
import { api_get_search_info} from "../../networks/others"

export default {
	name: 'HelloWorld',
	data () {
		return {
		      hidelist:true,//显示默认搜索
              input_search:"",
              pageNum:1,
              hotslist:[],
              historylist:[],
              newslist:[],
              showbtn:true,
		}
	},
	computed: {
        statehistorylist() {
          return this.$store.state.historylist
        },
    },
    created: function() {
		var context = this;
        context.historylist = context.statehistorylist;
        context.searchinput='';
        //热门搜索
        var promise = api_get_search_list(context);
        promise.then(function(res) {
            //console.log(res);
            context.hotslist=res
        }).catch(function(error){
            console.error(error);
        });
    },
    methods: {
        gotosearchlist(name){//点击热门搜索
            var that=this;
            that.input_search=name;
              
            that.getsearchlist(1);
        },
        getsearchlist: function (pageNum) {//获取搜索结果
              var that=this;
              var text = that.input_search;

              var historylist = that.historylist
              var flage = true;
              for (let i in historylist) {
                  if (historylist[i] == text) {  
                      //如果数组中有该项，flage变为false  
                      flage = false
                  }
              }  

              
              //如果通过上面的循环检测，flage依然是true，那么则说明原缓存数组中没有这个，我们就可以将其缓存起来  
              if (flage) {
                  historylist.push(text)  //把这个城市添加进要缓存的数组中  
              }  

              that.$store.commit("updatehistorylist",historylist);
    
              if (pageNum==1){
                  that.newslist=[];
              }

            var promise = api_get_search_info(that,text,pageNum);
            promise.then(function(res) {
                that.hidelist=false;
                if(res!=''){
                    that.newslist=that.newslist.concat(res.data);
                }       
                if (res.data == ''||res=='') {
                   that.showbtn=false;
                }
            }).catch(function(error){
                console.error(error);
            });
        },
        btnDel(){//input清空
              var that = this;
              that.hidelist=true;
              that.newslist=[];
              that.input_search='';
        },
        btnSearch(){
            var that = this;
            that.getsearchlist(1);
        },
        clearhistorylist(){//清空历史记录
            var that = this;
            that.historylist=[];
            that.$store.commit("updatehistorylist",[]);
        },
        delnowhistory(name){ //var that = this;
            var that = this;
            var historylist = that.historylist;
            for (let i in historylist) {
                if (historylist[i] == name) {
                    historylist.splice(i, 1);
                }
            }  
             that.$store.commit("updatehistorylist",historylist);
              
        },
        getmore(){
              var that = this;
              var pageNum = that.pageNum + 1;
              that.pageNum=pageNum;
              that.getsearchlist(pageNum);  
        },
         backto() {   
            this.$router.push({ path: '/'}) 
        },
        gotosearchinfo() {   
            this.$router.push({ path: '/'}) 
        },

    }

}
</script>


<style scoped>

.d-search {
    left: 0;
    top: 0;
    z-index: 1;
    width: 100%;
    height: 100%;
    padding: 8.5px;
    box-sizing: border-box;
    background-color: #fff;
}



.search-hd .item-left {
    display: flex;
    justify-content: initial;
    align-items: center;
    -webkit-box-flex: 1;
    flex: 1;
    background-color: #f8f8f8;
    height: 100%;
    padding: 0 8.5px;
    box-sizing: border-box;
    font-size:12px;
    padding-left:10px;

}



.search-hd {
    display: flex;
    justify-content: initial;
    align-items: center;
    height: 34px;
    margin-bottom: 13px;
        margin-left: 30px;
}

.search-input{
    margin-left: 10px;
    width: 100%;
}
.d-search .search-panel {
    margin-bottom: 13px;
}
.d-search .search-panel .title {
    font-size: 15px;
    color: #a5a4a4;
    margin-bottom: 13px;
    position: relative;
}


.d-search .search-panel .search-list-li{
    position: relative;
    height: 42px;
    line-height: 42px;
    font-size: 13px;
    border-bottom: 1px solid #efefef;
    text-overflow: -o-ellipsis-lastline;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
}
.t-red{
        color: #fc6769;
        margin-right: 4px;
}

.d-search .search-panel {
    margin-bottom: 13px;
}


.btn-search {  
  margin-left: 8px;  
  width: 15%;  
  line-height: 30px;  
  text-align: center;  
  border: 1px solid #eee;  
  border-radius: 3px;  
  font-size: 12px;
  height: 32px;
} 


.news {
    background-color: #fff;

}


.news-bd .news-tips {
    color: #a5a4a4;
    text-align: center;
    margin-bottom: 11px;
    font-size: 12px;
}

.bsk-color{
color: #f1514e;
}   

.news-bd-list-li:not(:first-child){
    border-top: 1px solid #efefef;
    padding-top: 11px;
    padding-bottom: 11px;
}

.news-bd .item-hd {
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

.news-bd .item-fd {
    position: relative;
    color: #a5a4a4;
    font-size: 12px;
    overflow: hidden;
}
.news-bd .item-fd .fd-left {
    float: left;
}
.news-bd .item-fd .fd-right {
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
    margin-bottom:50px;
}

.baseline {
    padding: 20px 0;
    text-align: center;
    position: relative;
    height: 22px;
    line-height: 22px;
    margin-bottom:50px;
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
width:19px;
text-align:center;

}

.f18{
    font-size: 18px;
}
input{
    background:#f8f8f8;
    border:none;
      outline:none;
}
.mt15{
    margin-top:15px;
}
em, i {
    font-style: normal;
}
.icon-chacha{
    width: 12px;
}
.backimg{
        width: 20px;
    position: absolute;
    margin-top: 6px;
}
</style>
