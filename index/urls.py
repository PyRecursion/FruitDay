from django.conf.urls import url,include
from .views import *

urlpatterns = [
    url(r'^login$',login_views,name="login"),
    url(r'^reg$',reg_views,name='reg'),
    url(r"^logout$",logout_views,name="logout"),
    url(r'^ckphone$',check_phone),
    url(r'^goodsinfo$',load_goods),
    url(r'check_login$',check_login),
    url(r'^',index_views,name='index'),

]