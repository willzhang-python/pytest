from django.db import models
# Create your models here.


class PicTest(models.Model):
    """上传图片"""
    goods_pic = models.ImageField(upload_to='booktest')


class AreaInfo(models.Model):
    """地址模型类"""
    # 地区名称 (verbose_name用于自定义标题)
    atitle = models.CharField(verbose_name='标题', max_length=20)
    # 自关联属性
    aParent = models.ForeignKey('self', verbose_name='父级', null=True, blank=True)

    def __str__(self):
        return self.atitle

    def title(self):
        return self.atitle
    title.admin_order_field = 'atitle'   # 用户排序
    title.short_description = '地区名称'   # 定义标题

    def parent(self):
        if self.aParent is None:
            return ''
        return self.aParent.atitle
    parent.short_description = '父级地区'