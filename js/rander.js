var time=new Date()
document.getElementById("img").src="'{{url_for('static',filename=\"user/portrait/{}.jpg\".format(info[4]))}}?v="+time+"'";