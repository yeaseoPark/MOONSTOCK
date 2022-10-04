from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    #업종 choice
    SECTOR_CHOICE = {
        ('manufacturing','Manufacturing'),
        ('wholesale','Wholesale business'),
        ('retail','Retail business'),
        ('restaurant','Restaurant business')
    }

    # 회사명 정의
    company_name = models.CharField(max_length=200, null=False)
    # 회사 번호 정의
    company_phone = models.CharField(max_length=140, null=True)
    # 회사 주소
    company_address = models.CharField(max_length=300, null=True)
    #업종 정의
    company_sector = models.CharField(max_length=80, choices=SECTOR_CHOICE)
    #대표자 이름 재정의
    representative_name = models.CharField(blank=True, max_length=255)
    #대표자 핸드폰 번호 정의
    representative_phone = models.CharField(max_length=140, null=True, blank=True)

    
