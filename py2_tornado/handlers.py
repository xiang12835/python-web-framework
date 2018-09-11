from views import *
import os.path


TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates")

HANDLERS = [(r'/', IndexHandler),
			(r'/login', LoginHandler),
			(r'/poem', PoemPageHandler)]
			
HANDLERS += [(r'/show', ShowHandler)]
