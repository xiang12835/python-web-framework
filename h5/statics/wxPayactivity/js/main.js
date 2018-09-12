function getCookie(name) {
	var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");　　
	return(arr = document.cookie.match(reg)) ? unescape(arr[2]) : null;
}

function setCookie(name, value, Days) {
	var exp = new Date();
	exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
	document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString() + "; path=/";
}


function getQueryString(name, str) {
  var s = str || window.location.search;
  var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
  var r = s.substr(1).match(reg);
  if (r != null) return unescape(r[2]);
  return null;
 
}

