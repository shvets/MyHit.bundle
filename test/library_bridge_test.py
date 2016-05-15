# coding=utf-8

import test_helper

import unittest

import library_bridge

class LibraryBridgeTest(unittest.TestCase):
    def setUp(self):
        self.subject = library_bridge.bridge

    def test_export_object(self):
        self.subject.export_object('str', ''.__class__)

        self.assertEqual(self.subject.objects, {'str': 'abc'.__class__})

    def test_export_objects(self):
        self.subject.export_objects({'str': ''.__class__, 'dict': dict().__class__})

        self.assertEqual(self.subject.objects, {'str': 'abc'.__class__, 'dict': dict().__class__})

if __name__ == '__main__':
    unittest.main()
