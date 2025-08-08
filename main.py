from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, render_template, request, redirect, flash, session
from datetime import datetime
from bson.objectid import ObjectId
import random
from passlib.hash import sha256_crypt
from datetime import datetime

uri = "mongodb+srv://aravindn2004:nArAyAnA28@cluster0.6yq2yjf.mongodb.net/?appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, tls = True, tlsAllowInvalidCertificates=True)
db = client.Blogger
app = Flask("Blogging")
app.config['SECRET_KEY'] = ';ljapw98u439p8lvkdfscv'


@app.route('/', methods = ["GET", "POST"])
def getStart():
    if (request.method == "GET"):
        blogs = db.blogs.find()
        return render_template("index.html", blogs = blogs) #Rendering index.html with all blogs in the database
    if (request.method == "POST"):
        if ("sign_up" in request.form):
            new_user = {"name": request.form['fName'], "email": request.form['email'], "pw": sha256_crypt.hash(request.form['pw'])}
            flash("Account registered")
            db.accounts.insert_one(new_user)
        if ("login_owner" in request.form):
            user = db.accounts.find_one({"email": request.form['email']})
            if (user):
                if (sha256_crypt.verify(request.form['pw'], user['pw'])):
                    session['name'] = user['name']
                    session['email'] = user['email']
                    url = "/dashboard/" + str(user["_id"])
                    return redirect(url)
                else:
                    flash("Incorrect Password")
                    return redirect('/')
            else:
                flash("Account not found")
                return redirect('/')
    return ""

@app.route("/logout", methods = ["GET", "POST"])
def logout():
    session.clear()
    return redirect('/')

@app.route("/dashboard/<acc_id>", methods = ["GET", "POST"])
def account_dashboard(acc_id):
    user = db.accounts.find_one({'_id':ObjectId(acc_id)})
    user_blogs = list(db.blogs.find({'user_name':user['name']}))
    if (request.method == "GET"):
        if (session['email'] != user['email']):
            flash("You are not logged in")
            return redirect('/')
        else:
            print(user_blogs)
            return render_template("account_page.html", blogs = user_blogs, user_name = user['name'])
    if (request.method == "POST"):
        if ("delete" in request.form):
            db.blogs.delete_one({"name":request.form["user_name"]})
            flash("blog successfully deleted")
            return redirect(f'/dashboard/{acc_id}')
        else:
            raw_date = datetime.now()
            actual_date = raw_date.strftime("%B %d, %Y") #Formatting datetime object into month day, year format
            blog_post = {"title":request.form['title'], "content":request.form['content'], "time": actual_date, 'user_name':user['name']}
            db.blogs.insert_one(blog_post)
            flash("Blog successfully posted! Check back with the main page to see your post")
            return redirect(f'/dashboard/{str(acc_id)}')
    return ""

@app.route("/delete/<_id>", methods = ["GET", "POST"])
def delete_blog(_id):
    blog = db.blog.find_one({'_id':ObjectId(_id)})
    user = db.accounts.find_one({'name':blog['user_name']}) #Getting user info from database to redirect user back to account page
    db.blog.delete_one({'_id':ObjectId(_id)})
    flash("blog deleted")
    return redirect(f'/dashboard/{user['_id']}')

    
if __name__ == '__main__':
    app.run(debug = True)   
    