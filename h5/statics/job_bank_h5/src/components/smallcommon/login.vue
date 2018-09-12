<template>
    <div>       
          <div class="mask login" @click.self="cancel_change_login">   
            <div class="form">
               <img class='close' src='../../assets/imgs/close.png'  @click.self='cancel_change_login'>
                <div class="d-login" v-if="!firstlogin">
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
                                            <input type="number" placeholder="请输入手机号码" 
                                             class="ipt-single" maxlength="11" name="phone"
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
                                                @click="getVerifyCode">
                                                获取验证码{{verify_name}}</span>

                                        </div>
                                    </div>
                                    <div class="error" id="error-msg"></div>
                                    <button class="submit" type="button" id="submit-login"  @click.stop.prevent="user_login">登录</button>
                                </form>
                                <div class="login-foot">
                                    <p>登录即代表你已同意公考黑板报<a href="http://mobile.winlesson.com/about/responsible">《用户协议》</a>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
            </div>
          </div>

          <!-- <div v-if="firstlogin" class="mask firstlogin">
                <div class="form">
                     <img class='close' src='../../assets/imgs/close.png'  @click.self='cancel_change_login'>
                    
                </div>
          </div> -->
    </div>
</template>

<script>
import { api_get_qrcode_img } from "../../networks/login"
import { api_get_polling_login } from "../../networks/login"
import { api_gzh_login } from "../../networks/login"


import { api_get_gzh_img } from "../../networks/login"
export default {
    name: 'HelloWorld',
    data () {
        return {
            username:'',
            verify_code:'',
            get_verify_code: 0,
            islogin:-1,
            firstlogin:true,
            openid:'',
            verify_name:'',
            scene:'',
            chat_timer:'',
            wximg:'',
        }
    },
    created: function() {
        var context = this;     
        var promise = api_get_gzh_img(context);
        promise.then(function(res) {
            console.log(res);
            console.log(res.scene);
            context.scene=res.scene;
            context.$store.commit("updateScene",res.scene);    
            context.wximg=res.url;
            //$("#imglogin").html("<img id='loginimg'   style='width:200px;' src="+res.url+" >");   
        }).catch(function(error){
            console.error(error);
        });
              
    },
    mounted: function() {
        var context = this;        
        this.chat_timer = setInterval(function() {
            context.pollinglogin();
        }, 3000)  
    },
    methods: {
        pollinglogin() {//轮询  3秒 
            var context = this;     
            var scene=context.scene;
            var promise = api_get_polling_login(context,scene);
            promise.then(function(res) {
                console.log(res.data.data);       
                if(res.data.data.status==1){//已注册  直接返回user
                    //清除定时器
                   clearInterval(context.chat_timer);
                    context.$store.dispatch('userLogin', res.data.data.user_id); 
                    context.$store.commit("updateShowmodel",false);
                      context.$message({
                      message: '登录成功',
                      type: 'success'
                    });
                    
                }
                if(res.data.data.status==2){//有openid无userid 
                    //清除定时器 
                    clearInterval(context.chat_timer);                
                    context.firstlogin=false;
                    console.log("open_id         "+res.data.data.open_id);
                    context.openid=res.data.data.open_id;
                  
                }                
            }).catch(function(error){
                console.error(error);
            });
        },
        cancel_change_login() {
             var _this = this;
            _this.$store.commit("updateShowmodel",false);
             console.log("cancel_change_login");

            //清除定时器
            clearInterval(_this.chat_timer);
        },
        beforeDestroy() {
            console.log("beforeDestroy");
           //清除定时器
           this.islogin=1;
           clearInterval(_this.chat_timer);
        },
        getVerifyCode(){
            var _this = this;
            if (_this.username == '') {
                _this.$message({
                  message: '请输入手机号码',
                  type: 'warning'
                });
                return false;
            }      
            _this.verify_name=60;
            var secrect=_this.getSecrect('815','674');
            var urls="https://api.web.platform.winlesson.com/user/get/phone/web/verify_code";
            this.axios.post(urls + '?from=web&platform=2&username=' + _this.username+'&secrect='+secrect).then(function(response){
              if (response.data.code != 200) {
                this.errors.verify_code = {error: true, errormsg: response.data.msg}
                return false
              }
              setTimeout(function () {
                 _this.verify_code=response.data.verifyCode;
              }, 3000);

              var timer = setInterval(function() {
                if (_this.verify_name <= 0) {
                  clearInterval(timer)
                }
                _this.verify_name -= 1
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
            console.log(_this.username);console.log(_this.openid);console.log(_this.scene);
            var promise = api_gzh_login(_this,_this.username,_this.openid,_this.scene);
            promise.then(function(res) {
                console.log(res);
                if(res.status=='200'){
                    _this.$message({
                      message: '登录成功',
                      type: 'success'
                    });
                    _this.$store.dispatch('userLogin', res.data.user_id);  
                    _this.$store.commit("updateShowmodel",false);
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
.login .form {
     width: 320px;
    padding: 20px 5px 40px 5px;
    margin: auto;
    margin-top: 10%;
    left: 0;
    right: 0;
    background: #fff;
    text-align: center;
        border-radius: 5px;
}
.firstlogin .form {
     width: 320px;
    padding: 20px 5px 40px 5px;
    margin: auto;
    margin-top: 10%;
    left: 0;
    right: 0;
    background: #fff;
    text-align: center;
        border-radius: 5px;
}
.mask {
    position: fixed;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    background: rgba(0, 0, 0, 0.4);
    z-index: 99;
}
.close{
      right: 20px;
    top: 20px;
    cursor: pointer;
    width: 20px;
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
    font-size: 16px;
    text-align: center;
}


.d-login .content-bd .bd-form {
    width: 100%;
    margin-top: 25px;
    font-size: 15px;
}
.d-login .content-bd .login-foot {
    padding-top: 15px;
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
    padding: 3px 10px;
    margin-top: 8px;
        cursor: pointer;
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
      line-height: 20px;
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
    font-size: 12px;
    left: 0;
    position: absolute;
    line-height: 43px;
    font-weight: 400;
}
.d-login .content-bd .login-foot p {
    text-align: center;
}

.d-login .content-bd p {
    font-size: 0.32rem;
    color: #999999;
    text-align: center;
}
.firstlogin .from img{
    display:none;
}
.d-login>img{
    display:none;
}
</style>
