<template>
  <div >   
      <div id="images">
          <img :src="url" style=" width: 100%;" alt="">
      </div>
      <div style="width: 100%;text-align: center;position: absolute;top: 10px;">
          <img style="pointer-events: none;" src="../../assets/imgs/camera_image.png" alt=""> 
       </div> 
  </div>
</template>

<script>

export default {
  data () {
    return {
        url:''
    }
  },
  computed: {
    stateOpenid() {     
        return this.$store.state.openid;
    },
    stateimg() {     
        return this.$store.state.prszimg;
    },
    stateimgdata() {     
        return this.$store.state.imgdata;
    },
  },
  created: function() {
        var context = this;
        $(".g-footer").addClass('hide');
        if (context.stateimg!='') {
          context.url= context.stateimg;
          // context.$message({
          //   message: '长按保存图片分享给朋友',
          //   type: 'success'
          // });
        }else{
          context.$router.push({ path: '/prszactive'});  
        }
        
  },
  mounted () {
    var link = window.location.href;
    this.wxShare(this.stateimgdata.title, this.stateimgdata.show, link);
  },
  methods: {     

     
  }
}
</script>

<style scoped>
.lyimg{
  width:100%;
}
.pstop{
      position: absolute;
    padding-top: 153px;
    width: 100%;
    display: flex;
    justify-content: center;
        height: 100%;
      
}
.showimg{
   position: absolute;
    width: 100%;
    text-align: center;
    padding-top: 25px;

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
    background-color: #5cb85c;
    border-color: #4cae4c;
     width: 85px;
  height:35px;
  letter-spacing: 2px;
}
.fileinput-button {
    position: relative;
    overflow: hidden;
    margin-top:200px;
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
    font-size: 200px;
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

.news-bd-list{
  padding-left:0;
      background: #fff;
    width: 70%;
    margin: 0 auto;
        border-top: 1px solid #eee;
}
.news-bd-list-li{

    padding-top: 11px;
    padding-bottom: 11px;
    text-decoration:none;
        cursor: pointer;
}
.item-hd {
    font-size:16px;
    line-height: 21px;
    margin-bottom: 5px;
    text-overflow: -o-ellipsis-lastline;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
     text-decoration:none;
     color: #f2a900;
}
.item-fd {
    position: relative;
    color: #a18477;
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

.showjob{
      position: absolute;
    z-index: 99;
    top: 187px;
    width: 100%;
}
.yzimg{
     width: 100px;
     position: absolute;
    right: 12%;
    top: 85px;
}
.show_text{
  text-align: center;
       width: 70%;
    margin: 10px auto;
        font-size: 12px;
    color: #a18477;
}
em, i {
    font-style: normal;
}
.lebtn{
      display: inline-block;
    width: 106px;
    height: 38px;
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
    min-width: 140px;
    height: 35px;
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

.qr_img{
    width: 80px;
}


.qr_lable{
  width: 50%;
    color: #f84177;
    font-size: 12px;
    text-align: left;
}
.mb70{
     margin-bottom: 32px;
}

</style>