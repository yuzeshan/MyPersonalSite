/**
 * Created by lenovo on 2015/4/29.
 */
/*页面加载完成前的加载效果*/
//获取浏览器页面可见高度和宽度
var _PageHeight = document.documentElement.clientHeight,
    _PageWidth = document.documentElement.clientWidth;
//计算loading框距离顶部和左部的距离（loading框的宽度为215px，高度为61px）
var _LoadingTop = _PageHeight > 300 ? (_PageHeight - 300) / 2 : 0,
    _LoadingLeft = _PageWidth > 400 ? (_PageWidth - 400) / 2 : 0;

//在页面未加载完毕之前显示的loading Html自定义内容
var _LoadingHtml = '<div id="loadingDiv" style="position:absolute;left:0;top:0;width:100%;height:' + _PageHeight + 'px;background:rgb(51,51,51);opacity:1.0;z-index:10000;">' +
        '<div style="position: absolute;left: ' + _LoadingLeft + 'px; top:' + _LoadingTop + 'px; width: 400px; height:300px; background:rgb(51,51,51) url(/static/img/3.gif) no-repeat scroll 5px 10px;"></div>' +
        '</div>';

//呈现loading效果
document.write(_LoadingHtml);

//window.onload = function () {
//    var loadingMask = document.getElementById('loadingDiv');
//    loadingMask.parentNode.removeChild(loadingMask);
//};

//监听加载状态改变
document.onreadystatechange = completeLoading;

//加载状态为complete时移除loading效果
function completeLoading() {
    if (document.readyState == "complete") {
        var loadingMask = document.getElementById('loadingDiv');
        loadingMask.parentNode.removeChild(loadingMask);


    }
}
