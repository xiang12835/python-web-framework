<template>
<div class="job-myinfor">
  <div class="job-tag">
    <span>学历：<span>{{education_str}}</span></span>
    <span>专业：<span>{{professional}}</span></span>
    <a href="javascript:;" class="zone-plus" @click="gotomyresume">完善简历</a>
    </div>
    <img v-if="firstshowimg==''" @click="hideimg" src="../../assets/imgs/sc.png" class="firstimg" alt="">
</div>
</template>

<script>
import { api_post_my_resume} from "../../networks/others"

export default {
	name: 'HelloWorld',
	data () {
	  return {
        education_str:'本科',
	    professional:'会计学',
        firstshowimg:'',
	  }
	},
	computed: {
        user() {
           return this.$store.state.user
        },
        stateAreaid() {
            return this.$store.state.Areaid
        },
        stateFirstImg() {
            return this.$store.state.firstshowimg
        },
    },
    watch: {
        stateAreaid: {
            deep: true,
            handler: function (val) {
                this.getmyresume();
            }
        }
    },
    created: function() {
       var context=this;
       context.getmyresume();
       context.firstshowimg=context.stateFirstImg;
       console.log(context.stateFirstImg);
    },
    methods: {
        getmyresume(){
            var context=this;
            var userid=context.user.user_id;
            if(userid!=''){
                var promise = api_post_my_resume(context,userid);
                promise.then(function(res) {
                    console.log(res);
                    context.education_str=res.user_resume.education_str;
                    context.professional=res.user_resume.professional;
                }).catch(function(error){
                    console.error(error);
                });
            }      
        },
        gotomyresume(){
            var context=this;
            var userid = context.user.user_id;
            if(userid!=''){
                this.$router.push({ path: '/myresume' })
            }  
            else{
                context.$message({
                  message: '请先登录',
                  type: 'warning'
                });
                context.$router.push({ path: '/login'})
            }    
        }, 
        hideimg(){
            var context=this;
            context.firstshowimg=1;
            context.$store.commit('updatafirstshowimg', 1);
         }, 
    }
}
</script>


<style scoped>
.job-myinfor {
    padding: 0px 10px;
    border: 1px solid #f1f4f6;
    background: #fff;
    border-bottom: none;
    border-top: none;
}

.job-myinfor span.myinfor-tag {
    font-size: 14px;
    height: 16px;
    line-height: 16px;
    float: left;
    margin-top: 3px;
    padding-right: 17px;
}

.job-myinfor span {
   display: inline-block;
    font-size: 12px;
    padding-right: 10px;
}

.job-myinfor span em {
    color: #202a34;
}


.job-tag{
   padding: 16px 0px;
    border: 1px solid #f1f4f6;
    border-left: none;
    border-right: none;
    min-height: 55px;
}
 .zone-plus {
    float: right;
    border: 1px solid #f1514e;
    border-radius: 1rem;
    color: #f1514e!important;
    font-size: 12px;
    background: #fff;
    padding: 4px 10px;
    margin-top: -3px;
}

.firstimg{
    height:40px;
    position: absolute;
    right:20px;
}
</style>
