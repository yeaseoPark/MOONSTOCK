from django import forms
from invItemMgmt.models import Item, BOM

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['code','name','registration_date','is_endItem','note']
        labels = {
            'code' : 'Code',
            'name' : 'Item Name',
            'registration_date' : 'Registration Date',
            'is_endItem' : 'Is end item?',
            'note' : 'Note',
        }