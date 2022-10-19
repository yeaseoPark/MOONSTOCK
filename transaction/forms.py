from django import forms
from .models import *
from django.core.exceptions import NON_FIELD_ERRORS
class inventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['referenceDate','item','amount']

        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "동일 품목을 동시에 입출고할 수는 없습니다. 다시 한 번 시간을 확인해주세요.",
            }
        }

class transactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['item','company','amount','price','referenceDate','note']

        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "동일 품목을 동시에 입출고할 수는 없습니다. 다시 한 번 시간을 확인해주세요.",
            }
        }

class produceForm(forms.ModelForm):
    class Meta:
        model = Produce
        fields = ['referenceDate','itemNode','amount']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "동일 품목을 동시에 입출고할 수는 없습니다. 다시 한 번 시간을 확인해주세요.",
            }
        }