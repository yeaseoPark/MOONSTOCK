from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *
from .forms import *

#end Item
@login_required(login_url='common:login')
def endItemIndex(request):
    page = request.GET.get('page',1) # 페이지
    kw = request.GET.get('kw','') #검색어
    endItem_list = Item.objects.filter(Q(is_endItem__exact = True) & Q(user__exact = request.user)).order_by('-registration_date')

    if kw:
        endItem_list = endItem_list.filter(
            Q(code__icontains= kw) |
            Q(name__icontains=kw) |
            Q(note__icontains=kw)
        ).distinct()

    paginator = Paginator(endItem_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'endItem_list' : page_obj, 'page':page, 'kw':kw}
    return render(request, 'metaData/endItem/endItemIndex.html', context)


@login_required(login_url='common:login')
def endItem_add(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            endItem = form.save(commit=False)

            if len(Item.objects.filter(Q(code__exact = endItem.code) & Q(user__exact = request.user) )) >=1:
                messages.error(request, "중복된 코드입니다. 다시 확인해주세요.")
            else:
                endItem.is_endItem = True
                endItem.user = request.user
                endItem.save()
                node = Node(item = endItem)
                Node.add_root(instance = node)
                return redirect('metaData:endItemIndex')
    else:
        form = ItemForm()
    context = {'form':form}
    return render(request, 'metaData/endItem/endItemForm.html', context)

@login_required(login_url='common:login')
def endItem_detail(request, endItem_id):
    end_item = Item.objects.get(id = endItem_id)
    if end_item.user != request.user:
        return redirect('metaData:endItemIndex')
    context = {'end_item': end_item}
    return render(request, 'metaData/endItem/endItem_detail.html', context)

@login_required(login_url='common:login')
def endItem_modify(request,endItem_id):
    end_item = get_object_or_404(Item, pk = endItem_id)
    if end_item.user != request.user:
        messages.error(request, "부적절한 사용")
        return redirect('metaData:endItemIndex')
    if request.method == 'POST':
        form = ItemForm(request.POST, instance = end_item)
        if form.is_valid():
            endItem = form.save(commit=False)
            endItem.user = request.user
            endItem.is_endItem = True
            endItem.save()
            return redirect("metaData:endItem_detail", endItem_id = endItem_id)
    else:
        form = ItemForm(instance=end_item)
    context = {'end_item': end_item, 'form':form}
    return render(request, 'metaData/endItem/endItemForm.html', context)

@login_required(login_url='common:login')
def endItem_delete(request,endItem_id):
    endItem = get_object_or_404(Item, pk=endItem_id)
    if request.user != endItem.user:
        messages.error(request,"부적절한 사용입니다")
        return redirect('metaData:endItemIndex')
    endItem.delete()
    return redirect("metaData:endItemIndex")


'''
BOM views
'''
@login_required(login_url='common:login')
def bomIndex(request):
    page = request.GET.get('page', 1)  # 페이지
    kw = request.GET.get('kw', '')  # 검색어

    annotated_list = Node.get_annotated_list()
    endItem_list = Item.objects.filter(Q(is_endItem__exact = True) & Q(user__exact = request.user))

    if kw:
        endItem_list = endItem_list.filter(
            Q(code__icontains=kw) |
            Q(name__icontains=kw) |
            Q(note__icontains=kw)
        ).distinct()

    temp_list = list()

    for item, info in annotated_list:
        if item.item.user == request.user:
            temp_list.append((item.item, info))

    temp_dict = dict()

    for item, info in annotated_list:
        if item.item.user == request.user:
            info['node_id'] = item.id
            if info['level'] == 0:
                end_Item = item.item
                temp_dict[end_Item] = [(end_Item, info)]

            else:
                temp_dict[end_Item].append((item.item, info))

    paginator = Paginator(endItem_list, 3) # 페이지당 3개씩 보여주기
    page_obj = paginator.get_page(page)

    annotated_list = temp_list
    context = {'annotated_list': annotated_list, 'annotated_dict':temp_dict,'endItem_list':page_obj, 'page':page,'kw':kw}
    return render(request, 'metaData/BOM/bomIndex.html', context)

@login_required(login_url='common:login')
def bom_add(request, node_id):
    endItem_id = request.GET['endItem_id']
    endItem = get_object_or_404(Item, pk = endItem_id)
    endItemNode = Node.objects.filter(item__exact = endItem)[0]

    parentNode = Node.objects.get(pk = node_id)
    parent = parentNode.item

    options = Item.objects.filter(Q(is_endItem__exact = False) & Q(user__exact = request.user)).exclude(pk = parent.id)

    exclude_option = list()
    for node in parentNode.get_descendants():
        exclude_option.append(node.item)

    options = list(set(options) - set(exclude_option))

    if parent.user != request.user:
        return redirect("common:login")

    if request.method == 'POST':
        child = Item.objects.get(Q(user__exact=request.user) & Q(id__exact = request.POST['item']))
        childNode = Node(item = child)
        parentNode.add_child(instance = childNode)

        return HttpResponse('<script type="text/javascript">opener.location.reload();window.close()</script>')
    else:
        form = bomForm()
    context = {'parent': parent, 'options':options}
    return render(request, 'metaData/BOM/bomForm.html', context)
@login_required(login_url='common:login')
def bom_delete(request, node_id):

    node = Node.objects.get(pk =node_id)
    item = node.item
    if item.user != request.user:
        messages.error(request,"인가된 사용자가 아닙니다")
        return redirect("metaData:bomIndex")
    node.delete()
    return redirect("metaData:bomIndex")

@login_required(login_url='common:login')
def vendorIndex(request):
    page = request.GET.get('page',1) # 페이지
    kw = request.GET.get('kw','') #검색어
    vendor_list = OtherCompany.objects.filter(Q(is_vendor__exact=True) & Q(user__exact = request.user))

    if kw:
        vendor_list = vendor_list.filter(
            Q(company_name__icontains = kw) |
            Q(note__icontains = kw)
        ).distinct()

    paginator = Paginator(vendor_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'vendor_list': page_obj, 'kw':kw, 'page':page}
    return render(request, 'metaData/vendor/vendorIndex.html', context)

@login_required(login_url='common:login')
def vendor_add(request):
    if request.method =='POST':
        form = otherCompanyForm(request.POST)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.is_vendor = True
            vendor.is_customer = False
            vendor.user = request.user
            vendor.save()
            return redirect('metaData:vendorIndex')
    else:
        form = otherCompanyForm()
    context = {'form':form}
    return render(request,'metaData/vendor/vendorForm.html', context)

@login_required(login_url='common:login')
def vendor_detail(request, vendor_id):
    vendor = OtherCompany.objects.get(id = vendor_id)
    if vendor.user != request.user:
        messages.error(request, "인가된 사용자가 아닙니다.")
        return redirect("metaData:vendorIndex")

    form = otherCompanyForm(instance=vendor)
    context = {'vendor': vendor,'form':form}
    return render(request, 'metaData/vendor/vendor_detail.html', context)

@login_required(login_url='common:login')
def vendor_delete(request, vendor_id):
    vendor = get_object_or_404(OtherCompany, pk = vendor_id)
    if vendor.user != request.user:
        messages.error(request, '인가된 사용자가 아닙니다')
        return redirect("metaData:vendorIndex")

    vendor.delete()
    return redirect("metaData:vendorIndex")

@login_required(login_url='common:login')
def vendor_modify(request, vendor_id):
    Vendor = get_object_or_404(OtherCompany, pk = vendor_id)
    if Vendor.user != request.user:
        messages.error(request, '인가된 사용자가 아닙니다')
        return redirect("metaData:vendorIndex")
    if request.method == 'POST':
        form =otherCompanyForm(request.POST, instance=Vendor)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.is_vendor = True
            vendor.is_customer = False
            vendor.user = request.user
            vendor.save()
            return redirect('metaData:vendor_detail', vendor_id = vendor_id)
    else:
        form = otherCompanyForm(instance=Vendor)
    context = {'form':form}
    return render(request, 'metaData/vendor/vendorForm.html', context)
@login_required(login_url='common:login')
def customerIndex(request):
    page = request.GET.get('page',1) # 페이지
    kw = request.GET.get('kw','') #검색어
    customer_list = OtherCompany.objects.filter(Q(is_customer__exact=True) & Q(user__exact = request.user))
    if kw:
        customer_list = customer_list.filter(
            Q(company_name__icontains=kw) |
            Q(note__icontains=kw)
        ).distinct()

    paginator = Paginator(customer_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'customer_list':page_obj,'kw':kw,'page':page}
    return render(request,'metaData/customer/customerIndex.html', context)
@login_required(login_url='common:login')
def customer_add(request):
    if request.method == 'POST':
        form = otherCompanyForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.is_vendor = False
            customer.is_customer = True
            customer.user = request.user
            customer.save()
            return redirect('metaData:customerIndex')
    else:
        form = otherCompanyForm()
    context = {'form':form}
    return render(request,'metaData/customer/customerForm.html', context)

@login_required(login_url='common:login')
def customer_detail(request, customer_id):
    customer = OtherCompany.objects.get(id =customer_id)
    if customer.user != request.user:
        messages.error(request,'인가된 사용자가 아닙니다')
        return redirect("metaData:customerIndex")
    form = otherCompanyForm(instance=customer)
    context = {'form': form, 'customer':customer}
    return render(request,'metaData/customer/customer_detail.html', context)

@login_required(login_url='common:login')
def customer_delete(request, customer_id):
    customer = get_object_or_404(OtherCompany, pk = customer_id)
    if customer.user != request.user:
        messages.error(request, '인가된 사용자가 아닙니다')
        return redirect("metaData:customerIndex")
    customer.delete()
    return redirect("metaData:customerIndex")
@login_required(login_url='common:login')
def customer_modify(request, customer_id):
    Customer = get_object_or_404(OtherCompany, pk=customer_id)
    if Customer.user != request.user:
        messages.error(request, '인가된 사용자가 아닙니다')
        return redirect("metaData:customerIndex")
    if request.method == 'POST':
        form = otherCompanyForm(request.POST, instance=Customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.is_vendor = False
            customer.is_customer = True
            customer.user = request.user
            customer.save()
            return redirect('metaData:customer_detail', customer_id = customer_id)
    else:
        form = otherCompanyForm(instance=Customer)
    context = {'form':form}
    return render(request,'metaData/customer/customerForm.html',context)


'''
Material
'''
@login_required(login_url='common:login')
def materialIndex(request):
    page = request.GET.get('page',1) # 페이지
    kw = request.GET.get('kw','') #검색어
    material_list = Item.objects.filter(Q(is_endItem__exact = False) & Q(user__exact = request.user)).order_by('-registration_date')

    if kw:
        material_list = material_list.filter(
            Q(code__icontains= kw) |
            Q(name__icontains=kw) |
            Q(note__icontains=kw)
        ).distinct()

    paginator = Paginator(material_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'material_list' : page_obj, 'page':page, 'kw':kw}
    return render(request, 'metaData/material/materialIndex.html', context)


@login_required(login_url='common:login')
def material_add(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)

            if len(Item.objects.filter(Q(code__exact = material.code) & Q(user__exact = request.user) )) >=1:
                messages.error(request, "중복된 코드입니다. 다시 확인해주세요.")
            else:
                material.is_endItem = False
                material.user = request.user
                material.save()
                return redirect('metaData:materialIndex')
    else:
        form = ItemForm()
    context = {'form':form}
    return render(request, 'metaData/material/materialForm.html', context)

@login_required(login_url='common:login')
def material_detail(request, material_id):
    material = Item.objects.get(id = material_id)
    if material.user != request.user:
        return redirect('metaData:materialIndex')
    context = {'material_item': material}
    return render(request, 'metaData/material/material_detail.html', context)

@login_required(login_url='common:login')
def material_modify(request,material_id):
    material_item = get_object_or_404(Item, pk = material_id)
    if material_item.user != request.user:
        messages.error(request, "부적절한 사용")
        return redirect('metaData:materialIndex')
    if request.method == 'POST':
        form = ItemForm(request.POST, instance = material_item)
        if form.is_valid():
            material = form.save(commit=False)
            material.user = request.user
            material.is_endItem = False
            material.save()
            return redirect("metaData:material_detail", material_id = material_id)
    else:
        form = ItemForm(instance=material_item)
    context = {'material_item': material_item, 'form':form}
    return render(request, 'metaData/material/materialForm.html', context)

@login_required(login_url='common:login')
def material_delete(request,material_id):
    material = get_object_or_404(Item, pk=material_id)
    if request.user != material.user:
        messages.error(request,"부적절한 사용입니다")
        return redirect('metaData:materialIndex')
    material.delete()
    return redirect("metaData:materialIndex")