import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms import ValidationError
from django.test import TestCase, Client

from .forms import MenuForm
from .models import Ingredient, Item, Menu


class FormTests(TestCase):
    '''This tests all of the forms in menu.'''
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
            description=('A kind of desert with pumpkin, cinnamon, nutmeg' +
                         ' more'),
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

    def test_menu_form(self):
        '''This tests the MenuForm for validity.'''
        form_data = {
            'season': 'Spring',
            'items': [self.item.pk],
            'expiration_date': datetime.date.today()
        }
        form = MenuForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_clean_hidden_field_menu_form(self):
        '''This tests the clean_hidden_field for validity.'''
        form_data = {
            'season': 'Spring',
            'items': [self.item.pk],
            'expiration_date': datetime.date.today(),
            'hidden_field': 'I am a bot. Rawr!!'
        }
        form = MenuForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_clean_season_menu_form(self):
        '''This tests the clean_season field for validity.'''
        form_data = {
            'season': 'This h@s punctu@tion.!@#$',
            'items': [self.item.pk],
            'expiration_date': datetime.date.today(),
        }
        form = MenuForm(data=form_data)
        self.assertFalse(form.is_valid())


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
        self.assertEqual(str(menu), 'Fall')


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
            description=('A kind of desert with pumpkin, cinnamon, nutmeg' +
                         ' more'),
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

    def test_item_detail_view(self):
        '''This tests the item detail view.'''
        resp = self.client.get(reverse('item_detail',
                                       kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/item_detail.html')
        self.assertContains(resp, 'Soda Fountain')
        self.assertContains(resp, 'Head Chef:')
        self.assertContains(resp, self.item.name)
        self.assertContains(resp, self.item.description)

    def test_bad_item_detail_view(self):
        '''This tests an invalid item pk in the item detail view.'''
        resp = self.client.get(reverse('item_detail',
                                       kwargs={'pk': 1204}))
        self.assertEqual(resp.status_code, 404)

    def test_item_list_view(self):
        '''This tests the item list view.'''
        resp = self.client.get(reverse('item_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/item_list.html')
        self.assertContains(resp, 'Soda Fountain')
        self.assertContains(resp, 'Pumpkin pie')

    def test_edit_menu_view(self):
        '''This tests the edit menu view and form.'''
        resp = self.client.get(reverse('menu_edit',
                               kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_edit.html')
        self.assertContains(resp, 'Change menu')
        self.assertContains(resp, self.menu.season)

    def test_menu_edit_view_with_form(self):
        '''This test that the user can edit a Menu.'''
        c = Client()
        form_data = {
            'season': 'Now this is Fall',
            'items': [self.item.pk],
            'expiration_date': datetime.date.today()
        }
        resp = c.post(reverse('menu_edit',
                              kwargs={'pk': self.menu.pk}), form_data)
        self.assertEqual(resp.status_code, 302)
        # The Menu.objects.get(pk=1) is because self.menu does not change
        # but the datbase does.
        self.assertEqual(Menu.objects.get(pk=1).season, 'Now this is Fall')

    def test_bad_edit_menu_view(self):
        '''This tests an invalid menu pk in the menu edit view.'''
        resp = self.client.get(reverse('menu_edit',
                                       kwargs={'pk': 1204}))
        self.assertEqual(resp.status_code, 404)

    def test_menu_delete_view(self):
        '''This tests the delete menu view.'''
        resp = self.client.get(reverse('menu_delete',
                               kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Do you want to delete this item?')
        self.assertContains(resp, self.menu.season)
        self.assertContains(resp, self.item)

    def test_menu_delete_view_confirmation(self):
        '''This test is the Menu item is actually deleted from the database.'''
        c = Client()
        resp = c.post(reverse('menu_delete',
                              kwargs={'pk': self.menu.pk}))
        # This 'POST' request should have deleted the Menu object.
        self.assertEqual(len(Menu.objects.all()), 0)
        self.assertRedirects(
            resp, reverse('menu_list'))

    def test_menu_detail_view(self):
        '''This tests the menu detail view.'''
        resp = self.client.get(reverse('menu_detail',
                               kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')
        self.assertContains(resp, 'On the menu this season')
        self.assertContains(resp, 'Menu expires on')
        self.assertContains(resp, self.item.name)
        self.assertContains(resp, self.menu.season)

    def test_menu_list_view(self):
        '''This tests the main homepage for menu.'''
        resp = self.client.get(reverse('menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')
        self.assertContains(resp, 'Soda Fountain')
        self.assertContains(resp, 'Fall')

    def test_menu_new_view(self):
        '''This tests the new menu view.'''
        resp = self.client.get(reverse('menu_new'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_edit.html')
        self.assertContains(resp, 'Soda Fountain')

    def test_menu_new_view_with_form(self):
        '''This tests that the user can submit a form.'''
        c = Client()
        form_data = {
            'season': 'Spring',
            'items': [self.item.pk],
            'expiration_date': datetime.date.today()
        }
        resp = c.post(reverse('menu_new'), form_data)
        self.assertEqual(resp.status_code, 302)
        # The pk is two on this redirect because this is the second
        # Menu item created in this test 1 for setUp 1 for the POST
        self.assertRedirects(
            resp, reverse('menu_detail', kwargs={'pk': 2}))
