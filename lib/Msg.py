#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: Msg.py
# Date: Fri Nov 21 14:10:21 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from datetime import datetime
from bs4 import BeautifulSoup
from .utils import ensure_bin_str, ensure_unicode

TYPE_MSG = 1
TYPE_IMG = 3
TYPE_SPEAK = 34
TYPE_VIDEO = 43
TYPE_EMOJI = 47
TYPE_LOCATION = 48
TYPE_LINK = 49
TYPE_VOIP = 50
TYPE_SYSTEM = 10000

class WeChatMsg(object):
    """ fields in concern"""
    FIELDS = ["msgSvrId","type","isSend","createTime","talker","content","imgPath"]
    FILTER_TYPES = [TYPE_SYSTEM]

    @staticmethod
    def filter_types(tp):
        if tp in WeChatMsg.FILTER_TYPES or tp > 10000 or tp < 0:
            return True
        return False

    def __init__(self, row):
        """ row: a tuple corresponding to FIELDS"""
        assert len(row) == len(WeChatMsg.FIELDS)
        for f, v in zip(WeChatMsg.FIELDS, row):
            setattr(self, f, v)
        self.createTime = datetime.fromtimestamp(self.createTime / 1000)
        if self.content:
            self.content = ensure_unicode(self.content)

    def msg_str(self):
        # TODO: fix more types
        if self.type == TYPE_LOCATION:
            soup = BeautifulSoup(self.content)
            loc = soup.find('location')
            label = loc['label']
            ret = label
            try:
                poiname = loc['poiname']
                if poiname:
                    ret = poiname
            except:
                pass
            return ret + " ({},{})".format(loc['x'], loc['y'])
        else:
            return self.content

    def __repr__(self):
        ret = u"{}|{}:{}:{}".format(
            self.type,
            ensure_unicode(self.talker) if not self.isSend else 'me',
            self.createTime,
            ensure_unicode(self.msg_str())).encode('utf-8')
        if self.imgPath:
            ret = u"{}|img:{}".format(ensure_unicode(ret.strip()), self.imgPath)
            return ret.encode('utf-8')
        else:
            return ret