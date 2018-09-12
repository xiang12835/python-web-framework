<template> 
<div>
     
 
   <ul class="g-footer">                    
        <li class="jobside current" @click="gotoJob">  
            <a >
                <img src="../../assets/imgs/ld.png" class="lefticon" alt=""> 
               实时职位
            </a>
        </li>  
        <li class="newside" @click="gotoNew">    
            <a>
                <img src="../../assets/imgs/gggl.png" class="lefticon" alt=""> 
                通知公示
            </a>
        </li>
         <li class="examside" @click="gotoexam">    
            <a >
                <img src="../../assets/imgs/zt.png" class="lefticon" alt=""> 
                真题题库
            </a>
        </li>   
        <li class="zbside" @click="gotozb">    
             <a href="http://mobile.winlesson.com/page/4">
                <img src="../../assets/imgs/zb.png" class="lefticon" alt="" style="width:20px"> 
             直播课</a>
        </li> 
        
         <li class="myside" @click="gotomy">    
             <a>
                <img src="../../assets/imgs/me.png" class="lefticon" alt=""> 
             我的</a>
        </li> 

                                
    </ul>

</div>
</template>
<script>

  export default {
    name: 'index-nav',
     data () {
        return {
            
        }
    },
    computed: {
        user() {
             return this.$store.state.user
        },
    },

    methods: {
        gotoJob(){
            $(".current").removeClass('current');
            $(".jobside").addClass('current');
            this.$router.push({ path: '/'})
        },
        gotoNew(){
            $(".current").removeClass('current');
            $(".newside").addClass('current');
            this.$router.push({ path: '/newspage'})
        },
        gotozb(){
            $(".current").removeClass('current');
            $(".zbside").addClass('current');

        },
        gotoexam(){
            $(".current").removeClass('current');
            $(".examside").addClass('current');
            if (this.user.user_id!='') {
                window.location.href = "https://examx.winlesson.com/?user_id="+this.user.user_id;
            }
            else{
                this.$message({
                  message: '请先登录',
                  type: 'warning'
                });
            } 
        },
        gotomy(){
            $(".current").removeClass('current');
            $(".myside").addClass('current');
            this.$router.push({ path: '/personpage'})
        },
    }
　}
</script>

<style scroll>
.g-footer {
    position: fixed;
    left: 0;
    bottom: 0;
    z-index: 999;
    width: 100%;
    height: 50px;
    box-sizing: border-box;
    display: flex;
    justify-content: space-around;
    align-items: center;
    border-top: 1px solid #efefef;
    background-color: #fff;
    margin-bottom: 0;
    padding-left:0;
}
.g-footer li {
    flex: 1;
     text-align:center;
     font-size:12px;
}
.g-footer li img{
    width:20px;
    display: block;
    margin:0 auto;
}

.current a{
        color: #f1514e!important;
}

ul, ol, li {
    list-style: none;
}

a {
    color: #262626!important;
    text-decoration: none;
}
</style>
