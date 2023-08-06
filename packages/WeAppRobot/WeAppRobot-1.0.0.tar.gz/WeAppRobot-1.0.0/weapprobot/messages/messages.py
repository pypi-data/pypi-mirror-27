# -*- coding: utf-8 -*-

import six
from weapprobot.messages.entries import StringEntry, IntEntry
from weapprobot.messages.base import WeAppRobotMetaClass


class MessageMetaClass(WeAppRobotMetaClass):
    pass


@six.add_metaclass(MessageMetaClass)
class WeChatMessage(object):
    message_id = IntEntry('MsgId', 0)
    target = StringEntry('ToUserName')
    source = StringEntry('FromUserName')
    time = IntEntry('CreateTime', 0)

    def __init__(self, message):
        self.__dict__.update(message)


class TextMessage(WeChatMessage):
    __type__ = 'text'
    content = StringEntry('Content')


class ImageMessage(WeChatMessage):
    __type__ = 'image'
    media_id = StringEntry('MediaId')
    img = StringEntry('PicUrl')


class MiniProgramPageMessage(WeChatMessage):
    __type__ = 'miniprogrampage'
    title = StringEntry('Title')
    app_id = StringEntry('AppId')
    page_path = StringEntry('PagePath')
    thumb_url = StringEntry('ThumbUrl')
    thumb_media_id = StringEntry('ThumbMediaId')


class UnknownMessage(WeChatMessage):
    __type__ = 'unknown'
