from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, render_template, request, redirect, flash, session
from datetime import datetime
from bson.objectid import ObjectId
import random
from passlib.hash import sha256_crypt

uri = "mongodb+srv://aravindn2004:nArAyAnA28@cluster0.6yq2yjf.mongodb.net/?appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, tls = True, tlsAllowInvalidCertificates=True)
db = client.One_Stop_Shop
app = Flask("One_Stop_Shop")
app.config['SECRET_KEY'] = ';ljapw98u439p8lvkdfscv'

cart = []


@app.route('/', methods = ["GET", "POST"])
def getStart():
    list_shops = []
    list_products = []
    accounts = db.accounts.find()
    products = db.products.find()
    for i in accounts:
        list_shops.append(i)
    for i in products:
        list_products.append(i)
    if (request.method == "GET"):
        print(cart)
        return render_template('index.html', list_shops = list_shops, list_products = list_products, length = len(cart))
    if (request.method == "POST"):
        if ("register_owner" in request.form):
            if (db.accounts.find_one({'email':request.form['email']})):
                flash("User already within databse")
                return redirect('/')
            encrypted = sha256_crypt.hash(request.form['pw'])
            temp_entry = {'shop_name':request.form['shop_name'], 'owner_name':request.form['owner_name'], 'email':request.form['email'], 'contact':request.form['contact'], 'pw':encrypted}
            db.accounts.insert_one(temp_entry)
            return redirect('/')
        if ("login_owner" in request.form):
            c = db.accounts.find_one({'email': request.form['email']})
            if (c):
                if (sha256_crypt.verify(request.form['pw'], c['pw'])):
                    session['email'] = c['email']
                    session['name'] = c['owner_name']
                    flash("Logged in")
                    name = "/shop_home/" + str(c["_id"])
                    return redirect(name)
                else:
                    flash("Incorrect password/email")
                    return redirect('/')
            else:
                flash("Email not found")
                return redirect('/')
        if ("buy_item" in request.form):
            add_to_cart(request.form['taken_count'], request.form['item_id'])
            return redirect('/')
            
        
            
@app.route("/shop_home/<_id>", methods = ["GET", "POST"])
def getHome(_id):
    products_all = db.products.find()
    if (request.method == "GET"):
        if ('email' in session):
            products = list(db.products.find({"shop":shop_id}))
            shop = db.accounts.find_one({'_id':ObjectId(_id)})
            return render_template("shop_home.html", shop_name = shop['shop_name'], products = products)
        else:
            flash("You need to log in before accessing the home page!")
            return redirect("/")
    if (request.method == "POST"):
        shop_id = ObjectId(_id)
        url = '/shop_home/', shop_id
        if ('add_product' in request.form):
            entry = {'name':request.form['item_name'], 'description':request.form['description'], 'price':request.form["unit_price"], 'quantity':request.form['quantity'], 'shop':shop_id}
            db.products.insert_one(entry)
            return redirect(url)
        if ("quantity_change" in request.form):
            item_id = ObjectId(request.form['item_id'])
            current_stock = int(db.products.find_one({"_id":item_id})['quantity'])
            db.products.update_one({"_id":item_id},{'$set':{'quantity':current_stock + int(request.form['new_quantity'])}})
            return redirect(url)

    return ""

@app.route("/logout", methods = ["GET", "POST"])
def logOut():
    session.clear()
    flash("Logout Successful")
    return redirect('/')

@app.route("/view_store/<email>", methods = ["GET", "POST"])
def view_home(email):
    global cart, item_count
    shop = db.accounts.find_one({"email":email})
    shop_id = ObjectId(shop["_id"])
    if (request.method == "GET"):
        list_products = list(db.products.find({'shop':shop_id}))
        shop = db.accounts.find_one({"email":email})
        print(shop)
        return render_template("view_store.html", products = list_products, shop_name = shop['shop_name'], length = len(cart))
    if (request.method == "POST"):
        if ("add_cart" in request.form):
            add_to_cart(request.form['taken_count'], request.form['item_id'])
            return redirect(f'/view_store/{email}')

def add_to_cart(amt_taken, item_id):
    global item_count
    item_id = ObjectId(item_id)
    amt_taken = int(amt_taken)
    item = db.products.find_one({'_id':item_id})
    if (amt_taken > int(item['quantity'])):
        flash("There is not enough of this item to be purchased!")
    db.products.update_one({'_id': item_id},{'$set':{'quantity':int(item['quantity']) - amt_taken}})
    current_item = {'name':item['name'], 'price':int(item['price']), 'amt':amt_taken, 'subtotal':amt_taken * int(item['price'])}
    # print(current_item)
    cart.append(current_item)
    print(cart)

@app.route('/view_cart', methods = ["GET", "POST"])
def view_cart():
    if (request.method == "GET"):
        total = 0
        for item in cart:
            total += item['subtotal']
        print(total, cart)
        return render_template('view_cart.html', cart = cart, total = total)
    if (request.method == "POST"):
        print("hello")
        session.clear()
        cart.clear()
        flash("Success!")
        return redirect('/')
    return ''

        

    
if __name__ == '__main__':
    app.run(debug = True)   
    