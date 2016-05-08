# coding=utf-8

import test_helper

import unittest
import json

from my_hit_service import MyHitService

class MyHitServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = MyHitService()

    def test_get_all_movies(self):
        result = self.service.get_all_movies()

        print(json.dumps(result, indent=4))

    def test_get_all_series(self):
        result = self.service.get_all_series()

        print(json.dumps(result, indent=4))

    def test_get_serial(self):
        series = self.service.get_all_series()['movies']

        serie = series[0]

        result = self.service.get_serie_info(serie['path'])

        print(json.dumps(result, indent=4))

    def test_get_popular_movies(self):
        result = self.service.get_popular_movies()

        print(json.dumps(result, indent=4))

    def test_get_popular_series(self):
        result = self.service.get_popular_series()

        print(json.dumps(result, indent=4))

    def test_get_soundtracks(self):
        result = self.service.get_soundtracks()

        print(json.dumps(result, indent=4))
        print(len(result["movies"]))

    def test_get_albums(self):
        result = self.service.get_soundtracks()['movies']

        albums = self.service.get_albums(result[0]['path'])

        print(json.dumps(albums, indent=4))

    def test_get_selections(self):
        result = self.service.get_selections()

        print(json.dumps(result, indent=4))

    def test_get_selection(self):
        selections = self.service.get_selections()['movies']

        selection = selections[0]
        print(json.dumps(selection, indent=4))

        result = self.service.get_selection(path=selection['path'])

        print(json.dumps(result, indent=4))

    def test_get_urls(self):
        movies = self.service.get_popular_movies()['movies']

        movie = movies[0]

        print(json.dumps(movie, indent=4))

        result = self.service.get_urls(movie['path'])

        print(json.dumps(result, indent=4))

    def test_get_serie_info(self):
        series = self.service.get_popular_series()['movies']

        serie = series[0]

        result = self.service.get_serie_info(serie['path'])

        print(json.dumps(result, indent=4))

    def test_get_play_list(self):
        movies = self.service.get_popular_movies()['movies']

        movie = movies[0]

        urls = self.service.get_urls(movie['path'])

        print(json.dumps(urls, indent=4))

        url = urls[0]

        play_list = self.service.get_play_list(url)

        print play_list

    def test_pagination_in_popular_movies(self):
        result = self.service.get_popular_movies(page=1)

        # print(json.dumps(result, indent=4))

        pagination = result['pagination']

        self.assertEqual(pagination['has_next'], True)
        self.assertEqual(pagination['has_previous'], False)
        self.assertEqual(pagination['page'], 1)

        result = self.service.get_popular_movies(page=2)

        #print(json.dumps(result, indent=4))

        pagination = result['pagination']

        self.assertEqual(pagination['has_next'], True)
        self.assertEqual(pagination['has_previous'], True)
        self.assertEqual(pagination['page'], 2)

    def test_search(self):
        query = 'red'

        result = self.service.search(query)

        print(json.dumps(result, indent=4))

    def test_film_filters(self):
        result = self.service.get_filters(mode='film')

        print(json.dumps(result, indent=4))

    def test_serie_filters(self):
        result = self.service.get_filters(mode='serial')

        print(json.dumps(result, indent=4))

    def test_convert_track_duration(self):
        text = '02:11'

        result = self.service.convert_track_duration(text)

        print result

    def test_get_play_list3(self):
        movies = self.service.get_popular_movies()['movies']

        movie = movies[0]

        urls = self.service.get_urls(movie['path'])

        print urls

        urls = self.service.get_play_list_urls3(urls[0])

        print(json.dumps(urls, indent=4))

        # print self.service.http_request(urls[0]).read()

        # play_list = self.service.get_play_list3(urls[0])
        #
        # print play_list

if __name__ == '__main__':
    unittest.main()
