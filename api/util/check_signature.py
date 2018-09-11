# coding=utf-8

"""
path:
/subject/search

args:
device=phone&pid=b68c597b8b39e24247a09815c7b13655ec02f6d2&guid=b68c597b8b39e24247a09815c7b13655ec02f6d2&from=2&userid=201709090047599524950688&page_count=20&_t_=1521536780&platform=android&search_type=1&search_query=%E6%B3%95%E5%88%B6%E5%92%8C%E7%A4%BC%E6%B2%BB%E6%B3%95&app_type=2&_s_=cf97aba99a4397897abaad93371c0b57&page=1&ver=5.0.1
"""
import hashlib
import md5


path = "/subject/search"
args = "device=phone&pid=b68c597b8b39e24247a09815c7b13655ec02f6d2&guid=b68c597b8b39e24247a09815c7b13655ec02f6d2&from=2&userid=201709090047599524950688&page_count=20&_t_=1521536780&platform=android&search_type=1&search_query=%E6%B3%95%E5%88%B6%E5%92%8C%E7%A4%BC%E6%B2%BB%E6%B3%95&app_type=2&_s_=cf97aba99a4397897abaad93371c0b57&page=1&ver=5.0.1"

l = sorted(args.split("&"))

args = "".join(l[1:])

print args

token_string = "GET" + ":" + path + ":" + args + ":" + "1521536780" + ":" + "821l1i1x3fv8vs3dxlj1v2x91jqfs3om"

m1 = md5.new()
m1.update(token_string)
print m1.hexdigest()

print hashlib.md5(token_string).hexdigest()


