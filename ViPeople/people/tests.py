from django.test import TestCase, Client
from django.db import models

from .models import People

PEOPLE_DATA = {
    'name': 'Guido',
    'phone': '20102020',
    'email': 'guido@python.com'
}

class PeopleUnitTest(TestCase):
    def setUp(self):
        self.guido = People.objects.create(**PEOPLE_DATA)

    def test_assert_people_shouve_have_a_unicode_representation(self):
        self.assertEquals(u'#1 - Guido', unicode(self.guido))

    def test_assert_people_shouve_have_an_absolute_url(self):
        self.assertEquals('/peoples/1/', self.guido.get_absolute_url())

    def test_assert_people_shouve_have_an_update_url(self):
        self.assertEquals('/peoples/1/update/', self.guido.get_update_url())

    def test_assert_people_shouve_have_an_delete_url(self):
        self.assertEquals('/peoples/1/delete/', self.guido.get_delete_url())


class PeopleModelTest(TestCase):
    def setUp(self):
        self.fields = {
            field.name: field for field in People._meta.fields
        }

    def test_assert_people_should_have_a_verbose_name(self):
        self.assertIn('Pessoa', People._meta.verbose_name)

    def test_assert_people_should_have_a_verbose_name_plural(self):
        self.assertIn('Pessoas', People._meta.verbose_name_plural)

    def test_assert_people_should_have_a_name(self):
        self.assertIn('name', People._meta.get_all_field_names())

    def test_assert_people_name_should_be_a_CharField(self):
        self.assertIsInstance(self.fields['name'], models.CharField)

    def test_assert_people_name_should_be_required(self):
        self.assertEqual(False, self.fields['name'].null)
        self.assertEqual(False, self.fields['name'].blank)

    def test_assert_people_name_should_have_at_most_50_characters(self):
        self.assertEqual(50, self.fields['name'].max_length)

    def test_assert_people_should_have_a_phone(self):
        self.assertIn('phone', People._meta.get_all_field_names())

    def test_assert_people_phone_should_be_a_CharField(self):
        self.assertIsInstance(self.fields['phone'], models.CharField)

    def test_assert_people_phone_should_be_required(self):
        self.assertEqual(False, self.fields['phone'].null)
        self.assertEqual(False, self.fields['phone'].blank)

    def test_assert_people_phone_should_have_at_most_50_characters(self):
        self.assertEqual(50, self.fields['phone'].max_length)

    def test_assert_people_should_have_a_email(self):
        self.assertIn('email', People._meta.get_all_field_names())

    def test_assert_people_email_should_be_a_EmailField(self):
        self.assertIsInstance(self.fields['email'], models.EmailField)

    def test_assert_people_email_should_be_required(self):
        self.assertEqual(False, self.fields['email'].null)
        self.assertEqual(False, self.fields['email'].blank)



class PeopleViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.people_data = PEOPLE_DATA.copy()

    def test_index(self):
        response = self.client.get('/')

        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(People.objects.none(),
                                 response.context['people_list'])

    def test_create_people(self):
        response = self.client.post('/peoples/create/', self.people_data,
                                    follow=True)
        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(People.objects.all(), ["<People: #1 - Guido>"])

        guido = response.context['object']
        self.assertEqual('Guido', guido.name)
        self.assertEqual('20102020', guido.phone)
        self.assertEqual('guido@python.com', guido.email)

    def test_update_people(self):
        guido = People.objects.create(**self.people_data)
        self.assertEquals(1, People.objects.count())

        new_people_data = self.people_data.copy()
        new_people_data['email'] = 'guido@python.org'

        self.assertEqual(self.people_data['email'], guido.email)
        response = self.client.post(guido.get_update_url(), new_people_data,
                                    follow=True)

        self.assertEqual(200, response.status_code)
        guido = response.context['object']
        self.assertEqual('Guido', guido.name)
        self.assertEqual('20102020', guido.phone)
        self.assertEqual('guido@python.org', guido.email)

    def test_delete_people(self):
        guido = People.objects.create(**PEOPLE_DATA)
        self.assertEquals(1, People.objects.count())

        response = self.client.post(guido.get_delete_url(), follow=True)

        self.assertEqual(200, response.status_code)
        self.assertEqual(0, People.objects.count())
        self.assertQuerysetEqual(People.objects.none(),
                                 response.context['people_list'])