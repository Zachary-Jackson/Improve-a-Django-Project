import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Ingredient, Item, Menu


class IngredientModelTests(TestCase):
    '''This tests to see if the Ingredient model works.'''
    def test_ingredient_creation(self):
        '''This creates an Ingredient object.'''
        ingredient = Ingredient.objects.create(name='Banana')
        self.assertEqual(ingredient.name, 'Banana')


class ItemModelTests(TestCase):
    '''This tests to see if the Item model works.'''
    def setUp(self):
        '''Creates an Ingredient object to use for the Item model.'''
        # This creates a User model to attach to the Item model.
        self.user = User.objects.create_user(
            username='tester',
            email='test@test.com',
            password='verysecret1'
        )
        # This creates an ingredient to attach to the Item model.
        Ingredient.objects.create(name='Banana')

    def test_item_creation(self):
        '''This creates an Item object.'''
        item = Item.objects.create(
            name='Banana pudding',
            description='A kind of desert with bannas, pudding, and cookies',
            chef=self.user,
            # created_date is left blank for default time
            standard=True,
        )
        # item.ingredients can have things added to it like bellow
        item.ingredients.add(Ingredient.objects.get(id=1))
        self.assertEqual(item.name, 'Banana pudding')


class MenuModelTests(TestCase):
    '''This tests to see if the Menu model works.'''
    def setUp(self):
        '''This creates an Item and Ingredient object for the Menu model.'''
        # This creates a User model to attach to the Item model.
        self.user = User.objects.create_user(
            username='tester',
            email='test@test.com',
            password='verysecret1'
        )
        # This creates an ingredient to attach to the Item model.
        Ingredient.objects.create(name='Pumpkin')

        item = Item.objects.create(
            name='Pumpkin pie',
            description='A kind of desert pumpkin, cinnamon, nutmed and more',
            chef=self.user,
            # created_date is left blank for default time
            standard=True,
        )
        # item.ingredients can have things added to it like bellow
        item.ingredients.add(Ingredient.objects.get(id=1))

    def test_menu_model_creation(self):
        '''This creates a Menu model object.'''
        # This gets a datetime object in the future for menu
        expiration_date = datetime.datetime.now()
        expiration_date += datetime.timedelta(1)
        menu = Menu.objects.create(
            season='Fall',
            # Get items working here temporary
            # created_date left blank to fill out on own
            expiration_date=expiration_date
        )
        menu.items.add(Item.objects.get(id=1))
        self.assertEqual(menu.season, 'Fall')


class MenuViewsTests(TestCase):
    '''This tests to see if the menu views work.'''
    def setUp(self):
        '''This creates an Item and Ingredient object for the Menu model.'''
        # This creates a User model to attach to the Item model.
        self.user = User.objects.create_user(
            username='tester',
            email='test@test.com',
            password='verysecret1'
        )
        # This creates an ingredient to attach to the Item model.
        Ingredient.objects.create(name='Pumpkin')

        self.item = Item.objects.create(
            name='Pumpkin pie',
            description='A kind of desert pumpkin, cinnamon, nutmed and more',
            chef=self.user,
            # created_date is left blank for default time
            standard=True,
        )
        # item.ingredients can have things added to it like bellow
        self.item.ingredients.add(Ingredient.objects.get(id=1))

        # This gets a datetime object in the future for menu
        expiration_date = datetime.datetime.now()
        expiration_date += datetime.timedelta(1)
        self.menu = Menu.objects.create(
            season='Fall',
            # Get items working here temporary
            # created_date left blank to fill out on own
            expiration_date=expiration_date
        )
        self.menu.items.add(Item.objects.get(id=1))

    def test_menu_list_view(self):
        '''This tests the main homepage for menu.'''
        resp = self.client.get(reverse('menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')
        self.assertContains(resp, 'Soda Fountain')

    def test_menu_edit_view(self):
        '''This tests menu edit view.'''
        resp = self.client.get(reverse('menu_edit',
                                       kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/change_menu.html')
        self.assertContains(resp, 'Change menu')
        self.assertContains(resp, 'Expiration Date:')
        self.assertContains(resp, self.menu.season)

    def test_menu_detail_view(self):
        '''This tests the menu detail view.'''
        resp = self.client.get(reverse('menu_detail',
                               kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')
        self.assertContains(resp, 'On the menu this season')
        self.assertContains(resp, 'Menu expires on')
        self.assertContains(resp, 'Pumpkin')
        self.assertContains(resp, self.menu.season)

    def test_item_detail_view(self):
        '''This tests the item detail view.'''
        resp = self.client.get(reverse('item_detail',
                                       kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/detail_item.html')
        self.assertContains(resp, 'Soda Fountain')
        self.assertContains(resp, 'Head Chef:')
        self.assertContains(resp, self.item.name)

    def test_menu_new_view(self):
        '''This tests the new menu item view.'''
        resp = self.client.get(reverse('menu_new'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_edit.html')
        self.assertContains(resp, 'Soda Fountain')
