from django.db import models

class Sgform(models.Model):
    usn = models.CharField(max_length=30)
    phn = models.CharField(max_length=11)
    eml = models.CharField(max_length=30)
    psd = models.CharField(max_length=20)
    photp = models.CharField(max_length=10, default='')
    emailotp = models.CharField(max_length=30)

# class upload(models.Model):
#     csv = models.FileField(upload_to='csvupload/')
#     def __str__(self):
#         return self.csv.name

