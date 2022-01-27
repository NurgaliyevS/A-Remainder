from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    title = models.CharField(max_length=100)
    #### Blank ~ True - необязательное поле для заполнения
    memo = models.TextField(blank=True)
    #### Auto_now_add  - делает так, чтобы
    #### Время создании записи не менялось
    created = models.DateTimeField(auto_now_add=True)
    #### DateTimeField (Null) ~ Для него именно null, а не blank
    datecompleted = models.DateTimeField(null=True, blank=True)
    #### Важность события
    important = models.BooleanField(default=False)
    ### Внешний ключ
    ### Берет ID пользователя и привязывает к нему
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title


# #
#
# # Create your models here.
