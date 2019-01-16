from rest_framework.test import APITestCase
from lists.models import List
from lists.models import Item

class ListTest(APITestCase):

    def test_saving_and_retrieving_list(self):
        list_ = List(name='everyday tasks')
        list_.save()

        first_item = Item()
        first_item.text = 'I am the first item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'I am the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)


        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)


        saved_first_item = saved_items[0]
        saved_second_item = saved_items[1]
        self.assertEqual(saved_first_item.text, 'I am the first item')
        self.assertEqual(saved_second_item.text, 'I am the second')




