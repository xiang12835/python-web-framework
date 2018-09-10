#! /usr/bin/env python
# coding=utf-8


import hashlib
import hmac
import json
import random
import re
import string
import time
import uuid
from datetime import datetime
from hashlib import sha1
import os
from django.core.exceptions import ObjectDoesNotExist
import shutil
import qrcode
import requests
import random
import urllib
from PIL import Image
import logging
# from app.api_util.qcloud.qcloud_file import QCloudFile


def upload_file(memfile, url="http://123.206.180.82/file/upload/", data=None, _headers=None):
    if not _headers:
        _headers = {"Content-Type": "multipart/form-data"}

    ff = memfile.name.split(".")

    r1 = random.randint(1,10000)
    r2 = random.randint(1,10000)

    tmp_path = './tmp_%s_%s.%s' % (r1,r2,ff[-1])

    save_tmp_file(memfile, tmp_path)
    files = {"files": open(tmp_path, 'rb')}

    r = requests.post(url, files=files)
    r_json = r.json()
    logging.info(r_json)
    remote_path = r_json.get("result", {}).get("filePath", None)

    if remote_path:
        os.remove(tmp_path)

    return remote_path


def upload_file_to_qcloud(file_obj):
    ff = file_obj.name.split(".")

    r1 = random.randint(1, 100000)
    r2 = random.randint(1, 100000)
    r3 = random.randint(1, 100000)

    file_format = ff[-1]
    file_format = file_format.lower()

    tmp_path = './wl_%s_%s_%s.%s' % (r1, r2, r3, file_format)
    save_tmp_file(file_obj, tmp_path)

    r = ''

    try:
        disk_file = open(tmp_path, 'rb')
        filename = 'wl_%s_%s_%s.%s' % (r1, r2, r3, ff[-1])

        if file_format in ("gif", "jpeg", "jpg", "png"):
            QCloudFile().upload_cms_image(disk_file, filename)
            r = "http://picture-10004299.file.myqcloud.com/cms/%s" % filename
        else:
            QCloudFile().upload_file(disk_file, filename)
            r = "http://picture-10004299.file.myqcloud.com/%s" % filename

    except Exception as e:
        logging.error(e)

    finally:
        if r:
            os.remove(tmp_path)

    return r


def save_crop(img_url,url="http://123.206.180.82/file/upload/"):

    logging.info(img_url)
    ff = img_url.split(".")
    r1 = random.randint(1,10000)
    r2 = random.randint(1,10000)
    tmp_path = './tmp_%s_%s.%s' % (r1,r2,ff[-1])
    img_data = urllib.urlopen(img_url).read()
    save_img(img_url , tmp_path)

    path_list =  []
    
    im = Image.open(tmp_path)
    w , h = im.size
    fragement = 4
    sub_height = h / fragement
    yu = h % fragement
    index = 1

    left = 0
    upper = 0
    right = w
    lower = sub_height

    for h in xrange(fragement):
        
        box = ( left, upper, right, lower )
        logging.info(box)
        crop_image = im.crop(box)

        i_tmp_path = './tmp_%s_%s_%s.%s' % (r1, r2 , index,ff[-1])

        crop_image.save(i_tmp_path,quality=95)
        #save_tmp_file(crop_image, i_tmp_path)
        files = {"files": open(i_tmp_path, 'rb')}
        r = requests.post(url, files=files)
        r_json = r.json()
        remote_path = r_json.get("result", {}).get("filePath", None)
        path_list.append(remote_path)

        logging.info(r_json)
        os.remove(i_tmp_path)
        
        upper += sub_height
        lower += sub_height

        index += 1
        if index == 4:
            lower+= yu

    os.remove(tmp_path)

    return path_list


def save_tmp_file(f, path):
    
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def save_img(img_url, file_name):
    # 下载图片，并保存到文件夹中

    try:
        urllib.urlretrieve(img_url, filename=file_name)
    except Exception as e:
        logging.error('file error: {}'.format(e))

