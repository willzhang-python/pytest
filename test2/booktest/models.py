from django.db import models


# 注意这个模型类管理器类是继承于models.Manager
class BookInfoManager(models.Manager):
    """图书模型管理器类"""
    # 1.改变查询的结果集
    # 重新定义all函数,过滤isDelete为false的内容
    def all(self):
        # 调用父类all方法获取所有的数据
        book = super().all()  # QuerySet
        # 对数据进行过滤
        book = book.filter(isDelete=False)
        # 返回book
        return book

    # 2.封装函数,操作模型类对应的数据表(增删改查)
    def create_book(self, btitle, bdate):
        # 创建图书对象
        # class_model = self.model
        # obj = class_model()
        obj = self.model()
        # 添加数据
        obj.bbook = btitle
        obj.bpub_date = bdate
        # 保存
        obj.save()
        # 返回数据
        return obj


# Create your models here.
class BookInfo(models.Model):
    """定义图示模型类"""
    # 图书名称
    # bbook = models.CharField(max_length=20, db_column="title")  # db_column 设置字段名称
    bbook = models.CharField(max_length=20)  # db_column 设置字段名称
    # 图书名称唯一
    # bbook = models.CharField(max_length=20, unique=True, db_index=True)  # unique名称要求唯一,建立索引
    # 价格,最大位数为10,小数为2
    # bprice = models.DecimalField(max_digits=10, decimal_places=2)
    # 出版日期
    bpub_date = models.DateField()
    # bpub_date = models.DateField(auto_now_add=True)  # 创建时间
    # bpub_date = models.DateField(auto_now=True)  # 更新时间
    # 阅读量
    bread = models.IntegerField(default=0)
    # 评论量
    bcomment = models.IntegerField(default=0)
    # 删除标记
    isDelete = models.BooleanField(default=False)
    # objects 此时是指向重新定义的图书管理器类
    objects = BookInfoManager()

    # class Meta:
    #     db_table = "booktest_bookinfo"  # 以下为执行类对应的表名

# '''
#     # 在类下面创建一个创建的类方法,但是这中方式不太好,
#     # 因为不要往类里面添加太多的东西,会显得很臃肿
#     # 可以考虑添加到图书馆模型管理类中去
#     @classmethod
#     def create_book(cls, btitle, bdate):
#         # 创建图书对象
#         obj = cls()
#         # 添加数据
#         obj.bbook = btitle
#         obj.bpub_date = bdate
#         # 保存
#         obj.save()
#         # 返回数据
#         return obj
#
#     def __str__(self):
#         return self.bbook
# '''


class HeroInfo(models.Model):
    """定义任务模型类"""
    # 英雄名
    hname = models.CharField(max_length=20)
    # 性别
    hgender = models.BooleanField(default=False)
    # 备注
    hcomment = models.CharField(max_length=200, null=True, blank=True)  # 允许为空及允许字段为空白
    # 关系属性
    hbook = models.ForeignKey("BookInfo")
    # 删除标记
    isDelete = models.BooleanField(default=False)


'''
class NewsType(models.Model):
    """新闻类型类"""
    # 类型名
    type_name = models.CharField(max_length=20)
    # 关系属性,代表属性下面的信息
    type_news = models.ManyToManyField("NewsInfo")


class NewsInfo(models.Model):
    """新闻类"""
    # 新闻标题
    title = models.CharField(max_length=128)
    # 发布时间
    pub_data = models.DateTimeField(auto_now_add=True)
    # 信息内容
    content = models.TextField()
    # 关系属性,代表内容所属的类型
    news_type = models.ManyToManyField("NewsType")


class EmployeeBasicInfo(models.Model):
    """员工基本信息"""
    # 姓名
    name = models.CharField(max_length=20)
    # 性别
    gender = models.BooleanField(default=False)
    # 年龄
    age = models.IntegerField
    # 关系属性,代表员工的详细信息
    employee_detail = models.OneToOneField('EmployeeDetailInfo')


class EmployeeDetailInfo(models.Model):
    """员工详细信息"""
    # 联系地址
    addr = models.CharField(max_length=256)
    # 教育经历
    # 关系属性,代表员工基本信息
    # employee_basic = models.OneToOneField('EmployeeBasicInfo') 
'''


class AreaInfo(models.Model):
    """地区模型类"""
    # 地区名称
    atitle = models.CharField(max_length=20)
    # 关系属性 代表当前地区的父级地区
    # 就是有三列,id列,第二列是城市列,第三列是上级地区,如广东省,下级地区是广州市下面的区
    aParent = models.ForeignKey("self", null=True, blank=True)
