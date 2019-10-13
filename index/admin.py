from django.contrib import admin
from .models import *

class GoodsAdmin(admin.ModelAdmin):
    list_display = ('title','price','spec','goods_type')
    list_display_links = ('title',)
    list_filter = ('goods_type',)



# Register your models here.
admin.site.register(User)
admin.site.register(GoodsType)
admin.site.register(Goods,GoodsAdmin)



