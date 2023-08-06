# -*- coding: utf-8 -*-

import time
import requests

from requests.compat import json as _json


class ClientException(Exception):
    pass


def check_error(json):
    """
    检测微信公众平台返回值中是否包含错误的返回码。
    如果返回码提示有错误，抛出一个 :class:`ClientException` 异常。否则返回 True 。
    """
    if "errcode" in json and json["errcode"] != 0:
        raise ClientException("{}: {}".format(json["errcode"], json["errmsg"]))
    return json


class Client(object):
    """
    微信 API 操作类
    通过这个类可以方便的通过微信 API 进行一系列操作，比如主动发送消息、创建自定义菜单等
    """

    def __init__(self, config):
        self.config = config
        self._token = None
        self.token_expires_at = None

    @property
    def appid(self):
        return self.config.get("APP_ID", None)

    @property
    def appsecret(self):
        return self.config.get("APP_SECRET", None)

    def request(self, method, url, **kwargs):
        if "params" not in kwargs:
            kwargs["params"] = {"access_token": self.token}
        if isinstance(kwargs.get("data", ""), dict):
            body = _json.dumps(kwargs["data"], ensure_ascii=False)
            body = body.encode('utf8')
            kwargs["data"] = body

        r = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        r.raise_for_status()
        r.encoding = "utf-8"
        json = r.json()
        if check_error(json):
            return json

    def get(self, url, **kwargs):
        return self.request(
            method="get",
            url=url,
            **kwargs
        )

    def post(self, url, **kwargs):
        return self.request(
            method="post",
            url=url,
            **kwargs
        )

    def grant_token(self):
        """
        获取 Access Token。

        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://api.weixin.qq.com/cgi-bin/token",
            params={
                "grant_type": "client_credential",
                "appid": self.appid,
                "secret": self.appsecret
            }
        )

    def get_access_token(self):
        """
        判断现有的token是否过期。
        用户需要多进程或者多机部署可以手动重写这个函数
        来自定义token的存储，刷新策略。

        :return: 返回token
        """
        if self._token:
            now = time.time()
            if self.token_expires_at - now > 60:
                return self._token
        json = self.grant_token()
        self._token = json["access_token"]
        self.token_expires_at = int(time.time()) + json["expires_in"]
        return self._token

    @property
    def token(self):
        return self.get_access_token()

    def code_to_session(self, code):
        """
        使用小程序 login code 获取用户信息。

        :param code: 小程序 wx.login() 返回的 code
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://api.weixin.qq.com/sns/jscode2session",
            params={
                "js_code": code,
                "grant_type": "authorization_code",
                "appid": self.appid,
                "secret": self.appsecret
            }
        )

    def upload_media(self, media_type, media_file):
        """
        上传临时多媒体文件。

        :param media_type: 媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb）
        :param media_file: 要上传的文件，一个 File-object
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/media/upload",
            params={
                "access_token": self.token,
                "type": media_type
            },
            files={
                "media": media_file
            }
        )

    def download_media(self, media_id):
        """
        下载临时多媒体文件。

        :param media_id: 媒体文件 ID
        :return: requests 的 Response 实例
        """
        return requests.get(
            url="https://api.weixin.qq.com/cgi-bin/media/get",
            params={
                "access_token": self.token,
                "media_id": media_id
            }
        )

    def send_text_message(self, user_id, content):
        """
        发送文本消息。

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param content: 消息正文
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data={
                "touser": user_id,
                "msgtype": "text",
                "text": {"content": content}
            }
        )

    def send_image_message(self, user_id, media_id):
        """
        发送图片消息。

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param media_id: 图片的媒体ID。 可以通过 :func:`upload_media` 上传。
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data={
                "touser": user_id,
                "msgtype": "image",
                "image": {
                    "media_id": media_id
                }
            }
        )

    def send_article_message(self, user_id, title, description, url, thumb_url):
        """
        发送图文链接。

        每次可以发送一个图文链接
        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param title: 消息标题
        :param description: 图文链接消息
        :param url: 图文链接消息被点击后跳转的链接
        :param thumb_url: 图片链接，非媒体ID。
        :return: 返回的 JSON 数据包
        """
        a = self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data={
                "touser": user_id,
                "msgtype": "link",
                "link": {
                    "title": title,
                    "description": description,
                    "url": url,
                    "thumb_url": thumb_url
                }
            }
        )
        print(a)

    def send_miniprogrampage_message(self, user_id, title, pagepath, thumb_media_id):
        """
        发送小程序卡片。

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param title: 消息标题
        :param pagepath: 小程序的页面路径，跟app.json对齐，支持参数，比如pages/index/index?foo=bar
        :param thumb_media_id: 图片的媒体ID。 可以通过 :func:`upload_media` 上传。
        :return: 返回的 JSON 数据包
        """
        return self.post(
            url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
            data={
                "touser": user_id,
                "msgtype": "miniprogrampage",
                "miniprogrampage": {
                    "title": title,
                    "pagepath": pagepath,
                    "thumb_media_id": thumb_media_id
                }
            }
        )
