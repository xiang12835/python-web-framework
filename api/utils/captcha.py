#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import Image
import ImageDraw
import ImageFont
import random
import cStringIO
import hashlib
import uuid
from cache import get_search, set_search


class CaptchaImage(object):

    ERROR_CODE_TIMEOUT = 2  # 验证码超时
    ERROR_CODE_WRANG = 1  # 验证码超时
    OK = 0  # 成功

    @classmethod
    def save_sid(cls, sid, val):
        set_search(sid, val, 10*60)

    @classmethod
    def get_sid(cls, sid):
        get_search(sid)

    def __init__(self, style):
        self._style = style
        self._img = None
        self._sessionid = None

    @property
    def sessionid(self):
        if self._sessionid is None:
            cur_time = int(time.time() * 1000)
            code = self._style.code
            self._sessionid = CaptchaImage.gen_sessionid(code, cur_time)
        return self._sessionid

    @classmethod
    def gen_sessionid(cls, code, cur_time):
        value = code.encode('utf-8')
        value = value.lower()
        value = 'captcha_code:{};cur_time:{}'.format(value, cur_time)
        value = hashlib.md5(value).hexdigest()
        return '{}.{}.{}'.format(cur_time, value,uuid.uuid1().hex)

    @classmethod
    def verify_sessionid(cls, sessionid, code):

        try:
            arrs = sessionid.split('.')
            cur_time = arrs[0]
            session_code = arrs[1]

            now = int(time.time() * 1000)
            if now - int(cur_time) > 600000:  # 10分钟过期
                return cls.ERROR_CODE_TIMEOUT

            session_code_md5 = cls.gen_sessionid(code, cur_time).split(".")[1]
            mem_value = cls.get_sid(sessionid)

            #成功条件1、sessionid memcached 里有。2、时间在有效期内。3、验证码正确。
            if session_code == session_code_md5:
                #################################
                ## 如果随机码验证成功,判断唯一性
                #################################
                if mem_value == "1":
                    #1 normal
                    #2 delete
                    cls.save_sid(sessionid, "2")

                #################################
                ## 如果memcache里有数据，且为2。
                ## 说明这个session id 是验证过的，返回错误。
                #################################
                elif mem_value == "2":
                    return cls.ERROR_CODE_WRANG

                return cls.OK
        except Exception as e:
            logging.exception(e)
        return cls.ERROR_CODE_WRANG

    def draw(self):
        #新建画布
        style = self._style
        im = Image.new('RGBA', (style.img_width, style.img_height))
        draw = ImageDraw.Draw(im)

        #写入验证码文字
        w, h = draw.textsize("M", font=style.font)
        span = 1
        x = style.img_width - (w + span) * style.count
        y = style.y_offset

        for i in style.code:
            #draw.text((width - 5 - w, 110), text, colour,font=font)
            draw.text((x, y), i, font=style.font, fill=style.font_color)
            w, h = draw.textsize(i,font=style.font)
            x += w + span #style.get_char_width(i)

        del draw
        self._img = im
        return im

    def save(self, stream):
        self._img.save(stream, 'GIF', transparency=0)


class CaptchaStyle(object):
    FONT_COLOR = [
        (72, 61, 139),
        (0, 100, 0),
        (25, 25, 112),
        (165, 42, 42),
        (139, 10, 80),
        (0, 0, 139),
    ]

    BG_COLOR = (255, 255, 255)

    LETTER = u'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # http://www.fonts2u.com/kids.%E5%AD%97%E4%BD%93
    FONT_PATH = 'api/util/fonts/trado.ttf'

    def __init__(self, img_width, img_height, count=4):
        self._img_width = img_width
        self._img_height = img_height
        self._count = count
        self._code = None
        self._font_size = None
        self._font = None

    @property
    def count(self):
        return self._count

    @property
    def code(self):
        if self._code is None:
            self._code = random.sample(self.__class__.LETTER, self._count)
            self._code = u''.join(self._code)
        return self._code

    @property
    def img_width(self):
        return self._img_width

    @property
    def img_height(self):
        return self._img_height

    @property
    def bg_color(self):
        return self.__class__.BG_COLOR

    @property
    def x_offset(self):
        return (self.img_width - self.font_size * self.count / 1.8) / 2

    @property
    def y_offset(self):
        return max((self.img_height - self.font_size) / 2, 0)

    def get_char_width(self, ch):
        if ch in ('m', 'w', 'M', 'W'):
            return self.font_size / 1.8
        elif ch.isupper():
            return self.font_size / 2.4
        else:
            return self.font_size / 3

    @property
    def font_size(self):
        if self._font_size is None:
            by_w = self._img_width / self._count + 2
            by_h = self._img_height
            self._font_size = int(round(min(by_w, by_h), 0))
        return self._font_size

    @property
    def font_color(self):
        return random.choice(self.__class__.FONT_COLOR)

    @property
    def font_path(self):
        return self.__class__.FONT_PATH

    @property
    def font(self):
        if self._font is None:
            self._font = ImageFont.truetype(self.font_path, self.font_size)
        return self._font


# class CaptchaStyleKids(CaptchaStyle):
#     FONT_PATH = 'others/fonts/kids.ttf'
#
#     def get_char_width(self, ch):
#         if ch in ('m', 'w', 'M', 'W'):
#             return self.font_size / 1.4
#         elif ch.isupper():
#             return self.font_size / 1.7
#         else:
#             return self.font_size / 2
#
#
# class CaptchaStyleDowntown(CaptchaStyle):
#     LETTER = u'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#     # FONT_PATH = '/Users/user/work/project/m-service/others/fonts/VTKS_DOWNTOWN.ttf'
#     FONT_PATH = '/Users/user/work/project/m-service/others/fonts/2.ttf'
#     def get_char_width(self, ch):
#         if ch in ('m', 'w', 'M', 'W'):
#             return self.font_size / 1.4
#         else:
#             return self.font_size / 2.3
#
#     @property
#     def y_offset(self):
#         return max((self.img_height - self.font_size) / 2, 0) - self.font_size / 6


class CaptchaUtil(object):

    @classmethod
    def get_captcha(cls, width, height, count=4):
        ret = {}
        style = CaptchaStyle(width, height, count)
        img = CaptchaImage(style)
        code = style.code
        ret['code'] = code.encode('utf-8')
        ret['sessionid'] = img.sessionid
        ret['height'] = height
        ret['width'] = width

        stream = cStringIO.StringIO()
        img.draw()
        img.save(stream)
        ret['img'] = stream.getvalue()
        CaptchaImage.save_sid(str(img.sessionid), "1")
        return ret

    @classmethod
    def check_captcha(cls, sessionid, code):
        return CaptchaImage.verify_sessionid(sessionid=sessionid, code=code)

if __name__ == '__main__':
    pass
    print CaptchaUtil.get_captcha(100, 100)

