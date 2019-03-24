from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField('名称',max_length=50,null=False)
    describe = models.TextField('描述',default="")
    create_time = models.DateTimeField('创建时间',auto_now=True)
    update_time = models.DateTimeField('更新时间', auto_now_add=True)
    status = models.BooleanField('状态',default=1)

    def __str__(self):
        return self.name