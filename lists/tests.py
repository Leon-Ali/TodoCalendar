import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from lists.models import List
from lists.models import Item


class ListModelTest(APITestCase):

    def test_saving_and_retrieving_list(self):
        user = User.objects.create(username='Leon', email='Leon@test.com', password='leon123')
        list_ = List(name='everyday tasks', user=user)
        list_.save()

        first_item = Item()
        first_item.text = 'I am the first item'
        first_item.list = list_
        first_item.date = datetime.date.today()
        first_item.status = Item.SCHEDULED
        first_item.save()

        second_item = Item()
        second_item.text = 'I am the second'
        second_item.list = list_
        second_item.date = datetime.date.today()
        second_item.status = Item.INPROGRESS
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)
        self.assertEqual(saved_list.name, 'everyday tasks')
        self.assertEqual(saved_list.user.id, user.id)


        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)


        saved_first_item = saved_items[0]
        saved_second_item = saved_items[1]

        self.assertEqual(saved_first_item.text, 'I am the first item')
        self.assertEqual(saved_first_item.status, Item.SCHEDULED)

        self.assertEqual(saved_second_item.text, 'I am the second')
        self.assertEqual(saved_second_item.status, Item.INPROGRESS)





class ListViewsTest(APITestCase):

    def setUp(self):
        self.test_user = User.objects.create(username='Edward', email='edwardelric@test.com', password='alchemist1')
        self.test_list = List.objects.create(name='test_list', user=self.test_user)
        self.test_item = Item.objects.create(text='Do this today', list=self.test_list, date=datetime.date.today())
        self.list_url = reverse('lists')

    def test_create_list(self):
        """
        Ensure we can create a list
        """
        data = {'name':'Good list', 'user':self.test_user.id}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(List.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])

    def test_retrieve_lists(self):
        """
        Ensure we can retrieve all lists
        """
        list_ = List.objects.create(name='Awesome list', user=self.test_user)
        response = self.client.get(self.list_url, format='json')
        self.assertIn('test_list', response.data[0]['name'])
        self.assertIn('Awesome list', response.data[1]['name'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(List.objects.count(), 2)

    def test_retrieve_list_by_id(self):
        """
        Ensure we can retrieve a list by given id
        """
        list_ = List.objects.create(name='Awesome list', user=self.test_user)
        response = self.client.get(f'/api/lists/{list_.id}/')
        self.assertIn('Awesome list', response.data['name'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(List.objects.count(), 2)

    def test_delete_list_by_id(self):
        """
        Ensure we can delete a list by given id
        """
        list_ = List.objects.create(name='Work list', user=self.test_user)
        response = self.client.delete(f'/api/lists/{list_.id}/')
        self.assertEqual(List.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_list_by_id(self):
        """
        Ensure we can partially update a list by given id
        """
        list_ = List.objects.create(name='Update me', user=self.test_user)
        response = self.client.put(f'/api/lists/{list_.id}/', data={'name':'Updated list'}, format='json')
        self.assertEqual(response.data['name'], 'Updated list')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_items_for_lists(self):
        """
        Ensure we can create items for a given list
        """
        data = {'text':'Workout', 'date':'2019-1-23'}
        list_ = List.objects.create(name="Need items", user=self.test_user)
        response = self.client.post(f'/api/lists/{list_.id}/items', data=data, format='json')
        self.assertEqual(Item.objects.count(), 2)
        self.assertEqual(List.objects.count(), 2)
        self.assertEqual('Workout', response.data['text'])
        self.assertEqual(list_.id, response.data['list'])
        self.assertEqual('scheduled', response.data['status'])
        self.assertIn('list', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_items_for_lists(self):
        """
        Ensure we can retrieve all items for a given list
        """
        list_ = List.objects.create(name="Daily goals", user=self.test_user)
        first_item = Item.objects.create(text='add tests for app', list=list_, date=datetime.date.today())
        second_item = Item.objects.create(text='go to gym', list=list_, date=datetime.date.today())
        third_item = Item.objects.create(text='read for 30 mins', list=list_, date=datetime.date.today())
        response = self.client.get(f'/api/lists/{list_.id}/items')
        response_list = [item['text'] for item in response.data]
        self.assertEqual(Item.objects.count(), 4)
        self.assertEqual(List.objects.count(), 2)
        self.assertIn(first_item.text, response_list)
        self.assertIn(second_item.text, response_list)
        self.assertIn(third_item.text, response_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_item_by_id(self):
        """
        Ensure we can delete an item by id
        """
        list_ = List.objects.create(user=self.test_user)
        item = Item.objects.create(text='delete me', list=list_, date=datetime.date.today())
        response = self.client.delete(f'/api/lists/{list_.id}/items/{item.id}')
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(response.data, None)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_item_by_id(self):
        """
        Ensure we can retrieve an item by id
        """
        item = Item.objects.create(text='wake up early', list=self.test_list, date=datetime.date.today(), status=Item.COMPLETED)
        response = self.client.get(f'/api/lists/{self.test_list.id}/items/{item.id}')
        self.assertEqual(response.data['text'], item.text)
        self.assertEqual(response.data['status'], 'completed')
        self.assertEqual(response.status_code, status.HTTP_200_OK)









