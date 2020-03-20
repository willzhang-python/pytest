from django.db import models
# 设计和表对应的类,模型类
# Create your models here.

# 一类
# 图书类
class BookInfo(models.Model):
    """图书模型"""
    # 图书名称,CharField说明是一个字符串,max_lenght制定字符串的最大长度
    btitle = models.CharField(max_length=20)

    # 出版日期,DateField说明是一个日期类型
    bpub_date = models.DateField()

    # 重写str方法以用于在管理后台展示书名
    def __str__(self):
        return self.btitle


# 多类
# 英雄类
class HeroInfo(models.Model):
    """英雄模型"""
    # 英雄名称
    hname = models.CharField(max_length=20)
    # 英雄性别
    hgender = models.BooleanField(default=False)
    # 英雄备注
    hcomment = models.CharField(max_length=128)
    # 关系属性 hbook,建立图书类和英雄人物类之间的一对多关系
    # 关系属性对应的表的字段名格式:关系属性名_id
    hbook = models.ForeignKey('BookInfo')

    def __str__(self):
        # 返回英雄页面
        return self.hname