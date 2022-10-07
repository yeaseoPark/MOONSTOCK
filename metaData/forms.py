from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['code','name','registration_date','is_endItem','price','note']
        labels = {
            'code' : 'Code',
            'name' : 'Item Name',
            'registration_date' : 'Registration Date',
            'is_endItem' : 'Is end item?',
            'price' : 'Price',
            'note' : 'Note',
        }