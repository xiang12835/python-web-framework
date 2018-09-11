<template>
  <div>
      <div>
        <div class="pstop">
          <div class="line hide"></div>
          <form class="btn btn-success fileinput-button" id="formid" enctype="multipart/form-data">
              <input id="camera_image"  name="image"  type="file"  accept="image/*" multiple  @change="tirggerFile($event)">
          </form>  
          
        </div> 
      </div> 
      <div  class="showimg" id="showimg"></div>   
      <img class="bgimg" src="../../assets/imgs/Photograph.png" alt="">  
  </div>
</template>

<script>

import { api_get_recongitionimg } from "../../networks/others"

export default {
  data () {
    return {

    }
  },
  mounted () {
    var link = window.location.href;
    this.wxShare('公考黑板报', '拍出我的职位', link);
    $(".g-footer").addClass('hide');
  },
  methods: {
       // 拍照
      tirggerFile : function (event) {
            var that=this;
            console.log(event);
            var file = event.target.files[0]; // (利用console.log输出看结构就知道如何处理档案资料)
            if (!/image\/\w+/.test(file.type)) {
                //alert("请确保文件为图像类型");
                return false;
            }

            var showimg = document.getElementById("showimg");
            var reader = new FileReader();       
            reader.readAsDataURL(file);
            reader.onload = function(e) {              
                 $("camera_image").val(this.result)  
                  //上传
                  showimg.innerHTML = '<img src="' + this.result + '" class="ddimg" style="width: 70%; margin-top:20%;" alt=""/>' 
                  $(".line").removeClass('hide');
             }

            that.showbg=false;
            $("#formid").addClass('hide');
            $(".pstop").addClass('black');
            $(".bgimg").addClass('hide');

            var formData = new FormData();

            formData.append('image',file);
            console.log(formData.get("image"));

            $.ajax({
              url: 'https://h5.platform.winlesson.com/t/upload/image',  
              type: 'POST',
              data: formData,
              cache: false,
              contentType: false,
              processData: false,
              success: function (data) {
                  that.getrecongition(data.url);            
              },  
              error: function (data) {  
                  console.log(data);  
              },  
              
          });        
      },
      getrecongition(url){
          var that=this;
          var promise = api_get_recongitionimg(that,url);
          promise.then(function(res) {
            console.log(res);
            if (res.data.url) {
               that.$store.commit("updateimg",res.data.url);
               that.$store.commit("updateperson",res.data.r);
               that.$router.push({ path: '/prszimg'}); 
            }
            else{
               alert("这张美颜闪爆了，请重新拍照");
               $("#formid").removeClass('hide');
               $(".pstop").removeClass('black');
               $(".bgimg").removeClass('hide');
                var showimg = document.getElementById("showimg");
                 showimg.innerHTML = '';
                   $(".line").addClass('hide');
            }           
          }).catch(function(error){
              console.error(error);
          });

      }
     
  }
}
</script>

<style scoped>
.pstop{
      position: absolute;
       width: 100%;
    display: flex;
    justify-content: center;
        height: 100%;
      
}
.showimg{
   position: absolute;
    width: 100%;
    text-align: center;
    padding-top: 15px;

}
.bgimg{
  width:100%;
  height:100%;
}

.btn {
    display: inline-block;
    padding: 6px 12px;
    margin-bottom: 0;
    font-size: 14px;
    font-weight: normal;
    line-height: 1.42857143;
    text-align: center;
    white-space: nowrap;
    vertical-align: middle;
    cursor: pointer;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    background-image: none;
    border: 1px solid transparent;
    border-radius: 4px;
}
.btn-success {
       color: #fff;
    background-color: #4cae4c;
    border-color: #4cae4c;
    width: 191px;
    height: 62px;
    letter-spacing: 2px;
    opacity: 0;
}
.fileinput-button {
       position: absolute;
    bottom: 28%;
}
input[type="file"] {
    display: block;
}

.fileinput-button input {
    position: absolute;
    top: 0;
    right: 0;
    margin: 0;
    opacity: 0;
    -ms-filter: 'alpha(opacity=0)';
    font-size: 100px;
    direction: ltr;
    cursor: pointer;
}
.hide{
  display:none;
}
.black{
  background-color:#000!important;
}
 .line{
    position: absolute;
    width: 80%;
    left: 10%;
    z-index: 2;
    border-top: 1px solid #f1514e;
    width: 80%;
    left: 10%;
    box-shadow:  0px 0px 40px red;
    animation: myScan 8s infinite alternate;
    -webkit-animation: myScan 8s infinite alternate;
}

@keyframes  myScan{
    from { top:0px; }
    to { top: 400px; }
}

.news-bd-list-li:first-child{
    padding-top: 4px;
    padding-bottom: 11px;
    text-decoration:none;
        cursor: pointer;
}
.news-bd-list-li:not(:first-child){
    border-top: 1px solid #efefef;
    padding-top: 11px;
    padding-bottom: 11px;
    text-decoration:none;
        cursor: pointer;
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
.news-bd-list{
  padding-left:0;
      background: #fff;
    width: 90%;
    margin: 0 auto;
    padding: 10px;
}
.showjob{
      position: absolute;
    z-index: 99;
    top: 60px;
    width: 100%;
}
.yzimg{
  width: 70px;
    margin-left: 30px;
}
.show_text{
  text-align: center;
    margin: 20px;
        font-size: 16px;
}
em, i {
    font-style: normal;
}
.lebtn{
      display: inline-block;
    width: 106px;
    height: 43px;
    line-height: 30px;
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
    text-align: center;
    background-color: #fff;
    color: #f1514e;
    border-radius: 0;
    right: 20px;
    font-size: 14px;
    border: none;
        opacity: 0.9;

}
.ribtn{
      display: inline-block;
    width: 159px;
    height: 43px;
    line-height: 30px;
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
    text-align: center;
    background-color: #f1514e;
    color: #fff;
    border-radius: 0;
    right: 20px;
    font-size: 14px;
    border: none;
        margin-left: 10px;
        z-index:99;
}
.smlable{
      color: #909399;
    font-size: 10px;
    margin-top: 10px;
}
.center{
  text-align:center;
      margin-top: 20px;

}
.cover{
      display: block;
    width: 100%;
    height: 100%;
    position: absolute;
    left: 0;
    top: 0;
    z-index: 99;
    background-color: #000000;
    opacity: 0.7;
}
#guide{
      display: block;
    top: 5px;
    text-align: right;
    position: absolute;
    z-index: 100;
        width: 100%;

}
#guide img {
    width: 260px;
    height: 180px;

}
</style>