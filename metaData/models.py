from django.db import models
from django.utils import timezone

from common.models import User


# Create your models here.
# 인벤토리 Item 테이블
class Item(models.Model):
    # 인벤토리 주인(유저별 관리)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    # 등록 코드
    code = models.CharField(max_length=200, null=False, blank=False)
    # 등록 품목 이름
    name = models.CharField(max_length=200, null=False, blank=False)
    # 인벤토리 품목 등록 일자
    registration_date = models.DateField(default=timezone.now)
    # end_item 여부 : 0이면 end item 이 아니고 1이면 end item 입니다.
    is_endItem = models.BooleanField(default=True)
    # 판매가 : end item 이 아닐 경우 판매가는 0으로 산정
    price = models.IntegerField(null=False, blank=False, default=0)
    # 비고
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.code + ":" + self.name

# end item 을 구성하는 BOM 테이블
class BOM(models.Model):
    # end item : 최종 만들어지는 item
    end_item = models.ForeignKey(Item, null=False, blank=False, on_delete=models.CASCADE, related_name='end_item')
    # 부모 노드
    parent_item = models.ForeignKey(Item, null =False, blank=False, on_delete=models.CASCADE, related_name='parent_item')
    # 자식 노드 : 부모 노드 = 자식 노드이면 root 노드로 가정
    child_item = models.ForeignKey(Item, null=False, blank=False, on_delete=models.CASCADE, related_name='child_item')
    # 부모 아이템을 만드는데 필요한 수량
    required = models.IntegerField(null=False, blank=False)
    # 깊이 : root 노드의 깊이 = 0
    level = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.end_item +'('+ str(self.level) + ")"







# 업체 (인벤토리 아이템을 사오는 곳) (is_seller 과 is_purchaser 로 판매 / 구매 업체를 나눈다)
"""
class Vendor(models.Model):
    # 업종 choice
    SECTOR_CHOICE = {
        ('manufacturing', 'Manufacturing'),
        ('wholesale', 'Wholesale business'),
        ('retail', 'Retail business'),
        ('restaurant', 'Restaurant business')
    }
    # 업체 명
    vendor = models.CharField(max_length=200, null=False, blank=False)
    # 업체 업종
    sector = models.CharField(max_length=80, choices=SECTOR_CHOICE)
    # 업체 전화번호
    phoneNum = models.CharField(max_length=200, null=False, blank=False)
    #업체 주소
    address = models.CharField(max_length=300, null=False, blank=False)
    # is_seller : 판매 업체 유무를 나타냄
    # 0이면 자사 입장에서 사오는 업체가 아니며 1이면 해당 vendor에게서 item을 사온다
    is_seller = models.BooleanField(null=False, blank=False)
    # is_purchaser : 판매 업체 유무를 나타냄
    # 0이면 자사 입장에서 item을 파는 업체가 아니며 1이면 해당 vendor에게서 item을 판다
    is_purchaser = models.BooleanField(null=False, blank=False)
"""