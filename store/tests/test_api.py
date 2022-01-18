import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book, UserBookRelation
from store.serializers import BookSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')

        self.book_1 = Book.objects.create(name='Test book 1', price=25,
                                          author_name='Author 1', owner=self.user)
        self.book_2 = Book.objects.create(name='Test book 2', price=55,
                                          author_name='Author 5')
        self.book_3 = Book.objects.create(name='Test book Author 1', price=55,
                                          author_name='Author 2')
        self.url = reverse('book-list')
        self.url2 = reverse('book-detail', args=(self.book_1.id,))

    def test_get(self):
        response = self.client.get(self.url)
        serializer_data = BookSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        response = self.client.get(self.url, data={'price': 55})
        serializer_data = BookSerializer([self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        response = self.client.get(self.url, data={'search': 'Author 1'})
        serializer_data = BookSerializer([self.book_1, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_ordering(self):
        response = self.client.get(self.url, data={'ordering': 'price'})
        serializer_data = BookSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, Book.objects.all().count())
        data = {"name": "Programming in Python 2",
                "price": 150,
                "author_name": "Mark Summerfield"}
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(
            self.url, data=json_data,
            content_type='application/json'
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_update(self):
        data = {
            "name": self.book_1.name, "price": 575,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(
            self.url2, data=json_data,
            content_type='application/json'
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(575, self.book_1.price)

    def test_delete(self):
        self.assertEqual(3, Book.objects.all().count())
        self.client.force_login(self.user)
        response = self.client.delete(self.url2)
        self.assertEqual(
            status.HTTP_204_NO_CONTENT,
            response.status_code
        )
        self.assertEqual(2, Book.objects.all().count())

    def test_update_not_owner(self):
        self.user2 = User.objects.create(username='test_username2')
        data = {
            "name": self.book_1.name, "price": 575,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(
            self.url2, data=json_data,
            content_type='application/json'
        )
        self.assertEqual(
            status.HTTP_403_FORBIDDEN, response.status_code
        )
        self.book_1.refresh_from_db()
        self.assertEqual(25, self.book_1.price)


class BooksRelationApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.user2 = User.objects.create(username='test_username2')

        self.book_1 = Book.objects.create(
            name='Test book 1', price=25,
            author_name='Author 1', owner=self.user
        )
        self.book_2 = Book.objects.create(
            name='Test book 2', price=55,
            author_name='Author 5'
        )
        self.url = reverse(
            'userbookrelation-detail',
            args=(self.book_1.id,)
        )

    def test_like(self):
        data = {'like': True}
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(
            self.url, data=json_data,
            content_type='application/json'
        )
        relation = UserBookRelation.objects.get(
            user=self.user, book=self.book_1
        )
        self.assertTrue(relation.like)
        self.assertEqual(
            status.HTTP_200_OK, response.status_code
        )
