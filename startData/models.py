from django.db import models

# Create your models here.
class Hs228M0809031355(models.Model):
    owner_id = models.IntegerField(blank=True, primary_key=True)
    time = models.TextField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    z = models.TextField(db_column='Z', blank=True, null=True)  # Field name made lowercase.     
    act = models.TextField(db_column='Act', blank=True, null=True)  # Field name made lowercase. 
    state = models.TextField(db_column='State', blank=True, null=True)  # Field name made lowercase.
    sequence = models.TextField(db_column='Sequence', blank=True, null=True)  # Field name made lowercase.
    keyword = models.TextField(db_column='Keyword', blank=True, null=True)  # Field name made lowercase.
    message_1 = models.TextField(db_column='Message_1', blank=True, null=True)  # Field name made lowercase.
    stt_1 = models.TextField(db_column='STT_1', blank=True, null=True)  # Field name made lowercase.
    message_2 = models.TextField(db_column='Message_2', blank=True, null=True)  # Field name made lowercase.
    stt_2 = models.TextField(db_column='STT_2', blank=True, null=True)  # Field name made lowercase.
    message_3 = models.TextField(db_column='Message_3', blank=True, null=True)  # Field name made lowercase.
    stt_3 = models.TextField(db_column='STT_3', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hs_228_m08_0903_1355'

class Hs230M0809031355(models.Model):
    owner_id = models.IntegerField(blank=True, null=True)
    time = models.TextField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    z = models.TextField(db_column='Z', blank=True, null=True)  # Field name made lowercase.     
    act = models.TextField(db_column='Act', blank=True, null=True)  # Field name made lowercase. 
    state = models.TextField(db_column='State', blank=True, null=True)  # Field name made lowercase.
    sequence = models.TextField(db_column='Sequence', blank=True, null=True)  # Field name made lowercase.
    keyword = models.TextField(db_column='Keyword', blank=True, null=True)  # Field name made lowercase.
    message_1 = models.TextField(db_column='Message_1', blank=True, null=True)  # Field name made lowercase.
    stt_1 = models.TextField(db_column='STT_1', blank=True, null=True)  # Field name made lowercase.
    message_2 = models.TextField(db_column='Message_2', blank=True, null=True)  # Field name made lowercase.
    stt_2 = models.TextField(db_column='STT_2', blank=True, null=True)  # Field name made lowercase.
    message_3 = models.TextField(db_column='Message_3', blank=True, null=True)  # Field name made lowercase.
    stt_3 = models.TextField(db_column='STT_3', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hs_230_m08_0903_1355'

class UserProfile(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    sex = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_profile'