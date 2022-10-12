from django import forms
from .models import *

SECTOR_CHOICE = {
        ('manufacturing','Manufacturing'),
        ('wholesale','Wholesale business'),
        ('retail','Retail business'),
        ('restaurant','Restaurant business')
    }

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

class materialForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['code','name','registration_date','is_endItem','note','required']
        labels = {
            'code' : 'Code',
            'name' : 'Item Name',
            'registration_date' : 'Registration Date',
            'is_endItem' : 'Is end item?',
            'note' : 'Note',
            'required' : 'Required',
        }


class otherCompanyForm(forms.ModelForm):
    company_sector = forms.ChoiceField(widget=forms.RadioSelect, choices=SECTOR_CHOICE)
    class Meta:
        model = OtherCompany
        fields = ['company_name','company_sector','company_phoneNum','company_address','company_email','note']
        labels = {
            'company_name' : 'Name',
            'company_sector' : 'Sector',
            'company_phoneNum' : 'Phone Number',
            'company_address' : 'Address',
            'company_email':'Email',
            'note':'Note'
        }

