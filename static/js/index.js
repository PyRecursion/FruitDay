var city=$(".select li")
	console.log(city)
	var curcity=$(".addr")
	for (var i = 0; i<city.length; i++) {
		city[i].onclick=function(event){
			curcity[0].innerText=event.target.innerText		
		}
	}

// 切换图片

var img=$("#banner").children()
var i=0
var timer =setTimeout(autoimg,2000)

function autoimg() {
	img[i].toggleClass("img1")
	i>img.length ? i=i+1 : i==0;

}



