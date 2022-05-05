from statistics import mode
from djongo import models


class lottery_table(models.Model):
    uid = models.CharField(verbose_name='uid', max_length=10)


class Member(models.Model):
    # title = models.CharField(verbose_name='標題',max_length=10)
    uid = models.CharField(verbose_name='員工編號', max_length=10)
    uname = models.CharField(verbose_name='員工姓名', max_length=10)
    lottery_state = models.IntegerField(verbose_name='中獎')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.uname

    class Meta:
        verbose_name = '員工'
        verbose_name_plural = verbose_name


# Create your models here.
