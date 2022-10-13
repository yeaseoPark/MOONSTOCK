from django.contrib import admin
from .models import *
from treebeard.forms import movenodeform_factory
from treebeard.admin import TreeAdmin

# Register your models here.
'''
class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Item)
'''

class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Node)

# admin.site.register(Item, CategoryAdmin)
admin.site.register(OtherCompany)
admin.site.register(Item)
admin.site.register(Node, CategoryAdmin)
