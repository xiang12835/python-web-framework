// 基本设置：
var base_url = "http://test.api.platform.winlesson.com/";
var topic_id = 1;
var user_id = "201609172200021311004891";
var urls = {
  detail: "info/topic/detail",
  top_clist: "info/topic/top/comment_list",
  clist: "info/topic/comment_list",
  post: "info/topic/comment/post",
  admire: "info/topic/comment_admire/post"
};
getTopicDetail();
getTopNComments();
getAllComments();
/* ---------------------------------- 页面交互部分 --------------------------------*/
$(function() {
  // 页面样式：
  // 头图大小控制
  $(".banner").each(function() {
    var _this = $(this);
    _this.height(_this.width() / 375 * 150);
  });
  $("#activity_title").on('click',function(){
    window.location.href='description.html'
  })
  // 点赞行为：
  $('body').on('click', '.doilike', function() {
    var _this = $(this);
    // 发送
    $.ajax({
      url: base_url + urls.admire,
      data: {
        cid: _this.parents("li").data("cid"),
        user_id: _this.parents("li").data("uid")
      },
      type: "post",
      success: function(res) {
        if (res.code != 200) return false;
        // 样式调整
        // 撤销赞：
        if (_this.hasClass('liked')) {
          _this.addClass('like').removeClass('liked')
            .next().text(parseInt(_this.next().text()) - 1);
        }
        // 点赞：
        else if (_this.hasClass('like')) {
          _this.addClass('liked').removeClass('like')
            .next().text(parseInt(_this.next().text()) + 1);
        }
      }
    })
  });
  //
  //进入话题评论对话框：
  $("#fake").on("click", function() {
    $("#mask").show();
    $("#dialog").find("blockquote").hide()
      .parent().show().find("#reply_content").focus();
    $('#reply_content').attr('data-cid', '');
  });
  $("#mask").on("click", function() {
    $("#mask").hide();
    $("#dialog").hide();
  });
  //
  // 回复特定的评论：
  $('body').on('click', '.comment', function() {
    // 要回复谁？
    var _this = $(this);
    // 显示评论框：
    $('#mask').show();
    $('#dialog').find('blockquote img').attr('src', _this.parents("li").find('.portrait img').attr('src'))
      .parents('blockquote').find('.content').text(_this.parents("li").find('.content').text())
      .parents('blockquote').show()
      .parents('#dialog').show().find("#reply_content").focus();
    $('#reply_content').attr('data-cid', _this.parents("li").data("cid"));
  });
  //
  // 提交按钮的行为：
  $('#dialog #submit').on('click', function() {
    var data = {
      tid: topic_id,
      user_id: user_id,
      content: $('#reply_content').val()
    };
    if (!!$('#reply_content').attr('data-cid')) {
      data.reply_comment_id = $('#reply_content').attr('data-cid');
    }
    // console.log(data);
    $.ajax({
      url: base_url + urls.post,
      type: 'post',
      data: data,
      success: function(res) {
        if (res.code != 200) return false;
        // 评论提交成功：
        alert("您的评论提交成功！");
        $('#all_comments').html('');
        getAllComments();
        $("#mask").hide();
        $("#dialog").hide();
      }
    })
  });
})
/* ---------------------------------- 封装的行为： ------------------------------ */
// 话题基本信息：
function getTopicDetail() {
  $.ajax({
    url: base_url + urls.detail + "?tid=" + topic_id,
    type: "get",
    success: function(res) {
      if (res.code != 200) return false;
      var topic_data = res.topic;
      document.getElementById('banner').src = topic_data.background_image;
      document.getElementById('title').innerText = topic_data.title;
      document.getElementById('activity_title').innerHTML = topic_data.activity_title+'<i class="more"></i>';
      document.getElementById('activity_desc').innerText = topic_data.activity_desc;
    }
  })
}
// 最赞回应：
function getTopNComments() {
  $.ajax({
    url: base_url + urls.top_clist + "?tid=" + topic_id + "&user_id=" + user_id,
    type: "get",
    success: function(res) {
      if (res.code != 200) return false;
      appendComments(res.comments, $('#best_comments'));
    }
  })
}
// 最全回应：
function getAllComments() {
  $.ajax({
    url: base_url + urls.clist + "?tid=" + topic_id + "&user_id=" + user_id,
    type: "get",
    success: function(res) {
      if (res.code != 200) return false;
      appendComments(res.comments, $('#all_comments'));
    }
  })
}
// 处理评论显示：
function appendComments(obj, parent) {
  var comments = obj;
  for (var i = 0; i < comments.length; i++) {
    var c = comments[i];
    var li_temp = '<li data-uid="' + c.user.user_id + '" data-cid="' + c.id + '"><header><span class="portrait"><img src="' + c.user.image_url + '"></span><span class="username">' + c.user.nickname + '</span>\
        <span class="addTime">' + c.created_at.toString().slice(5) + '</span><span class="goRight">\
        <i class="doilike ' + (c.admire_status ? 'liked' : 'like') + '"></i><i class="likeNum">' + c.admire_count + '</i><i class="comment"></i></span></header><div class="content">';
    // 引用：
    if (!!c.reply_content && JSON.stringify(c.reply_content) !== "{}") {
      li_temp += '<blockquote> <span class="username">' + c.reply_content.nickname + '</span>' + c.reply_content.content + '</blockquote>';
    }
    li_temp += c.content + '</div></li>';
    parent.append(li_temp);
  }
}
/* ---------------------------------- 库函数： ------------------------------ */
// 向APP回传userId：
// window.getappuserid.getUserID()
// document.getElementById("test").onclick = function(e) {
//   if (!!window.getappuserid) {
//     stopDefault(e);
//     alert(window.getappuserid.getUserID());//此对象会调用postUserIdStr(str)，调用成功的方法写在函数中。
//     return false;
//   } else {
//     stopDefault(e);
//     alert("未找到getappuserid对象！")
//   }
// }
// 提供给APP调用的方法：
// 允许APP向网页内传入userId。
// 注意！不要返回字符串！有些Android设备会将返回值打印出来，从而覆盖页面。
function postUserIdStr(str) {
  if (str) {
    // $(screen).append("<li>正在调用postUserIdStr(),传入参数为：" + str + "</li>");
    return true;
  }
  // $(screen).append("<li>正在调用postUserIdStr(),无传入参数！</li>");
  return false;
}
// ------------------------LIB------------------------------- //
// 获取URL参数
function getQueryString(name, str) {
  var s = str || window.location.search;
  var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
  var r = s.substr(1).match(reg);
  if (r != null) return unescape(r[2]);
  return null;
}
// 阻止默认事件
function stopDefault(e) {
  if (e && e.preventDefault) e.preventDefault();
  else window.event.returnValue = false;
  return false;
}
