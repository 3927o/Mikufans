function update_like(rpid,likes_now){
    var xhr
    var formData = new FormData()
    // 实例化一个 XMLHttpRequest 对象
    if (window.XMLHttpRequest) {
      xhr = new XMLHttpRequest();
    } else if (window.ActiveXObject) { // IE 6及以下
      xhr = new ActiveXObject("Microsoft.XMLHTTP");
    }
    // 绑定 xhr.readyState 改变时调用的回调
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                console.log(xhr.responseText)
                console.log('请求成功')
            } else {
            console.log('请求错误')
            }
        }
    }
    formData.append('rpid',rpid)
    formData.append('likes_now',likes_now)
    xhr.open('POST','update_like');
    // 设置请求头（可选）
    xhr.setRequestHeader('Accept', '*/*')
    // 发出请求
    xhr.send(formData);
    var likes=xhr.responseText
    document.getElementsByClassName("likes_"+rpid).innerHTML=likes
}