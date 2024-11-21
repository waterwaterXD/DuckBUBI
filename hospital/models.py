from django.db import models

# Create your models here.
class Hospital(models.Model):
    name = models.CharField(max_length=255)  # 醫院名稱
    address = models.CharField(max_length=255)  # 地址
    phone = models.CharField(max_length=20)  # 電話
    website = models.URLField(max_length=200, blank=True, null=True)  # 網站 (可選)
    photo = models.ImageField(upload_to='hospital_photos/', blank=True, null=True)  # 醫院照片 (可選)
    county = models.CharField(max_length=100, null=True)  # 縣市
    district = models.CharField(max_length=100, null=True)  # 行政區

    def __str__(self):
        return self.name