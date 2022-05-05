from statistics import mode
from djongo import models

class lottery_table(models.Model):
    uid = models.CharField(verbose_name='員工編號', max_length=10)
    urand = models.IntegerField(verbose_name='中獎亂數')  


class lottery(models.Model):
    lname = models.CharField(verbose_name='獎項名稱', max_length=10)
    lnum = models.IntegerField(verbose_name='獎項數量')

    def __str__(self):
        return self.uname

    class Meta:
        verbose_name = '獎項名稱'
        verbose_name_plural = verbose_name


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


class User_py:
    def __inti__(self, _id, _uid, _uname, _lottery):
        self.id = _id
        self.uid = _uid
        self.uname = _uname
        self.lottery = _lottery
# Create your models here.
