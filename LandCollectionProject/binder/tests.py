from .bindernator import Bindernator 
from unittest import TestCase
from math import ceil
class test_Bindernator(TestCase):

    def setUp(self):
        self.items = 50
        self.volume_size =4
        self.page_size = 2
        self.paginator = Bindernator(range(1,self.items),self.volume_size,self.page_size)

    def test_basic_sort(self):

        volumes_count = ceil(self.items / (self.volume_size * self.page_size))

        self.assertEqual(len(self.paginator.volumes),volumes_count)


    def test_get_row(self):
        volume = 2
        page =3
        row = 2
        item = self.paginator.get(volume,page,row)
        itemcalc = ((volume -1 )* self.volume_size * self.page_size) + ((page - 1) *self.page_size) + row
        self.assertEqual(item, itemcalc)




