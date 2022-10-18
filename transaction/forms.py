from django import forms
from .models import *

class inventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['referenceDate','item','amount']

class transactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['item','company','amount','price','referenceDate','note']
