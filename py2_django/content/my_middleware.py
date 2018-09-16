# 2-6 Middleware
class MyMiddleware(object):
	def __init__(self):
		print 'Hello, this is my middleware!'

	def process_view(self,request,func, args,kwargs):
		print func