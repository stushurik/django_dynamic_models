# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import DynamicModel


class Test(TestCase):

    yaml = """
        users:
            title: Пользователи
            fields:
                - {id: name, title: Имя, type: char}
                - {id: paycheck, title: Зарплата, type: int}
                - {id: date_joined, title: Дата поступления на работу, type: date}


        rooms:
            title: Комнаты
            fields:
                - {id: department, title: Отдел, type: char}
                - {id: spots, title: Вместимость, type: int}
    """

    # @classmethod
    # def tearDownClass(cls):
    #     super(Test, cls).tearDownClass()
    #
    #     def __remove(arg, dirname, fnames):
    #         for name in fnames:
    #             os.remove(os.path.join(dirname, name))
    #
    #     os.path.walk(settings.TEST_MIGRATION_DIR, __remove, None)
    #     os.rmdir(settings.TEST_MIGRATION_DIR)

    # def test_index(self):
    #
    #     response = self.client.get(reverse('index'))
    #     self.assertEqual(response.status_code, 200)
    #
    #     self.assertContains(response, '/models/dynamicmodel/')
    #
    # def test_get_table_data(self):
    #
    #     dm = DynamicModel.objects.create(description=self.yaml)
    #     response = self.client.post(
    #         reverse('ajax_get_model', kwargs={'model': 'dynamicmodel'}),
    #         {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
    #     )
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, dm.description)
    #
    # def test_model_generation(self):
    #     DynamicModel.objects.create(description=self.yaml)
    #     response = self.client.get(reverse('generate'))
    #     self.assertRedirects(response, reverse('index'))
    #
    #     self.assertTrue(ContentType.objects.filter(model='users'))
    #     self.assertTrue(ContentType.objects.filter(model='rooms'))

    def test_get_table_data_of_generated(self):
        DynamicModel.objects.create(description=self.yaml)
        response = self.client.get(reverse('generate'), follow=True)

        self.assertContains(response, '/models/users/')
        self.assertContains(response, '/models/rooms/')

        params = {
            u'form-0-department': [u'1'],
            u'form-0-spots': [u'1'],
            u'form-MAX_NUM_FORMS': [u'1000'],
            u'form-TOTAL_FORMS': [u'1'],
            u'form-0-id': [u''],
            u'form-INITIAL_FORMS': [u'0']
        }

        response = self.client.post(
            reverse('ajax_get_model', kwargs={'model': 'rooms'}),
            params, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        print response
