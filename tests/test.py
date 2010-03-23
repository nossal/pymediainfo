import os
import unittest
from xml.dom import minidom

from pymediainfo import MediaInfo


class MediaInfoTest(unittest.TestCase):

    def setUp(self):
        self.xml_data = open(os.path.join(os.path.dirname(__file__), 'data/sample.xml'), 'rb').read()

    def test_populate_tracks(self):
        xml = minidom.parseString(self.xml_data)
        mi = MediaInfo(xml)
        self.assertEqual(4, len(mi.tracks))

    def test_valid_video_track(self):
        xml = minidom.parseString(self.xml_data)
        mi = MediaInfo(xml)
        for track in mi.tracks:
            if track.track_type == 'Video':
                self.assertEqual('DV', track.codec)
                self.assertEqual('Interlaced', track.scan_type)
                break

    def test_track_integer_attributes(self):
        xml = minidom.parseString(self.xml_data)
        mi = MediaInfo(xml)
        for track in mi.tracks:
            if track.track_type == 'Audio':
                self.assertTrue(isinstance(track.duration, int))
                self.assertTrue(isinstance(track.bit_rate, int))
                self.assertTrue(isinstance(track.sampling_rate, int))
                break

    def test_track_other_attributes(self):
        xml = minidom.parseString(self.xml_data)
        mi = MediaInfo(xml)
        for track in mi.tracks:
            if track.track_type == 'General':
                self.assertEqual(5, len(track.other_file_size))
                self.assertEqual(4, len(track.other_duration))
                break

    def test_load_mediainfo_from_string(self):
        mi = MediaInfo(self.xml_data)
        self.assertEqual(4, len(mi.tracks))


if __name__ == '__main__':
    import sys, os
    os.chdir(os.path.dirname(__file__))

    try:
        import nose
    except ImportError:
        print ('nose is required to run the pymediainfo test suite')
        sys.exit(1)

    try:
        # make sure the current source is first on sys.path
        sys.path.insert(0, '..')
        import pymediainfo
    except ImportError:
        print ('Cannot find pymediainfo to test: %s' % sys.exc_info()[1])
        sys.exit(1)

    nose.main()