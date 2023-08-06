# -*- coding: utf-8 -*-
import time

from collections import defaultdict, namedtuple
from weapprobot.utils import is_string, to_text


def renderable_named_tuple(typename, field_names, tempalte):
    class TMP(namedtuple(typename=typename, field_names=field_names)):
        __TEMPLATE__ = tempalte

        @property
        def args(self):
            # https://bugs.python.org/issue24931
            return dict(zip(self._fields, self))

        def process_args(self, kwargs):
            args = defaultdict(str)
            for k, v in kwargs.items():
                if is_string(v):
                    v = to_text(v)
                args[k] = v
            return args

        def render(self):
            return to_text(
                self.__TEMPLATE__.format(**self.process_args(self.args))
            )

    TMP.__name__ = typename
    return TMP


class WeChatReply(object):
    def process_args(self, args):
        pass

    def __init__(self, message=None, **kwargs):
        if message and "source" not in kwargs:
            kwargs["source"] = message.target

        if message and "target" not in kwargs:
            kwargs["target"] = message.source

        if 'time' not in kwargs:
            kwargs["time"] = int(time.time())

        args = defaultdict(str)
        for k, v in kwargs.items():
            if is_string(v):
                v = to_text(v)
            args[k] = v
        self.process_args(args)
        self._args = args

    def render(self):
        return to_text(self.TEMPLATE.format(**self._args))

    def __getattr__(self, item):
        if item in self._args:
            return self._args[item]


class TransferCustomerServiceReply(WeChatReply):
    TEMPLATE = to_text("""
    <xml>
    <ToUserName><![CDATA[{target}]]></ToUserName>
    <FromUserName><![CDATA[{source}]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[transfer_customer_service]]></MsgType>
    <TransInfo>
         <KfAccount><![CDATA[{account}]]></KfAccount>
     </TransInfo>
    </xml>
    """)


class SuccessReply(WeChatReply):
    def render(self):
        return "success"
