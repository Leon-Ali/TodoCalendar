from rest_framework.test import APITestCase
from lists.models import List


class ListTest(APITestCase):

    def test_saving_and_retrieving_list(self):
        list_ = List()
        list_.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)




