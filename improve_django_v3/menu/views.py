import datetime
from operator import attrgetter

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from .models import Item, Menu
from .forms import MenuForm


def item_list(request):
    '''This returns a list of all Item objects to the user.'''
    items = Item.objects.all()
    items = sorted(items, key=attrgetter('created_date'))
    return render(request, 'menu/item_list.html', {'items': items})


def item_detail(request, pk):
    '''This shows the user information about an Item.'''
    try:
        item = Item.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/item_detail.html', {'item': item})


def menu_list(request):
    '''This returns a list of all the Menus.'''
    all_menus = Menu.objects.all().prefetch_related('items')
    menus = []
    for menu in all_menus:
        if menu.expiration_date >= datetime.date.today():
            menus.append(menu)

    menus = sorted(menus, key=attrgetter('expiration_date'))
    return render(request,
                  'menu/list_all_current_menus.html', {'menus': menus})


def menu_detail(request, pk):
    '''This shows the user information about a Menu.'''
    menu = Menu.objects.get(pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def create_new_menu(request):
    '''This creates a new Menu object.'''
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.created_date = datetime.date.today()
            menu.expiration_date = form.cleaned_data['expiration_date']
            menu.save()
            for item in form.cleaned_data['items']:
                menu.items.add(item)
            menu.save()
            return redirect('menu_detail', pk=menu.pk)
    else:
        form = MenuForm()
    return render(request, 'menu/menu_new.html', {'form': form})


def edit_menu(request, pk):
    '''This allows a user to edit a Menu object.'''
    instance = get_object_or_404(Menu, pk=pk)
    form = MenuForm(request.POST or None, instance=instance,
                    initial={'expiration_date': instance.expiration_date}
                    )

    if request.method == 'POST':
        if form.is_valid():
            instance.expiration_date = form.cleaned_data['expiration_date']
            form.save()
            return redirect('menu_list')
    return render(request, 'menu/menu_new.html', {'form': form})
