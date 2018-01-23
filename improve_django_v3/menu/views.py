from datetime import datetime
from operator import attrgetter

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Item, Menu
from .forms import MenuForm


def item_list(request):
    '''This returns a list of all Item objects to the user.'''
    items = Item.objects.all()
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
        # The menu.expiration_date check is temporary until
        # the Menu model is updated.
        if menu.expiration_date:
            if menu.expiration_date >= timezone.now():
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
            menu.created_date = timezone.now()
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
    menu = get_object_or_404(Menu, pk=pk)
    items = Item.objects.all()
    if request.method == "POST":
        menu.season = request.POST.get('season', '')
        menu.expiration_date = datetime.strptime(
            request.POST.get('expiration_date', ''), '%m/%d/%Y')
        # This gets all of the names of the items the user requested
        # and gets the item object associated with it. Then it appends
        # the item to menu.items
        menu_names = request.POST.get('items', '')
        menu.items.clear()
        for item in menu_names:
            menu.items.add(Item.objects.get(name=menu_names))
        menu.save()

        # This routes the user back to the homepage.
        return HttpResponseRedirect(reverse('menu_list'))

    return render(request, 'menu/menu_change.html', {
        'menu': menu,
        'items': items,
        })
