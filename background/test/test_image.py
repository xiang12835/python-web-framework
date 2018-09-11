# coding=utf-8

import urllib
import random
import logging


def save_img(img_url, file_name):
    # 下载图片，并保存到文件夹中

    try:
        urllib.urlretrieve(img_url, filename=file_name)
    except Exception as e:
        logging.error('file error: {}'.format(e))



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
        row = []
        for j in xrange(length):
            _tuple = (l[j], l[i])
            row.append(_tuple)

        matrix.append(row)

    return matrix



if __name__ == '__main__':

    img_url = "http://img.winlesson.com/images/3ee98d602d98845a2a6ef430fe2f99e3.jpg"

    r1 = random.randint(1, 10000)
    r2 = random.randint(1, 10000)

    ff = img_url.split(".")

    file_format = ff[-1]
    file_format = file_format.lower()

    tmp_path = './tmp_%s_%s.%s' % (r1, r2, file_format)
    save_img(img_url, tmp_path)

    # print gen_matrix()

