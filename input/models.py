from django.db import models

# Create your models here.


class Daily_Records(models.Model):
    l_date = models.DateField(auto_now_add= True)
    init_login = models.TimeField(null=True, blank=True)
    logout_time = models.TimeField(null=True, blank=True)
    assignments = models.CharField(max_length = 200, null=True)
    login_hours = models.DurationField(null=True, blank=True)
    
    @staticmethod
    def delete_all():
        Daily_Records.objects.all().delete()
