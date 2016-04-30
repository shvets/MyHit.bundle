# coding=utf-8

import test_helper

import unittest
import json

from my_hit_service import MyHitService

class MyHitServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = MyHitService()

    def test_get_get_all_movies(self):
        result = self.service.get_all_movies()

        print(json.dumps(result, indent=4))

    def test_get_get_all_serials(self):
        result = self.service.get_all_serials()

        print(json.dumps(result, indent=4))

    def test_get_get_popular_movies(self):
        result = self.service.get_popular_movies()

        print(json.dumps(result, indent=4))

    def test_get_get_popular_serials(self):
        result = self.service.get_popular_serials()

        print(json.dumps(result, indent=4))

    def test_get_soundtracks(self):
        result = self.service.get_soundtracks()

        print(json.dumps(result, indent=4))

    def test_get_selections(self):
        result = self.service.get_selections()

        print(json.dumps(result, indent=4))

    def test_get_get_urls(self):
        movies = self.service.get_popular_movies()['movies']

        movie = movies[0]

        print(json.dumps(movie, indent=4))

        result = self.service.get_urls(movie['path'])

        print(json.dumps(result, indent=4))

    def test_get_play_list2(self):
        movies = self.service.get_popular_movies()['movies']

        movie = movies[0]

        urls = self.service.get_urls(movie['path'])

        # urls2 = self.service.get_play_list_urls(urls[0])

        print(json.dumps(urls, indent=4))

        url = urls[0]

        play_list = self.service.get_play_list2(url)

        print play_list

    def test_get_play_list3(self):
        movies = self.service.get_popular_movies()['movies']

        movie = movies[0]

        urls = self.service.get_urls(movie['path'])

        print urls

        urls = self.service.get_play_list_urls3(urls[0])

        print(json.dumps(urls, indent=4))

        print self.service.http_request(urls[0]).read()

        # play_list = self.service.get_play_list3(urls[0])
        #
        # print play_list


    def test_pagination_in_popular_movies(self):
        result = self.service.get_popular_movies(page=1)

        # print(json.dumps(result, indent=4))

        pagination = result['pagination']

        self.assertEqual(pagination['has_next'], True)
        self.assertEqual(pagination['has_previous'], False)
        self.assertEqual(pagination['page'], 1)

        result = self.service.get_popular_movies(page=2)

        # print(json.dumps(result, indent=4))

        pagination = result['pagination']

        self.assertEqual(pagination['has_next'], True)
        self.assertEqual(pagination['has_previous'], True)
        self.assertEqual(pagination['page'], 2)

if __name__ == '__main__':
    unittest.main()
