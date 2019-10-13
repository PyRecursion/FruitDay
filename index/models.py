from django.db import models


# Create your models here.

#用户信息
class User(models.Model):
    phone=models.CharField(max_length=11)
    name=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    email=models.EmailField(null=True,blank=True)
    isActive=models.BooleanField(default=True)

    def __str__(self):
        return self.name
    def __repr__(self):
        return "<user:{}>".format(self.name)
    class Meta:
        db_table='user'


#商品类型
class GoodsType(models.Model):
    title=models.CharField(max_length=20,verbose_name="商品类型")
    picture=models.ImageField(upload_to='static/upload/goodstype',null=True,verbose_name="类型图")
    desc=models.TextField(verbose_name="类型描述")

    def __repr__(self):
        return self.title
    __str__=__repr__
    class Meta:
        db_table='goodStype'
        verbose_name_plural='商品类型信息'


class Goods(models.Model):
    title=models.CharField(max_length=50,verbose_name='商品名称')
    price=models.DecimalField(max_digits=7,decimal_places=2,verbose_name='商品价格')
    spec=models.CharField(max_length=20,verbose_name='计数单位')
    picture=models.ImageField(upload_to='static/upload/goods',null=True,verbose_name='商品图片')
    isActive=models.BooleanField(default=True,verbose_name='是否上架')
    goods_type=models.ForeignKey(GoodsType,verbose_name='商品所属类')

    def __repr__(self):
        return self.title
    __str__=__repr__

    class Meta:
        db_table="goods"
        verbose_name_plural="商品"


class Cart(models.Model):
    amount=models.IntegerField(max_length=2,verbose_name='数量')
    user=models.ForeignKey(User,db_column='user_id',verbose_name='购物车用户')
    good=models.ForeignKey(Goods,db_column='good_id',verbose_name='所选商品')

    def __repr__(self):
        return "{}:{}:{}".format(self.user,self.amount,self.good)
    __str__=__repr__

    class Meta:
        db_table="cart"
        verbose_name_plural="购物车"
