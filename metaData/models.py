from django.db import models
from treebeard.mp_tree import MP_Node
from django.utils import timezone

from common.models import User


# Create your models here.
# 인벤토리 Item 테이블
'''
class Item(MP_Node):
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
    # parent 를 만드는데 필요한 수량
    required = models.IntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return self.code + ":" + self.name

    def get_previous(self):
        if not self.is_root():
            return self.get_prev_sibling()

    def get_next(self):
        if not self.is_root():
            return self.get_next_sibling()

    def get_is_root(self):
        return self.is_root()
'''

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
    # parent 를 만드는데 필요한 수량
    required = models.IntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return self.code + ":" + self.name

class Node(MP_Node):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=False, blank=False)
    note = models.TextField(null=True, blank=True, default="")

    def __str__(self):
        return self.item.code + ":" + self.item.name

    def get_previous(self):
        if not self.is_root():
            return self.get_prev_sibling()

    def get_next(self):
        if not self.is_root():
            return self.get_next_sibling()

    def get_is_root(self):
        return self.is_root()

# 업체 (인벤토리 아이템을 사오는 곳) (is_seller 과 is_purchaser 로 판매 / 구매 업체를 나눈다)

class OtherCompany(models.Model):
    # 업종 choice
    SECTOR_CHOICE = {
        ('manufacturing', 'Manufacturing'),
        ('wholesale', 'Wholesale business'),
        ('retail', 'Retail business'),
        ('restaurant', 'Restaurant business')
    }
    # 업체 명
    company_name = models.CharField(max_length=200, null=False, blank=False)
    # 업체 업종
    company_sector = models.CharField(max_length=80, choices=SECTOR_CHOICE, null=True)
    # 업체 전화번호
    company_phoneNum = models.CharField(max_length=200, null=True, blank=True)
    #업체 주소
    company_address = models.CharField(max_length=300, null=True, blank=True)
    # 업체 이메일 주소
    company_email = models.CharField(max_length=300, null=True, blank=True)
    # is_vendor : 판매 업체 유무를 나타냄
    # 0이면 자사 입장에서 사오는 업체가 아니며 1이면 해당 vendor에게서 item을 사온다
    is_vendor = models.BooleanField(null=False, blank=False)
    # is_customer : 판매 업체 유무를 나타냄
    # 0이면 자사 입장에서 item을 파는 업체가 아니며 1이면 해당 vendor에게서 item을 판다
    is_customer = models.BooleanField(null=False, blank=False)
    # 특이 사항
    note = models.TextField(null=True, blank=True)
    # 해당 업체와 거래하는 업체 (즉 자사)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name ='myCompany')

    def __str__(self):
        return self.company_name + "(" + self.company_sector + ")"