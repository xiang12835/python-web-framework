/**
 *  基于jQuery的倒数计时器 袁雅宜 2017-07-28
 *  支持时分秒，支持多个对象
 *  只能传入唯一的jQuery对象
 *  支持修改show()
 *  支持d:h:m:s和h:m:s两种显示模式。
 **/


// 参数：指定显示元素，结束时间，分隔符，时间显示样式，开始时间，自定义时间显示函数
function Countdown($obj, endTimeStr, divideChar, timeformate, startTimeStr, formateShow) {
  // 加入基本样式代码。
  if ($("style#countdown_style").length <= 0) {
    $("head").append('<style id="countdown_style" type="text/css"></style>');
  }
  $("style#countdown_style").append($obj.selector +'>* {text-decoration: none; font-style: normal;}');
  // 查错：
  if (!$obj.length) { console.error("Countdown Error: Is this a jQuery object?"); return false; } else if ($obj.length > 1) { console.error("Countdown Error: One thing at a time!"); return false; }
  // 初始化
  var divideChar = divideChar ? divideChar : ":",
    arr = endTimeStr.split(/[- : \/ ']/),
    endTime = new Date(arr[0], arr[1] - 1, arr[2], arr[3], arr[4], arr[5]),
    startTime = startTimeStr ? new Date(startTimeStr) : new Date(),
    per = endTime - startTime;

  if (endTime == "Invalid Date" || startTime == "Invalid Date") { console.error("Countdown Error: Wrong Date Format！"+endTimeStr); return false; }
  if (per < 0) { console.error("Countdown Error: You CAN'T end it before it start！"+endTimeStr); return false; }

  if (timeformate == 'd:h:m:s') {
    $obj.append("<d></d><i>天</i><h></h><i>" + divideChar + "</i><m></m><i>" + divideChar + "</i><s></s>");
  } else { //(timeformate == 'h:m:s')
    $obj.append("<h></h><i>" + divideChar + "</i><m></m><i>" + divideChar + "</i><s></s>");
  }

  var obj = {
    d: $obj.find("d"),
    h: $obj.find("h"),
    m: $obj.find("m"),
    s: $obj.find("s"),
    dd: parseInt(per / (1000 * 60 * 60)) % 24,
    hh: parseInt(per / (1000 * 60 * 60)),
    mm: parseInt(per / (1000 * 60)) % 60,
    ss: parseInt(per / 1000) % 60,
    // 输出：
    show: formateShow ? formateShow : function() {
      if (timeformate == 'd:h:m:s') {
        this.d.text(this.hh/24 <= 0 ? "0" + this.hh % 24 : parseInt(this.hh / 24));
        this.h.text(this.hh % 24 < 10 ? "0" + this.hh % 24 : this.hh % 24);
      } else {
        this.h.text(this.hh < 10 ? "0" + this.hh : this.hh);
      }
      this.m.text(this.mm < 10 ? "0" + this.mm : this.mm);
      this.s.text(this.ss < 10 ? "0" + this.ss : this.ss);
    },
    // 计算：以小时为准
    count: function() {
      if (this.ss > 0) {
        this.ss -= 1;
      } else if (this.ss == 0) {
        if (this.mm > 0) {
          this.mm -= 1;
          this.ss = 59;
        } else if (this.mm == 0) {
          if (this.hh > 0) {
            this.hh -= 1;
            this.mm = 59;
          } else if (this.hh == 0) {
            console.info("Countdown END!");
            clearInterval(this.timer);
          } else {
            console.error("error h");
          }
        } else {
          console.error("error m");
        }
      } else {
        console.error("error s")
      }
    },
    // 内部用的计时器
    _setTimer: function() {
      var _this = this;
      this.timer = setInterval(function() {
        _this.count();
        _this.show();
      }, 1000);
    }
  }
  // obj 结束
  obj.show();
  obj._setTimer();
  return obj;
}

var f = function() {
  if (this.hh >= 24) {
    this.h.text(parseInt(this.hh / 24) + "天")
  } else {
    this.h.text(this.hh + "时");
  }
  this.m.text(this.mm < 10 ? "0" + this.mm : this.mm);
  this.s.text(this.ss < 10 ? "0" + this.ss : this.ss);
}
// 参数：指定显示元素，结束时间，分隔符，时间显示样式，开始时间，自定义时间显示函数
// var c = new Countdown($("#counter"), "2017/8/1 24:00:00", "-", "d:h:m:s", "2017/7/28 13:23:00", f);

