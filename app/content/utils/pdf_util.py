# coding=utf-8


""" 安装指南

一、centos系统安装中文字体

文档：
https://pypi.org/project/pdfkit/0.4.1/
https://www.cnblogs.com/chengJAVA/p/5292014.html


$ mkdir /usr/share/fonts/simsun
拷贝windows中的simsun.ttc到/usr/share/fonts/simsun/

# 然后执行以下命令

$ cd /usr/share/fonts/simsun
$ mkfontscale
$ mkfontdir
$ fc-cache -fv

# 执行以下命令让字体生效

$ source /etc/profile


# 补充，如果上面安装失败我们可参考下面方法

1、修改字体文件的权限，使root用户以外的用户也可以使用

 代码如下	复制代码
$ cd /usr/share/fonts/chinese/TrueType
$ chmod 755 *.ttf

2、建立字体缓存

 代码如下	复制代码
$ mkfontscale （如果提示 mkfontscale: command not found，需自行安装 # yum install mkfontscale ）
$ mkfontdir
$ fc-cache -fv （如果提示 fc-cache: command not found，则需要安装# yum install fontconfig ）



二、安装 wkhtmltopdf

Centos：

$ wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/	wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
$ xz -d wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
$ tar xvf wkhtmltox-0.12.4_linux-generic-amd64.tar
$ cd wkhtmltox/bin
$ sudo mv ./wkhtmltopdf /usr/bin/wkhtmltopdf
$ sudo chmod +x /usr/bin/wkhtmltopdf


Mac安装：
$ brew install Caskroom/cask/wkhtmltopdf


Debian/Ubuntu:

$ sudo apt-get install wkhtmltopdf



三、安装 pdfkit

$ pip install pdfkit


"""


import random
import os
from app.bskgk.utils import upload_file
import  urllib, urllib2

from django.conf import settings


def url_to_html(paper_id):
    cms_host = settings.CMS_HOST
    paper_url =cms_host + "/course/paper_to_pdf/" + paper_id
    return paper_url


def gen_pdf(html_url):
    import pdfkit
    abs_path = settings.CMS_HOST + '/static/html_to_pdf/index_page.html'
    option = {
            'page-size': 'A4',
            'margin-top': '1in',
            'margin-right': '0.99in',
            'margin-bottom': '1in',
            'margin-left': '0.99in',
            'header-html': abs_path,
            'header-line':None,
            'header-spacing': 5,
            # 'page-offset': 0,
            'footer-center': "[page]",
            'encoding': "utf-8",
            # 'minimum-font-size': 10,
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 10,
            }
    user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
    headers = {"User-Agent": user_agent}
    req = urllib2.Request(html_url, headers=headers)
    res = urllib2.urlopen(req)
    body = res.read()
    pdf_name = gen_random_string(16) + '.pdf'
    try:
        pdfkit.from_string(body, pdf_name, options=option)
    except Exception as e:
        print e

    return pdf_name





def convert_html_to_pdf(html_url):
    import pdfkit
    """转换PDF"""

    # return "http://img.winlesson.com/files/d24b933232ff1f01b322dee0756da7eb.pdf"

    # 1. 生成 PDF 文件

    pdf_name = gen_pdf(html_url)

    pdf_path = os.path.abspath(pdf_name)


    # 2. 上传 PDF
    disk_file = open(pdf_path)
    pdf_size = os.path.getsize(pdf_path)

    from django.core.files.uploadedfile import InMemoryUploadedFile

    # file, field_name, name, content_type, size, charset
    file_obj = InMemoryUploadedFile(disk_file, pdf_path, pdf_path, 'pdf', pdf_size, None)
    remote_url = upload_file(file_obj)

    # print remote_url

    if pdf_path:
        os.remove(pdf_path)

    return remote_url



def gen_random_string(length):
    import pdfkit
    import string

    chars = string.ascii_letters+string.digits
    return ''.join([random.choice(chars) for _ in range(length)])



