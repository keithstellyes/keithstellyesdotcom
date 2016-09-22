from flask import Flask
from flask import request
from flask import Response
from flask import redirect
from mtg_lookup.mtg_lookup import do_search
app = Flask(__name__)

#ipaddr info api:
#http://ip-api.com/json/208.80.152.201

#THE CARD IMAGES ARE DOWNLOADED FROM:
#http://www.slightlymagic.net/forum/viewtopic.php?f=15&t=18042&p=190624#p190624

def log(s):
    print(s)

@app.route("/")
def hello():
    return Response(open('pages/home.html'))

@app.route("/style.css")
def style_css():
    return Response(open('pages/style.css').read(),mimetype="text/css")

@app.route("/<img>.png")
def png(img):
    return Response(open("pages/" + img + '.png','br').read(), mimetype="image/png")

@app.route("/<url>.html")
def redir(url):
    if url == "home":
        return redirect("/")
    return redirect("/" + url)

@app.route("/home")
def redir_home():
    return redirect("/")

@app.route("/projects")
def projects_page():
    return Response(open('pages/projects.html'))

@app.route("/contact")
def contact_page():
    return Response(open('pages/contact.html'))

@app.route("/apps")
def apps_page():
    #return Response(open('pages/apps.html'))
    return redirect("/apps/mtg-lookup")

@app.route("/apps/mtg-lookup")
def mtg_lookupp():
    return Response(open('pages/mtglookup.html'))

@app.route("/apps/mtg-lookup/mtg_sendquery",methods=["POST"])
def mtg_sendqueryy():
    s = do_search(request.form['query'],open('data/mtg-lookupresults.html').read())
    return Response(s,mimetype="text/html")

@app.route("/send_contact",methods=["POST"])
def send():
    print("Name:",request.form['name'])
    print("E-mail:",request.form['email'])
    print("Body:",request.form['body'])
    #s = do_search(request.form['body'],open('data/mtg-lookupresults.html').read())
    return Response(open('pages/send_contact.html'))
    #return Response(s,mimetype="text/html")

if __name__ == "__main__":
    import os
    port = os.environ.get("PORT")
    try:
        app.run("0.0.0.0",int(port))
    except TypeError:
        app.run()
