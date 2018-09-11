<template>
   <div>
    <div class="g-header">
        <div class="hd">个人中心</div>
    </div>

    <div class='g-wrapper mt90'>  
        <div class="my-hd">
            <div class="hd-info"  v-if="user.user_id==''">
                <div class='hd-info-span'>
                    <img src="../../assets/imgs/me01.png" class='hd-info-img'> 
                </div>
                <div class="info-text">
                    <em class="info-tex-em">Hi，你好</em>
                    <button type="button"  class="info-button" @click="gotologin">去登录</button>              
                </div>
             </div>

             <div class="hd-info"  v-if="user.user_id">
                <div class='hd-info-span'>
                    <img v-if="userInfo.headimgurl" :src="userInfo.headimgurl" class='hd-info-img'>
                </div>
                <div class="info-text">
                    <em class="info-tex-em">Hi，你好{{userInfo.nickname}}</em>           
                </div>
             </div>
        </div>

        <div class="van-cell-group van-hairline--top-bottom">
                <div class="van-cell dflex van-hairline van-cell--clickable" @click="gotomyresume">           
                    <div class="van-cell__title">
                    <em class="icon icon-lan iconfont icon-education"></em>
                    
                        <span class="van-cell-text">我的简历</span>
                        <div class="arrow"></div>
                    </div>              
                </div>
                <div class="van-cell dflex van-hairline van-cell--clickable" @click="gotoremind">           
                    <div class="van-cell__title">
                    <em class="icon icon-hong iconfont icon-education"></em>
                    
                        <span class="van-cell-text">我的提醒</span>
                        <div class="arrow"></div>
                    </div>              
                </div>    
                <div class="van-cell dflex van-hairline van-cell--clickable" @click='gotomycollect'>
                    <div class="van-cell__title">
                        <em class="icon icon-cheng iconfont icon-shoucang"></em>
                        <span class="van-cell-text">我的职位收藏</span>
                        <div class="arrow"></div>
                    </div>
                </div> 
                <div class="van-cell dflex van-hairline van-cell--clickable"  @click='gotomynews'>
                    <div class="van-cell__title">
                        <em class="icon icon-zi iconfont icon-shoucang"></em>
                        <span class="van-cell-text">我的公告收藏</span>
                        <div class="arrow"></div>
                    </div>
                </div> 
        </div>

        <div class="van-cell-group van-hairline--top-bottom mt10">
            <a href="http://mobile.winlesson.com/page/4" target="_blank">
                <div class="van-cell dflex van-hairline van-cell--clickable">            
                    <div class="van-cell__title">
                        <em class="icon icon-lv iconfont icon-live_icon"></em>
                        <span class="van-cell-text">直播课</span>
                         <div class="arrow"></div>
                    </div>
                </div> 
            </a> 
            <a href="http://mobile.winlesson.com/page/4" target="_blank">
                <div class="van-cell dflex van-hairline van-cell--clickable">          
                    <div class="van-cell__title">
                        <em class="icon icon-hong iconfont icon-zixun"></em>
                        <span class="van-cell-text">备考专区</span>
                        <div class="arrow"></div>
                    </div>                    
                </div>
            </a>           
        </div>

        <div class="van-cell-group van-hairline--top-bottom mt10">
            <a href="http://mobile.winlesson.com/page/4" target="_blank">
                 <div class="van-cell dflex van-hairline van-cell--clickable">                   
                    <div class="van-cell__title">
                        <em class="icon icon-zi iconfont icon-ren3"></em>
                        <span class="van-cell-text">关于我们</span>
                         <div class="arrow"></div>
                    </div>                   
                </div> 
            </a>          
        </div>


         <!-- <div class="van-cell-group van-hairline--top-bottom mt10"  v-if="user.user_id=='201801061033083594073816'||user.user_id=='201702071511512892383865'"> -->
        <div class="van-cell-group van-hairline--top-bottom mt10" > 
                 <div class="van-cell dflex van-hairline van-cell--clickable" @click="gotoprsc">                   
                    <div class="van-cell__title">
                        <em class="icon icon-zi iconfont icon-ren3"></em>
                        <span class="van-cell-text">颜职认证</span>
                         <div class="arrow"></div>
                    </div>                   
                </div>          
        </div>


        <div class="van-cell-group van-hairline--top-bottom mt10"  v-if="user.user_id=='201801061033083594073816'||user.user_id=='201702071511512892383865'">
             <div class="van-cell dflex van-hairline van-cell--clickable" @click="csgotoprsc">                   
                    <div class="van-cell__title">
                        <em class="icon icon-zi iconfont icon-ren3"></em>
                        <span class="van-cell-text">cs颜职认证</span>
                         <div class="arrow"></div>
                    </div>                   
                </div>          
        </div>




    
    </div>
</div>  
</template>

<script>

export default {
	name: 'HelloWorld',
	data () {
		return {
		      login_user_id: '',
              userInfo:[],
		}
	},
	computed: {
        stateUserInfo() {     
          return this.$store.state.userInfo;
        },
         user() {
             return this.$store.state.user
        },
    },
    watch: {
        user: {
            deep: true,
            handler: function (val) {
               
            }
        },
    },
    created: function() {
		this.userInfo=this.stateUserInfo;
        console.log(this.userInfo);
        var link = window.location.href;
        this.wxShare('公考黑板报', '公务员实时职位查询_事业单位招聘公告', link);
          $(".g-footer").removeClass('hide');
    },
    methods: {
        gotomyresume(){
            if (this.user.user_id!='') {
                this.$router.push({ path: '/myresume'})
            }
            else{
                this.$message({
                  message: '请先登录',
                  type: 'warning'
                });
                this.$router.push({ path: '/login'})
            } 
        },
        gotomycollect(){
            if (this.user.user_id!='') {
               this.$router.push({ path: '/mycollect'})
            }
            else{
                this.$message({
                  message: '请先登录',
                  type: 'warning'
                });
                this.$router.push({ path: '/login'})
            } 
        },
        gotomynews(){
            if (this.user.user_id!='') {
               this.$router.push({ path: '/mynews'})
            }
            else{
                this.$message({
                  message: '请先登录',
                  type: 'warning'
                });
                this.$router.push({ path: '/login'})
            } 
        },
        gotologin(){
            this.$router.push({ path: '/login'})
        },
        gotoremind(){
            if (this.user.user_id!='') {
                this.$router.push({ path: '/remindpage'})
            }
            else{
                this.$message({
                  message: '请先登录',
                  type: 'warning'
                });
                this.$router.push({ path: '/login'})
            } 
        },
        gotoprsc(){
            this.$router.push({ path: '/prszactive'})
        },
        csgotoprsc(){
            this.$router.push({ path: '/csprszactive'})
        },
    }

}
</script>


<style scoped>
.g-header {
    position: fixed;
    left: 0;
    top: 0;
    z-index: 8;
    width: 100%;
    line-height: 38px;
    background-color: #f1514e;
    color: #fff;
    height: 40px;
}
.g-header .hd {
     color: #fff;
    font-size: 16px;
    text-align: center;
    padding: 0 1rem;
    text-overflow: -o-ellipsis-lastline;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
         margin: 0 auto;
    width: 100px;
       display: flex;
    justify-content: center;
}

.g-wrapper {
    position: relative;
    min-height: 100%;
    background: #f8f8f8;
    border-bottom: 1px solid #efefef;
}

.mt90 {
    margin-top: 40px;
    margin-bottom: 10px;
}
.my-hd {
    background: #fff;
    border-bottom: 1px solid #efefef;
    margin-bottom: 11px;
    padding: 16px;
    display: flex;
    align-items: center;
    
}
.hd-info-img{
    max-width: 100%;
    max-height: 100%;
}

.hd-info-span{
    float: left;
    width: 66px;
    height: 66px;
    line-height: 66px;
    border-radius: 50%;
    overflow: hidden;
    text-align: center;
    border: 1px solid #f1f1f1;
}

.my-hd .hd-info .info-text {
    margin-left: 75px;
}

.info-tex-em{
   color:#333;
float:left;
font-size:18px;
overflow:21px;
text-overflow:ellipsis;
display:-webkit-box;
-webkit-line-clamp:1;
-webkit-box-orient:vertical;
margin-right: 10px;
}

.info-button{
   background:#f1514e;
color:#fff;
border-radius:5px;
padding:4px 13px;
font-size:12px;
height:24px;
line-height:14px;
outline:none;
 border:none;
}
.info-text{
    margin-top: 20px;
}


.van-cell-group {
    background-color: #fff;
}
.van-hairline--top-bottom::after {
    border-width: 1px 0;
}
.van-hairline::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 200%;
    height: 200%;
    -webkit-transform: scale(.5);
    transform: scale(.5);
    -webkit-transform-origin: 0 0;
    transform-origin: 0 0;
    pointer-events: none;
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
    border: 0 solid #e5e5e5;
}
.van-cell {
    width: 100%;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    padding: 10px 15px;
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
    line-height: 24px;
    position: relative;
    background-color: #fff;
    color: #333;
    font-size: 14px;
    overflow: hidden;
}

.van-cell:not(:last-child)::after {
    left: 15px;
    right: 0;
    width: auto;
    -webkit-transform: scale(1,.5);
    transform: scale(1,.5);
    border-bottom-width: 1px;
}

.mt10 {
    margin-top: 10px;
}
.mt5 {
    margin-top: 5px;
}

.arrow{
    width: 10px;
    height: 10px;
    border-top: 1px solid #999;
    border-right: 1px solid #999;
    position: absolute;
    right: 15px;
    transform: rotate(45deg);
    top:20px;
}

.icon{
    padding:2px;
    font-size:12px;
    color:#fff;
    margin-right: 5px;
    border-radius: 2px;
}

.icon-lan{
    background-color:#36baf5;
}

.icon-cheng{
    background-color:#fa7959;
}

.icon-lv{
    background-color:#31c09d;
}

.icon-hong{
    background-color:#fa6566;
}

.icon-zi{
    background-color:#d067d4;
}
em, i {
    font-style: normal;
}
</style>
