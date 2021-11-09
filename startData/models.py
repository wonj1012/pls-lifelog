from django.db import models

# Create your models here.
class UserProfile(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    sex = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_profile'