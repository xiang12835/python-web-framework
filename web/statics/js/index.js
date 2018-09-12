// 奖项设置：
// award:奖项[1|2|3|0], angle:开始角度, awardText:奖项说明, detailText:细节描述)
var option=[
  {
    award: 0,
    angle: [45, 90, 180, 270, 315],
    awardText: '',
    detailText: '没有中奖的小伙伴也不要气馁哦，还有海量公考精品课程免费听！'
  },
  {
    award: 1,
    angle: 135,
    awardText: '获得价值999元的线上公考辅导课程《2017公务员省考状元班》',
  },
  {
    award: 2,
    angle: 225,
    awardText: '获得必胜课课程代金券100元',
  },
  {
    award: 3,
    angle: 0,
    awardText: '获得现金红包10元',
  }
];

$(function() {
  // 初始化：定位
  platePosition();
  // 抽奖行为：
  $("#lotteryBtn").on("click",function(){
    // 获取获奖信息：
    showResult(1);
  });
  // 蒙层行为：
  $(".layer").on("click",function(){
    $(".mask").hide();
    $(".layer").hide();
  });
  $(".layer .container").on("click",function(){
    stopBubble();
  })
});
$(window).on("resize", function() {
  platePosition();
})

// -----------------库函数----------------------//
// 获奖说明：
function showResult(num) {
  var obj=option[num];
  var angle=0;
  if(typeof(obj.angle)=="object") {
    var angleArr = obj.angle;
    angle = angleArr[Math.floor(Math.random() * angleArr.length)];
  }else {
    angle=obj.angle;
  }
  rotateFunc(obj.award, angle, obj.awardText, obj.detailText);
}

// 旋转
function rotateFunc(award, angle, awardText, detailText) {
  console.log(award+";"+angle+";"+awardText+";"+detailText);
  $('#lotteryBtn').stopRotate();
  $("#lotteryBtn").rotate({
    angle: 0,
    duration: 5000,
    animateTo: angle + (Math.random() * 45) + 1440,
    callback: function() {
      displayLayer(award, awardText, detailText);
      console.log(award);
    }
  });
};

// 转盘定位：
function platePosition() {
  $(".ly-plate").css("top", $(".bg").height() * .60638);
  // console.log($(".ly-plate").offset().top);
}

// 显示蒙层：
function displayLayer(award, awardText = "",
  detailText="请前往必胜课官网完善个人信息，领取奖品！") {
  // type:win|lose;
  // titleText:一等奖 二等奖 (for win)
  // awardText:红色奖品说明
  // detailText:灰色提示
  var win = "";
  switch (award) {
    case 1:
      award = "一";
      win = true;
      break;
    case 2:
      award = "二";
      win = true;
      break;
    case 3:
      award = "三";
      win = true;
      break;
    default:
      win = false;
      break;
  }

  var layer = $(".layer"),
    title = layer.find(".title"),
    awardE = layer.find(".award"),
    detail = layer.find(".detail"),
    btnl = layer.find(".btnl"),
    btnr = layer.find(".btnr");

  if (win) {
    layer.addClass("win");
    title.html("恭喜你<small>抽中" + award + "等奖</small>");
    awardE.html(awardText);
    detail.html(detailText);
    btnl.html("下载APP");
    btnr.html("前往官网");
  } else {
    layer.addClass("lose");
    title.html("谢谢参与");
    detail.html(detailText);
    btnl.html("下载必胜APP");
    btnr.html("前去免费听课");
  }

  $(".mask").show();
  $(".layer").show();
}

function stopBubble(e) {
//如果提供了事件对象，则这是一个非IE浏览器
if(e && e.stopPropagation) {
　　//因此它支持W3C的stopPropagation()方法
　　e.stopPropagation();
} else {
　　//否则，我们需要使用IE的方式来取消事件冒泡
　　window.event.cancelBubble = true;
}
return false;
}
