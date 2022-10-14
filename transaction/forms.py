from django import forms
from .models import *

class inventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['referenceDate','item','ammount']
