# coding=utf-8

import test_helper

import unittest

import os
from bookmark_storage import BookmarkStorage
from storage import Storage
from media_info import MediaInfo

class BookmarkStorageTest(unittest.TestCase):
    def setUp(self):
        self.subject = BookmarkStorage('test_storage.json')

    def tearDown(self):
        if os.path.exists(self.subject.file_name):
            os.remove(self.subject.file_name)
    #
    # def test_sanitize(self):
    #     item = MediaInfo(season=None)
    #
    #     new_item = self.subject.sanitize(item)
    #
    #     self.assertEqual('season' in new_item, False)

    def test_find_video(self):
        Storage.add(self.subject, MediaInfo('video', path='path1'))
        Storage.add(self.subject, MediaInfo('video', path='path2'))

        search_item = MediaInfo(path='path1')

        self.assertEqual(self.subject.find(search_item)['path'], 'path1')

    def test_find_season_no_season_attribute(self):
        Storage.add(self.subject, MediaInfo(type=MediaInfo.SEASON, path='path3', season='season1'))
        Storage.add(self.subject, MediaInfo(type=MediaInfo.SEASON, path='path4', season='season2'))

        search_item = MediaInfo(type=MediaInfo.SEASON, path='path1')

        self.assertEqual(self.subject.find(search_item), None)

    def test_find_season_with_wrong_season_attribute(self):
        Storage.add(self.subject, MediaInfo(type=MediaInfo.SEASON, path='path3', season='season1'))
        Storage.add(self.subject, MediaInfo(type=MediaInfo.SEASON, path='path4', season='season2'))

        search_item = MediaInfo(type=MediaInfo.SEASON, path='path1', season='season3')

        self.assertEqual(self.subject.find(search_item), None)

    def test_find_season_with_correct_season_attribute(self):
        Storage.add(self.subject, MediaInfo(type=MediaInfo.SEASON, path='path3', season='season1'))
        Storage.add(self.subject, MediaInfo(type=MediaInfo.SEASON, path='path4', season='season2'))

        search_item = MediaInfo(type=MediaInfo.SEASON, path='path4', season='season2')

        self.assertEqual(self.subject.find(search_item)['path'], 'path4')

    def test_find_episode_no_season_attribute(self):
        Storage.add(self.subject, MediaInfo(type=MediaInfo.EPISODE, path='path5', season='season3', episode="episode1"))
        Storage.add(self.subject, MediaInfo(type=MediaInfo.EPISODE, path='path6', season='season4', episode="episode2"))

        search_item = MediaInfo(type=MediaInfo.EPISODE, path='path5')

        self.assertEqual(self.subject.find(search_item), None)

    def test_find_episode_with_season_attribute_no_episode_attribute(self):
        Storage.add(self.subject, MediaInfo(type=MediaInfo.EPISODE, path='path5', season='season3', episode="episode1"))
        Storage.add(self.subject, MediaInfo(type=MediaInfo.EPISODE, path='path6', season='season4', episode="episode2"))

        search_item = MediaInfo(type=MediaInfo.EPISODE, path='path5', season='season3')

        self.assertEqual(self.subject.find(search_item), None)

    def test_find_episode_with_season_attribute_and_episode_attribute(self):
        Storage.add(self.subject, MediaInfo(type=MediaInfo.EPISODE, path='path5', season='season3', episode="episode1"))
        Storage.add(self.subject, MediaInfo(type=MediaInfo.EPISODE, path='path6', season='season4', episode="episode2"))

        search_item = MediaInfo(type=MediaInfo.EPISODE, path='path5', season='season3', episode="episode1")

        self.assertEqual(self.subject.find(search_item)['path'], 'path5')

    def test_add_no_repeat(self):
        item = MediaInfo(path='path1')

        self.subject.add(item)
        self.subject.add(item)

        self.assertEqual(len(self.subject.items()), 1)

    def test_remove(self):
        item = MediaInfo(path='path1')

        self.subject.add(item)

        self.assertEqual(len(self.subject.items()), 1)

        self.subject.remove(item)

        self.assertEqual(len(self.subject.items()), 0)

if __name__ == '__main__':
    unittest.main()
