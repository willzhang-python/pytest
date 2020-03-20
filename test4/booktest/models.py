from django.db import models


# Create your models here.
class BooInfo(models.Model):
    """定义图书模型类"""
    bbook = models.CharField(max_length=20)
    bpub_date = models.DateField()
    bread = models.IntegerField(default=0)
    bcomment = models.IntegerField(default=0)
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'booktest_bookinfo'