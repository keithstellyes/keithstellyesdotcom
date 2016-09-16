"""
AUTHOR: Keith Stellyes
This is for automating parts of the my website's design process.

This "compiles" the various templates. It is multiple stages.
All pages must be within the /pages/ directory , and all templates begin with a
_ in their name. _home.html compiles to home.html.
Here's the process per template:

#1. See if it is a markdown-only template. These follow the following syntax:
<!--MARKDOWN ONLY! TITLE;MD-->
TITLE OF WEBPAGE
MARKDOWN-FILE-NAME-IN /data

See _home.html for an example. This is replaced with another template that
continues along. This template is only-md.html located in /data/

#2. Insert the Python code
Genshi's execution enviroment and variables is local to each template it seems.
Normally a page might look like:

<?python
def my_func():
    return "o hi"
?>
...
<body><p>
${my_func()}
</p></body>

Instead of just copy-pasting the same func's, the script basically does that,
replacing <!--ENTRY:PYTHON--> with the Python code. This Python code is stored
at /data/tmplt-funcs.py

#3. Run through the Genshi template engine
The core of the fun here, this will actually parse what is left over. Important
note: It uses a perfectionistic XML engine at its core, so 99% of HTML code
you find in the wild and in tutorials, samples, etc. will throw errors. This
leads to a bit of funky functions, but this is the best I got.
Note that the function, set_title_etc() found in every file, also adds a
comment with a time stamp and a random number for fun + debug purposes.
"""

import os
import os.path
from genshi.template import MarkupTemplate as MT

"""
def compile_tmplt(ipath,opath):
    tmpl = MT(open(ipath,'r').read())
    f = open(opath,'w')
    f.write(str(tmpl.generate()))
    f.close()
"""

def compile_tmplt(ipath,opath,py_to_insert):
    #Insert the Python at the beginning for the Genshi template engine
    s_to_insert = "<?python\n" + py_to_insert + "\n?>"
    s = open(ipath,'r').read()
    if s.startswith('<!--MARKDOWN ONLY! TITLE;MD-->\n'):
        s = s.split('\n')
        title = s[1]
        body = s[2]
        s = open(data_dir + 'only-md.html').read()
        s = s.replace('_TITLE_',title)
        s = s.replace('_BODY_',body)
    #The file uses <!--ENTRY:PYTHON--> as the entry point for insertion
    s = s.replace('<!--ENTRY:PYTHON-->',s_to_insert)
    tmpl = MT(s)
    f = open(opath,'w')
    f.write(str(tmpl.generate()))
    f.close()

f = os.path.dirname(os.path.realpath(__file__))

page_dir = f + '/pages/'
data_dir = f + '/data/'
py_file_to_insert = f + '/data/tmplt-funcs.py'
py_code = open(py_file_to_insert,'r').read()

for f in os.listdir(page_dir):
    if f[0] == '_' and os.path.isfile(page_dir + f):
        compile_tmplt(page_dir + f, page_dir + f[1:],py_code)
