#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ykdl.simpleextractor import SimpleExtractor
from ykdl.util.html import get_content, add_header
from ykdl.util.match import match1, matchall

class HuyaLive(SimpleExtractor):
    name = u"Huya Live (虎牙直播)"

    def __init__(self):
        SimpleExtractor.__init__(self)
        add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3')
        self.live = True
        self.title_pattern = 'liveRoomName = \"([^\"]+)'
        self.url_pattern = 'hasvedio: \'([^\']+)'
        self.artist_pattern = 'videoTitle = \"([^\"]+)'

    def get_info(self):
        assert self.v_url[0], u"主播正在休息"
        return 'm3u8', float('inf')

site = HuyaLive()
