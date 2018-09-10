# coding=utf-8

from __future__ import unicode_literals

import os
import sys
import logging
import urllib
import random


PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir, os.pardir))
# sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir, os.pardir, os.pardir))

from base.settings import load_django_settings

load_django_settings('python-web-framework.base')


def save_img(img_url, file_name):
    # 下载图片，并保存到文件夹中

    try:
        urllib.urlretrieve(img_url, filename=file_name)
    except Exception as e:
        logging.error('file error: {}'.format(e))


def gen_user_image_url(_url):
    from upload_util import upload_file_to_qcloud
    from django.core.files.uploadedfile import InMemoryUploadedFile
    import random
    import os

    # 1. 下载图片
    r1 = random.randint(1, 10000)
    ff = _url.split(".")
    file_format = ff[-1]
    file_format = file_format.lower()
    img_name = 'tmp_%s.%s' % (r1, file_format)

    img_path = os.path.abspath(img_name)

    save_img(_url, img_path)

    # 2. 生成文件对象
    disk_file = open(img_path)
    img_size = os.path.getsize(img_path)
    # file, field_name, name, content_type, size, charset
    file_obj = InMemoryUploadedFile(disk_file, img_path, img_path, file_format, img_size, None)

    # 3. 上传图片
    r = upload_file_to_qcloud(file_obj)

    # 4. 删除本地文件
    if img_path:
        os.remove(img_path)

    return r





def gen_matrix(l=None):
    """
    matrix = [
        [(5, 5), (80, 5), (160, 5)],
        [(5, 80), (80, 80), (160, 80)],
        [(5, 160), (80, 160), (160, 160)],
    ]

    [[(5, 5), (80, 5), (160, 5)], [(5, 80), (80, 80), (160, 80)], [(5, 160), (80, 160), (160, 160)]]
    :param l:
    :return:
    """

    if l == None:
        l = [5, 80, 160]

    matrix = []
    length = len(l)

    for i in xrange(length):
        # row = []
        for j in xrange(length):
            _tuple = (l[j], l[i])
            matrix.append(_tuple)

        # matrix.append(row)

    return matrix




if __name__ == '__main__':

    img_url = "http://img.winlesson.com/images/3ee98d602d98845a2a6ef430fe2f99e3.jpg"

    # r1 = random.randint(1, 10000)
    # r2 = random.randint(1, 10000)
    #
    # ff = img_url.split(".")
    #
    # file_format = ff[-1]
    # file_format = file_format.lower()
    #
    # tmp_path = './tmp_%s_%s.%s' % (r1, r2, file_format)
    # save_img(img_url, tmp_path)
    #
    # print gen_matrix()

    r = gen_user_image_url(img_url)
    print r
