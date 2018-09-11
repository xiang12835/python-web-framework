#coding=utf-8
import os

def load_settings(settings, debug=True, **kwargs):
    pass
def check_settings(settings):
    pass


def load_tonardo_settings(tonardo_settings={}):
    tonardo_settings.update({
            'cookie_secret': '3f85eb25881ddd5c31f715542ae856c4',
            'template_path': os.path.join(os.path.dirname(__file__), "templates"),
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
    })
