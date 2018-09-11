import re, os, logging


#https://pypi.python.org/packages/c2/e3/a57a410a867d20fe869354f82896f4874614ecd2b63bfee14b5ab7f3c9fb/pyahocorasick-1.1.4.tar.gz#md5=850eed8264eef383b2671bbc95c2692c

class KeywordFilter(object):
    tree = None

    def __init__(self):
        try:
            import ahocorasick

            self.tree =  ahocorasick.Automaton()
            cf = file(os.path.join(os.path.dirname(__file__), 'cw.txt'))
            for c in cf.readlines():
                w = c.replace('\n', '')               
                self.tree.add_word(w , w)
            self.tree.make_automaton()

        except Exception, e:
            logging.error(str(e))

    def mark_filte(self, content):
        if self.tree is None:
            return content

        content = content.encode('utf8')

        for end_index, original_value in self.tree.iter(content):
            start_index = end_index - len(original_value) + 1

            #print original_value
            content = content.replace(original_value,"**")

          
        #print content
        return unicode(content, 'utf8')




    def output(self, content):
        return re.sub(r'\[\*\*(.*?)\*\*\]', '**', content)

    def search(self, content):
        if self.tree is None:
            return False
        return self.tree.search(content.encode('utf8'))

keyword = KeywordFilter()