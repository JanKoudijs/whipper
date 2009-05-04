# -*- Mode: Python; test-case-name: morituri.test.test_image_cue -*-
# vi:si:et:sw=4:sts=4:ts=4

import os
import tempfile
import unittest

from morituri.test import common

from morituri.image import table, cue

class KingsSingleTestCase(unittest.TestCase):
    def setUp(self):
        self.cue = cue.Cue(os.path.join(os.path.dirname(__file__),
            'kings-single.cue'))
        self.cue.parse()
        self.assertEquals(len(self.cue.tracks), 11)

    def testGetTrackLength(self):
        t = self.cue.tracks[0]
        self.assertEquals(self.cue.getTrackLength(t), 17811)
        # last track has unknown length
        t = self.cue.tracks[-1]
        self.assertEquals(self.cue.getTrackLength(t), -1)

class KingsSeparateTestCase(unittest.TestCase):
    def setUp(self):
        self.cue = cue.Cue(os.path.join(os.path.dirname(__file__),
            'kings-separate.cue'))
        self.cue.parse()
        self.assertEquals(len(self.cue.tracks), 11)

    def testGetTrackLength(self):
        # all tracks have unknown length
        t = self.cue.tracks[0]
        self.assertEquals(self.cue.getTrackLength(t), -1)
        t = self.cue.tracks[-1]
        self.assertEquals(self.cue.getTrackLength(t), -1)

class KanyeMixedTestCase(unittest.TestCase):
    def setUp(self):
        self.cue = cue.Cue(os.path.join(os.path.dirname(__file__),
            'kanye.cue'))
        self.cue.parse()
        self.assertEquals(len(self.cue.tracks), 13)

    def testGetTrackLength(self):
        t = self.cue.tracks[0]
        self.assertEquals(self.cue.getTrackLength(t), -1)


class WriteCueTestCase(unittest.TestCase):
    def testWrite(self):
        fd, path = tempfile.mkstemp(suffix='morituri.test.cue')
        os.close(fd)

        it = table.IndexTable()
        

        t = table.ITTrack(1)
        t.index(1, path='track01.wav', relative=0)
        it.tracks.append(t)

        t = table.ITTrack(2)
        t.index(0, path='track01.wav', relative=1000)
        t.index(1, path='track02.wav', relative=0)
        it.tracks.append(t)

        self.assertEquals(it.cue(), """FILE "track01.wav" WAVE
  TRACK 01 AUDIO
    INDEX 01 00:00:00
  TRACK 02 AUDIO
    INDEX 00 00:13:25
FILE "track02.wav" WAVE
    INDEX 01 00:00:00
""")

        
