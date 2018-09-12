<template>
  <div class="newspage">
    <header class="g-header">
        <h2 class="hd">通知公示</h2>
        <img src="../../assets/imgs/xxtx.png" class="iconxxtx" @click="gotoxxtx" >
         <span class="badge" v-if="num!=0">{{num}}</span>
        <img src="../../assets/imgs/search.png" class="iconsearch"  @click="gotosearch">
    </header>
    <div class="mt90">   
        <GkSk></GkSk>
        <newsType></newsType>
        <newsList></newsList>
    </div>
  </div>
</template>

<script>
import GkSk from '../smallcommon/GkSk.vue'
import newsType from '../smallcommon/newsType.vue'
import newsList from '../smallcommon/newsList.vue'

import { api_get_count } from "../../networks/others"

export default {
  name: 'newspage',
  data () {
    return {
        num:'',
    }
  },
  components:{
      GkSk,
      newsType,
      newsList,
  },
   computed: {
        user() {
             return this.$store.state.user
        },
  },
   watch: {
        user: {
            deep: true,
            handler: function (val) {
                this.getcount();
            }
        },
  },
  created: function() {
        var context=this;
        context.getcount();
        var link = window.location.href;
        this.wxShare('公考黑板报', '公务员实时职位查询_事业单位招聘公告', link);
    },
  methods: {
    getcount(){
            var context=this;
            var userid=context.user.user_id;
            if(userid!=''){
                var context = this;
                var promise = api_get_count(context,userid);
                promise.then(function(res) {
                    console.log("消息角标");
                    console.log(res);
                    context.num=res.data.unread_count;
                }).catch(function(error){
                    console.error(error);
                });
            }
        },
    gotosearch(){
        this.$router.push({ path: 'Searchlist'});
    },
    gotoxxtx(){
        this.$router.push({ path: '/remindpage'});
    },

  }
}
</script>


<style scoped>
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
.g-header .iconsearch {
    position: absolute;
     left: 10px;
    top: 10px;
    z-index: 1;
    color: #fff;
    font-size: 0.67rem;
    width: 23px;
    text-align: center;
}
.mt90{
  margin-top:45px;
}
.newspage{
   background-color: #f8f8f8;
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
.badge {
    display: inline-block;
    width: 15px;
    height: 15px;
    font-size: 9px;
    font-weight: 700;
    color: #fff;
    text-align: center;
    white-space: nowrap;
    vertical-align: middle;
    background-color: #ff4949;
    border-radius: 50%;
    position: absolute;
    top: 4px;
    right: 1px;
    border: 1px solid #fff;
   padding: 3px 0 0 0 ;
}
</style>
