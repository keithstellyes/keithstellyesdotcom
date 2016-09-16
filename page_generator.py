from genshi.template import MarkupTemplate as MT

def compile_tmplt(path):
    tmpl = MT(open(path,'r').read())
    f = open('out.html','w')
    f.write(str(tmpl.generate()))
