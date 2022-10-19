from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from treebeard.mp_tree import MP_Node
from django.utils import timezone
from django.db.models import Q
from common.models import User
from metaData.models import Item, OtherCompany, Node

class Inventory(models.Model):
    # 기준 일시
    referenceDate = models.DateTimeField(blank=False, null=False, default=timezone.now)
    # 재고 품목
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=False, null=False)
    # 재고 량
    amount = models.IntegerField(blank=False, null=False, default=0)
    # 초기 재고 여부 확인
    is_initial = models.BooleanField(blank=False, null=False, default=False)
    # note
    note = models.TextField(blank=True, null=True, default='')

    class Meta:
        unique_together = ('referenceDate', 'item')


    def __str__(self):
        return "[" + str(self.referenceDate) + "]" + self.item.code + "-" + self.item.name

class Transaction(models.Model):
    # 거래 일시
    referenceDate = models.DateTimeField(blank=False, null=False, default=timezone.now)
    # 거래 품목
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=False, null=False)
    # 거래량
    amount = models.IntegerField(blank=False, null=False, default=0)
    # 거래 가격
    price = models.IntegerField(blank=False, null=False, default=0)
    # 거래 업체
    company = models.ForeignKey(OtherCompany, on_delete=models.SET_NULL, null=True)
    # is_buy = True 이면 내가 살 때의 거래
    is_buy = models.BooleanField(blank=True, null=False, default=False)
    # is_sell = True 이면 내가 팔 때의 거래
    is_sell = models.BooleanField(blank=True, null=False, default=False)
    # 기타 거래 내용
    note = models.TextField(blank=True,null=True, default='')

    class Meta:
        unique_together = ('referenceDate', 'item')

    def __str__(self):
        return "[" + str(self.referenceDate) + "]" + self.item.code + "-" + self.item.name

    def clean(self):
        init_inv_exist = True

        try:
            init_inv = Inventory.objects.filter(Q(item__exact = self.item) & Q(is_initial__exact = True))[0]
        except Exception as e:
            init_inv_exist = False

        if init_inv_exist == True:
            if init_inv.referenceDate > self.referenceDate:
                raise ValidationError({'referenceDate':('최초 상품 등록일을 다시 확인해주세요. 최초 상품 등록일 전에 입고하실 수 없습니다.')})

        if self.amount <= 0:
            raise ValidationError({'amount':('주문 수량이 0보다 작을 수는 없습니다.')})
        if self.price <= 0:
            raise ValidationError({'price': ('주문 가격이 0보다 작을 수는 없습니다.')})

class Produce(models.Model):
    # 생산 일자
    referenceDate = models.DateTimeField(blank=False, null=False, default=timezone.now)
    # 생산하는 품목(endItem)
    itemNode = models.ForeignKey(Node, null = False, blank=False, on_delete=models.CASCADE)
    # 생산하는 수량
    amount = models.IntegerField(blank=False, null=False, default=0)
    class Meta:
        unique_together = ('referenceDate', 'itemNode')

    def __str__(self):
        return "[" + str(self.referenceDate) + "]" + self.itemNode.item.code + "-" + self.itemNode.item.name + "(produce)"

    def clean(self):
        making_item = self.itemNode.item
        ingredient_query = self.itemNode.get_children()

        for ingredientNode in ingredient_query:
            ingredient = ingredientNode.item
            init_inv_exist = True
            try:
                init_inv = Inventory.objects.filter(Q(item__exact = ingredient) & Q(is_initial__exact = True))[0]
            except Exception as e:
                init_inv_exist = False

            if init_inv_exist == True:
                if init_inv.referenceDate > self.referenceDate:
                    raise ValidationError({'referenceDate': ('최초 재료 등록일을 다시 확인해주세요. 최초 재료 등록일 전에 생산하실 수 없습니다.')})

        init_inv_exist = True
        try:
            init_inv = Inventory.objects.filter(Q(item__exact = making_item) & Q(is_initial__exact = True))[0]
        except Exception as e:
            init_inv_exist = False

        if init_inv_exist == True:
            if init_inv.referenceDate > self.referenceDate:
                raise ValidationError({'referenceDate': ('최초 상품 등록일을 다시 확인해주세요. 최초 상품 등록일 전에 생산하실 수 없습니다.')})

        if self.amount <= 0:
            raise ValidationError({'amount':('주문 수량이 0보다 작을 수는 없습니다.')})


