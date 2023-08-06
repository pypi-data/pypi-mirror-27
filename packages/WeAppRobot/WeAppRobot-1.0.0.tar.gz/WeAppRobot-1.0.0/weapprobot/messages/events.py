# -*- coding: utf-8 -*-

import six
from weapprobot.messages.entries import StringEntry, IntEntry
from weapprobot.messages.base import WeAppRobotMetaClass


class EventMetaClass(WeAppRobotMetaClass):
    pass


@six.add_metaclass(EventMetaClass)
class WeChatEvent(object):
    target = StringEntry('ToUserName')
    source = StringEntry('FromUserName')
    time = IntEntry('CreateTime')
    message_id = IntEntry('MsgID', 0)

    def __init__(self, message):
        self.__dict__.update(message)


class UserEnterTempsessionEvent(WeChatEvent):
    __type__ = 'user_enter_tempsession_event'
    session_from = StringEntry('SessionFrom')


class UnknownEvent(WeChatEvent):
    __type__ = 'unknown_event'
