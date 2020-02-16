
//个人空间修改信息，花里胡哨没啥用
function move(){
    document.getElementById("container_change").style.display="block"
    document.getElementById("container_change").style.transform="translate(0px,-300px)"
    document.getElementById("info_movie").style.transform="translate(0px,-300px)"
}
function cancel(){
    document.getElementById("container_change").style.display="none"
    document.getElementById("info_movie").style.transform="translate(0px,300px)"
}

//更新点赞
function update_like(rpid){
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
                var likes=xhr.responseText
                document.getElementById("likes_"+rpid).innerHTML=likes
                console.log(xhr.responseText)
                console.log('请求成功')
            } else {
            console.log('请求错误')
            }
        }
    }
    formData.append('rpid',rpid)
    xhr.open('POST','/update_like');
    // 设置请求头（可选）
    xhr.setRequestHeader('Accept', '*/*')
    // 发出请求
    xhr.send(formData);
}

//更新点赞
function update_like_movie(av){
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
                var likes=xhr.responseText
                document.getElementById("likes_movie").innerHTML=likes
                console.log(xhr.responseText)
                console.log('请求成功')
            } else {
            console.log('请求错误')
            }
        }
    }
    formData.append('av',av)
    xhr.open('POST','/update_like_movie');
    // 设置请求头（可选）
    xhr.setRequestHeader('Accept', '*/*')
    // 发出请求
    xhr.send(formData);
}

//更新收藏
function update_collection(av){
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
                var likes=xhr.responseText
                document.getElementById("collection").innerHTML=likes
                console.log(xhr.responseText)
                console.log('请求成功')
            } else {
            console.log('请求错误')
            }
        }
    }
    formData.append('av',av)
    xhr.open('POST','/update_collection');
    // 设置请求头（可选）
    xhr.setRequestHeader('Accept', '*/*')
    // 发出请求
    xhr.send(formData);
}

//换页
function change_page(page,movie){
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
                var content=xhr.responseText;
                document.getElementById("comment_list").innerHTML=content;
                console.log("插入成功，以下为评论内容");
                console.log("以下为返回内容")
                console.log(xhr.responseText)
                console.log('请求成功')
            } else {
            console.log('请求错误')
            }
        }
    }
    formData.append('page',page)
    formData.append('movie',movie)
    xhr.open('POST','/change_page');
    // 设置请求头（可选）
    xhr.setRequestHeader('Accept', '*/*')
    // 发出请求
    xhr.send(formData);
}

//换页
function change_page_class(page,Class){
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
                var content=xhr.responseText;
                document.getElementById("left").innerHTML=content;
                console.log('请求成功')
            } else {
            console.log('请求错误')
            }
        }
    }
    formData.append('page',page)
    formData.append('Class',Class)
    xhr.open('POST','/change_page_class');
    // 设置请求头（可选）
    xhr.setRequestHeader('Accept', '*/*')
    // 发出请求
    xhr.send(formData);
}

//删除
function del(index,obj){
    var xhr
    var formData = new FormData()
    // 实例化一个 XMLHttpRequest 对象
    if (window.XMLHttpRequest) {
      xhr = new XMLHttpRequest();
    } else if (window.ActiveXObject) { // IE 6及以下
      xhr = new ActiveXObject("Microsoft.XMLHTTP");
    }
    var a
    if(obj=='pl') a='comment'
    else a='movie'
    // 绑定 xhr.readyState 改变时调用的回调
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var content=xhr.responseText;
                document.getElementById(a+"_"+index).innerHTML="删除成功！";
                console.log('请求成功')
            } else {
            console.log('请求错误')
            }
        }
    }
    formData.append('index',index)
    formData.append('obj',obj)
    xhr.open('POST','/delete');
    // 设置请求头（可选）
    xhr.setRequestHeader('Accept', '*/*')
    // 发出请求
    xhr.send(formData);
}

//回复
function reply(user){
    document.getElementById("send").value="@"+user+":"
}
