# coding=utf-8

import test_helper

import unittest
import json

from my_hit_service import MyHitService

class MyHitServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = MyHitService()

    def test_get_get_popular__movies(self):
        result = self.service.get_movies("/film/?s=3")

        print(json.dumps(result, indent=4))

    def test_get_get_urls(self):
        movies = self.service.get_movies("/film/?s=3")

        movie = movies[0]

        print movie

        result = self.service.get_urls(movie['path'])

        print(json.dumps(result, indent=4))

    def test_get_play_list(self):
        # new_series = self.service.get_new_series()
        #
        # path = new_series[0]['path']

        # urls = self.service.retrieve_urls(path)

        url = 'http://i543.hotcloud.org/vod/vod/d3/48/00000000000248d3_4_5_01.smil/manifest.f4m'

        base_url = url.replace('.f4m', '.m3u8')

        urls = self.service.get_play_list_urls(base_url)

        # print(json.dumps(urls, indent=4))

        play_list = self.service.get_play_list2(base_url, urls[0])

        print play_list

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
