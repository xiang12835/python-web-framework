# coding=UTF-8

# from django.shortcuts import render
from django.http import HttpResponse,Http404

# Create your views here.
def hello(request):
	return HttpResponse("hello world!")

def hello1(request,num):
	try:
		num = int(num)
		return HttpResponse("This is " + str(num))
	except ValueError:
		raise Http404()

from django.shortcuts import render_to_response

# def views(request):
# 	return render_to_response('2.html',{"name":"hello"})

from app.content.forms import Mybook
# from django.http import HttpResponse
# from django.shortcuts import render_to_response


def mybook(request):
	if request.method == 'POST':
		form = Mybook(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			name = data["name"]
		  	return HttpResponse(name)

	form = Mybook()
	return render_to_response('book.html',{'form':form})


# 高级视图，法一

#def view1(request):
#	return render_to_response('1.html')
#def view2(request):
#	return render_to_response('2.html')

# def views(request,template_name):
# 	return render_to_response(template_name)

# 高级视图，法二
def view1(request):
	return render_to_response('1.html')
def view2(request):
	return render_to_response('2.html')
def views(func):
	def view(request):
		# do something
		return func(request)
	return view


# 3-2 序列化——第一个API，返回JSON数据
# from app.learning.models import Book
# from app.learning.serializers import BookSerializer

# from django.http import StreamingHttpResponse
# from rest_framework.renderers import JSONRenderer

# class JSONResponse(StreamingHttpResponse):
# 	def __init__(self,data,**kwargs):
# 		content = JSONRenderer().render(data)
# 		kwargs['content_type'] = 'application/json'
# 		super(JSONResponse,self).__init__(content,**kwargs)

# def book_list(request,num):
# 	if request.method == 'GET':
# 		b = Book.objects.get(id=num)
# 		ser = BookSerializer(b)
# 		return JSONResponse(ser.data)

# 3-3-1 基于类的视图
# from rest_framework import APIView
# from rest_framework import Response
#
# class BookList(APIView):
# 	def get(self,request,format=None):
# 		books = Book.objects.all()
# 		ser = BookSerializer(books,many=True)
# 		return Response(ser.data)
#
# 	def post(self,request,format=None):
# 		ser = BookSerializer(request.DATA)
# 		if ser.is_valid():
# 			ser.save()
# 			return Response(ser.data)
# 		return Response(ser.errors)
#
# class BookDetail(APIView):
# 	def get(self,request,num,format=None):
# 		books = Book.objects.all(id=num)
# 		ser = BookSerializer(b)
# 		return Response(ser.data)


# # 3-3-2 通用视图
# from rest_framework import generics

# class BookList(APIView):
# 	queryset=Book.objects.all()
# 	serializer_class=BookSerializer


# 2-5-1 django自带的小缓存
from app.content.models import Book
from django.core.cache import cache

def view(request):
	if cache.get('book'):
		b=cache.get('book')
	else:
		b=Book.objects.all()
		cache.set('book',b)
	return render_to_response('1.html',{'book':b})


# # 2-5-2 django可以缓存整个视图的方法
# from django.decorators.cache import cache_page
# @cache_page(60*15)  #配置过期的时间
# def view(request):
# 	b=Book.objects.all()
# 	return render_to_response('1.html',{'book':b})
