from django.test import TestCase

from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):

        book_1 = Book.objects.create(name='Test book 1', price=25, author_name='Vlad')
        book_2 = Book.objects.create(name='Test book 2', price=55, author_name='Danila')
        data = BookSerializer([book_1, book_2], many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '25.00',
                'author_name': 'Vlad',
            },
            {
                'id': book_2.id,
                'name': 'Test book 2',
                'price': '55.00',
                'author_name': 'Danila',
            }
        ]
        self.assertEqual(expected_data, data)


