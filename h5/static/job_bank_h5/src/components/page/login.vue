<template>
    <div>
        <header class="g-header">
            <h2 class="hd">登录</h2>
            <img src="../../assets/imgs/返回_2.png"  @click="backto" class="backimg" alt="">
        </header>
        <div class="pt90">
            <section class="g-wrapper login-wrap">
                <!-- 绑定手机 -->
                <div class="d-login">
                    <div class="vertical">
                        <div class="content-bd">
                            <div class="login-logo">
                                <img src="../../assets/imgs/gklogo.png">
                            </div>
                            <h3 class="title">欢迎登录公考黑板报</h3>
                            <form action="" class="bd-form">
                                <div class="item">
                                    <label>手机号</label>
                                    <div class="lg-phone">
                                        <input type="number" placeholder="请输入手机号码" class="ipt-single" maxlength="11" name="phone"
                                         v-model='username'>
                                        <i class="icon-remove remove-phone"></i>
                                    </div>
                                </div>
                                <div class="item">
                                    <label>验证码</label>
                                    <div class="lg-code">
                                        <input type="number" placeholder="请输入验证码" 
                                                class="ipt-single" name="captch" 
                                                v-model="verify_code">
                                        <span class="verify-btn" id="verify-btn"  
                                            @click="getVerifyCode"
                                            :class="{grey:get_verify_code>0}">
                                            {{get_verify_code>0 ? get_verify_code+'秒' :'获取验证码'}}
                                            </span>

                                    </div>
                                </div>
                                <div class="error" id="error-msg"></div>
                                <button class="submit" type="button" id="submit-login"   @click.stop.prevent="user_login">登录</button>
                            </form>
                            <div class="login-foot">
                                <p>登录即代表你已同意公考黑板报<a href="http://mobile.winlesson.com/about/responsible">《用户协议》</a></p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            
        </div>
    </div>
</template>

<script>

import { api_gzh_login } from "../../networks/login"

export default {
	name: 'HelloWorld',
	data () {
		return {
            username: '',
		    verify_code: '',
            get_verify_code: 0,
            openid:'',
            userInfo:[],
            scene:'',
		}
	},
	computed: {
        stateOpenid() {     
            return this.$store.state.openid;
        },
        stateUserInfo() {     
            return this.$store.state.userInfo;
        },
    },
    created: function() {
        var context = this;
        context.openid=context.stateOpenid; 
		context.userInfo=context.stateUserInfo;  


        console.log(context.openid);
        console.log(context.userInfo);        
    },
    methods: {
    	backto() {   
           this.$router.go(-1);
        },
        getVerifyCode() {
            if (!this.username || this.username == ''){ 
                this.$message({
                  message: '请输入手机号',
                  type: 'warning'
                });
                return false
            }
            if (this.get_verify_code > 0) return false
            var _this = this
            this.get_verify_code = 60

            var secrect=_this.getSecrect('815','674');
            
            var url="https://api.web.platform.winlesson.com/user/get/phone/web/verify_code"
            this.axios.post(url + '?from=web&platform=2&username=' + this.username+'&secrect='+secrect).then(function(response){
              if (response.data.code != 200) {
                this.errors.verify_code = {error: true, errormsg: response.data.msg}
                return false
              }
              setTimeout(function () {
                 _this.verify_code=response.data.verifyCode;
              }, 2000);
              var timer = setInterval(function() {
                if (_this.get_verify_code <= 0) {
                  clearInterval(timer)
                }
                _this.get_verify_code -= 1
              }, 1000)
            })
          },
          getSecrect(a,b){
             var dd ='69b'+a+'047'+b+'83cf'
             return dd;
          },
          user_login() {
            var _this = this;
            if (_this.username == '') {
                _this.$message({
                  message: '请输入手机号码',
                  type: 'warning'
                });
                return false;
            }     
            console.log(_this.username);console.log(_this.openid);console.log(_this.scene);console.log(_this.userInfo.headimgurl,_this.userInfo.sex,_this.userInfo.nickname);

            var promise = api_gzh_login(_this,_this.username,_this.openid,_this.scene,_this.userInfo.headimgurl,_this.userInfo.sex,_this.userInfo.nickname);
            promise.then(function(res) {
                console.log(res);
                if(res.status=='200'){
                    _this.$message({
                      message: '登录成功',
                      type: 'success'
                    });
                    _this.$store.commit('getopenid', res.data.openid);
                    _this.$store.dispatch('userLogin', res.data.user_id);  
                     _this.$router.go(-1);
                    if(_this.chat_timer) { //如果定时器还在运行 或者直接关闭，不用判断
                       clearInterval(_this.chat_timer); //关闭
                    }     
           
                }
                  
            }).catch(function(error){
                console.error(error);
            });
        }

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
.pt90{
  padding-top:55px;
}
.g-wrapper {
    position: relative;
    min-height: 100%;
}
.d-login {
    position: fixed;
    left: 0;
    top: 0;
    z-index: 1;
    width: 100%;
    height: 100%;
    padding: 0.2667rem;
    box-sizing: border-box;
    background-color: #fff;
    position: relative;

}
.d-login .content-bd {
    margin: 45px 15px 15px;
    font-size: 15px;
}
.d-login .content-bd .login-logo {
    height: 60px;
    text-align: center;
    margin-bottom: 10px;
}
.d-login .content-bd .login-logo  img{
    height: 60px;

}
.d-login .content-bd .title {
    margin-bottom: 10px;
}

.d-login .content-bd .title {
    font-size: 20px;
    text-align: center;
}


.d-login .content-bd .bd-form {
    width: 100%;
    margin-top: 25px;
    font-size: 15px;
}
.d-login .content-bd .login-foot {
    padding-top: 37px;
}
.d-login .content-bd .item {
    height: 40px;;
    line-height: 40px;;
    margin-bottom: 5px;
    border-bottom: 1px solid #efefef;
    position: relative;
}
.d-login .content-bd .item .lg-phone {
    position: absolute;
    top: 0;
    left: 40px;
    right: 0;
    padding-right: 22px;
}
.d-login .content-bd .item .lg-phone .ipt-single {
    margin: 0;
    width: 100%;
}

.d-login .content-bd .item .ipt-single {
    width: 242px;
    height: 30px;
}
textarea, input, select {
    font-size: 14px;
    border: none;
    outline: 0;
    resize: none;
}

input, select, textarea {
    color: #222;
    font: normal normal 12px "Microsoft YaHei", Simsun, Arial, Helvetica, sans-serif;
}
.d-login .content-bd .item .lg-code {
    position: absolute;
    top: 0;
    left: 40px;
    right: 0;
}
.d-login .content-bd .item .lg-code .verify-btn {
    position: absolute;
    top: 0;
    right: 0;
}

.d-login .verify-btn {
    font-size: 12px;
    background-color: #fc6769;
    color: #fff;
    border-radius: 14px;
    line-height: 20px;
    padding: 7px 10px;
}
.d-login .content-bd .submit {
    width: 100%;
    height: 40px;
    box-sizing: border-box;
    margin-top: 30px;
    font-size: 15px;
    background-color: #f1514e;
    color: #fff;
    border-radius: 40px;
    outline:none;
    border: none;
}
.backimg{
    width:23px;
    position: absolute;
    top: 10px;
    left: 5px;
}
h1, h2, h3, h4, h5, h6 {
    font-weight: 300;
}
label {
    display: inline-block;
    max-width: 100%;
    margin-bottom: 5px;
    font-weight: 0;
    font-size:12px; 
}
.d-login .content-bd .login-foot p {
    text-align: center;
}

.d-login .content-bd p {
    font-size: 12px;
    color: #999999;
    text-align: center;
}

</style>
