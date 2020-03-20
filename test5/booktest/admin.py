from django.contrib import admin
from booktest.models import AreaInfo, PicTest
# Register your models here.


class AreaStackedInline(admin.StackedInline):
    # 写多类的名字
    # 这个是用来展示省下面的详细信息
    model = AreaInfo
    extra = 2


class AreaTabularInline(admin.TabularInline):
    model = AreaInfo
    extra = 2


class AreaInfoAdmin(admin.ModelAdmin):
    """地区模型管理类"""
    list_per_page = 10
    # 下面这个title是模型类中定义的方法
    # 默认可以排序的,但是title这个方法的话需要在模型类中定义
    list_display = ['id', 'atitle', 'title', 'parent']
    actions_on_bottom = True
    actions_on_top = False
    list_filter = ['atitle']  # 列表页的过滤栏
    search_fields = ['atitle']  # 列表页上的搜索框
    # fields = ['aParent', 'atitle']
    fieldsets = (
        ('基本', {'fields': ['atitle']}),
        ('高级', {'fields': ['aParent']})
    )

    # inlines = [AreaStackedInline]
    inlines = [AreaStackedInline]


admin.site.register(AreaInfo, AreaInfoAdmin)
admin.site.register(PicTest)