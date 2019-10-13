from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
import json
from django.core import serializers
import decimal

# Create your views here.
def index_views(request):
    user_name=request.session.get("name")
    print('**************',locals())
    return render(request,'index.html',locals())

def login_views(request):
    if request.method=="GET":
        if "uid" in request.COOKIES:
            uid=request.COOKIES["uid"]
            user=User.objects.get(id=uid)
            phone=user.phone
            pwd=user.password
        return render(request,'login.html',locals())
    if request.method=="POST":
        uphone=request.POST["phone"]
        upwd=request.POST["pwd"]
        user=User.objects.filter(phone=uphone,password=upwd)
        if user:
            user=user[0]
            request.session['name'] = user.name
            request.session['id'] = user.id
            if request.POST.get('rpwd'):
                resp = redirect('/index')
                resp.set_cookie("uphone",user.phone,60*60*24*30)
                resp.set_cookie("uid",user.id,60*60*24*30)
                return resp
            else:
                return redirect('/index')
        return HttpResponse("用户名密码错误")


def reg_views(request):
    if request.method=="GET":
        return  render(request,'reg.html')
    if request.method=="POST":
        phone=request.POST["uphone"]
        ckphone=User.objects.filter(phone=phone)
        if ckphone:
            return render(request,"reg.html",locals())   #todo 验证重复
        name=request.POST.get("uname")
        password = request.POST.get("upwd")
        email= request.POST.get("uemail")
        #存数据库
        user=User()
        user.phone=phone
        user.name=name
        user.password=password
        user.email=email
        user.save()

        request.session["name"]=user.name
        request.session["id"] = user.id
        return redirect('/index')

def logout_views(request):
    if request.session["name"] and request.session["id"]:
        del request.session["name"]
        del request.session["id"]
    return redirect("/index")

#验证手机号是否已存在
def check_phone(request):
    uphone=request.GET["data"]
    print('*********',uphone)
    user=User.objects.filter(phone=uphone)
    if user:
        dic={
            "flag":"0",
            "msg":'手机号已注册请重新输入',
        }
    else:
        dic = {
            "flag": "1",
            "msg": '可以用的手机号',
        }
    dicjson = json.dumps(dic)
    return HttpResponse(dicjson)

def load_goods(request):
    goodtypes=GoodsType.objects.values()
    # goods=Goods.objects.values()
    lst=[]
    # print(goodtypes)
    for  goodtype in goodtypes:
        dic={}
        dic["type"]=goodtype
        # print(dic)
        goodtypeobj = GoodsType.objects.get(title=goodtype.get('title'))
        goods=goodtypeobj.goods_set.order_by('-id').values()
        lst1=[]
        for good in goods[0:10]:
            lst1.append(good)
        dic["goods"] = lst1
        lst.append(dic)
    print(lst)

    class DecimalEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, decimal.Decimal):
                return float(o)
            super(DecimalEncoder, self).default(o)
    jsonstr=json.dumps(lst, cls=DecimalEncoder)


    return HttpResponse(jsonstr)


def check_login(request):
    user_name = request.session.get("name")
    user_id = request.session.get("id")
    if user_name and user_id:

        good_id=request.GET.get("id")
        ucart=Cart.objects.filter(user_id=user_id,good_id=good_id)
        if ucart:
            ucart=ucart[0]
            ucart.amount+=1
            ucart.save()
        else:
            cart=Cart()
            cart.user_id=user_id
            cart.good_id=good_id
            cart.amount=1
            cart.save()
        return  HttpResponse(json.dumps({"flag":1}))

    else:
        dic={
            "flag":0
        }
        return HttpResponse(json.dumps(dic))
