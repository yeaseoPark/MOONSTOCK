from django.db import models
from treebeard.mp_tree import MP_Node
from django.utils import timezone

from common.models import User
from metaData.models import *

class Inventory(models.Model):
    # 기준 일시
    referenceDate = models.DateTimeField(blank=False, null=False, default=timezone.now)
    # 재고 품목
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=False, null=False)
    # 재고 량
    ammount = models.IntegerField(blank=False, null=False, default=0)
    # 초기 재고 여부 확인
    is_initial = models.BooleanField(blank=False, null=False, default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['referenceDate', 'item'], name='refDate and item composite key')
        ]

    def __str__(self):
        return "[" + str(self.referenceDate) + "]" + self.item.code + "-" + self.item.name

    